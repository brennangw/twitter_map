var geoTweets = [];
var markers = [];
var filters = ["soccer", "football", "basketball"];
var distance = 10;
var map = null;
class GeoTweet {
    constructor(data) {
        this.text = data.text;
        this.coordinates = {"lat": Number(data.coordinates["lat"]), "lng": Number(data.coordinates["long"])};
    }

    get formattedContent() {
        var fc = "<div><p>"+this.text+"</p></div>";
        return fc;
    }

}

function tweetsDisplay() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }

    geoTweets.filter(function (geoTweet) {
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
                "long" : event.latLng.lng(),
                "distance" : distance
            },
            success: function(tweetData) {
                console.log(tweetData);
            }
        });
    });
}


// This example displays a marker at the center of Australia.
// When the user clicks the marker, an info window opens.

function init() {
    return $.ajax({
        type: "GET",
        url: "/tweets",
        success: function(tweetData) {
            geoTweets = tweetData.map(function(tweetData) {
                return new GeoTweet(tweetData)
            });
            initGoogleMapDisplay();
            tweetsDisplay();
        }
    })
}

$(document).ready(function() {
    $('#filterForm').submit(function (e) {
        e.preventDefault();
        //var formData =$('#filterForm').serialize();
        //distance = parseInt(formData[0].value);
        filters = $('#filterForm').serializeArray().reduce(
            function(accumulater, curr) {
                accumulater.push(curr.value);
                return accumulater;
            }, []);
        distance = filters.shift();
        console.log(distance);
        console.log(filters);
        tweetsDisplay();
    });
    init();
});
