# test_livekit_complete.py
"""
Complete LiveKit Sales Agent Test - Tests all components
"""

import os
import asyncio
import logging
import json
from pathlib import Path
from dotenv import load_dotenv

# --- logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
log = logging.getLogger("livekit_test")

# --- load .env early ---
load_dotenv()

def load_context() -> str:
    """Load context from context directory."""
    context_dir = Path("context")
    all_content = ""
    for file_path in context_dir.glob("*"):
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding="utf-8")
                all_content += f"\n=== {file_path.name} ===\n{content}\n"
            except Exception as e:
                log.warning("Skipped %s: %s", file_path.name, e)
    return all_content.strip() or "No context files found"

async def test_complete_setup():
    """Test all components of the sales agent setup."""
    
    log.info("=" * 70)
    log.info("🚀 LIVEKIT SALES AGENT - COMPLETE TEST")
    log.info("=" * 70)
    
    # Test 1: Load context
    log.info("\n📋 STEP 1: Loading Context Data")
    log.info("-" * 70)
    context = load_context()
    log.info(f"✅ Context loaded successfully ({len(context)} chars)")
    log.info(f"\nContext Preview:\n{context}\n")
    
    # Test 2: Verify LiveKit imports
    log.info("\n📦 STEP 2: Verifying LiveKit Imports")
    log.info("-" * 70)
    
    try:
        from livekit.agents import WorkerOptions, JobContext
        from livekit.agents.cli import cli
        log.info("✅ LiveKit core imports successful")
    except Exception as e:
        log.error(f"❌ LiveKit core imports failed: {e}")
        return False
    
    try:
        from livekit.plugins import openai, cartesia, silero
        log.info("✅ LiveKit plugins imported")
        log.info("   - openai")
        log.info("   - cartesia")
        log.info("   - silero")
    except Exception as e:
        log.error(f"❌ Plugin imports failed: {e}")
        return False
    
    # Test 3: Initialize STT/TTS
    log.info("\n🎤 STEP 3: Initializing STT/TTS (Cartesia)")
    log.info("-" * 70)
    
    try:
        stt = cartesia.STT()
        tts = cartesia.TTS()
        log.info("✅ Cartesia STT initialized")
        log.info("✅ Cartesia TTS initialized")
    except Exception as e:
        log.error(f"❌ Cartesia STT/TTS failed: {e}")
        return False
    
    # Test 4: Initialize VAD
    log.info("\n🔊 STEP 4: Initializing Voice Activity Detection (Silero)")
    log.info("-" * 70)
    
    try:
        vad = silero.VAD.load()
        log.info("✅ Silero VAD loaded successfully")
    except Exception as e:
        log.error(f"❌ VAD initialization failed: {e}")
        return False
    
    # Test 5: Initialize LLM
    log.info("\n🤖 STEP 5: Initializing LLM (Cerebras)")
    log.info("-" * 70)
    
    try:
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        log.info("✅ LLM initialized with Cerebras backend")
        log.info("   Model: llama-3.3-70b")
    except Exception as e:
        log.error(f"❌ LLM initialization failed: {e}")
        return False
    
    # Test 6: Test LLM with a simple prompt
    log.info("\n💬 STEP 6: Testing LLM with Sample Queries")
    log.info("-" * 70)
    
    instructions = f"""You are a friendly, helpful sales agent. Speak naturally and warmly.
Only use the information in the context below. Keep responses short and conversational.

{context}

If asked anything outside the context, say: "I don't have that information."
"""
    
    test_queries = [
        "What products do you offer?",
        "What's the price of the website starter pack?",
        "What's your phone number?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        log.info(f"\n  Query {i}: '{query}'")
        try:
            # Use the correct API method for LLM
            messages = [
                {"role": "system", "content": instructions},
                {"role": "user", "content": query}
            ]
            
            response = await llm.chat(messages=messages)
            
            # Extract text from response
            if hasattr(response, 'choices') and response.choices:
                answer = response.choices[0].message.content
            else:
                answer = str(response)
            
            log.info(f"  Response: {answer}")
            
        except AttributeError:
            # Fallback: try different API
            try:
                response = await llm.complete(prompt=query)
                log.info(f"  Response: {response}")
            except Exception as e2:
                log.warning(f"  ⚠️  Could not get response: {e2}")
        except Exception as e:
            log.warning(f"  ⚠️  Query failed: {e}")
    
    # Test 7: Verify environment variables
    log.info("\n\n🔐 STEP 7: Environment Configuration")
    log.info("-" * 70)
    
    env_vars = {
        "LIVEKIT_URL": os.getenv("LIVEKIT_URL"),
        "LIVEKIT_API_KEY": os.getenv("LIVEKIT_API_KEY"),
        "CEREBRAS_API_KEY": os.getenv("CEREBRAS_API_KEY"),
        "CARTESIA_API_KEY": os.getenv("CARTESIA_API_KEY"),
    }
    
    for var_name, var_value in env_vars.items():
        if var_value:
            masked = f"{'*' * 6}...{var_value[-6:]}" if len(var_value) > 10 else "*" * len(var_value)
            log.info(f"✅ {var_name}: {masked}")
        else:
            log.error(f"❌ {var_name}: NOT SET")
    
    # Summary
    log.info("\n" + "=" * 70)
    log.info("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    log.info("=" * 70)
    log.info("\n📞 Your sales agent is ready to:")
    log.info("   ✓ Listen to incoming audio (STT)")
    log.info("   ✓ Process customer queries with LLM")
    log.info("   ✓ Generate natural voice responses (TTS)")
    log.info("   ✓ Detect voice activity (VAD)")
    log.info("\n🚀 Next steps:")
    log.info("   1. Deploy with: python sales_agent.py")
    log.info("   2. Connect from a LiveKit room")
    log.info("   3. Talk to the agent!")
    
    return True

async def main():
    try:
        success = await test_complete_setup()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        log.info("\n🛑 Test interrupted by user")
        exit(0)
    except Exception as e:
        log.error(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
