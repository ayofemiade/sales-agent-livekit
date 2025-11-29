from livekit.agents import llm
import inspect

print("ChatContext.add_message signature:")
print(inspect.signature(llm.ChatContext.add_message))

# Check what it expects
ctx = llm.ChatContext()
print("\nChatContext methods:", [m for m in dir(ctx) if not m.startswith('_')])

# Try creating message separately
msg = llm.ChatMessage(role="system", content=["test"])
print(f"\nCreated message: {msg}")

# Try adding it
try:
    ctx.add_message(msg)
    print("✅ add_message(msg) works!")
except Exception as e:
    print(f"❌ add_message(msg) failed: {e}")

# Try with keyword
try:
    ctx2 = llm.ChatContext()
    ctx2.add_message(message=msg)
    print("✅ add_message(message=msg) works!")
except Exception as e:
    print(f"❌ add_message(message=msg) failed: {e}")
