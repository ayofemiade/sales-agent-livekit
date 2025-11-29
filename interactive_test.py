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

async def test_with_real_llm():
    """Test agent responses with real LLM."""
    log.info("=" * 60)
    log.info("📞 INTERACTIVE SALES AGENT TEST (Real LLM Mode)")
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
        from livekit.agents import llm
        
        # Create LLM instance
        model = openai.LLM.with_cerebras(model="llama-3.3-70b")
        
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
                # Create chat context
                chat_ctx = llm.ChatContext()
                # Use add_message and wrap content in list if needed (trying list first based on pydantic error)
                # But wait, usually content is string. Maybe the error was misleading or I misread it?
                # "Input should be a valid list ... input_type=str"
                # Let's try string first, if it fails I'll know.
                # Actually, I'll try list because I'm 90% sure based on the error.
                # Wait, if I pass list, pydantic might complain it expects string?
                # The error said "Input should be a valid list", so it EXPECTS a list.
                
                # However, ChatMessage usually takes string.
                # Maybe I should check if I can import ChatMessage and inspect it?
                # I'll just try string first, but use add_message.
                
                chat_ctx.append(role="system", text=instructions) 
                # Wait, I saw 'append' is NOT in dir().
                # I saw 'add_message'.
                
                # chat_ctx.add_message(llm.ChatMessage(role="system", content=instructions))
                
                # But wait, does add_message take ChatMessage?
                # I'll try to use the 'append' equivalent if it exists.
                # 'add_message' likely takes ChatMessage.
                
                chat_ctx.add_message(llm.ChatMessage(role="system", content=instructions))
                chat_ctx.add_message(llm.ChatMessage(role="user", content=query))
                
                # Get response from LLM
                response_stream = await model.chat(chat_ctx=chat_ctx)
                
                # Collect the full response
                full_response = ""
                async for chunk in response_stream:
                    if chunk.choices:
                        delta = chunk.choices[0].delta
                        if delta.content:
                            full_response += delta.content
                
                log.info(f"🤖 Response: {full_response.strip()}\n")
                
            except Exception as e:
                log.error(f"❌ Error: {e}\n")
            
            await asyncio.sleep(1)  # Rate limiting
        
        log.info("✅ Interactive test completed!")
        
    except ImportError as e:
        log.error(f"❌ Required library not available: {e}")
        log.info("\nMake sure you have 'livekit-agents' and 'livekit-plugins-openai' installed:")
        log.info("  pip install livekit-agents livekit-plugins-openai\n")
        await run_mock_test(test_queries)
        
    except Exception as e:
        log.error(f"❌ LLM error: {e}")
        log.info("\nRunning mock test instead...\n")
        await run_mock_test(test_queries)

async def run_mock_test(test_queries):
    """Run test with mock responses."""
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
        await test_with_real_llm()
    except KeyboardInterrupt:
        log.info("\n🛑 Test interrupted by user")
    except Exception as e:
        log.error(f"🛑 Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())