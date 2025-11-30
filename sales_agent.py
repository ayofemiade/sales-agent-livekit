# sales_agent.py
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# --- logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
log = logging.getLogger("sales_agent")

# --- load .env early ---
load_dotenv()

# --- defensive imports for LiveKit ---
try:
    from livekit.agents import (
        AutoSubscribe,
        JobContext,
        WorkerOptions,
        cli,
    )
    from livekit.agents.voice import Agent
    from livekit.plugins import openai, cartesia
except Exception as e:
    raise SystemExit(f"Missing livekit packages or incompatible versions: {e}")

# Try to import silero (optional)
try:
    from livekit.plugins import silero
except ImportError:
    silero = None
    log.warning("Silero VAD not available")

# --- environment keys ---
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

if not CARTESIA_API_KEY:
    raise SystemExit("❌ Please set CARTESIA_API_KEY in your .env file")

# --- context loader ---
def load_context() -> str:
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

# --- entrypoint: executes per job ---
async def entrypoint(ctx: JobContext):
    log.info("🚀 Sales Agent starting...")

    # Load context
    context_data = load_context()
    log.info("✅ Loaded context (%d chars)", len(context_data))

    # Instructions for the agent
    initial_instructions = f"""You are a friendly, helpful sales agent. Speak naturally and warmly.
Only use the information in the context below.

{context_data}

RULES:
  - If asked anything outside the context, say: "I don't have that information."
  - Keep responses short and conversational for speaking.
  - Be helpful and encouraging.
"""

    # Initialize VAD (try silero, fall back to None)
    vad_instance = None
    if silero:
        try:
            vad_instance = silero.VAD.load()
            log.info("VAD loaded")
        except Exception as e:
            log.warning(f"VAD init failed: {e}, using no VAD")

    # Connect to the room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    log.info("Connected to room")

    # Create the voice agent - this automatically starts it
    agent = Agent(
        instructions=initial_instructions,
        vad=vad_instance,
        stt=cartesia.STT(),
        llm=openai.LLM.with_cerebras(model="llama-3.3-70b"),
        tts=cartesia.TTS(),
        allow_interruptions=True,
    )
    
    # The agent lifecycle is managed by the framework
    # Just call on_enter to start the session
    await agent.on_enter()
    log.info("🗣️ Voice agent started")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
