var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var x = new XMLHttpRequest();
var link = process.argv.slice(2)[0];
var r = new RegExp("http://sports.williamhill.com/bet/en-gb/betting/e/([0-9]*)/+");
var matches = link.match(r);
if (matches[1] == undefined) {
	LogWrite("Pattern not found in link: " + link);		// break work next
}
var id = matches[1];
/*
	id - id of match
	str_mode - "goals", "other markets", etc
	output: html text of the response
*/

//var popular = GetHttpResponseGet(link);
var goals = GetResponse(id, "goals");
var regJSON = new RegExp("\"markets\"[^<]+\]", "ig");
//var handicaps = GetResponse(id, "handicaps");
//var other_markets = GetResponse(id, "other markets");
//console.log (goals);
var gl = goals.match(regJSON);
var i = 0;
var headers = [];	// заголовки (например, "Total Team Goals")
var info = [];		// массив массивов; все ячейки со значениями и тексом (текст, числитель, знаменатель)
//var r1 = new RegExp("\{[^\}]+\"lp_num\".+\"([0-9]+)\"[^\}]+\"lp_den\".+\"([0-9]+)\"[^\}]+\"name\".+\"(.+)\"","ig");
//tmp = r1.exec(gl[0]);
//tmp = r1.exec(gl[0]);
//console.log(tmp[1], tmp[2], tmp[3]);
for (i=0;i<1;++i){
	var tmp;
	tmp = (gl[i].match(new RegExp("\"mkt_name\".+\"(.+)\"", "i")));
	headers[i] = tmp[1];
	var r1 = new RegExp("\{[^\}]+\"lp_num\".+\"([0-9]+)\"[^\}]+\"lp_den\".+\"([0-9]+)\"[^\}]+\"name\".+\"(.+)\"","ig");
	var k = 0;
	var ar_texts = [];
	while ((tmp = r1.exec(gl[0])) != null) {
		var text_tmp = [];
		text_tmp[0] = tmp[3];
		text_tmp[1] = tmp[1];
		text_tmp[2] = tmp[2];
		ar_texts[k++] = text_tmp;
	}
	info[i] = ar_texts;
}
//console.log(goals);
//console.log(GetText(goals));
function ExtractFromJSON(text) {
	var header; var texts = []; var chisl = []; var znam = [];
	
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
	return "";
}
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
	var post="action=GoEv&ev_id="+ev_id+"&ExpandEvCollection=1&UseEvCollectionId="+collection_id;
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