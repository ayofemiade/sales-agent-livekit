# sales_agent.py
import os
import asyncio
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
    from livekit.agents import WorkerOptions, JobContext
    from livekit.agents.cli import cli
except Exception as e:
    raise SystemExit(f"Missing livekit packages or incompatible versions: {e}")

# optional plugin imports
openai = cartesia = silero = None
try:
    from livekit.plugins import openai as _openai, cartesia as _cartesia, silero as _silero
    openai, cartesia, silero = _openai, _cartesia, _silero
    log.info("Plugins imported")
except Exception as e:
    log.warning("Optional plugins failed to import: %s", e)

# --- environment keys ---
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# Only Cartesia is required for STT/TTS
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
async def entry(ctx: JobContext):
    log.info("🚀 Sales Agent starting...")

    context_data = load_context()
    log.info("✅ Loaded context (%d chars)", len(context_data))

    # Initialize plugins
    llm = stt = tts = vad = None

    if openai:
        try:
            llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
            log.info("LLM initialized (Cerebras)")
        except Exception as e:
            log.warning("LLM init failed: %s", e)

    if cartesia:
        try:
            stt = cartesia.STT()
            tts = cartesia.TTS()
            log.info("Cartesia STT/TTS initialized")
        except Exception as e:
            log.warning("Cartesia init failed: %s", e)

    if silero:
        try:
            vad = silero.VAD.load()
            log.info("Silero VAD loaded")
        except Exception as e:
            log.warning("VAD init failed: %s", e)

    # Instructions for the agent
    instructions = f"""
    You are a friendly, helpful sales agent. Speak naturally and warmly.
    Only use the information in the context below.

    {context_data}

    RULES:
      - If asked anything outside the context, say: "I don't have that information."
      - Keep responses short for speaking.
    """

    # ===== CONNECT CORRECTLY =====
    connection = await ctx.connect()

    async with connection as agent:
        welcome = "Hello! I'm your virtual sales assistant. How can I help you today?"

        if hasattr(agent, "say") and asyncio.iscoroutinefunction(agent.say):
            try:
                log.info("Sending welcome message...")
                await agent.say(welcome)
            except Exception as e:
                log.warning("agent.say failed: %s", e)
        else:
            log.info("No TTS available. Welcome: %s", welcome)

        log.info("🗣️ Agent is live and listening...")

        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            log.info("Agent shutdown requested.")

# --- Worker options ---
def build_worker_options_for_entry(entry_fn):
    for param in ("entrypoint_fnc", "entry", "entrypoint"):
        try:
            return WorkerOptions(**{param: entry_fn})
        except TypeError:
            continue
    raise TypeError("WorkerOptions cannot accept entry function.")

if __name__ == "__main__":
    options = build_worker_options_for_entry(entry)
    cli.run_app(options)
