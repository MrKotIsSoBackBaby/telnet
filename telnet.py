# basic TELNET implementation in python, using socket.
# made by _hackerbob_
import socket


class TelnetClient:
    def __init__(self, host, port=23, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self):
        """Establish connection to the Telnet server."""
        self.sock = socket.create_connection((self.host, self.port), self.timeout)
        return self.read_until(b"\n")  # Read initial response

    def write(self, data: bytes):
        """Send a command and return the response."""
        if self.sock:
            self.sock.sendall(data)
            return self.read_until(b"\n")
        return None

    def read_until(self, expected, bufsize=4096):
        """Read until a specific byte sequence is encountered."""
        data = b""
        self.sock.settimeout(self.timeout)  # Avoid infinite blocking
        while not data.endswith(expected):
            try:
                chunk = self.sock.recv(bufsize)
                if not chunk:
                    break  # Connection closed
                data += chunk
            except socket.timeout:
                break  # Stop reading if timeout occurs
        return data

    def close(self):
        """Close the connection."""
        if self.sock:
            self.sock.close()
            self.sock = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *a):
        self.close()
