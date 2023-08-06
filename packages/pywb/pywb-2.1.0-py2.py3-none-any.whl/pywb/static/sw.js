
// Install
self.addEventListener('install', function(event) {
//  console.log("SW Installed");
});

//var static_prefix = "http://localhost:8080/static/";

//var check_replay_prefix = "http://localhost:8080/live/";

var sp = new URLSearchParams(self.location.search);
var check_replay_prefix = sp.get("prefix");

var static_prefix = self.location.origin + "/static/";

//console.log(check_replay_prefix);

var mod = "mp_";
var replay_prefix = check_replay_prefix + mod + '/';


self.addEventListener('fetch', function(event) {
  const url = event.request.url;
  console.log("Fetch: " + url);

  var request = event.request;

  if (!url.startsWith(check_replay_prefix) && !url.startsWith(static_prefix)) {
    var init_opts = {"method": request.method,
                     "headers": request.headers,
                     "credentials": request.credentials,
                     //"mode": request.mode == "navigate" ? "cors" : request.mode,
                     "mode": request.mode,
                     "cache": request.cache,
                     "redirect": request.redirect,
                     "referrer": request.referrer,
                    };

    //request = event.request.clone();

    if (request.method == "POST" || request.method == "PUT") {
      //init_opts.body = request.blob();
      let promise = request.blob().then(function(res) {
          init_opts.body = res;

          request = newRequest(event, request, init_opts);
          return fetch(request);
        });

      event.respondWith(promise);
      return;
    }

    request = newRequest(event, request, init_opts);

  }

  event.respondWith(fetch(request));

});

function getReferrerOrigin(request) {
  if (request.referrer.startsWith(check_replay_prefix)) {
    return request.referrer.substr(replay_prefix.length)
  }

  return request.referrer;
}

function newRequest(event, request, init_opts) {
  const url = request.url;
  var newUrl = undefined;

  if (url.startsWith(self.location.origin)) {
    let path = url.substr(self.location.origin.length);
    let baseUrl = new URL(path, getReferrerOrigin(request)).href;
    newUrl = replay_prefix + baseUrl;
  } else if (url.startsWith("http:") || url.startsWith("https:") || url.startsWith("//")) {
    //newUrl = replay_prefix + mod + "/" + url;
    newUrl = replay_prefix + url;
  } else if (url.startsWith("/") || !(url.startsWith("data:") || url.startsWith("blob:") || url.startsWith("file:"))) {
    newUrl = new URL(url, request.referrer).href;
  }

  if (newUrl) {
    console.log("New Url: " + newUrl);

    request = new Request(newUrl, init_opts);
  }

  return request;
}



