# 🎯 How to Test Your Sales Agent

## ✅ Your Agent is Ready!

All component tests passed successfully:
- ✅ Context loading works
- ✅ LiveKit imports successful  
- ✅ Cartesia STT/TTS initialized
- ✅ Cerebras LLM configured
- ✅ Environment variables set

## 🚀 Quick Start - 3 Easy Ways to Test

### Option 1: LiveKit Studio (Recommended - Easiest)

This is the fastest way to test your agent:

1. **Start your agent locally:**
   ```bash
   python sales_agent.py
   ```

2. **Open LiveKit Studio:**
   - Go to https://studio.livekit.io/

3. **Enter your credentials:**
   - Copy `LIVEKIT_URL` from your `.env` file
   - Copy `LIVEKIT_API_KEY` from your `.env` file  
   - Copy `LIVEKIT_API_SECRET` from your `.env` file

4. **Join or create a room:**
   - Enter any room name (e.g., "test-room")
   - Click "Connect"

5. **Talk to your agent:**
   - Your agent will automatically join the room
   - Allow microphone access
   - Start speaking!
   - Try questions like:
     - "What products do you offer?"
     - "How much does the website starter pack cost?"
     - "What's included in the package?"

---

### Option 2: Web Test Interface (Local)

1. **Start your agent:**
   ```bash
   python sales_agent.py
   ```

2. **Open the test interface:**
   - Open `test_interface.html` in your browser
   - Or run a simple server:
     ```bash
     python -m http.server 8000
     ```
   - Then visit http://localhost:8000/test_interface.html

3. **Follow the on-screen instructions**

---

### Option 3: LiveKit Playground

1. **Start your agent:**
   ```bash
   python sales_agent.py
   ```

2. **Use LiveKit Playground:**
   - Visit https://playground.livekit.io/
   - Enter your LiveKit URL and credentials
   - Connect and test

---

## 🧪 What to Test

Ask your agent these questions:

### Should Work (In Context):
- ✅ "What products do you offer?"
- ✅ "How much does it cost?"
- ✅ "What's included in the website package?"
- ✅ "How long is the hosting support?"
- ✅ "Tell me about your services"

### Should Say "I don't have that information":
- ❌ "What's your phone number?"
- ❌ "Do you offer mobile apps?"
- ❌ "What's your address?"

---

## 📊 Monitoring Your Agent

When you run `python sales_agent.py`, you'll see logs like:

```
INFO:sales_agent:🚀 Sales Agent starting...
INFO:sales_agent:✅ Loaded context (234 chars)
INFO:sales_agent:Plugins imported
INFO:sales_agent:LLM initialized (Cerebras)
INFO:sales_agent:Cartesia STT/TTS initialized
INFO:sales_agent:🗣️ Agent is live and listening...
```

---

## 🛠️ Troubleshooting

### Agent not responding?
1. Check your agent is running (`python sales_agent.py`)
2. Verify all API keys in `.env` are correct
3. Make sure you're in the same room
4. Check microphone permissions in your browser

### "Connection failed"?
1. Verify LIVEKIT_URL is correct (should start with `wss://`)
2. Check LIVEKIT_API_KEY and LIVEKIT_API_SECRET
3. Make sure your LiveKit server is running

### No audio?
1. Allow microphone access in your browser
2. Check your speaker/headphone volume
3. Try using headphones to avoid echo

---

## 🎨 Customizing Your Agent

### Change the context:
Edit `context/product.json` with your actual products

### Modify instructions:
Edit the `instructions` in `sales_agent.py` (lines 87-96)

### Switch TTS voice:
Modify Cartesia TTS settings in `sales_agent.py`

---

## 📈 Next Steps

Once testing works:

1. **Add more products** to `context/product.json`
2. **Customize the agent's personality** in instructions
3. **Deploy to production** (see deployment guides)
4. **Integrate with your website**

---

## 🆘 Need Help?

- Check LiveKit docs: https://docs.livekit.io/
- Cartesia docs: https://docs.cartesia.ai/
- Test all components: `python test_livekit_complete.py`

---

**Ready to test? Run:** 
```bash
python sales_agent.py
```

**Then visit:** https://studio.livekit.io/ 🚀
