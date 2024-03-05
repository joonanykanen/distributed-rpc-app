# server.py, JN, 05.03.2024
import os
import sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import requests

# Warning The xmlrpc.server module is not secure against maliciously constructed data.
# If you need to parse untrusted or unauthenticated data see XML vulnerabilities.
# https://docs.python.org/3/library/xml.html#xml-vulnerabilities


# Restrict to a particular path
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)  # The default value is ('/', '/RPC2')


# XML database file path
XML_FILE = "db.xml"

# Wikipedia API URL
WIKI_URL = "https://en.wikipedia.org/w/api.php"


def add_note(topic: str, text: str, timestamp: str) -> str:
    """
    Function to add a note to the XML database
    """
    try:
        # If database mock file exists, load it; otherwise, create a new one
        if os.path.isfile(XML_FILE):
            tree = ET.parse(XML_FILE)
            root = tree.getroot()
        else:
            root = ET.Element("data")

        # Check if the topic already exists
        topic_exists = False
        for topic_elem in root.findall("topic"):
            if topic_elem.attrib.get("name") == topic:
                topic_exists = True
                note_elem = ET.SubElement(topic_elem, "note")
                note_elem.attrib["name"] = (
                    f"Note {len(topic_elem.findall('note'))}"  # Don't increment len + 1 since it's 0-based
                )
                note_text = ET.SubElement(note_elem, "text")
                note_text.text = text
                note_timestamp = ET.SubElement(note_elem, "timestamp")
                note_timestamp.text = timestamp

        # If topic does not exist, create a new one
        if not topic_exists:
            topic_elem = ET.SubElement(root, "topic")
            topic_elem.attrib["name"] = topic
            note_elem = ET.SubElement(topic_elem, "note")
            note_elem.attrib["name"] = "Note 1"
            note_text = ET.SubElement(note_elem, "text")
            note_text.text = text
            note_timestamp = ET.SubElement(note_elem, "timestamp")
            note_timestamp.text = timestamp

        # Write the updated XML data back to the file
        tree = ET.ElementTree(root)
        tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

        return "Note added successfully."
    except Exception as e:
        return f"Error: {e}"


def get_notes(topic: str) -> list[dict[str, str]] | str:
    """
    Function to get notes from the XML database for a given topic
    """
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()

        notes = []

        for topic_elem in root.findall("topic"):
            if topic_elem.attrib.get("name") == topic:
                for note_elem in topic_elem.findall("note"):
                    note = {}
                    note["name"] = note_elem.attrib["name"]
                    note["text"] = note_elem.find("text").text
                    note["timestamp"] = note_elem.find("timestamp").text
                    notes.append(note)
        return notes
    except Exception as e:
        return f"Error: {e}"


def search_wikipedia(search_term: str):
    """
    Function to search Wikipedia for additional information
    Returns the first link to the article from the search results
    """
    try:
        params = {
            "action": "opensearch",
            "search": search_term,
            "limit": 1,
            "format": "json",
        }

        response = requests.get(
            url=WIKI_URL,
            params=params,
        )
        wiki_link = response.json()[3][0]
        return wiki_link
    except Exception as e:
        return f"Error: {e}"


def run():
    # Get the port from command line arguments
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Please provide a valid integer port number.")
            sys.exit(1)
    else:
        print("Port number not provided. Please provide a valid integer port number.")
        sys.exit(1)

    # Initiate the server
    server = SimpleXMLRPCServer(("localhost", PORT), requestHandler=RequestHandler)

    # Register functions with the server
    server.register_function(add_note)
    server.register_function(get_notes)
    server.register_function(search_wikipedia)

    # Run the server's main loop
    print(f"Server is listening on PORT {PORT}...")
    server.serve_forever()


if __name__ == "__main__":
    run()

# eof
