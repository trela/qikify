import SimpleHTTPServer
import SocketServer
import subprocess, signal, sys

class ViewServer(object):

    def __init__(self, http_port = 8000, node_port = 8001):
        self.http_port = http_port
        self.node_port = node_port
    
    def sigint_replace(self):
        # Ignore the SIGINT signal by setting the handler to the standard
        # signal handler SIG_IGN.
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def run(self):
        print 'starting view server'
        sys.stdout.flush()
        try:
            self.p_http = subprocess.Popen(
                ["python", "-m", "SimpleHTTPServer"],
                preexec_fn = self.sigint_replace
            )
            
            self.p_node = subprocess.Popen(
                ["node", "app.js"],
                preexec_fn = self.sigint_replace
            )
            
            # Run forever, and wait for Ctrl+C
            while True:
                pass

        except KeyboardInterrupt:
            print 'shutting down view server'
            self.p_http.terminate()
            self.p_node.terminate()
        
        
          