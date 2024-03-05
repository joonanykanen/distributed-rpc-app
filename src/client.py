# client.py, JN, 05.03.2024
import xmlrpc.client
import datetime
import pprint

# Warning The xmlrpc.client module is not secure against maliciously constructed data.
# If you need to parse untrusted or unauthenticated data see XML vulnerabilities.
# https://docs.python.org/3/library/xml.html#xml-vulnerabilities

# Server address
BALANCER_ADDRESS = "http://localhost:8000"  # Running locally

# Server connection
BALANCER_PROXY = xmlrpc.client.ServerProxy(BALANCER_ADDRESS)
SERVER_ADDRESS = (
    BALANCER_PROXY.get_server()  # This needs the load balancer to have a working get_server method
)
SERVER_PROXY = xmlrpc.client.ServerProxy(SERVER_ADDRESS)

# Schema for timestamps
TIMESTAMP_SCHEMA = "%m/%d/%y - %H:%M:%S"


def add_note(topic: str, text: str, timestamp: str) -> int:
    """
    Function to add a note to the server.
    """
    try:
        result = SERVER_PROXY.add_note(topic, text, timestamp)
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def get_notes(topic: str) -> int:
    """
    Function to get notes from the server for a given topic.
    """
    try:
        result = SERVER_PROXY.get_notes(topic)
        pprint.pprint(result)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def search_wikipedia(search_term: str) -> str | int:
    """
    Function to search Wikipedia for additional information.
    """
    try:
        result = SERVER_PROXY.search_wikipedia(search_term)
        print(result)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return 1


# Main function
def main():
    while True:
        print("1. Add Note")
        print("2. Get Notes")
        print("3. Search Wikipedia")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            timestamp = datetime.datetime.now().strftime(TIMESTAMP_SCHEMA)
            topic = input("Enter the topic: ")
            text = input("Enter the text: ")
            add_note(topic, text, timestamp)
        elif choice == "2":
            topic = input("Enter the topic: ")
            get_notes(topic)
        elif choice == "3":
            search_term = input("Enter the search term: ")
            if search_term == "":
                search_term = "Default Search Term"
            search_result = search_wikipedia(search_term)
            add_search_results = input(
                "Would you like to add the search results as a note? (Y/n): "
            )
            if add_search_results.lower() == "y" or add_search_results == "":
                timestamp = datetime.datetime.now().strftime(TIMESTAMP_SCHEMA)
                add_note(search_term, search_result, timestamp)
        elif choice == "4":
            return 0
        else:
            print("Invalid choice. Please try again.")

        # Make some space between the choices
        print()


if __name__ == "__main__":
    main()

# eof
