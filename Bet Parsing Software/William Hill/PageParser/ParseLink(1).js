//var client = new XMLHttpRequest();
//process.argv.forEach(function (val, index, array) {
//  console.log(index + ': ' + val);
//});
var args = process.argv.slice(2);
console.log(args[0]);
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var tmp = new XMLHttpRequest();
//console.log("LOL 1");
//var x = HttpRequest("http://sports.williamhill.com/bet/en-gb","POST",function(req){console.log(req);},"action=GoEv&ev_id="+"6812892"+"&ExpandEvCollection=1&UseEvCollectionId="+25+"&playJSON=1&ev_status=A",false);
//console.log("LOL 2");
var x = 3;
if (x==undefined)
	console.log("Undefined");
else{
	console.log(x.responseText);
//	console.log("LOL 3");
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