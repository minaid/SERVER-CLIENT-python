import time
import os, platform
import subprocess
from threading import Thread
import Queue
#import ast



"""
def ping(dest_name,count,que):
        
        #Epistrefei False ean dn apadisei se kapoio ping o server
        #Alliws epistrefei to average RTT
       
        sum = 0
        if  (platform.system().lower()=="windows"):
                ping_str="-n "+count
        else:
                ping_str="-c "+count
                start=time.time()
                # Ping 
                p=os.system("ping " + ping_str + " " + dest_name)
                duration=time.time() - start
                #Ypologismos tou average RTT se seconds
                if (p==0):
                        que.put(sum/count)
                else:
                        que.put(-1)
"""
def ping(dest_name,count):
    if platform.system() == "Windows":
        ping_response = subprocess.Popen(["ping", dest_name, "-n", count], stdout=subprocess.PIPE).stdout.read()
    else:
        ping_response = subprocess.Popen(["ping", dest_name, "-C", count], stdout=subprocess.PIPE).stdout.read()
    print(ping_response)
    m=ping_response.split()
    print("The Average time is :" , m[-1:] )
    print('\n')
    return m[-1:]
        
#================================================================================
import socket
"""
def traceroute(dest_name,que):
        dest_addr = socket.gethostbyname(dest_name)
        port = 33434
        max_hops = 2
        icmp = socket.getprotobyname('icmp')
        udp = socket.getprotobyname('udp')
        ttl = 1
        while True:
            recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
            send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            recv_socket.bind(("", port))
            send_socket.sendto("", (dest_name, port))
            curr_addr = None
            curr_name = None
            try:
                _, curr_addr = recv_socket.recvfrom(512)
                curr_addr = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
            except socket.error:
                pass
            finally:
                send_socket.close()
                recv_socket.close()
            if curr_addr is not None:
                curr_host = "%s (%s)" % (curr_name, curr_addr)
            else:
                curr_host = "*"
            print ("%d\t%s" % (ttl, curr_host))
            ttl += 1
            if curr_addr == dest_addr or ttl > max_hops:
                break
        que.put(ttl)
#=================================================================================
"""
def traceroute(dest_name):

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





def main():
        
        #Anoigei ena Tcp socket gia na epikinwnisei client me ton relay
        #s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #s.bind(("",17642))
        
        sock=socket.socket()
        host=socket.gethostname()
        port=17622
        sock.bind((host,port))
        sock.listen(10)
        conn, addr=sock.accept()
        print('i just got a connection from ' ,addr)
        conn.send(b' you have been connected to relay')
        
        
        #s.bind(("",17643))
        #s.bind((host,17643))
        #s.listen(1)
        #connect, address=s.accept()	
        #resp=(conn.recv(1024)).strip()

        conn,addr =sock.accept()

        resp=conn.recv(1024)  # Read from newly accepted socket
        print(resp)
        
        #resp=sock.recv(1024)
        """
        x=0
        for x in range(0,(len(resp)-1)):
                if(resp[x]==","):
                        count=int(resp[0:x-1])
                        break
        #dest_name=int(resp[x+1:len(resp)-1])
        dest_name=resp[x+1:len(resp)-1]
        """
        #print(resp[:1])
        #count=resp[:1]
        #print(count)
        #dest_name=resp[2:]
        #print(dest_name)


        x=0
        while x<len(resp):
	#for x in range(0,(len(resp)-1)):
                if(resp[x]==","):
                        count=resp[0:x]
                        break
                x+=1
        dest_name=resp[x+1:len(resp)]


        
        #dest_name="www.google.com"
        #count=str(3)
        print("Ping times:%s"%count)
        print("\n")
        print("Address to ping:%s"%dest_name)
        print("\n")
        
        #dest_name="www.google.com"
        #count=20
        que = Queue.Queue()
        #Ftiaxnw ta threads
        #pingg = threading.Thread(target=ping, args=(dest_name, count ,que))
        pingg= Thread(target=lambda q , arg1,arg2: q.put(ping(arg1,arg2)),args=(que,dest_name, count))
        #pingg.setDaemon(True)
        #trace = threading.Thread(target=traceroute, args=(dest_name, que))
        trace= Thread(target=lambda q , arg1: q.put(traceroute(arg1)),args=(que,dest_name))
        
        #trace.setDaemon(True)
        #Ekinw ta threads
        pingg.start()
        trace.start()
        #Tou lew na perimenei na teliwsei to thread gia na kanei exit
        pingg.join()
        trace.join()
        rtt=que.get()
        print(rtt)
        print ("\n")
        ttl=que.get()
        print(ttl)
        print ("\n")
        #Stelnei ston Client tis metriseis kai kleinei to socket
        conn.send("RTT:"+str(rtt)+",TTL:"+str(ttl)+".")
        conn.close
        
        
        
#=================================================================================
if __name__=="__main__":
        main()
