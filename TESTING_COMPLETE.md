# Testing Your Sales Agent

## What I Fixed

The issue was that you were using an older API for the LiveKit agents library. The newer version (1.1.7) changed how agents are started:

**Old way (doesn't work):**
```python
agent.start(ctx.room)
await agent.say("Hello!")
```

**New way (correct):**
```python
session = agent.on_enter(ctx)
await session.say("Hello!")
```

## How to Test

### Option 1: Using Your Custom Interface (Recommended)

1. **Make sure both servers are running:**
   - Server 1: `python server.py` (running on http://localhost:8000)
   - Server 2: `python sales_agent.py dev` (the agent)

2. **Open your browser:**
   - Go to http://localhost:8000
   - Click "Start Agent Test"
   - Allow microphone access when prompted
   - You should hear the agent say "Hello! I'm your virtual sales assistant. How can I help you today?"
   - Start speaking to test!

### Option 2: Using LiveKit Studio

1. Go to https://studio.livekit.io/
2. Enter your credentials from `.env`:
   - LiveKit URL: `wss://ore-pr9my2ai.livekit.cloud`
   - API Key: (from your .env)
   - API Secret: (from your .env)
3. Create or join a room (any name)
4. The agent will automatically join and greet you
5. Start speaking!

## Troubleshooting

- **Agent not speaking?** Check the terminal running `python sales_agent.py dev` for errors
- **Can't connect?** Make sure your `.env` file has the correct LiveKit credentials
- **No audio?** Check your browser's microphone permissions

## What's Next

You now have a working voice agent! You can:
- Modify the context files in the `context/` folder to change what the agent knows
- Edit `sales_agent.py` to customize the agent's behavior
- Update the greeting message or instructions
