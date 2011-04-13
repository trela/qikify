/*
 *
 * Attribution: adapted from socket-chat, on github at:
 *  			https://github.com/arunjitsingh/socket-chat
 *
 */

/* Imports */
var io   = require('socket.io'),
    http = require('http'),
    fs   = require('fs'),
    util = require('util'),
    url  = require('url'),
    path = require('path'),
    mime = require('mime'),
    sys  = require('sys'),
    spawn = require('child_process').spawn;

/* Constants */
var outputFile = 'output.log';


function findType(uri) {
  var ext = uri.match(/\.\w+$/gi);
  if (ext && ext.length > 0) {
    ext = ext[0].split(".")[1].toLowerCase();
    return mime.lookup(ext);
  }
  return undefined;
}

function sendError(code, response) {
  response.writeHead(code);
  response.end();
  return;
}

var app = http.createServer(function(request, response) {
  var uri = url.parse(request.url).pathname;
  if (uri === '/') {
    uri = '/index.html';
  } else if (uri === '/app.js') {
    sendError(404, response);
    return;
  }
  var _file = path.join(process.cwd(), uri);

  path.exists(_file, function(exists) {
    if (!exists) {
      sendError(404, response);
    } else {
      fs.stat(_file, function(err, stat) {
        var file = __dirname + uri,
            type = findType(uri),
            size = stat.size;
        if (!type) {
          sendError(500, response);
        }
        response.writeHead(200, {'Content-Type':type, 'Content-Length':size});
        var rs = fs.createReadStream(file);
        util.pump(rs, response, function(err) {
          if (err) {
            console.log("ReadStream, WriteStream error for util.pump");
            response.end();
          }
        });
      });
    }
  });

});


/* Web server set up here */
var clients = [];
var socket  = io.listen(app, {transports:['websocket', 'xhr-polling']}),
  	buffer  = [],
  	MAXBUF  = 1024,
  	json 	= JSON.stringify;

socket.on('connection', function(client) {
  client.on('message', function(data) {
	// Run task request
	if ((/^(RUNTASK:).*$/ig).test(data)) {
		console.log("RUNNING ANALYSIS: Let's do this. Leeeroy...");
		client.send(json({announcement:'Running analysis now.'}));
        
		/* Run child process */
		var child = spawn('python', ['-u', 'main.py'], {cwd:'../framework'});
		child.stdout.setEncoding('ascii');
		child.stderr.setEncoding('ascii');
		
		child.stdout.on('data', function(data) {
		    console.log('stdout: ' + data);
		    client.broadcast(json({'username':'stdout', 'message':data}));
		    client.send(json({'username':'stdout', 'message':data}));
		    
		    /* Append stdout to buffer */
  		    if (data.length > 0) {
  	        buffer.push({'username':'stdout', 'message':data});
                if (buffer.length > MAXBUF) {
                    buffer.shift();
                }
            }
		});
		
		child.stderr.on('data', function (data) {
          if (/^execvp\(\)/.test(data.asciiSlice(0,data.length))) {
            console.log('Failed to start child process.');
          }
          
		  /* Append stderr to buffer */
		  if (data.length > 0) {
              buffer.push({'username':'stderr', 'message':data});
              if (buffer.length > MAXBUF) {
                  buffer.shift();
              }
          }
        });
        
        child.on('exit', function (code) {
          console.log('child process exited with code ' + code);
        });
        
		return;
	}
	
	// Initial connection
    if ((/^(USERNAME:).*$/ig).test(data)) {
      var parts = data.split(":");
      var username = parts[1];
	
	  // ensure non-blank username.
      if (!username || username == '') {
        client.send(json({announcement:"You must specify a username. Please reload the app."}));
        return;
      }

	  // ensure unique username.
      var usernames = clients.map( function(client) { return client.username; } );
      if (usernames.indexOf(username) >= 0) {
        client.send(json({announcement:"Username in use"}));
        return;
      }

      client.username = username;
      client.broadcast(json({announcement:client.username+' joined'}));
      console.log(client.sessionId + " = " + client.username);
      client.send(json({messages:buffer}));
      client.send(json({userlist:usernames}));
      client.send(json({announcement:"Connected! Hello, " + username + "!"}));
	  client.send(json({announcement:"all your base are belong to us."}));
      clients.push(client);
      return;
    } 

    if (!client.username) {
      client.send(json({announcement:"You must specify a username. Please reload the app."}));
      return;
    }
    
    /* Append user msg to buffer */
    buffer.push({'user':client.sessionId, 'username':client.username, 'message':data});
    if (buffer.length > MAXBUF) {
      buffer.shift();
    }
	
	console.log(data);
    client.broadcast(json({'username':client.username, 'message':data}));
  });

  client.on('disconnect', function() {
    if (client.username) {
      client.broadcast(json({announcement:(client.username)+' left chat'}));
    }
    var pos = clients.indexOf(client);
    if (pos >= 0) {
      clients.splice(pos, 1);
    }
  });
});



if (!module.parent) {
  app.listen(9202);
  console.log("The MVC framework app is listening on port 9202.. Go to http://localhost:9202");
}