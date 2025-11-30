# Test script to verify Agent API
import asyncio
from livekit.agents.voice import Agent

async def test_agent():
    # Create a simple agent
    agent = Agent(
        instructions="You are a test agent",
    )
    
    # Check what methods are available
    print("Agent methods:")
    print([m for m in dir(agent) if not m.startswith('_')])
    
    # Check if session exists before on_enter
    try:
        print(f"\nSession before on_enter: {agent.session}")
    except Exception as e:
        print(f"\nNo session before on_enter: {e}")
    
    # Call on_enter
    result = agent.on_enter()
    print(f"\non_enter() returned: {result}")
    
    # Check if session exists after on_enter
    try:
        print(f"Session after on_enter: {agent.session}")
        print(f"Session type: {type(agent.session)}")
        print(f"Session methods: {[m for m in dir(agent.session) if not m.startswith('_') and callable(getattr(agent.session, m))]}")
    except Exception as e:
        print(f"Error accessing session: {e}")

if __name__ == "__main__":
    asyncio.run(test_agent())
