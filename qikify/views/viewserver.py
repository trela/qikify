"""View server implementation.
"""
import subprocess, signal, sys, os

def sigint_replace():
    """Ignore the SIGINT signal by setting the handler to the standard signal
    handler SIG_IGN.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


class ViewServer(object):
    """Run a view server.
    """
    
    def __init__(self, http_port = 8000, node_port = 8001):
        self.http_port = http_port
        self.node_port = node_port
        self.resource_dir = os.path.join(os.path.dirname(__file__), 'resources')
        self.p_http = None
        self.p_node = None
        
    def run(self):
        """This function runs the view server, comprised of a simple python http
        server along with a node.js web sockets server. The http server handles 
        all static resources, and the node.js server permits pushing updates to
        connected clients.
        """
        print 'starting view server'
        sys.stdout.flush()
        
        try:
            # start http server
            self.p_http = subprocess.Popen(
                ["python", "-m", "SimpleHTTPServer"],
                preexec_fn = sigint_replace,
                cwd = self.resource_dir
            )
            
            # start node.js server
            self.p_node = subprocess.Popen(
                ["node", "app.js"],
                preexec_fn = sigint_replace,
                cwd = self.resource_dir
            )
            
            # Run forever, and wait for Ctrl+C
            while True:
                pass
                
        except KeyboardInterrupt:
            print '\nterminating view server'
            self.p_http.terminate()
            self.p_node.terminate()


