import os , subprocess
import socket
import sys
import struct
import time
from threading import Thread
import Queue
import platform


servers = {}
relays = {}

def parse_files():
	
	print str(sys.argv)
	if( len(sys.argv) != 5 ):
		print "Error in arguments"
		exit(1)
	
	if( str(sys.argv[1]) != "-e" and str(sys.argv[3]) != "-r" ):
		print "Error in arguments"
		exit(1)
	
	fs = open(str(sys.argv[2]), "r")
	s_lines = fs.readlines()
	fs.close()
	
	l = [x.rstrip() for x in s_lines]
	ll = [x.split(",") for x in l]

	for line in ll:
		servers[str(line[1].strip())] = str(line[0].strip())
	
	print servers
			
	rs = open(str(sys.argv[4]), "r")
	r_lines = rs.readlines()
	rs.close()
	
	l = [x.rstrip() for x in r_lines]
	ll = [x.split(",") for x in l]

	for line in ll:
		relays[str(line[0].strip())] = [str(line[1].strip()),str(line[2].strip())]
	
	print relays







def pingg(hostname,var):
    if platform.system() == "Windows":
        ping_response = subprocess.Popen(["ping", hostname, "-n", var], stdout=subprocess.PIPE).stdout.read()
    else:
        ping_response = subprocess.Popen(["ping", hostname, "-C", var], stdout=subprocess.PIPE).stdout.read()
    print(ping_response)
    x=ping_response.split()
    print("The Average time is :" , x[-1:] )
    print('\n')
    return x[-1:]

def main(dest_name):

    dest_addr = socket.gethostbyname(dest_name)
    # Define UDP and ICMP
    udp = socket.getprotobyname('udp')
    icmp = socket.getprotobyname('icmp')
    timer = 1
    port = 33434
    maxHops = 2
    totalRTT = 0

    while True:
        # Create sender and receiver. Sender uses UDP, receiver uses IDMP
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)

        # Assign TTL to sender, increment TTL
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, timer)

        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        receiver.settimeout(15.0)

        # Bind socket and send message from sender to receiver
        receiver.bind(("", port))
        sender.sendto("", (dest_name, port))

        # Ensures that not receiving won't stall the program
        # receiver.setblocking(0)

        addr = None
        name = None
        count = 0

        try:
            # Keep track of RTT
            startTime = time.time()
            # Reads an array of 512-byte sized blocks from sender into addr
            (_,addr) = receiver.recvfrom(512)
            addr = addr[0]
            # Try to get site name
            try:
                name = socket.gethostbyaddr(addr)[0]
            except socket.error:
                name = addr
        # Process socket errors
        except socket.error as exc:
            pass
        # Close both sockets
        finally:
            sender.close()
            receiver.close()
            endTime = time.time()
            # Record RTT, total RTT, convert to ms
            RTT = (endTime - startTime) * 1000
            totalRTT += RTT

        if addr is not None:
            host = "%s (%s)" % (name, addr)
        else:
            host = "*"
        print("%d\t%s" % (timer, host))
        print(" %f" % RTT + " ms")

        timer += 1
        if addr == dest_addr or timer > maxHops:
            print("Total RTT: %f\n" % totalRTT)
            print("Hop count: %d\n" % timer)
            break
        
    return timer


if __name__ == "__main__":

    #parse_files()

    sock=socket.socket()
    host=socket.gethostname()
    #port=54321
    port=17622

    sock.connect((host,port))

    print (sock.recv(1024))
 

    
    que = Queue.Queue()
    var = raw_input("Please enter the number of pings: ")
    hostname = "google.com"

    answer=str(var) + "," + "google.com"




    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    #data = client_socket.recv(512)
    #key=timeInput()

    #code="player,100,200,30,30,player2,0,1"
    
    #code="chat,hi,Marc"
    #client_socket.send(bytes(code,"UTF-8"))
    client_socket.send(answer)



    
    #sock.sendall(answer)




    #sock.send("google.com")
    #sock.send(var)
    
    #t1=Thread(target=main,args=('www.google.com',))
    t1= Thread(target=lambda q, arg1: q.put(main(arg1)), args=(que, 'www.google.com'))
    #t2=Thread(target=pingg,args=(hostname,))
    t2= Thread(target=lambda q , arg1,arg2: q.put(pingg(arg1,arg2)),args=(que, hostname,var))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    av = que.get()
    hops= que.get()
    print ("The total hops are:")
    print hops
    print ("The average time is:")
    print av


    sock.close()
