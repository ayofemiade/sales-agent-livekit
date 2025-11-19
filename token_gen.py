import os
from livekit import api
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("LIVEKIT_API_KEY")
api_secret = os.getenv("LIVEKIT_API_SECRET")
livekit_url = os.getenv("LIVEKIT_URL")

token = api.AccessToken(api_key, api_secret) \
    .with_identity("moyo-test-user") \
    .with_name("Moyosore") \
    .with_grants(api.VideoGrants(
        room_join=True,
        room="playground"  # Room name for Agents Playground
    )) \
    .to_jwt()

print("\n🔑 Generated Room Token:\n")
print(token)
print("\nUse this token in the LiveKit Agents Playground.")
