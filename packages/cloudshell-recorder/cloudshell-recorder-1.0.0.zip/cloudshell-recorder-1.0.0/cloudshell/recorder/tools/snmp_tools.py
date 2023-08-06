

from pysnmp.entity.config import usmHMACMD5AuthProtocol, usmHMACSHAAuthProtocol, usmHMAC128SHA224AuthProtocol, \
    usmHMAC192SHA256AuthProtocol, usmHMAC256SHA384AuthProtocol, usmHMAC384SHA512AuthProtocol, usmNoAuthProtocol, \
    usmDESPrivProtocol, usm3DESEDEPrivProtocol, usmAesCfb128Protocol, usmAesCfb192Protocol, \
    usmAesBlumenthalCfb192Protocol, usmAesCfb256Protocol, usmAesBlumenthalCfb256Protocol, usmNoPrivProtocol





AUTH_PROTOCOLS = {
    'MD5': usmHMACMD5AuthProtocol,
    'SHA': usmHMACSHAAuthProtocol,
    'SHA224': usmHMAC128SHA224AuthProtocol,
    'SHA256': usmHMAC192SHA256AuthProtocol,
    'SHA384': usmHMAC256SHA384AuthProtocol,
    'SHA512': usmHMAC384SHA512AuthProtocol,
    'NONE': usmNoAuthProtocol
}

PRIV_PROTOCOLS = {
    'DES': usmDESPrivProtocol,
    '3DES': usm3DESEDEPrivProtocol,
    'AES': usmAesCfb128Protocol,
    'AES128': usmAesCfb128Protocol,
    'AES192': usmAesCfb192Protocol,
    'AES192BLMT': usmAesBlumenthalCfb192Protocol,
    'AES256': usmAesCfb256Protocol,
    'AES256BLMT': usmAesBlumenthalCfb256Protocol,
    'NONE': usmNoPrivProtocol
}

ENTIRE_SNMP_OID_LIST = ["1.0", "1.2", "1.3", "1.4", "1.5"]

DEFAULT_SNMP_OID_LIST = ["1.0.8802.1.1.2.1",
                         "1.2.840.10006.300.43.1.1",
                         "1.2.840.10006.300.43.1.2.1",
                         "1.3.6.1.2.1.10.7.2",
                         "1.3.6.1.2.1.26.4",
                         "1.3.6.1.2.1.26.5",
                         "1.3.6.1.2.1.2.2.1",
                         "1.3.6.1.2.1.25.6.3.1",
                         "1.3.6.1.2.1.31",
                         "1.3.6.1.2.1.4.20",
                         "1.3.6.1.2.1.4.28",
                         "1.3.6.1.2.1.4.30",
                         "1.3.6.1.2.1.47.1.1",
                         "1.3.6.1.2.1.47.1.3.2"]
# Commented "1.3.6.1.2.1.4.21.1", "1.3.6.1.2.1.4.22.1.2", "1.3.6.1.2.1.4.22.1.4",
# ATM-MIB "1.3.6.1.2.1.37.1.11.1",
# BGP-MIB "1.3.6.1.2.1.15.2", "1.3.6.1.2.1.15.3.1.1", "1.3.6.1.2.1.15.3.1.17", "1.3.6.1.2.1.15.3.1.18",
# "1.3.6.1.2.1.15.3.1.19", "1.3.6.1.2.1.15.3.1.2", "1.3.6.1.2.1.15.3.1.20", "1.3.6.1.2.1.15.3.1.21",
# "1.3.6.1.2.1.15.3.1.5", "1.3.6.1.2.1.15.3.1.7", "1.3.6.1.2.1.15.3.1.9", "1.3.6.1.2.1.15.4", "1.3.6.1.2.1.15.4.0",
# MPLS-MIB "1.3.6.1.3.95.2.2.1.5", "1.3.6.1.3.95.2.2.1.8", "1.3.6.1.2.1.10.166.3.2.2.1", "1.3.6.1.2.1.10.166.4.1.3.2.1",
# ADSL-LINE-MIB "1.3.6.1.2.1.10.94.1.1.1.1.1", "1.3.6.1.2.1.10.94.1.1.1.1.2", "1.3.6.1.2.1.10.94.1.1.1.1.4",
# "1.3.6.1.2.1.10.94.1.1.2.1.8", "1.3.6.1.2.1.10.94.1.1.3.1.8",
# OSPF-MIB "1.3.6.1.2.1.14.1", "1.3.6.1.2.1.14.7.1.1", "1.3.6.1.2.1.14.7.1.12",
# "1.3.6.1.2.1.14.7.1.3", "1.3.6.1.2.1.14.7.1.4", "1.3.6.1.2.1.14.7.1.5",
# Bridge-MIB "1.3.6.1.2.1.17.1", "1.3.6.1.2.1.17.2", "1.3.6.1.2.1.17.4",
# DOCSIS-MIB "1.3.6.1.2.1.10.127",
# DS1-MIB "1.3.6.1.2.1.10.18.6.1.12", "1.3.6.1.2.1.10.18.6.1.5", "1.3.6.1.2.1.10.18.6.1.9",
# DS3-MIB  "1.3.6.1.2.1.10.30.5.1.11", "1.3.6.1.2.1.10.30.5.1.5", "1.3.6.1.2.1.10.30.5.1.9",
# ISDN-MIB "1.3.6.1.2.1.10.20.1.2.1.1",
# SONET-MIB "1.3.6.1.2.1.10.39.1.1.1.1.8",
# RMON2-MIB "1.3.6.1.2.1.16.19.12",
# FRAME-RELAY-DTE-MIB "1.3.6.1.2.1.10.32.2.1.12", "1.3.6.1.2.1.10.32.2.1.13", "1.3.6.1.2.1.10.32.2.1.3",
