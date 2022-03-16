from http.server import BaseHTTPRequestHandler, HTTPServer, ThreadingHTTPServer
from ipaddress import IPv4Address, IPv6Address, ip_address
from os.path import normcase
from pathlib import PurePath
from socket import IPPROTO_IPV6, IPV6_V6ONLY, AddressFamily, getfqdn
from socketserver import TCPServer
from typing import Any, Literal, Tuple, Type, Union

from ..ipaddress import IPAddress
from ..types import never


def create_server(
    binding: Union[PurePath, Tuple[Union[IPAddress, Literal[""], str], int]],
    handler: Type[BaseHTTPRequestHandler],
) -> HTTPServer:

    dualstack_ipv6 = False
    if isinstance(binding, PurePath):
        addr_fam = AddressFamily.AF_UNIX
        srv_addr: Any = normcase(binding)
    elif isinstance(binding, tuple):
        ip, port = binding
        srv_addr = (str(ip), port)

        if isinstance(ip, IPv4Address):
            addr_fam = AddressFamily.AF_INET
        elif isinstance(ip, IPv6Address) or not ip:
            dualstack_ipv6 = True
            addr_fam = AddressFamily.AF_INET6
        else:
            ipv = ip_address(ip)
            if isinstance(ipv, IPv4Address):
                addr_fam = AddressFamily.AF_INET
            elif isinstance(ipv, IPv6Address) or not ip:
                dualstack_ipv6 = True
                addr_fam = AddressFamily.AF_INET6
            else:
                never(ipv)

    else:
        never(binding)

    class Server(ThreadingHTTPServer):
        address_family = addr_fam

        def server_bind(self) -> None:
            if dualstack_ipv6:
                self.socket.setsockopt(IPPROTO_IPV6, IPV6_V6ONLY, 0)
            TCPServer.server_bind(self)

            if isinstance(binding, PurePath):
                self.server_name = self.socket.getsockname()
            elif isinstance(binding, tuple):
                self.server_name = getfqdn().encode("idna").decode()
                if isinstance(self, HTTPServer):
                    _, actual_port, *_ = self.socket.getsockname()
                    self.server_port = actual_port
            else:
                never(binding)

    server = Server(srv_addr, handler)
    return server
