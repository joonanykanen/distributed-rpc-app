# balancer.py, JN, 05.03.2024
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import random

# Warning The xmlrpc.client module is not secure against maliciously constructed data.
# If you need to parse untrusted or unauthenticated data see XML vulnerabilities.
# https://docs.python.org/3/library/xml.html#xml-vulnerabilities

# Warning The xmlrpc.server module is not secure against maliciously constructed data.
# If you need to parse untrusted or unauthenticated data see XML vulnerabilities.
# https://docs.python.org/3/library/xml.html#xml-vulnerabilities

# List of server addresses
SERVER_ADDRESSES = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003",
]

PORT = 8000


def get_server_address():
    """
    Function to select a server address using round-robin strategy.
    """
    address = random.choice(SERVER_ADDRESSES)

    # This is the most simple way to implement error-handling
    # Consider using a more sophisticated strategy
    try:
        server = ServerProxy(address)
        server.ping()
        return address
    except Exception:
        print(f"Server {address} is not available, trying another one...")
        return get_server_address()


# XML-RPC handler class
class LoadBalancerHandler:
    def get_server(self):
        """
        Method to get a server address.
        """
        return get_server_address()


# Run the XML-RPC server
def run():
    server = SimpleXMLRPCServer(("localhost", PORT))
    server.register_instance(LoadBalancerHandler())
    print(f"Load balancer listening on port {PORT}...")
    server.serve_forever()


if __name__ == "__main__":
    run()

# eof
