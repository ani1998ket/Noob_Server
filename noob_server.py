import os
import sys
import signal
import socket

def init():
    HOST, PORT = '', 8888

    with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as s:
        
        s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        s.bind( (HOST, PORT) )
        s.listen(1)
        print( "Server listening on port", PORT )
        
        while True:
            conn, addr = s.accept()
            request = conn.recv( 1024 )
            
            if not request:
                conn.close()
                continue

            response =  process_header( request.decode('utf-8' ))

            conn.sendall( response )
            conn.close()

def process_header( request ):
    
    request = request.split(' ')
    response = '' 
    proto = request[0]
    file_path = request[1].split("\r\n")[0]
    f = None
    
    if( file_path == '/' ):
        file_path = "/index.html"
    
    print( "request file", file_path )
    print("------------")
    if( proto == 'GET' ):
        try:
            f = open( file_path[1:] )
            response = "HTTP/1.1 200 OK\n\n"
            response += f.read()
        except:
            f = open( ".server/404.html" )
            response = "HTTP/1.1 404 Not Found\n\n"
            response += f.read()

    return response.encode( 'ascii' )

def handler( signum, frame ):
    print( "Exiting the server")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal( signal.SIGINT, handler )
    init()
