import socket
import sys
import time
import matplotlib.pyplot as plt

#getting RTTs: setting up the single message client sends (with input number of probes & message size)
def measure_rtt(client_socket, num_probes, size, server_delay):
    rtt_list = []
    
    #starting probe seq number from 1 to input number
    for i in range(1, num_probes + 1):
        payload = 'a' * size  
        message = f'm {i} {payload} {server_delay}\n'  
        start_time = time.time()  
        client_socket.send(message.encode())
        end_time = time.time()  
        rtt = (end_time - start_time) * 1000  
        rtt_list.append(rtt)
        print(f"Probe {i}: RTT = {rtt:.2f} ms")

    return rtt_list

#getting throughputs: same message
def measure_throughput(client_socket, num_probes, size, server_delay):
    total_data_sent = size * num_probes  
    start_time = time.time()  

    for i in range(1, num_probes + 1):
        payload = 'X' * size
        message = f'm {i} {payload} {server_delay}\n'   #<PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n
        client_socket.send(message.encode())
    end_time = time.time() 
    total_time = end_time - start_time 
    throughput = (total_data_sent / total_time) / 1024 
    return throughput


def plot_rtt(rtt_data, sizes):
    plt.figure()
    plt.plot(sizes, rtt_data, marker='o')
    plt.title('RTT vs Payload Size')
    plt.xlabel('Payload Size (bytes)')
    plt.ylabel('RTT (ms)')
    plt.grid()
    # plt.show()

def plot_throughput(throughput_data, sizes):
    plt.figure()
    plt.plot(sizes, throughput_data, marker='o')
    plt.title('Throughput vs Payload Size')
    plt.xlabel('Payload Size (KB)')
    plt.ylabel('Throughput (KBps)')
    plt.xticks(sizes)  
    plt.grid()
    # plt.show()

def main():
    if len(sys.argv) != 3:
        print("Use the following format: python client.py <server_ip> <port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])

    #setting up rtt 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    setup_message_rtt = "s rtt 10 100 0\n"      #<PROTOCOL PHASE><WS><PROBE SEQUENCE NUMBER><WS><PAYLOAD>\n
    client_socket.send(setup_message_rtt.encode())
    response = client_socket.recv(1024).decode()
    print(f"Received: {response}")


    #collecting and plotting the RTT measurements
    sizes_rtt = [1, 100, 200, 400, 800, 1000]
    rtt_results = []
    for size in sizes_rtt:
        rtt_data = measure_rtt(client_socket, 10, size, 0)  
        mean_rtt = sum(rtt_data) / len(rtt_data)
        rtt_results.append(mean_rtt)
    plot_rtt(rtt_results, sizes_rtt)
    
    #plotting RTT with higher server delay 
    rtt_results_1000ms = []
    for size in sizes_rtt:
        rtt_data = measure_rtt(client_socket, 10, size, 1000)  
        mean_rtt = sum(rtt_data) / len(rtt_data)
        rtt_results_1000ms.append(mean_rtt)
    plot_rtt(rtt_results_1000ms, sizes_rtt, label='RTT (1000 ms delay)')

    #setting up throughput 
    setup_message_tput = "s tput 10 1024 0\n"  
    client_socket.send(setup_message_tput.encode())
    response = client_socket.recv(1024).decode()
    print(f"Received: {response}")

    #collecting and plotting throughput measurements
    throughput_results_1000ms = []
    for size in sizes_throughput:
        throughput = measure_throughput(client_socket, 10, size, 1000) 
        throughput_results_1000ms.append(throughput)
    plot_throughput(throughput_results_1000ms, [size // 1024 for size in sizes_throughput], label='Throughput (1000 ms delay)')

    
    #plotting tput with higher server delay 
    sizes_throughput = [1024, 2048, 4096, 8192, 16384]  
    throughput_results = []
    for size in sizes_throughput:
        throughput = measure_throughput(client_socket, 10, size, 1000) 
        throughput_results.append(throughput)
    plot_throughput(throughput_results, [size // 1024 for size in sizes_throughput]) 

    # Send termination message
    termination_message = "t\n"  
    client_socket.send(termination_message.encode()) 
    response = client_socket.recv(1024).decode()  
    print(f"Received: {response}") 

    client_socket.close()
      # Show all plots at once
    plt.show()

if __name__ == "__main__":
    main()
