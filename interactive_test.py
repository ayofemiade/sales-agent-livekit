# interactive_test.py
"""
Interactive test script to test your sales agent with sample queries.
Run this to simulate customer conversations without needing LiveKit connection.
"""

import os
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

# --- logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
log = logging.getLogger("interactive_test")

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

async def test_with_mock_llm():
    """Test agent responses with a mock LLM (simulated responses)."""
    log.info("=" * 60)
    log.info("📞 INTERACTIVE SALES AGENT TEST (Mock Mode)")
    log.info("=" * 60)
    
    context_data = load_context()
    
    # Sample test queries
    test_queries = [
        "What products do you offer?",
        "How much does the website starter pack cost?",
        "Tell me about your services",
        "What's included in the package?",
        "How long is the hosting support?",
        "Do you offer custom websites?",
        "What's your phone number?",  # Should say "I don't have that information"
    ]
    
    try:
        from livekit.plugins import openai
        
        llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
        
        instructions = f"""
You are a friendly, helpful sales agent. Speak naturally and warmly.
Only use the information in the context below.

{context_data}

RULES:
  - If asked anything outside the context, say: "I don't have that information."
  - Keep responses short and conversational for speaking.
  - Be helpful and encouraging.
"""
        
        log.info("\n🚀 Testing agent responses...\n")
        
        for i, query in enumerate(test_queries, 1):
            log.info(f"📝 Query {i}: {query}")
            
            try:
                response = await llm.agentic_loop(
                    messages=[
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": query}
                    ]
                )
                
                log.info(f"🤖 Response: {response}\n")
                
            except Exception as e:
                log.error(f"❌ Error: {e}\n")
            
            await asyncio.sleep(1)  # Rate limiting
        
        log.info("✅ Interactive test completed!")
        
    except Exception as e:
        log.error(f"❌ LLM not available: {e}")
        log.info("\nRunning mock test instead...\n")
        
        # Mock responses for testing without API
        mock_responses = {
            "What products do you offer?": "We offer a Website Starter Pack - a modern 3-page website built with HTML/CSS/JavaScript, including a contact form and hosting support for 1 month. It's priced at ₦50,000.",
            "How much does the website starter pack cost?": "The Website Starter Pack costs ₦50,000.",
            "Tell me about your services": "We specialize in affordable website solutions. Our main offering is the Website Starter Pack at ₦50,000.",
            "What's included in the package?": "The package includes a modern 3-page website, HTML/CSS/JS development, a contact form, and 1 month of hosting support.",
            "How long is the hosting support?": "The hosting support is included for 1 month with our Website Starter Pack.",
            "Do you offer custom websites?": "I don't have that information about custom website services. I can only tell you about our Website Starter Pack.",
            "What's your phone number?": "I don't have that information.",
        }
        
        log.info("🎭 Testing with mock responses:\n")
        
        for i, query in enumerate(test_queries, 1):
            log.info(f"📝 Query {i}: {query}")
            response = mock_responses.get(query, "I don't have that information.")
            log.info(f"🤖 Response: {response}\n")
            await asyncio.sleep(0.5)
        
        log.info("✅ Mock test completed!")

async def main():
    try:
        await test_with_mock_llm()
    except KeyboardInterrupt:
        log.info("\n🛑 Test interrupted by user")
    except Exception as e:
        log.error(f"🛑 Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
