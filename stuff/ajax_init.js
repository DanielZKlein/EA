// to enable ajax functionality, include this script and put heartBeat() in your ready function

var ajaxRefreshFunctions = new Array(); // all functions that need to be called before sending out a refresh request
var ajaxRefreshCallbackFunctions = new Array(); // all functions that want to be notified of an ajax reply; these should take the JSON object and do sth to the page
var ajaxFrequency = 400;
var ajaxStopRefresh = false; // for debug purposes

// ajaxDoRefresh: should be called by the periodic heartbeat function. Collects data from all the refreshFunctions
function dbug(obj) {
	try {
		console.log(obj);
	} catch(e) {
	}
}

function ajaxDoRefresh() {

	refreshObject = {};
	for (i=0; i < ajaxRefreshFunctions.length; i++) {
		$.extend(refreshObject, ajaxRefreshFunctions[i]());
	}
	$.getJSON('/ajax/', refreshObject, ajaxTakeRefresh);
	$("#ajaxstatus").html("syncing...");
}

function ajaxTakeRefresh(JSONobj) {
	$("#ajaxstatus").html("thinking...");
	for (i = 0; i < ajaxRefreshCallbackFunctions.length; i++) {
		ajaxRefreshCallbackFunctions[i](JSONobj);
	}
	heartBeat()
}

function heartBeat() {

	if (ajaxStopRefresh) {
		$("#ajaxstatus").html("killed");
		return;
	}
	setTimeout(ajaxDoRefresh, ajaxFrequency);
	$("#ajaxstatus").html("synced");
}