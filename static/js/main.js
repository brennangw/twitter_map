var geoTweets = [];
var markers = [];
var filters = ["soccer", "football", "basketball"];
var distance = 5000;
var map = null;
var streaming = false;
var intervalId = null;
class GeoTweet {
    constructor(data) {
        this.user = data.user;
        this.text = data.text;
        this.coordinates = {"lat": Number(data.coordinates["lat"]),
            "lng": Number(data.coordinates["long"])};
    }

    get formattedContent() {
        var fc = "<div><p>"+this.text+
            "</p><h5>"+this.user+"</h5></div>";
        return fc;
    }

}

function tweetsDisplay(useFilters) {

    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }

    geoTweets.filter(function (geoTweet) {
        if (!useFilters) {
            return true;
        }
        for (let filter of filters) {
            if (geoTweet.text.toLowerCase().indexOf(filter) > 0) {
                return true;
            }
        }
        return false;
    }).forEach(function(geoTweet) {
        var infowindow = new google.maps.InfoWindow({
            ///todo: make the content prettier by following the online example.
            content: geoTweet.formattedContent
        });

        var marker = new google.maps.Marker({
            position: geoTweet.coordinates,
            map: map,
            //todo: make better titles
            title: geoTweet.text.slice(1,5)
        });
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });
        markers.push(marker);
    });
}

function initGoogleMapDisplay() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: {lat: 0., lng: 0.}
    });
    google.maps.event.addListener(map, 'rightclick', function(event) {
        return $.ajax({
            type: "POST",
            url: "/geoSearch",
            data: {
                "lat" : event.latLng.lat(),
                "lng" : event.latLng.lng(),
                "distance" : distance
            },
            success: function(tweetData) {
                 geoTweets = tweetData.map(function(tweetData) {
                    return new GeoTweet(tweetData)
                });
                getFilters($('#filterForm').serializeArray());
                tweetsDisplay(false);
            }
        });
    });
}


function streamPoll() {
    return $.ajax({
            type: "POST",
            url: "/streamPoll",
            data: {
                "text" : filters.join(" ")
            },
            success: function(tweetData) {
                 geoTweets = tweetData.map(function(tweetData) {
                    return new GeoTweet(tweetData)
                });
                getFilters($('#filterForm').serializeArray());
                tweetsDisplay(false);
            }
        });
}


function getTweets(useFilters) {
    return $.ajax({
        type: "GET",
        url: "/tweets",
        success: function(tweetData) {
            geoTweets = tweetData.map(function(tweetData) {
                return new GeoTweet(tweetData)
            });
            tweetsDisplay(useFilters);
        }
    })
}

function getFilters(serializedArray) {
    filters =
            serializedArray.reduce(
            function(accumulater, curr) {
                accumulater.push(curr.value);
                return accumulater;
            }, []);
        distance = filters.shift();
}

$(document).ready(function() {
    $('#streamButton').click(function (e) {
        if (streaming) { //stopping
             clearInterval(intervalId);
            intervalId = null;

            $('#streamButton').html("Start Stream");

        } else { //starting
            intervalId = setInterval(streamPoll,1000);
            $('#streamButton').html("Stop Stream");
        }
        streaming = !streaming;
    });
    $('#showAll').click(function (e) {
        e.preventDefault();
        getFilters($('#filterForm').serializeArray());
        getTweets(false);
    });
    $('#filterForm').submit(function (e) {
        e.preventDefault();
        getFilters($('#filterForm').serializeArray());
        getTweets(true);
    });
    $('#showFilteredButton').click(function (e) {
        getFilters($('#filterForm').serializeArray());
        tweetsDisplay(true);
    });
    initGoogleMapDisplay();
    getFilters($('#filterForm').serializeArray());
    getTweets(true);
    console.log("done with init");
});
