/*
input:
	arg1 - ссылка на страницу с информацией
	arg2 - название файла, в которых сохраняется результат работы
	arg3 - название первой команды (оно будет записано в файл-результат)
	arg4 - название второй команды (оно будет записано в файл-результат)
*/
const NoBet = -1;
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var x = new XMLHttpRequest();
var link = process.argv.slice(2)[0];
var file_name = process.argv.slice(3)[0];
var global_cmd1 = ""; var global_cmd2 = "";
try {
	global_cmd1 = process.argv.slice(4)[0];
	global_cmd1 = global_cmd1.replace(new RegExp("\n"), "");
	global_cmd2 = process.argv.slice(5)[0];
	global_cmd2 = global_cmd2.replace(new RegExp("\n"), "");
}
catch (e) {}
var r = new RegExp("http://sports.williamhill.com/bet/en-gb/betting/e/([0-9]*)/+");
var matches = link.match(r);
if (matches[1] == undefined) {
	LogWrite("Pattern not found in link: " + link);		// break work next
}
var id = matches[1];
var other_info = []; var goals_info = []; var main_info = []; var handicaps_info = [];
var main_html = GetHttpResponseGet(link);
//console.log(GetDateTime(main_html));
if (!IsEmptyResponse(main_html)) {
	var regJSON = new RegExp("\"markets\"[^<]+\]", "ig");
	var gl = main_html.match(regJSON);
	main_info = ExtractFromJSONMain(gl);
}
//PrintInfo(main_info);
var goals = GetResponse(id, "goals");
if (!IsEmptyResponse(goals)) {
	var regJSON = new RegExp("\"markets\"[^<]+\]", "ig");
	var gl = goals.match(regJSON);
	goals_info = ExtractFromJSON(gl);
}
//PrintInfo(goals_info);

//var handicaps = GetResponse(id, "handicaps");

/*var other_markets = GetResponse(id, "other markets");
var other_info = [];
if (!IsEmptyResponse(other_markets)) {
	var regJSON = new RegExp("\"markets\"[^<]+\]", "ig");
	var gl = other_markets.match(regJSON);
	other_info = ExtractFromJSON(gl);
}*/
/*for (i=0;i<headers.length;++i){
	console.log(headers[i]);
	for(j=0;j<info[i].length;++j)
		console.log(info[i][j]);
}*/
var match_id = GetMatchId(main_html);
var cmds = GetCmdNames(main_html);
var datetime = GetDateTime(main_html);
var ml = InitArray(6);
var total_under = InitArray(21);
var total_over = InitArray(21);
var total_home_over = InitArray(21);
var total_home_under = InitArray(21);
var total_away_over = InitArray(21);
var total_away_under = InitArray(21);
var odds = InitArray(6);  // total(odd, even), home(odd, even), away(odd, even)
var asian_total_under = InitArray(21);
var asian_total_over = InitArray(21);

var handicap_home = InitArray(41);
var handicap_away = InitArray(41);
var asian_handicap_home = InitArray(40);
var asian_handicap_away = InitArray(40);
var total_equal = InitArray(11);
var home_to_score = InitArray(2);	// [0] - no; [1] - yes
var away_to_score = InitArray(2);	// [0] - no; [1] - yes
var both_to_score = InitArray(2);	// [0] - no; [1] - yes
var winning_margin_home = InitArray(11);
var winning_margin_away = InitArray(11);
var correct_score = new Array(16);
var any_other_score = NoBet;
for (i=0; i<16; ++i) {
	correct_score[i] = new Array(16);
}
//console.log(correct_score[0].length, correct_score[1].length, correct_score[2].length);
if (main_info.length != 0) {
	var i = 0; var headers = main_info[0]; var info = main_info[1];
	for (i=0; i<headers.length; ++i) {
		var h = headers[i].toLowerCase();
		var events = info[i];
		if (h == "match betting") {
			for (j=0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				if (events[j][2] == cmds[0]) { ml[0] = value; }
				else if (events[j][2] == cmds[1]) { ml[2] = value; }
				else if (events[j][2].toLowerCase() == "draw") { ml[1] = value; }
			}
		}
		if (h == "double chance") {
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				if (events[j][2] == cmds[0] + " Or Draw") { ml[3] = value; }
				else if (events[j][2] == cmds[1] + " Or Draw") { ml[4] = value; }
				else if (events[j][2] == cmds[0] + " Or " + cmds[1]) { ml[5] = value; }
			}
		}
		if (h == "total match goals under/over") {
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				if (events[j][2].substr(0, 4) == "Over") {
					var index = parseFloat(events[j][2].slice(5))*2;
					total_over[index] = value;
				}
				else {		// == "Under"
					var index = parseFloat(events[j][2].slice(6))*2;
					total_under[index] = value;
				}
			}
		}
		if (h == "both teams to score") {
			for (j = 0; j<events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				if (events[j][2] == "Yes") { both_to_score[1] = value; }
				else if (events[j][2] == "No") { both_to_score[0] = value; }
			}
		}
		if (h == cmds[1].toLowerCase() + " to score") {
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				if (events[j][2] == "Yes") { away_to_score[1] = value; }
				else if (events[j][2] == "No") { away_to_score[0] = value; }
			}
		}
		if (h == cmds[0].toLowerCase() + " to score") {
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				if (events[j][2] == "Yes") { home_to_score[1] = value; }
				else if (events[j][2] == "No") { home_to_score[0] = value; }
			}
		}
		if (h == "correct score") {
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				var re = new RegExp("([0-9]+)[^0-9]*([0-9]+)", "i");
				var index1 = events[j][2].search(new RegExp(cmds[0]));
				var index2 = events[j][2].search(new RegExp(cmds[1]));
				var index3 = events[j][2].search(new RegExp("Draw"));
				var tmp = events[j][2].match(re);
				if (tmp == null) {	// throw an error
					console.log("Error in parsing Correct Scrore\n");
				}
				else {
					var x = parseInt(tmp[1]);
					var y = parseInt(tmp[2]);
					if (index2 != -1) {
						var c = x; x = y; y = c;
					}
					//console.log("x, y: ", x, y);
					correct_score[x][y] = value;
				}
			}
		}
		if (h == "match handicaps") {
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				var index1 = events[j][2].search(new RegExp(cmds[0], "i"));
				var index2 = events[j][2].search(new RegExp(cmds[1], "i"));
				var re = new RegExp("([-+][0-9]+)", "i");
				var tmp;
				var home = index1 != -1 && index2 == -1;
				var away = index1 == -1 && index2 != -1;
				var both = index1 != -1 && index2 != -1;
				if (home) {	// handicap_home
					tmp = events[j][2].match(re);
				}
				else if (away) {	// handicap_away
					tmp = events[j][2].match(re);
				}
				else if (both) {
					continue;
				}
				var g = (parseInt(tmp[1]) - 0.5)*2 + 20;
				if (g >= handicap_home.length || g < 0) {
					console.log("Error in Handicaps index", events[j][2]);
					continue;
				}
				if (home) { handicap_home[g] = value; }
				else if (away) { handicap_away[g] = value; }
			}
		}
	}
}

if (goals_info.length != 0) {
	var i = 0; var headers = goals_info[0]; var info = goals_info[1];
	for (i=0; i<headers.length; ++i) {
		var h = headers[i].toLowerCase();
		var events = info[i];
		//console.log(h);
		//console.log(events);
		if (h == "total match goals odd/even") {
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				if (events[j][2] == "Odd") { odds[0] = value; }
				else if (events[j][2] == "Even") { odds[1] = value; }
			}
		}
		//var re = new RegExp(cmds[0].toLowerCase() + " under/over", "i");
		//console.log(h.match(re));
		if (h.indexOf(cmds[0].toLowerCase() + " under/over") == 0) {
			var re = new RegExp(".*([0-9]{1,2}[.][0-9]?).*", "i");
			var tmp = h.match(re);
			if (tmp == null) {
				var re = new RegExp(".*([0-9]{1,2}).*", "i");
				tmp = h.match(re);
			}
			if (tmp == null) {
				console.log("error in total match goals odd/even");
				break;
			}
			var index = parseFloat(tmp[1])*2;
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				//console.log(events[j][2]);
				if (events[j][2].substr(0, 4) == "Over") {
					total_home_over[index] = value;
				}
				else { total_home_under[index] = value; }
			}
		}
		if (h.indexOf(cmds[1].toLowerCase() + " under/over") == 0) {
			var re = new RegExp(".*([0-9]{1,2}[.][0-9]?).*", "i");
			var tmp = h.match(re);
			if (tmp == null) {
				var re = new RegExp(".*([0-9]{1,2}).*", "i");
				tmp = h.match(re);
			}
			if (tmp == null) {
				console.log("error in total match goals odd/even");
				break;
			}
			var index = parseFloat(tmp[1])*2;
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				//console.log(events[j][2]);
				if (events[j][2].substr(0, 4) == "Over") {
					total_away_over[index] = value;
				}
				else { total_away_under[index] = value; }
			}
		}
		if (h == "total match goals") {
			for (j = 0; j < events.length; ++j) {
				var value = events[j][0] / events[j][1] + 1;
				if (events[j][2].search(new RegExp("More", "i")) != -1) continue;
				if (events[j][2] == "None") { total_equal[0] = value; }
				else if (events[j][2] == "One") { total_equal[1] = value; }
				else if (events[j][2] == "Two") { total_equal[2] = value; }
				else if (events[j][2] == "Three") { total_equal[3] = value; }
				else if (events[j][2] == "Four") { total_equal[4] = value; }
				else if (events[j][2] == "Five") { total_equal[5] = value; }
				else if (events[j][2] == "Six") { total_equal[6] = value; }
				else if (events[j][2] == "Seven") { total_equal[7] = value; }
				else if (events[j][2] == "Eight") { total_equal[8] = value; }
				else if (events[j][2] == "Nine") { total_equal[9] = value; }
				else if (events[j][2] == "Ten") { total_equal[3] = value; }
			}
		}
	}
}
PrintOutput(match_id, cmds, datetime, ml, total_under, total_over, odds, total_home_under, 
	total_home_over, asian_total_under, asian_total_over, handicap_home, handicap_away,
	asian_handicap_home, asian_handicap_away, total_equal, home_to_score, away_to_score, 
	both_to_score, winning_margin_home, winning_margin_away, correct_score, any_other_score);

/*var info = main_info[1];
for (i=0;i<info.length;++i){
	for (j=0; j<info[i].length;++j) {
		var http://sports.williamhill.com/bet/en-gb/betting/e/6871163/Aston-Villa-v-Leicester.htmlevent = info[i][j];
		//if (event[0] == cmds[0]) console.log(event);
	}
}
console.log(info.length);
PrintOutput(match_id, cmds, datetime, ml);*/

/*
	severity - 0..10; 0 - самая слабая, 10 - самая сильная
	text
*/
function ThrowError(severity, text) {
	console.log(text);
	if (severity == 10) {
		x = 1;
	}
	return;
}
	
/*
	печатает извлеченную информацию в файл
	!!! ОШИБКА всегда печатается 2015 год !!!
*/
function PrintOutput(match_id, cmds, datetime, ml, total_under, total_over, odds, total_home_under, 
	total_home_over, asian_total_under, asian_total_over, handicap_home, handicap_away,
	asian_handicap_home, asian_handicap_away, total_equal, home_to_score, away_to_score, 
	both_to_score, winning_margin_home, winning_margin_away, correct_score, any_other_score) {
	var fs = require('fs');
	var text = "";
	if (global_cmd1 != "" && global_cmd2 != "") {
		cmds[0] = global_cmd1;
		cmds[1] = global_cmd2;
	}
	text += cmds[0] + "\n" + cmds[1] + "\n";
	text += "2015" + " " + datetime[1] + " " + datetime[0] + "\n";
	text += datetime[2] + " " + datetime[3] + "\n";
	text += TestValue(ml[0]) + "\n" + TestValue(ml[1]) + "\n" + TestValue(ml[2]) + "\n" + 
		TestValue(ml[3]) + "\n" + TestValue(ml[4]) + "\n" + TestValue(ml[5]) + "\n";
	var i;
	for (i=0;i<21; ++i) {
		text += TestValue(total_under[i]) + " ";
	}
	text += "\n";
	for (i=0;i<21; ++i) {
		text += TestValue(total_over[i]) + " ";
	}
	text += "\n";
	text += TestValue(odds[0]) + "\n" + TestValue(odds[1]) + "\n";	// total(odd, even)
	text += TestValue(odds[2]) + "\n" + TestValue(odds[3]) + "\n";	// home(odd, even)
	text += TestValue(odds[4]) + "\n" + TestValue(odds[5]) + "\n";	// away(odd, even)
	for (i=0;i<21; ++i) {
		text += TestValue(total_home_under[i]) + " ";
	}
	text += "\nTotal Home Over\n";
	for (i=0;i<21; ++i) {
		text += TestValue(total_home_over[i]) + " ";
	}
	text += "\nTotal Away Under\n";
	for (i=0;i<21; ++i) {
		text += TestValue(total_away_under[i]) + " ";
	}
	text += "\nTotal Away Over";
	for (i=0;i<21; ++i) {
		text += TestValue(total_away_over[i]) + " ";
	}
	text += "\nAsian Totals Under/Over\n";
	for (i = 0; i<21; ++i) {
		text += TestValue(asian_total_under[i]) + " ";
	}
	text += "\nHandicap Home/Away\n";
	for (i = 0; i<41; ++i) {
		text += TestValue(handicap_home[i]) + " ";
	}
	text += "\n";
	for (i = 0; i<41; ++i) {
		text += TestValue(handicap_away[i]) + " ";
	}
	text += "\nAsian Handicap Home/Away\n";
	for (i = 0; i<40; ++i) {
		text += TestValue(asian_handicap_home[i]) + " ";
	}
	text += "\n";
	for (i = 0; i<40; ++i) {
		text += TestValue(asian_handicap_away[i]) + " ";
	}
	text += "\nTotal Equal\n";
	for (i = 0; i<total_equal.length; ++i) {
		text += TestValue(total_equal[i]) + " ";
	}
	text += "\nOdinary\n";
	text += TestValue(home_to_score[1]) + "\n" + TestValue(both_to_score[0]) + "\n" + TestValue(both_to_score[1]) + "\n" + TestValue(away_to_score[1]) + "\n";
	text += "\nWinning Margin Hime/Away\n";
	for (i = 0; i<winning_margin_home.length; ++i) {
		text += TestValue(winning_margin_home[i]) + " ";
	}
	text += "\n";
	for (i = 0; i<winning_margin_away.length; ++i) {
		text += TestValue(winning_margin_away[i]) + " ";
	}
	text += "\nCorrect Score\n";
	//console.log("corr ", correct_score.length, "\n");
	for (i=0; i<correct_score.length; ++i) {
		for (j=0; j<correct_score[i].length; ++j) {
			text += TestValue(correct_score[i][j]) + " ";
		}
		text += "\n";
	}
	text += TestValue(any_other_score);
	//console.log(text);
	fs.writeFile(file_name, text);
}
function TestValue(value) {
	if (value == undefined) { return NoBet; }
	else if (value == NaN) {
		return NoBet;
	}
	else if (value == null) {
		return NoBet;
	}
	else if (value <= 1) {
		return NoBet;
	}
	return Math.round(value) == value ? value : value.toFixed(2);
}
/*
	Инициализирует массив константами NoBet
*/
function InitArray(n) {
	var arr = [];
	for (i=0;i<n;++i) arr[i] = NoBet;
	return arr;
}
/*
	получает id команды по названию команды
*/
function GetCmdIdByName(cmd_name) {
	return cmd_name;
}
function GetMatchId(html) {
	return "id0";
}
function GetDateTime(html) {
	var re = new RegExp("Bet until[^0-9]+([0-9]{2})[^a-z]+(...)[^0-9]+([0-9]{2}).([0-9]{2})", "i");
	var m = html.match(re);
	return [parseInt(m[1]), MapMonth(m[2]), CalcRealTime(parseInt(m[3])), parseInt(m[4])];
}
function GetCmdNames(html) {
	var re = new RegExp("<h2>([^<]+)</h2>", "i");
	var m = html.match(re);
	var re = new RegExp("[\n\t]+(.+) v (.+) - All", "i");
	var mm = m[1].match(re);
	return [GetCmdIdByName(mm[1]), GetCmdIdByName(mm[2])];
}
/* преобразование времени к адекватной часовой зоне */
function CalcRealTime(time) { return time + 4; }
/* m == "Dec", m == "Jan", etc. */
function MapMonth(m) {
	m = m.toLowerCase();
	if (m == "jan") return 1;
	else if (m == "feb") return 2;
	else if (m == "mar") return 3;
	else if (m == "apr") return 4;
	else if (m == "may") return 5;
	else if (m == "jun") return 6;
	else if (m == "jul") return 7;
	else if (m == "aug") return 8;
	else if (m == "sep") return 9;
	else if (m == "oct") return 10;
	else if (m == "nov") return 11;
	else if (m == "dec") return 12;
	else return -1;
}
function PrintInfo(parsed_info) {
	var headers = parsed_info[0];
	var info = parsed_info[1];
	for (i=0;i<headers.length;++i){
		console.log(headers[i]);
		for(j=0;j<info[i].length;++j)
			console.log(info[i][j]);
	}
	console.log("Info printed.");
	return 0;
}
function IsEmptyResponse(html) {
	/*var i;
	for (i=0; i<html.length; ++i) {
		var ch = html[i];
		if (ch != '\n' || ch != '\t' || ch != ' ')
			return false;
	}
	return true;*/
	if (html == undefined) return true;
	if (html.length < 300) return true;
	else return false;
}
function ExtractFromJSONMain(JSON_array) {
	var gl = JSON_array[0];
	var re = new RegExp("\"ev_mkt_id\".+\"(.+)\"[^\}]+\"mkt_name\".+\"(.+)\"", "ig");
	var tmp;
	var headers = []; var ids = [];
	var i = 0;
	while ((tmp = re.exec(gl)) != null) {
		headers[i] = tmp[2];
		ids[i++] = tmp[1];
	}
	var arr = []; var id = [];
	var re = new RegExp("\"ev_mkt_id\".+\"(.+)\"[^\}]+\"lp_num\".+\"(.+)\"[^\}]+\"lp_den\".+\"(.+)\"[^\}]+\"name\".+\"(.+)\"", "ig");
	i = 0;
	while ((tmp = re.exec(gl)) != null) {
		id[i] = tmp[1];
		arr[i++] = [tmp[2], tmp[3], tmp[4]];
	}
	var parsed_info = []; var j = 0;
	for (i=0;i<headers.length;++i){
		//console.log(headers[i]);
	}
	for (i=0; i<headers.length; ++i) {
		var info = []; k = 0;
		while (id[j] == ids[i]) {
			info[k++] = (arr[j]);
			j++;
		}
		//console.log(info);
		parsed_info[i] = info;
	}
	return [headers, parsed_info];
}
function ExtractFromJSON(JSON_array) {
	var gl = JSON_array;
	var headers = []; var info = [];
	//console.log(gl.length);
	for (i=0;i<gl.length;++i){
		var tmp1 = (gl[i].match(new RegExp("\"mkt_name\".+\"(.+)\"", "i")));
		headers[i] = tmp1[1];
		//console.log(headers[i]);
		var r1 = new RegExp("\{[^\}]+\"lp_num\".+\"([0-9]+)\"[^\}]+\"lp_den\".+\"([0-9]+)\"[^\}]+\"name\".+\"(.+)\"","ig");
		var k = 0;
		var ar_texts = [];
		while (true) {
			var tmp = r1.exec(gl[i]);
			if (tmp == null) break;
			var text_tmp = [];
			//console.log(tmp[3], tmp[1], tmp[2]);
			text_tmp[0] = tmp[1];
			text_tmp[1] = tmp[2];
			text_tmp[2] = tmp[3];
			ar_texts[k++] = text_tmp;
			//console.log(tmp[1], tmp[2], tmp[3]);
		}
		info[i] = ar_texts;
	}
	return [headers, info];
}

function DelEnter(text) {
	var i; var res = "";
	for (i=0;i<text.length;++i) {
		var ch = text[i];
		if (ch != "\n")
			res += ch;
	}
	return res;
}
function GetText(html) {
	var i;
	var inTag = 0;
	var text = "";
	for (i=0; i<html.length;++i) {
		var ch = html[i];
		if (ch == "<") {
			inTag++;
		}
		else if (ch == ">") {
			inTag--;
		}
		else if (inTag == 0) {
			if (ch != "\n" && ch != "\t" && ch != " ")
				text += ch;
		}
	}
	return text;
}
function GetHttpResponseGet(link) {
	var xmlHttp = null;
	xmlHttp = new XMLHttpRequest();
	xmlHttp.open( "GET", link, false );
	xmlHttp.send( null );
	return xmlHttp.responseText;
}
/*
	my_id - id of match
	str_mode - "goals", "other markets", etc
	output: html text of the response
*/
function GetResponse(my_id, str_mode) {
	var ev_id; var id; var collection_id;
	ev_id = String(my_id);
	if (str_mode == "goals") {
		id = "collection25";
		collection_id = 25;
	}
	else if (str_mode == "other markets") {
		id = "collectionOther";
		collection_id = 'other'
	}
	else if (str_mode == "handicaps") {
		id = "collection71";
		collection_id = 71;
	}	
	var res = HttpRequest("http://sports.williamhill.com/bet/en-gb","POST",function(req){return;},
		"action=GoEv&ev_id="+ev_id+"&ExpandEvCollection=1&UseEvCollectionId="+collection_id+"&playJSON=1&ev_status=A",false);
	
	return res.responseText;
}
function LogWrite(str) {
	console.log(str);
}
function getXMLHttpRequest(){
	var httpReq=false;
	try{httpReq=new XMLHttpRequest}
	catch(e){
		var type=["MSXML2.XMLHTTP.3.0","MSXML2.XMLHTTP","Microsoft.XMLHTTP"],i=0,len=type.length;
		for(;i<len;i++)
			try{httpReq=new ActiveXObject(type[i]);break}
			catch(e){}
	}
	finally {return httpReq}
}
function GetCollectionData(id,collection_id,ev_id){
	var obj=this;
	var post="action=WriteGoEv&ev_id="+ev_id+"&ExpandEvCollection=1&UseEvCollectionId="+collection_id;
	if(document.push_enabled)
		post+="&playJSON=1&ev_status="+document.ls_event.status;
	HttpRequest(document.cgi_url,"POST",function(req){obj.EvCallback(req,id)},post,true)
}
function HttpRequest(_url,_method,_callback,_post,_varAsync,_extra_hdrs,_error_check_callback,_error_callback){
	var req=getXMLHttpRequest();
	if(!req){console.log("Your browser does not support AJAX, please upgrade");return}
	if(typeof _varAsync==="undefined"||typeof _varAsync==="object"){
		_varAsync=true;
		_extra_hdrs=null
	}
	req.open(_method,_url,_varAsync);
	req.setRequestHeader("Content-Type","application/x-www-form-urlencoded;");
	if(typeof _extra_hdrs==="object"&&_extra_hdrs!==null){
		var hdr;
		for(hdr in _extra_hdrs)
			req.setRequestHeader(hdr,_extra_hdrs[hdr])
	}
	/*if(_varAsync)
		req.onreadystatechange=function(){
		if(req.readyState==4){
			if(browser.ie||browser.ffox)
				req.onreadystatechange=new Function;
			if(typeof _error_callback==="function"&&typeof _error_check_callback==="function"&&_error_check_callback(req.status)==false)
				return _error_callback(req);
			_callback(req);
		}
	}*/
	if(_method=="POST")
		req.send(_post);
	else req.send(null);
	if(!_varAsync)
		_callback(req);
	return req
}