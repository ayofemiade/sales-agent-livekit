#!/usr/bin/env python3
# console_test.py
"""
Console-based LiveKit Sales Agent Tester
Test your agent with text input directly in the console without needing LiveKit Studio
"""

import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = logging.getLogger()

load_dotenv()

def load_context() -> str:
    """Load product context"""
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

async def create_agent():
    """Initialize the LLM"""
    from livekit.plugins import openai
    
    context_data = load_context()
    
    instructions = f"""You are a friendly, helpful sales agent. Speak naturally and warmly.
Only use the information in the context below. Keep responses short and conversational.

{context_data}

RULES:
  - If asked anything outside the context, say: "I don't have that information."
  - Be helpful and encouraging.
  - Keep responses natural and conversational.
"""
    
    llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
    return llm, instructions

async def chat_with_agent(llm, instructions):
    """Interactive chat with the agent"""
    log.info("\n" + "=" * 60)
    log.info("💬 SALES AGENT - CONSOLE TEST")
    log.info("=" * 60)
    log.info("\nWelcome! I'm your virtual sales assistant.")
    log.info("Type your questions below. Type 'quit' or 'exit' to end.\n")
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                log.info("\n👋 Thanks for testing! Goodbye.")
                break
            
            # Add to history
            conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Build messages for LLM
            messages = [
                {"role": "system", "content": instructions},
                *conversation_history
            ]
            
            # Get response
            log.info("Agent: ", end="", flush=True)
            
            try:
                response = await llm.chat(messages=messages)
                
                # Extract response text
                if hasattr(response, 'choices') and response.choices:
                    answer = response.choices[0].message.content
                else:
                    answer = str(response)
                
                print(answer)
                
                # Add agent response to history
                conversation_history.append({
                    "role": "assistant",
                    "content": answer
                })
                
                print()  # Blank line for readability
                
            except AttributeError as e:
                log.error(f"Error processing response: {e}")
                log.info("Please try again.\n")
            
        except KeyboardInterrupt:
            log.info("\n\n👋 Chat ended by user. Goodbye!")
            break
        except EOFError:
            log.info("\n👋 End of input. Goodbye!")
            break
        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Please try again.\n")

async def main():
    log.info("\n" + "=" * 60)
    log.info("🚀 Initializing Sales Agent...")
    log.info("=" * 60)
    
    try:
        # Show context
        context = load_context()
        log.info("\n📋 Agent Context Loaded:")
        log.info("-" * 60)
        log.info(context)
        
        # Initialize LLM
        log.info("\n🤖 Initializing LLM (Cerebras)...")
        llm, instructions = await create_agent()
        log.info("✅ LLM ready!\n")
        
        # Start chat
        await chat_with_agent(llm, instructions)
        
    except ImportError as e:
        log.error(f"❌ Missing dependency: {e}")
        log.info("\nMake sure to install: pip install -r requirements.txt")
        return 1
    except Exception as e:
        log.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        log.info("\n\n🛑 Interrupted by user")
        exit(0)
