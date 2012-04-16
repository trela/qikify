import json, zmq

class ViewServerMixin(object):
    """This class allows child classes to send data to the viewserver by
    providing a log_to_viewserver convenience method.
    """
    def __init__(self, name, port, context):
        self.name              = name
        self.context           = context
        self.socket_viewserver = self.context.socket(zmq.PUB)
        self.socket_viewserver.bind('tcp://127.0.0.1:%d' % port)
        
    def update_view(self, msg):
        self.socket_viewserver.send(json.dumps(msg))

        
        
        
