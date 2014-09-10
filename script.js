$(document).ready(
	function() {
		
		//The browser's javascript cache must be slain!
		function get_cache_buster(){
			var maximum = 1;
			var minimum = 200000;
			var randomnumber = Math.floor(Math.random() * (maximum - minimum + 1)) + minimum;
			return randomnumber;
		}
		
		//Turning tweet links into direct links back to twitter
		function processTweetLinks(text) {
			    var exp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/i;
			    text = text.replace(exp, "<a href='$1' target='_blank'>$1</a>");
			    exp = /(^|\s)#(\w+)/g;
			    text = text.replace(exp, "$1<a href='http://twitter.com/hashtag/$2' target='_blank'>#$2</a>");
			    exp = /(^|\s)@(\w+)/g;
			    text = text.replace(exp, "$1<a href='http://www.twitter.com/$2' target='_blank'>@$2</a>");
			    return text;
		}
		
		//Firing an ajax method at the server. This server cannot handle JSONP calls - so we iframed the whole 
		//widget so we wouldn't need to fire cross domain requests.
		function get_tweets(){
			var num = get_cache_buster()
			$.ajax({
					type: "GET",
					url: "/place/where/your/json_file/is_stored/tweets.json?" + num,
					dataType: "json",
					success: function(data){
						var tweet_data = data;
						var tweet_info = [];
						for (i = 0; i < tweet_data.length; i++) { 
							var t_container = {}
							t_container['status'] = processTweetLinks(tweet_data[i].status)
							t_container['time'] = tweet_data[i].time
							t_container['handle'] = tweet_data[i].handle
							t_container['image'] = tweet_data[i].image
							t_container['name'] = tweet_data[i].reporter
							tweet_info.push(t_container)
						}
							
						var tweet_source = $('#tweets').html();
						var tweet_template = Handlebars.compile(tweet_source);

						$('#mcd_tweets').append(tweet_template({objects: tweet_info}))
					}
					
				});	
		}
		
		//Firing another request at our server
		function get_updates(){
			var num = get_cache_buster();
				$.ajax({
					type: "GET",
					url: "/place/where/your/json_file/is_stored/updates.json?" + num,
					dataType: "json",
					success: function(data){
						//UPDATE THE LIVE UPDATES
						var news_items = data;
						var source = $('#ticker-list').html();
						var template = Handlebars.compile(source);

						$('#mcd_updates').append(template({objects: news_items}))
					}
					
				});	
		}

		get_tweets()
		get_updates()
		
		//This updates the information every five minutes.
		setInterval(function(){
			$('#mcd_tweets').fadeOut(500, function(){
				$(this).empty();
				setTimeout(get_tweets, 200);
				setTimeout($(this).fadeIn(), 300);
			});

			$('#mcd_updates').fadeOut(500, function(){
				$(this).empty();
				setTimeout(get_updates, 200);
				setTimeout($(this).fadeIn(), 300);
			});
		}, 300000);
});