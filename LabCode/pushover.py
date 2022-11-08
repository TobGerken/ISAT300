import http.client, urllib

conn = http.client.HTTPSConnection("api.pushover.net:443")
conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": "enter your App token/key here",
        "user": "enter your User token/key here",
        "message": "ISAT300 is the best!!",
    }), { "Content-type": "application/x-www-form-urlencoded" })
conn.getresponse()