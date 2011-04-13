io.setPath('/');
if ('undefined'===typeof(io)) { throw new Error("Application failed to load: Socket.IO not found"); }
var socket = new io.Socket("localhost", {port:9202});

$(document).ready(function() {
	// Hide chat interface until after login.
	$("div#container").hide();
	$("#loginButton, #submitButton, #runtaskButton").button();
	$("#loginForm :input:visible:enabled:first").focus();

	// Login form submit calls init() to start the chat interface.
	$("#loginButton").click(function() { return init(); });
	$("#loginForm").submit( function() { return init(); });

	// Submit button / enter keypress submit the chat message.
	$("#submitButton").click(function() { 
		pushMsg( $('#im').val() ); 
		$('#im').val('');
  		$('#im').focus();
	});
	$('#imchat').submit(function() { return pushMsg( $('#im').val() ); });	
	$('#runtaskButton').click(function() { return runtask(); });
});

// This function grabs the username from the login box and sends a login
// request message to the server. It also associates the pullMsg() handler
// function with the websocket so that messages will be handled there.
var init = function() {
	var username = $("#loginText").val();
	$("#login").fadeOut(function() { 
		$("div#container").show();
		$("#chats").scrollTop($("#chats")[0].scrollHeight); 
	});
  	socket.on('message', pullMsg);
  	socket.connect();
	socket.send("USERNAME:" + username);
	return false;
};

// This function sends a request to the server to run a task.
var runtask = function() {
	socket.send("RUNTASK:");
	return false;
};

// This function pushes a message to the server from the chat box.
var pushMsg = function(msg) {
  	if (msg) {
		socket.send(msg);
    	renderMsg({message:msg});
  	}
	return false;
};

var pullMsg = function(data) {
  if ("string"===typeof(data)) { data = JSON.parse(data); }
  return renderMsg(data);
};

var renderMessage = function(message) {
	var username = (message.username) ? message.username : "me";
	return "<li class='chat'><span class='user'>" + username + ": </span>" + 
		   					"<span class='message'>" + message.message + "</span></li>";
};

var renderMsg = function(data) {
	// Just a single message
  	if (data && data.message) {        
    	$('#chats').append(renderMessage(data));
  	}
	// Announcement
	else if (data && data.announcement) {
		$('#chats').append("<li class='information'>" + data.announcement + "</li>");
	} 
	// User list
	else if (data && data.userlist && data.userlist.length) {
		$('#chats').append("<li class='information'>Users: " + data.userlist.join(", ") + "</li>");
	}
	// Batch messages
	if (data && data.messages) {     
    	for (var msg in data.messages) {
    		$('#chats').append(renderMessage(data.messages[msg]));
    	}
  	}
	$("#chats").scrollTop($("#chats")[0].scrollHeight);
	return false;
};