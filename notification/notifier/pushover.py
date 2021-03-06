import http.client
import urllib.request, urllib.parse, urllib.error

__author__ = 'oker'

class PushoverNotifier:
    def notify(self, notification):
        conn = http.client.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
          urllib.parse.urlencode({
            "token": notification.user_to_notify.profile.pushover_app_key,
            "user": notification.user_to_notify.profile.pushover_user_key,
            "message": notification.message,
          }), { "Content-type": "application/x-www-form-urlencoded" })
        status = conn.getresponse().status
        if status >= 200 and status < 300:
            print("Done")
        else:
            # todo: error handling
            print("Unable to connect.")