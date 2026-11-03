from socket import *

mailServer = "smtp.example.com"
serverPort = 25

sender = "sender@example.com"
recipient = "recipient@example.com"

subject = "My First SMTP Email"
body = "Hello! This is my first email using Python sockets."

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, serverPort))


def receive_response():
    response = clientSocket.recv(2048).decode()
    print(response)
    return response


def send_command(command):
    print(command)
    clientSocket.sendall((command + "\r\n").encode())
    return receive_response()


receive_response()

send_command("EHLO client.example.com")
send_command(f"MAIL FROM:<{sender}>")
send_command(f"RCPT TO:<{recipient}>")
send_command("DATA")

message = (
    f"From: {sender}\r\n"
    f"To: {recipient}\r\n"
    f"Subject: {subject}\r\n"
    "\r\n"
    f"{body}\r\n"
    ".\r\n"
)

clientSocket.sendall(message.encode())
receive_response()

send_command("QUIT")

clientSocket.close()






