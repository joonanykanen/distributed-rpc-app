# Documentation for the Distributed Note-taking Application

![Assignment Model](/static/images/assignment_model.svg)

## Overview
The Distributed Note-taking Application is a client-server system designed to allow users to add, retrieve, and search notes on various topics. The system consists of three main components: the client, server, and load balancer.

## Components
### Client (client.py):
The client script provides a command-line interface for users to interact with the server.
Users can add notes, retrieve notes for specific topics, and search Wikipedia for additional information.
The client communicates with the server using XML-RPC calls.

### Server (server.py):
The server script implements the core functionality of the application.
It handles requests from clients, including adding notes to the XML database, retrieving notes, and searching Wikipedia.
The server uses XML-RPC to communicate with clients and performs operations on the XML database and Wikipedia API.

### Load Balancer (balancer.py):
The load balancer distributes incoming client requests among multiple instances of the server.
It implements a round-robin strategy to evenly distribute the load across server instances.
Clients interact with the load balancer to obtain the address of a server instance.

## Usage
### Client Usage:
1. Run the `client.py` script.
2. Follow the prompts to add notes, retrieve notes for specific topics, or search Wikipedia.
3. The client communicates with the server via RPC calls.

### Server Usage:
1. Run the `server.py {PORT}` script.
2. The server listens for incoming RPC calls from clients and performs the requested operations.
3. The server manages the XML database and interacts with the Wikipedia API to provide additional information.

### Load Balancer Usage:
1. Run the `balancer.py` script.
2. The load balancer listens for client requests and forwards them to available server instances.
3. It evenly distributes the load across server instances to ensure scalability and fault tolerance.

## Security Considerations
Warning: The `xmlrpc.client` and `xmlrpc.server` modules used in this assignment are not secure against maliciously constructed data. Ensure that the server is trusted and that the data exchanged between client and server is safe. 

## Conclusion
The Distributed Note-taking Application provides a convenient way for users to manage and retrieve notes on various topics. By leveraging RPC communication and distributed architecture, the application aims to ensure scalability, fault tolerance, and transparency. Users can seamlessly interact with the system through a simple command-line interface, while the server and load balancer handle the complexities of data management and load distribution.