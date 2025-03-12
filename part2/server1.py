import socket
import sys
import time

def main():
    if len(sys.argv) != 2:
        print("Incorrect input. Please use the following format: python server.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(1)
    print(f"Server is listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
    
        try:
            connection_setup = client_socket.recv(1024).decode().strip()
            print(f"Received: {connection_setup}")
            
            if connection_setup.startswith("s ") and ("rtt" in connection_setup or "tput" in connection_setup):
                client_socket.send(b"200 OK: Ready\n")
                
                #to keep track of the probe sequence numbers 
                parts = connection_setup.split()
                max_probes = int(parts[2])
                seq = 1  
                
                #echo 
                while True:
                        probe_message = client_socket.recv(1024).decode().strip()
                        
                        #checking for termination
                        if probe_message == 't':
                            client_socket.send(b"200 OK: Closing Connection\n")
                            print("Termination message received. Closing connection.")
                            break
                        
                        if not probe_message:
                            break
                        
                        #validating probe message (incomplete or invalid check)
                        message_parts = probe_message.split()
                        if len(message_parts) < 2 or message_parts[0] != 'm' or int(message_parts[1]) != seq or int(message_parts[1]) > max_probes:
                            client_socket.send(b"404 ERROR: Invalid Measurement Message\n")
                            print("Invalid measurement message received. Closing connection.")
                            break
                        
                        print(f"Echoing back: {probe_message}")
                        client_socket.send(probe_message.encode())
                        
                        #to track probe sequence number incrementing by 1
                        seq += 1
            else:
                client_socket.send(b"404 ERROR: Invalid Connection Setup Message\n")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            client_socket.close()

if __name__ == "__main__":
    main()