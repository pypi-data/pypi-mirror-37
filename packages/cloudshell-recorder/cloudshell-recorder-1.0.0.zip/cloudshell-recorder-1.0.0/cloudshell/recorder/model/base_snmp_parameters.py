from abc import abstractproperty
import socket

import sys

from pyasn1.type import univ
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp, udp6


class BaseSnmpParameters(object):
    def __init__(self, ip, port=161, is_ipv6=False, timeout=2000, retry_count=2, get_bulk_flag=False,
                 continue_on_errors=0, get_bulk_repetitions=25, v3_context_engine_id=None, v3_context=''):
        self.ip = ip
        self.continue_on_errors = continue_on_errors
        self.get_bulk_repetitions = get_bulk_repetitions
        self.timeout = timeout
        self.output_file = list()
        self.retry_count = retry_count
        self.get_bulk_flag = get_bulk_flag
        self.v3_context_engine_id = v3_context_engine_id
        self.v3_context = v3_context
        if self.v3_context_engine_id:
            if self.v3_context_engine_id[2:] == '0x':
                self.v3_context_engine_id = univ.OctetString(hexValue=self.v3_context_engine_id[2:])
            else:
                self.v3_context_engine_id = univ.OctetString(self.v3_context_engine_id)
        if self.v3_context:
            if self.v3_context[:2] == '0x':
                self.v3_context = univ.OctetString(hexValue=self.v3_context[2:])
            else:
                self.v3_context = univ.OctetString(self.v3_context)
        if ip:
            try:
                agent_udp_endpoint = \
                    socket.getaddrinfo(ip,
                                       port,
                                       socket.AF_INET, socket.SOCK_DGRAM,
                                       socket.IPPROTO_UDP)[0][4][:2]
            except socket.gaierror:
                sys.stderr.write('ERROR: unknown hostname {}\r\n'.format(ip))
                sys.exit(-1)
        else:
            sys.stderr.write('ERROR: unknown hostname {}\r\n'.format(ip))
            sys.exit(-1)

        self._snmp_engine = engine.SnmpEngine()

        config.addTargetParams(self._snmp_engine, 'pms', self.get_user, self.get_security,
                               self.get_snmp_version)

        if agent_udp_endpoint:
            if is_ipv6:
                config.addSocketTransport(
                    self._snmp_engine,
                    udp6.domainName,
                    udp6.Udp6SocketTransport().openClientMode()
                )
                config.addTargetAddr(
                    self._snmp_engine, 'tgt', udp6.domainName, agent_udp_endpoint, 'pms',
                    self.timeout, self.retry_count
                )
            else:
                config.addSocketTransport(
                    self._snmp_engine,
                    udp.domainName,
                    udp.UdpSocketTransport().openClientMode()
                )
                config.addTargetAddr(
                    self._snmp_engine, 'tgt', udp.domainName, agent_udp_endpoint, 'pms',
                    self.timeout, self.retry_count
                )
        else:
            sys.stderr.write('ERROR: Failed to communicate with provided IP Address {}\r\n'.format(ip))
            sys.exit(-1)

    @abstractproperty
    def get_security(self):
        pass

    @abstractproperty
    def get_user(self):
        pass

    @abstractproperty
    def get_snmp_version(self):
        pass

    @property
    def snmp_engine(self):
        return self._snmp_engine

    def close_snmp_engine_dispatcher(self):
        self.snmp_engine.transportDispatcher.closeDispatcher()
