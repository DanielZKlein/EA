// things this script needs to do
// update the player lists in the teams and move the arrow accordingly
// --> this involves:
// * receiving an up-to-date player list from server, which includes team affiliations
// * writing them to the divs
// * highlighting "me" 
// * putting the arrow in
// * (eventually) indicating afk-ness
 
ajaxRefreshFunctions.push(playersRefresh);
ajaxRefreshCallbackFunctions.push(playersTakeRefresh);
 
function playersRefresh() {
 
	rv = new Object();
	rv["players" + thisGameId + "refresh"] = "yesplease";
	return rv;
 
 }
 
function gameSwapTeams() {

	$.get("/swapteamongame/" + thisGameId);


}
function playersTakeRefresh(JSONobj) {
	
	if (JSONobj.playerupdates[thisGameId]) {
		updatePlayerLists(JSONobj.playerupdates[thisGameId]);
	} else {
		dbug("empty refresh and we are " + thisGameId + ":");
		console.dir(JSONobj.playerupdates[4]);
	}
}
 
function updatePlayerLists(update) {
	team1 = update.team1;
	team2 = update.team2;
	myteam = ""; 
	$("#clmid").empty();
	$("#crmid").empty();
	for (key in team1) {
		name = team1[key];
		$("#clmid").append("<div>" + name + "</div>");
		if (name == myName) {
			myteam = "team1";
		}
	}
	for (key in team2) {
		name = team2[key];
		$("#crmid").append("<div>" + name + "</div>");
		if (name == myName) {
			myteam = "team2";
		}
	}
	if (myteam == "team1") {
	
		$("#cmhteam1").css("display", "block");
		$("#cmhteam2").css("display", "none");
	
	} else {

		$("#cmhteam2").css("display", "block");
		$("#cmhteam1").css("display", "none");
	
	}
}