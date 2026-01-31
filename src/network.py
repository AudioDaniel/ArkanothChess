import socket
import json
import time

class NetworkManager:
    def __init__(self):
        self.conn = None
        self.socket = None

    def host_game(self, host='0.0.0.0', port=5000):
        """
        Hosts a game on the specified port.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen(1)
        print(f"Waiting for opponent on port {port}...")
        self.conn, addr = self.socket.accept()
        print(f"Connected by {addr}")
        return self.conn

    def join_game(self, host, port=5000):
        """
        Joins a game at the specified host and port.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.socket.connect((host, port))
                break
            except ConnectionRefusedError:
                print("Connection refused. Retrying in 2 seconds...")
                time.sleep(2)
        self.conn = self.socket
        print(f"Connected to {host}:{port}")
        return self.conn

    def send_action(self, action_type, start, end):
        """
        Sends an action (move or attack) to the opponent.
        """
        if not self.conn:
            return

        message = {
            "type": action_type,
            "start": start,
            "end": end
        }
        data = json.dumps(message).encode('utf-8')
        # Send length header first to ensure complete message reception
        header = len(data).to_bytes(4, byteorder='big')
        self.conn.sendall(header + data)

    def receive_action(self):
        """
        Receives an action from the opponent.
        Blocks until a message is received.
        """
        if not self.conn:
            return None

        # Read header (4 bytes)
        header = self._recv_all(4)
        if not header:
            return None
        msg_len = int.from_bytes(header, byteorder='big')

        # Read body
        data = self._recv_all(msg_len)
        if not data:
            return None

        return json.loads(data.decode('utf-8'))

    def _recv_all(self, n):
        """
        Helper to receive exactly n bytes.
        """
        data = b''
        while len(data) < n:
            packet = self.conn.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def close(self):
        if self.conn:
            self.conn.close()
        if self.socket:
            self.socket.close()
