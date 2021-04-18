from ipaddress import IPv4Network, IPv6Network

RFC_1918 = (
    IPv4Network("192.168.0.0/16"),
    IPv4Network("172.16.0.0/12"),
    IPv4Network("10.0.0.0/8"),
)

RFC_4193 = IPv6Network("fc00::/7")
RFC_4193_LOCAL = IPv6Network("fd00::/8")
