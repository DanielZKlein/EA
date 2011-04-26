if (!window.chat_init_loaded) {
	window.chat_init_loaded = true;
	ajaxRefreshFunctions.push(chatRefresh);
	ajaxRefreshCallbackFunctions.push(chatTakeRefresh);

	var chats = new Object(); // A list of chat instances used on this page
	// write to it like this:
	// chats[{{chatid}}] = new Object();
	// chats[{{chatid}}]['users'] = new Array();
	// chats[{{chatid}}]['id'] = {{chatid}};
	// chats[{{chatid}}]['chatboxid'] = "chat{{chatid}}box";
	// chats[{{chatid}}]['userlistid'] = "chat{{chatid}}userlist";

	// I imagine every single chat module registering itself like so:
	// window.chatLastids["chat{{chat.id}}refresh"] = 0;
	// Then, whenever we get a new lastid in takerefresh, we write it in
	// no this is bullshit. Do this instead:
	// window.chatLastids[{{chatid}}] = 0;
	// still bullshit. How about this:
	// chats[{{chatid}}]['lastid'] = 0;

	function chatInit() {
		for (chat in chats) {
			mychat = chats[chat];
			$("#"+mychat.formid).submit(function(event){
				chatSay(chat, $("#"+mychat.inputid).val());
				$("#" + mychat.inputid).val(""); 
				event.preventDefault();
			});
			$("#"+mychat.inputid).keydown(function(event){
				keydown(event);
				});
			$("body").keyup(function(event) {
				keyup(event);
				});
		}
	}

	playsound = true;

	function enddelay() {
		playsound = true;
	}

	keyisdown = false;

	function keyup(event) {

		keyisdown = false;

	}

	function keydown(event) {

		nonsoundkeys = [16, 17, 18, 9, 20]; // alt, ctrl, shift, tab, caps lock
		if (nonsoundkeys.indexOf(event.keyCode) > -1) {
			return;
		}
		dbug(event.keyCode);
		if (keyisdown) {
			return; // don't play sounds for holding down a key
		}
		keyisdown = true;
		switch (event.keyCode) {
		
			case 8:
				filename = "type_bspace";
				break;
			case 13:
				filename = "type_return";
				break;
			default:
				filename = "type";
		}
		if (filename == "type") {
			if (playsound) {
				audio = document.createElement('audio');
				audio.setAttribute('src', 'http://127.0.0.1:8000/stuff/' + filename + '.ogg'); 
				audio.load();
				audio.volume = 0.3;
				audio.play();
				playsound = false;
				setTimeout("enddelay();", 150);
			} else {
				audio = document.createElement('audio');
				audio.setAttribute('src', 'http://127.0.0.1:8000/stuff/' + filename + 'silent.ogg'); 
				audio.load();
				audio.volume = 0.2;
				audio.play();
			}
		} else {
			audio = document.createElement('audio');
			audio.setAttribute('src', 'http://127.0.0.1:8000/stuff/' + filename + '.ogg'); 
			audio.load();
			audio.play();
		}
	}

	function chatSay(id, what) {
		// send a line of chat to the backend. D'oh.
		$.get("/chatsay/"+id, "text="+what);
	}

	function chatRefresh() {

		// For now, go through all the chats registered and create and object of "chatXXrefresh" : lastid
		chatLastIds = new Object();
		for (chat in chats) { 
			chatLastIds["chat" + chat + "refresh"] = chats[chat]['lastid'];
		}
		
		return chatLastIds

	}

	function chatTakeRefresh(JSONobj) {
		// a bit on code distribution. I could have chosen to have the "join" and "leave" actions automatically create the corresponding text in the chatbox, but I didn't. Reasons:
		// 1) I want all user-facing text in python for sanity (and eventual i18n, of course)
		// 2) I may not ALWAYS want to trigger that text (for instance when you first request a chat, all players in it "join") (how are we going to make that happen on django-side?)

		for (id in JSONobj.chatqueues) {
			if (JSONobj.chatqueues[id].length > 0) {
				userListChanged = false;
				chatBoxChanged = false;
				mychat = chats[id];
				being_a_dick:
				for (a_id in JSONobj.chatqueues[id]) {
					action = JSONobj.chatqueues[id][a_id];
					// action is an array: action[0] is the command, action[1] is the argument
					switch (action[0]) {
						case "join":
							// A new player joined the chat. Add to userlist and mark as changed for refresh
							if (action[1] in mychat.users) {
								dbug("Warning! Attempting to join a user to a chat that already contains the user. Continuing.");
								continue being_a_dick;
							}
							mychat.users[action[1]] = new Object();
							mychat.users[action[1]].nick = action[2];
							mychat.users[action[1]].status = action[3];
							userListChanged = true;
							break;
						case "leave":
							// A player left the chat
							if (!action[1] in mychat.users) {
								dbug("Warning! Attempting to remove a user from a chat that didn't include him. Continuing.");
								continue being_a_dick;
							}
							mychat.users.splice(action[1],1); 
							userListChanged = true;
							break;
						case "say":
							// A message was sent to the chat. Add it to the chatbox
							// Remember to end all text sent with a <br>. Or sth.
							oldtext = $("#"+mychat.chatboxid).html();
							newtext = oldtext + action[1];
							$("#"+mychat.chatboxid).html(newtext);
							chatBoxChanged = true;
							break;
						case "status":
							// a user has changed his status
							// still not sure how to handle this. Do I want a LINE type that contains this info? It's fiddly, since it would only update when queried.
							break;
						case "newlastid":
							mychat.lastid = action[1];
							break;
					}
				}
				if (userListChanged) {
					newlist = "";
					for (user in mychat.users) {
						myuser = mychat.users[user];
						newlist += myuser.nick + " (" + myuser.status + ")<br>";
					}
					$("#"+mychat.userlistid).html(newlist);
				}
				if (chatBoxChanged) {
					chatarea = document.getElementById(mychat.chatboxid);
					chatarea.scrollTop = chatarea.scrollHeight;
				}
			}
		}
	}
}