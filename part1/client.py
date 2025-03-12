#By Medha (U06825414) and Akshith (U36327874)
import socket
import sys #I use sys to get user input for the hostname (or IP) and port number. We could also use the regular input() way of doing this.
def main(): #Main function of the program that hosts all the logic.
    if len(sys.argv) != 3:
        print("Error! Use the following format: python client.py <hostname/IP> <port number>")
        sys.exit(1) #same as explained in the server.py file

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((hostname, port))

    try:
        while True:
            message = input("Enter a message to echo. Type exit to quit: ")
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode('utf-8'))
            response = b'' #using b cause the response here is gonna be in bytes (byte literals)
            while True:
                part = client_socket.recv(1024)
                response += part
                if len(part) < 1024:
                    break
            print(f"Echoed back: {response.decode('utf-8')}") #the server sends the exact same set of bytes back so we need to decode it again.
    finally:
        client_socket.close()

if __name__ == "__main__":
    main() #Calling the main function.