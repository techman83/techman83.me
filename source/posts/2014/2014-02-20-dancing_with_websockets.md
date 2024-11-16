Dancing with WebSockets
=======================

```{post} 2014-02-20
:tags: programming, perl, dancer, websockets
:category: Programming
:author: techman83
```

I learnt during the development of the [EventStreamR](https://github.com/plugorgau/eventstreamr) frontend that websockets are cool! Another learning project of mine is [NanodeControl](https://github.com/techman83/NanodeControl) and after learning what all the cool new things are available I wanted to have a crack at making it more modern.

After a bit of search around I came across [Dancer::Plugin::WebSocket](http://search.cpan.org/~ironcamel/Dancer-Plugin-WebSocket-0.0100/lib/Dancer/Plugin/WebSocket.pm). Expanding on the example provided here is a simple web page with simple messages and forked calls. It utilises the the Twiggy AnyEvent based non-blocking (asynchronous) and lightweight PSGI web server.

You'll need some libraries, my favourite way to install them is [cpanm](http://search.cpan.org/~miyagawa/App-cpanminus-1.7001/lib/App/cpanminus.pm):

```bash
cpanm -S Plack Twiggy Dancer Dancer::Plugin::WebSocket AnyEvent::Util
```

app.pl
```perl
use Dancer ':syntax';
use Dancer::Plugin::WebSocket;
use AnyEvent::Util;

set logger => 'console';
set log => 'core';

get '/' => sub {q[
    <html>
    <head>
    <script>
      var ws_path = "ws://localhost:5000/_hippie/ws";
      var socket = new WebSocket(ws_path);
      socket.onopen = function() {
          document.getElementById('conn-status').innerHTML = 'Connected';
      };
      socket.onmessage = function(e) {
          var data = JSON.parse(e.data);
          console.log(data);
          if (data.msg) {
            document.getElementById('content').innerHTML = data.msg;
            setTimeout(function() {
              document.getElementById('content').innerHTML = 'No current message';
            }, 5000);
          }
      };
      function send_msg(message) {
          socket.send(JSON.stringify({ msg: message }));
      }
      function get_long() {
        var xmlHttp = null;

        xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", '/long', false );
        xmlHttp.send( null );
        document.getElementById('content').innerHTML = 'Waiting...';
      }
    </script>
    </head>
    <body>
    Connection Status: <span id="conn-status"> Disconnected </span>
    <input value="Send Message" type=button onclick="send_msg('hello')" />
    <input value="Get Long Call" type=button onclick="get_long()" /><br>
    <span id="content"> No current message </span>
    </body>
    </html>
]};

get '/long' => sub {
    debug("Stations Called");
    fork_call {
      debug("Forking");
      sleep 5;
    } sub {
      my $data = 'Forked result!';
      ws_send $data;
      debug("Message Sent");
    };
    return;
};

dance;
```

Launch the script with plackup:

```bash
plackup -s Twiggy socket_dance.pl -p 5000
```

Browse to http://localhost:5000 and you should be greeted with a page. Press the buttons and watch the magic happen!

I did encounter issues with the latest version of chrome on page refreshes sending bad data crashing twiggy, looks like there are some [bug reports](https://github.com/miyagawa/Twiggy/pull/39) indirectly relating to it. However it does work on initial page load and seems to work correctly on firefox :-)

NOTE: I found a solution, instead of using the builtin AnyEvent::Loop, use EV. From what I've read it's a faster and more robust event backend. The errors from chrome still occur, however the server keeps going inside of barfing and dying. As long as EV is available AnyEvent will use it (unless otherwise configured).
