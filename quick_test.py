#!/usr/bin/env python3
# quick_test.py
"""
Quick test - Validates your agent works without connecting to LiveKit
Perfect for development and debugging
"""

import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger()

load_dotenv()

def test_env():
    """Check environment setup"""
    log.info("\n🔐 Environment Check")
    log.info("-" * 50)
    
    required = ["CARTESIA_API_KEY", "CEREBRAS_API_KEY", "LIVEKIT_API_KEY"]
    all_good = True
    
    for key in required:
        val = os.getenv(key)
        if val:
            log.info(f"✅ {key}")
        else:
            log.error(f"❌ {key} - NOT SET")
            all_good = False
    
    return all_good

def test_imports():
    """Check all imports"""
    log.info("\n📦 Import Check")
    log.info("-" * 50)
    
    try:
        import livekit.agents
        log.info("✅ livekit.agents")
    except:
        log.error("❌ livekit.agents")
        return False
    
    try:
        from livekit.plugins import openai, cartesia, silero
        log.info("✅ livekit.plugins.openai")
        log.info("✅ livekit.plugins.cartesia")
        log.info("✅ livekit.plugins.silero")
    except Exception as e:
        log.error(f"❌ plugins: {e}")
        return False
    
    return True

def test_services():
    """Initialize services"""
    log.info("\n🤖 Service Initialization")
    log.info("-" * 50)
    
    try:
        from livekit.plugins import openai, cartesia, silero
        
        # LLM
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        log.info("✅ LLM (Cerebras Llama 3.3-70B)")
        
        # STT/TTS
        stt = cartesia.STT()
        tts = cartesia.TTS()
        log.info("✅ STT (Cartesia)")
        log.info("✅ TTS (Cartesia)")
        
        # VAD
        vad = silero.VAD.load()
        log.info("✅ VAD (Silero)")
        
        return True
    except Exception as e:
        log.error(f"❌ Service init failed: {e}")
        return False

def test_context():
    """Check context files"""
    log.info("\n📋 Context Check")
    log.info("-" * 50)
    
    from pathlib import Path
    context_dir = Path("context")
    
    if not context_dir.exists():
        log.error("❌ context/ directory not found")
        return False
    
    files = list(context_dir.glob("*"))
    if not files:
        log.error("❌ No context files found")
        return False
    
    for f in files:
        log.info(f"✅ {f.name}")
    
    return True

def main():
    log.info("\n" + "=" * 50)
    log.info("⚡ QUICK AGENT TEST")
    log.info("=" * 50)
    
    results = {
        "Environment": test_env(),
        "Imports": test_imports(),
        "Services": test_services(),
        "Context": test_context(),
    }
    
    log.info("\n" + "=" * 50)
    log.info("📊 Results")
    log.info("=" * 50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, result in results.items():
        status = "✅" if result else "❌"
        log.info(f"{status} {test}")
    
    log.info(f"\n{passed}/{total} checks passed")
    
    if all(results.values()):
        log.info("\n✅ Your agent is ready!")
        log.info("\n🚀 Run: python sales_agent.py")
        return 0
    else:
        log.info("\n❌ Please fix the errors above")
        return 1

if __name__ == "__main__":
    exit(main())
