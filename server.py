import http.server
import socketserver
import json
import os
from livekit import api
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PORT = 8000
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/test_interface.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        if self.path == '/token':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Generate token
            api_key = os.getenv("LIVEKIT_API_KEY")
            api_secret = os.getenv("LIVEKIT_API_SECRET")
            livekit_url = os.getenv("LIVEKIT_URL")

            if not api_key or not api_secret or not livekit_url:
                self.wfile.write(json.dumps({"error": "Missing environment variables"}).encode())
                return

            # Create a random participant name or use a default
            participant_name = "TestUser"
            room_name = "test-room"

            grant = api.VideoGrants(
                room_join=True,
                room=room_name,
            )
            
            token = api.AccessToken(api_key, api_secret) \
                .with_identity(participant_name) \
                .with_name(participant_name) \
                .with_grants(grant) \
                .to_jwt()
            
            response = {
                "token": token,
                "url": livekit_url,
                "room": room_name
            }
            
            self.wfile.write(json.dumps(response).encode())
            return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"Server running at http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
