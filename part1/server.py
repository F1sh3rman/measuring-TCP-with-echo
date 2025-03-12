#By Medha (U06825414) and Akshith (U36327874)
import socket
import sys #I use sys here to take the port as an argument.
def main(): #Main function of the program that hosts all the logic
    if len(sys.argv) != 2:
        print("Incorrect input. Please use the following format: python server.py <port number>")
        sys.exit(1) #.exit(1) indicates an abnormal ending to the program.
    
    port = int(sys.argv[1]) #accepting the port the server needs to run on.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating a socket using the IPv4 address (AF_INET) and specifying TCP protocol.
    server_socket.bind(('', port)) #binding the port
    server_socket.listen(5) #5 here represents the maximum number of queued connections.
    print(f"Server active! Now listening for distant echoes from {port}...")

    while True: #I use this loop to continously accept incoming connections.
        client_socket, addr = server_socket.accept() 
        print(f"Connection from {addr} has been established!")

        while True: #and this loop for extra credit. TO receive data more than 1024 bytes in length.
            data = client_socket.recv(1024)
            if not data:
                break  #If there is is no data, break out of the loop (closes socket)
            print(f"Received: {data.decode('utf-8')}") #Since we're using TCP, we need to decode the data from bytes. I use this only to print it on
            #...the server terminal.
            client_socket.sendall(data)  #Sending back the exact same encoded message we received from the client program.

        client_socket.close()
        print(f"Connection with {addr} closed.")

if __name__ == "__main__":
    main()