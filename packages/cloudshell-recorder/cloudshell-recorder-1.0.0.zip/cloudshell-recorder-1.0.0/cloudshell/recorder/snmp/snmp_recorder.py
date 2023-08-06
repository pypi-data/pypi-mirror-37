import time
import sys

import traceback
from pyasn1.type import univ
from pysnmp.proto import rfc1902
from pysnmp.proto import rfc1905

from cloudshell.recorder.model.snmp_record import SnmpRecord

try:
    from pysnmp.carrier.asynsock.dgram import udp6
except ImportError:
    udp6 = None
from pysnmp.entity.rfc3413 import cmdgen
from snmpsim import error, log


class SnmpRecorder(object):
    def __init__(self, snmp_parameters):
        self.snmp_parameters = snmp_parameters
        self.output_file = list()
        self.data_file_handler = SnmpRecord()
        self._oid = None
        self._stop_oid = None
        self._cmd_gen = None

    def create_snmp_record(self, oid, stop_oid=None, get_subtree=True):
        self._oid = univ.ObjectIdentifier(oid)
        if stop_oid:
            self._stop_oid = univ.ObjectIdentifier(stop_oid)
        elif get_subtree:
            _stop_oid = "{}{}".format(oid[:-1], int(oid[-1:]) + 1)
            self._stop_oid = univ.ObjectIdentifier(_stop_oid)

        cb_ctx = {
            'total': 0,
            'count': 0,
            'errors': 0,
            'iteration': 0,
            'reqTime': time.time(),
            '': True,
            'retries': self.snmp_parameters.continue_on_errors,
            'lastOID': oid
        }

        if self.snmp_parameters.get_bulk_flag:
            self._cmd_gen = cmdgen.BulkCommandGenerator()

            self._cmd_gen.sendVarBinds(
                self.snmp_parameters.snmp_engine,
                'tgt',
                self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                0, self.snmp_parameters.get_bulk_repetitions,
                [(self._oid, None)],
                self.cb_fun, cb_ctx
            )
        else:
            self._cmd_gen = cmdgen.NextCommandGenerator()

            self._cmd_gen.sendVarBinds(
                self.snmp_parameters.snmp_engine,
                'tgt',
                self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                [(self._oid, None)],
                self.cb_fun, cb_ctx
            )

        log.msg('Sending initial %s request for %s ....' % (
            self.snmp_parameters.get_bulk_flag and 'GETBULK' or 'GETNEXT', self._oid))

        t = time.time()

        # Python 2.4 does not support the "finally" clause

        exc_info = None

        try:
            self.snmp_parameters.snmp_engine.transportDispatcher.runDispatcher()
        except KeyboardInterrupt:
            log.msg('Shutting down process...')
        except Exception:
            exc_info = sys.exc_info()

        t = time.time() - t

        cb_ctx['total'] += cb_ctx['count']

        log.msg('OIDs dumped: %s, elapsed: %.2f sec, rate: %.2f OIDs/sec, errors: %d' % (
            cb_ctx['total'], t, t and cb_ctx['count'] // t or 0, cb_ctx['errors']))

        if exc_info:
            for line in traceback.format_exception(*exc_info):
                log.msg(line.replace('\n', ';'))

        return self.output_file

    def cb_fun(self, snmp_engine, send_request_handle, error_indication,
              error_status, error_index, var_bind_table, cb_ctx):
        if error_indication and not cb_ctx['retries']:
            cb_ctx['errors'] += 1
            log.msg('SNMP Engine error: %s' % error_indication)
            return
        # SNMPv1 response may contain noSuchName error *and* SNMPv2c exception,
        # so we ignore noSuchName error here
        if error_status and error_status != 2 or error_indication:
            log.msg('Remote SNMP error %s' % (error_indication or error_status.prettyPrint()))
            if cb_ctx['retries']:
                try:
                    next_oid = var_bind_table[-1][0][0]
                except IndexError:
                    next_oid = cb_ctx['lastOID']
                else:
                    log.msg('Failed OID: %s' % next_oid)
                # fuzzy logic of walking a broken OID
                if len(next_oid) < 4:
                    pass
                elif (self.snmp_parameters.continue_on_errors - cb_ctx[
                    'retries']) * 10 / self.snmp_parameters.continue_on_errors > 5:
                    next_oid = next_oid[:-2] + (next_oid[-2] + 1,)
                elif next_oid[-1]:
                    next_oid = next_oid[:-1] + (next_oid[-1] + 1,)
                else:
                    next_oid = next_oid[:-2] + (next_oid[-2] + 1, 0)

                cb_ctx['retries'] -= 1
                cb_ctx['lastOID'] = next_oid

                log.msg('Retrying with OID %s (%s retries left)...' % (next_oid, cb_ctx['retries']))

                # initiate another SNMP walk iteration
                if self.snmp_parameters.get_bulk_flag:
                    self._cmd_gen.sendVarBinds(
                        snmp_engine,
                        'tgt',
                        self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                        0, self.snmp_parameters.get_bulk_repetitions,
                        [(next_oid, None)],
                        self.cb_fun, cb_ctx
                    )
                else:
                    self._cmd_gen.sendVarBinds(
                        snmp_engine,
                        'tgt',
                        self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                        [(next_oid, None)],
                        self.cb_fun, cb_ctx
                    )

            cb_ctx['errors'] += 1

            return

        if self.snmp_parameters.continue_on_errors != cb_ctx['retries']:
            cb_ctx['retries'] += 1

        if var_bind_table and var_bind_table[-1] and var_bind_table[-1][0]:
            cb_ctx['lastOID'] = var_bind_table[-1][0][0]

        stop_flag = False

        # Walk var-binds
        for varBindRow in var_bind_table:
            for oid, value in varBindRow:
                # EOM
                # _add_line = True
                if self._stop_oid and oid >= self._stop_oid:
                    stop_flag = True
                    # _add_line = False
                if (value is None or
                        value.tagSet in (rfc1905.NoSuchObject.tagSet,
                                         rfc1905.NoSuchInstance.tagSet,
                                         rfc1905.EndOfMibView.tagSet)):
                    stop_flag = True

                # remove value enumeration
                if value.tagSet == rfc1902.Integer32.tagSet:
                    value = rfc1902.Integer32(value)

                if value.tagSet == rfc1902.Unsigned32.tagSet:
                    value = rfc1902.Unsigned32(value)

                if value.tagSet == rfc1902.Bits.tagSet:
                    value = rfc1902.OctetString(value)

                # Build .snmprec record

                context = {
                    'origOid': oid,
                    'origValue': value,
                    'count': cb_ctx['count'],
                    'total': cb_ctx['total'],
                    'iteration': cb_ctx['iteration'],
                    'reqTime': cb_ctx['reqTime'],
                    'startOID': self._oid,
                    'stop_flag': stop_flag,
                }

                try:
                    # line = ""
                    # if _add_line:
                    line = self.data_file_handler.format(oid, value, **context).replace("|", ", ")
                except error.MoreDataNotification:
                    cb_ctx['count'] = 0
                    cb_ctx['iteration'] += 1

                    more_data_notification = sys.exc_info()[1]
                    if 'period' in more_data_notification:
                        log.msg(
                            '%s OIDs dumped, waiting %.2f sec(s)...' % (
                                cb_ctx['total'], more_data_notification['period']))
                        time.sleep(more_data_notification['period'])

                    # initiate another SNMP walk iteration
                    if self.snmp_parameters.get_bulk_flag:
                        self._cmd_gen.sendVarBinds(
                            snmp_engine,
                            'tgt',
                            self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                            0, self.snmp_parameters.get_bulk_repetitions,
                            [(self._oid, None)],
                            self.cb_fun, cb_ctx
                        )
                    else:
                        self._cmd_gen.sendVarBinds(
                            snmp_engine,
                            'tgt',
                            self.snmp_parameters.v3_context_engine_id, self.snmp_parameters.v3_context,
                            [(self._oid, None)],
                            self.cb_fun, cb_ctx
                        )

                    stop_flag = True  # stop current iteration

                except error.NoDataNotification:
                    pass
                except error.SnmpsimError:
                    log.msg('ERROR: %s' % (sys.exc_info()[1],))
                    continue
                else:
                    # if _add_line and line:
                    self.output_file.append(line)

                    cb_ctx['count'] += 1
                    cb_ctx['total'] += 1

                    if cb_ctx['count'] % 100 == 0:
                        log.msg('OIDs dumped: %s/%s' % (
                            cb_ctx['iteration'], cb_ctx['count']))

        # Next request time
        cb_ctx['reqTime'] = time.time()
        # Continue walking
        return not stop_flag
