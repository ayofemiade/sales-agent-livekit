from livekit.agents import llm
import inspect

# Check ChatMessage signature
print("ChatMessage signature:")
print(inspect.signature(llm.ChatMessage))

# Try to create one
try:
    msg = llm.ChatMessage(role="system", content="test")
    print("\n✅ Works with content='test'")
    print(f"Message: {msg}")
except Exception as e:
    print(f"\n❌ Error with content='test': {e}")

# Try with list
try:
    msg2 = llm.ChatMessage(role="system", content=["test"])
    print("\n✅ Works with content=['test']")  
    print(f"Message: {msg2}")
except Exception as e:
    print(f"\n❌ Error with content=['test']: {e}")
