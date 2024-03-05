# balancer.py, JN, 05.03.2024
from xmlrpc.server import SimpleXMLRPCServer
import random

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
    return address


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
