/**
 * Get all data about football mathes from www.sbobet.com.
 */

/* Add some useful methods to String class */
String.prototype.replaceAll =
    function (search, replace) {
        return this.split(search).join(replace);
    };

String.prototype.trim =
    function() {
        return this.replace(/^\s+|\s+$/g, '');
    };

String.prototype.ltrim =
    function() {
        return this.replace(/^\s+/,'');
    };

String.prototype.rtrim =
    function() {
        return this.replace(/\s+$/,'');
    };

String.prototype.fulltrim =
    function() {
        return this.replace(/(?:(?:^|\n)\s+|\s+(?:$|\n))/g,'').replace(/\s+/g,' ');
    };

/* Global parameters */
var num_days = 3; // number of days to parse
var date_array = []; // array of the formatted dates, which will be initialized in main()
var match_urls_parsed = false; // will be true when parse urls will finish
/**
 * Array of formatted dates (YYYY-MM-DD) in an amount of num_days.
 */
function get_date_array() {
    var date = new Date();

    for (var i = 0; i < num_days; i++) {
        var day = date.getDate();
        var month = date.getMonth() + 1;
        var year = date.getFullYear();
        // add date to the array
        date_array.push([year + "-" + month + "-" + day]);
        date.setDate(date.getDate() + 1);
    }
    return date_array;
}


function find_match_urls(func) {
    var https = require('https');

    var options = {
        host: 'www.sbobet.com',
        headers: {'user-agent': 'Mozilla/5.0'},
        path: '/euro/football'
    };

    callback = function(response) {
        var str = '';

//another chunk of data has been recieved, so append it to `str`
        response.on('data', function (chunk) {
            str += chunk;
        });

//the whole response has been recieved, so we just print it out here
        response.on('end', function () {
            console.log(str);
        });
    }

    https.request(options, callback).end();
}


/**
 * Get array of all urls to the match specific pages for the corresponding day.
 * @param func
 */
function find_match_urls1(func) {
    // use https protocol for www.sbobet.com
    var https = require('https');

    // options for GET request to get https://www.sbobet.com/euro/football html page
    var options = {
        hostname: 'www.sbobet.com',
        port: 443,
        encoding: 'binary',
        path: '/euro/football/',
        headers: {'user-agent': 'Mozilla/5.0 (Macintosh; ' +
        'Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, ' +
        'like Gecko) Chrome/35.0.1916.47 Safari/537.36'},
        agent: false,
        method: 'GET'
    };

    // process the request
    var request = https.request (options,
        function(response) {
            // finally the page will be a concatenation of chunks from the server
            var page = '';

            response.on('data', function(chunk) {
	            page += chunk;
            });

            // parse html page for match urls
            response.on ('end', function () { parse_urls(page); });
       }
    );
    request.on('error', function(e) {
			console.error(e);
    });

    request.end();

}

function parse_urls(page) {
    //page = "<td class=Icons";
    console.log(page);
    //var pattern = /<td class=Icons/;
    //var match  = pattern.exec(page);
    //console.log(match);
}

function parse_match(url) {
    var toFind = '$P.onUpdate(\'od\',';
    var x = str.indexOf (toFind);
    str = str.substr (x + toFind.length);

    x = str.indexOf (');');
    str = str.substr (0, x);

    //console.log (str);

    //опасно, может быть выполнен удаленный код
    log ('eval str');
    eval ('var a = ' + str);
    //log (a);

    var x = a [2];
    //log ('-----');
    //log (x);

    x = x [0][1];
    //log ('-----');

    //log (x);
    var toRet = [];
    for (var k in x) {
        var val = x [k];
        val = val [2];

        toRet.push ({
            'name': val [1],
            'name2': val [2],
            'xz': val [3],
            'xz2': val [4],
            'date': val [5]
        });
        //log (val);
    }
    func (toRet);
}

/**
 * Start point of information processing.
 */
function main() {
    find_match_urls(function (res) {
    	log ('Yahoooo!!!!');
    	log (res);
    });
}

main();

function log (txt) {
	console.log (txt);
}
