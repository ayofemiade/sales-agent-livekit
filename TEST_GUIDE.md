# 🤖 Sales Agent LiveKit - Testing Guide

Your sales agent is fully built and ready to test! Here's how to do it.

## ✅ What's Been Tested

Your agent has passed all component tests:
- ✅ **Context Loading** - Product data loaded successfully
- ✅ **STT (Speech-to-Text)** - Cartesia STT initialized
- ✅ **TTS (Text-to-Speech)** - Cartesia TTS ready
- ✅ **LLM** - Cerebras LLM (Llama 3.3-70B) configured
- ✅ **VAD (Voice Activity Detection)** - Silero VAD loaded
- ✅ **Environment** - All API keys configured

## 🧪 Testing Options

### Option 1: Quick Component Test
Test all components without connecting to LiveKit:

```bash
python test_livekit_complete.py
```

This validates:
- All imports work
- API keys are correct
- STT/TTS can initialize
- LLM can load

### Option 2: Run the Live Agent
Deploy your agent to LiveKit:

```bash
python sales_agent.py
```

Then:
1. Open [LiveKit Studio](https://studio.livekit.io/)
2. Connect to your room: `wss://ore-pr9my2ai.livekit.cloud`
3. Use your API credentials from `.env`
4. Click "Start Agent" with this agent
5. Speak to the agent!

### Option 3: Mock Testing (No API Calls)
Run with mock LLM responses (for development):

```bash
python interactive_test.py
```

## 📝 Agent Context

Your agent has access to this context:

```json
{
  "products": [
    {
      "name": "Website Starter Pack",
      "price": "₦50,000",
      "description": "Modern 3-page website with HTML/CSS/JS, contact form, 1 month hosting support"
    }
  ]
}
```

The agent will:
- Answer questions about your products
- Redirect unknown queries with "I don't have that information"
- Speak naturally and warmly
- Keep responses short for voice

## 🚀 Deployment Steps

1. **Verify all tests pass:**
   ```bash
   python test_livekit_complete.py
   ```

2. **Start your agent:**
   ```bash
   python sales_agent.py
   ```

3. **Connect from LiveKit Studio:**
   - Navigate to https://studio.livekit.io/
   - Enter your room URL from `.env` (LIVEKIT_URL)
   - Use your API credentials
   - Create/join a room
   - Start the agent

4. **Talk to your agent!**
   - Ask "What products do you offer?"
   - Ask "How much does it cost?"
   - The agent will respond with your product info

## 🔧 Troubleshooting

### "No module named 'livekit'"
```bash
pip install -r requirements.txt
```

### "CARTESIA_API_KEY not set"
Ensure your `.env` file has all required keys:
- CARTESIA_API_KEY
- CEREBRAS_API_KEY
- LIVEKIT_URL
- LIVEKIT_API_KEY
- LIVEKIT_API_SECRET

### Agent not responding
1. Check agent logs for errors
2. Verify API keys are valid
3. Ensure you're in the same room
4. Check audio input/output is working

## 📚 Project Structure

```
sales-agent-livekit/
├── sales_agent.py              # Main agent (run this)
├── test_agent.py               # Component tests
├── test_livekit_complete.py    # Complete system test
├── interactive_test.py         # Mock interaction test
├── requirements.txt            # Python dependencies
├── package.json               # Node dependencies
├── .env                       # API keys (keep secret!)
└── context/
    └── product.json           # Agent knowledge base
```

## 🎯 Next Steps

1. Run `python test_livekit_complete.py` to verify everything works
2. Connect to LiveKit Studio and test the agent
3. Customize `context/product.json` with your real products
4. Update agent instructions in `sales_agent.py` as needed
5. Deploy to production!

---

**Built with:** LiveKit + Cerebras LLM + Cartesia STT/TTS + Silero VAD
