from http.server import BaseHTTPRequestHandler
from cowpy import cow

class handler (BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.send_header('content-type', 'text-plain')
    self.end_headers()
    message = cow.Cowacter().milk('Hello from Python')
    self.wfile.write(message.encode())
    reutrn

from cowpy import os

from cowpy import google_auth_oauthlib.flow
from cowpy import googleapiclient.discovery
from cowpy import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.search().list(
        part="snippet",
        channelId="UCJplp5SjeGSdVdwsfb9Q7lQ"
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()