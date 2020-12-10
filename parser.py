import sys

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
	
	
parse_files()
