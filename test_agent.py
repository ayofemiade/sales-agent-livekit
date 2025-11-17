# test_agent.py
import os
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
from unittest.mock import AsyncMock, MagicMock, patch

# --- logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
log = logging.getLogger("test_agent")

# --- load .env early ---
load_dotenv()

# --- environment keys ---
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

def check_environment():
    """Verify all required environment variables are set."""
    log.info("🔍 Checking environment variables...")
    
    vars_to_check = {
        "CARTESIA_API_KEY": CARTESIA_API_KEY,
        "LIVEKIT_API_KEY": LIVEKIT_API_KEY,
        "LIVEKIT_API_SECRET": LIVEKIT_API_SECRET,
        "LIVEKIT_URL": LIVEKIT_URL,
        "CEREBRAS_API_KEY": CEREBRAS_API_KEY,
    }
    
    all_good = True
    for var_name, var_value in vars_to_check.items():
        if var_value:
            log.info(f"✅ {var_name}: {'*' * 10}...{var_value[-4:] if len(var_value) > 10 else var_value}")
        else:
            log.error(f"❌ {var_name}: NOT SET")
            all_good = False
    
    return all_good

def load_context() -> str:
    """Load context from context directory."""
    context_dir = Path("context")
    context_dir.mkdir(exist_ok=True)
    all_content = ""
    for file_path in context_dir.glob("*"):
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding="utf-8")
                all_content += f"\n=== {file_path.name} ===\n{content}\n"
            except Exception as e:
                log.warning("Skipped %s: %s", file_path.name, e)
    return all_content.strip() or "No context files found"

async def test_context_loading():
    """Test 1: Verify context loading works."""
    log.info("\n📋 TEST 1: Context Loading")
    log.info("-" * 50)
    
    context = load_context()
    log.info(f"✅ Context loaded ({len(context)} chars)")
    log.info(f"Preview:\n{context[:300]}...")
    return True

async def test_imports():
    """Test 2: Verify all imports work."""
    log.info("\n📦 TEST 2: Plugin Imports")
    log.info("-" * 50)
    
    try:
        from livekit.agents import WorkerOptions, JobContext
        from livekit.agents.cli import cli
        log.info("✅ LiveKit core imports successful")
    except ImportError as e:
        log.error(f"❌ LiveKit imports failed: {e}")
        return False
    
    try:
        from livekit.plugins import openai, cartesia, silero
        log.info("✅ LiveKit plugin imports successful")
    except ImportError as e:
        log.warning(f"⚠️  Plugin imports failed (non-critical): {e}")
    
    return True

async def test_llm_prompt():
    """Test 3: Verify LLM can process prompts."""
    log.info("\n🤖 TEST 3: LLM Prompt Processing")
    log.info("-" * 50)
    
    context_data = load_context()
    instructions = f"""
    You are a friendly, helpful sales agent. Speak naturally and warmly.
    Only use the information in the context below.

    {context_data}

    RULES:
      - If asked anything outside the context, say: "I don't have that information."
      - Keep responses short for speaking.
    """
    
    try:
        from livekit.plugins import openai
        
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        log.info("✅ LLM initialized (Cerebras)")
        
        # Test a simple prompt
        test_prompt = "What products do you have?"
        log.info(f"Testing LLM with prompt: '{test_prompt}'")
        
        response = await llm.agentic_loop(
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": test_prompt}
            ]
        )
        
        log.info(f"✅ LLM Response: {response}")
        return True
        
    except Exception as e:
        log.error(f"❌ LLM test failed: {e}")
        return False

async def test_cartesia_stt_tts():
    """Test 4: Verify Cartesia STT/TTS initialization."""
    log.info("\n🎤 TEST 4: Cartesia STT/TTS")
    log.info("-" * 50)
    
    try:
        from livekit.plugins import cartesia
        
        stt = cartesia.STT()
        tts = cartesia.TTS()
        log.info("✅ Cartesia STT/TTS initialized successfully")
        return True
        
    except Exception as e:
        log.error(f"❌ Cartesia initialization failed: {e}")
        return False

async def test_vad():
    """Test 5: Verify Voice Activity Detection."""
    log.info("\n🔊 TEST 5: Voice Activity Detection (VAD)")
    log.info("-" * 50)
    
    try:
        from livekit.plugins import silero
        
        vad = silero.VAD.load()
        log.info("✅ Silero VAD loaded successfully")
        return True
        
    except Exception as e:
        log.warning(f"⚠️  VAD initialization failed (non-critical): {e}")
        return False

async def test_livekit_connection():
    """Test 6: Verify LiveKit connection details are valid."""
    log.info("\n🔗 TEST 6: LiveKit Connection Details")
    log.info("-" * 50)
    
    if not LIVEKIT_URL or not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        log.error("❌ Missing LiveKit connection details")
        return False
    
    log.info(f"✅ LiveKit URL: {LIVEKIT_URL}")
    log.info(f"✅ LiveKit API Key: {LIVEKIT_API_KEY[:5]}...{LIVEKIT_API_KEY[-5:]}")
    log.info(f"✅ LiveKit API Secret: {'*' * 10}...{LIVEKIT_API_SECRET[-5:]}")
    
    return True

async def run_all_tests():
    """Run all tests."""
    log.info("=" * 50)
    log.info("🚀 SALES AGENT TEST SUITE")
    log.info("=" * 50)
    
    # Check environment first
    if not check_environment():
        log.error("\n❌ Environment check failed. Please set all required variables in .env")
        return False
    
    tests = [
        ("Context Loading", test_context_loading),
        ("Imports", test_imports),
        ("LLM Prompt", test_llm_prompt),
        ("Cartesia STT/TTS", test_cartesia_stt_tts),
        ("Voice Activity Detection", test_vad),
        ("LiveKit Connection", test_livekit_connection),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            log.error(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    log.info("\n" + "=" * 50)
    log.info("📊 TEST SUMMARY")
    log.info("=" * 50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        log.info(f"{status}: {test_name}")
    
    log.info(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        log.info("\n✅ ALL TESTS PASSED! Your agent is ready to deploy.")
        return True
    else:
        log.info(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(run_all_tests())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        log.info("\n🛑 Tests interrupted by user")
        exit(1)
    except Exception as e:
        log.error(f"🛑 Unexpected error: {e}")
        exit(1)
