from ipaddress import (
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
)
from typing import Union

IPAddress = Union[IPv4Address, IPv6Address]
IPNetwork = Union[IPv4Network, IPv6Network]
IPInterface = Union[IPv4Interface, IPv6Interface]

LOOPBACK_V4 = IPv4Network("127.0.0.0/8")
LOOPBACK_V6 = IPv6Network("::1/128")

PRIVATE_V4 = (
    IPv4Network("10.0.0.0/8"),
    IPv4Network("172.16.0.0/12"),
    IPv4Network("192.168.0.0/16"),
)

PRIVATE_V6 = IPv6Network("fc00::/7")
PRIVATE_V6_ULA = IPv6Network("fd00::/8")


LINK_LOCAL_V4 = IPv4Network("169.254.0.0/16")
LINK_LOCAL_V6 = IPv6Network("fe80::/10")
