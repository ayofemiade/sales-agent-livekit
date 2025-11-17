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

# plugin imports are optional (silero may require extra deps)
openai = None
cartesia = None
silero = None
try:
    from livekit.plugins import openai as _openai, cartesia as _cartesia, silero as _silero
    openai, cartesia, silero = _openai, _cartesia, _silero
    log.info("Plugins: openai/cartesia/silero imported")
except Exception as e:
    log.warning("One or more livekit plugins failed to import (optional): %s", e)

# --- environment keys ---
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# Basic sanity check
if not CEREBRAS_API_KEY or not CARTESIA_API_KEY:
    raise SystemExit("❌ Please set CEREBRAS_API_KEY and CARTESIA_API_KEY in your .env file")

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

# --- entrypoint: what the worker runs for each job ---
async def entry(ctx: JobContext):
    """
    ctx: JobContext provided by livekit.agents runtime.
    This function must be async. We:
      - wait for a connection object from ctx.connect()
      - use it as an async context manager
      - speak a welcome via agent.say() if available, otherwise fallback to log
      - keep the worker alive (so it can handle incoming events)
    """
    log.info("🚀 Sales Agent starting (entry)...")
    context_data = load_context()
    log.info("✅ Context loaded (%d chars)", len(context_data))

    # initialize optional plugins (best-effort)
    llm = stt = tts = vad = None
    if openai is not None:
        try:
            llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
            log.info("openai LLM initialized (Cerebras)")
        except Exception as e:
            log.warning("openai plugin init failed: %s", e)

    if cartesia is not None:
        try:
            stt = cartesia.STT()
            tts = cartesia.TTS()
            log.info("cartesia STT/TTS initialized")
        except Exception as e:
            log.warning("cartesia plugin init failed: %s", e)

    if silero is not None:
        try:
            vad = silero.VAD.load()
            log.info("silero VAD loaded")
        except Exception as e:
            log.warning("silero VAD init failed (optional): %s", e)

    # Agent personality / instructions (kept for potential LLM usage)
    instructions = f"""
    You are a friendly, professional sales agent who speaks with warmth and clarity.
    Use ONLY the information provided in the context below.
    {context_data}
    RULES:
      - If something isn't in the context, say: "I don't have that information."
      - Keep replies short and natural for speech.
    """

    # ===== CONNECT CORRECTLY =====
    # ctx.connect() is a coroutine that returns a connection-like object.
    conn = await ctx.connect()  # await the coroutine first
    # Now use the returned object as an async context manager
    async with conn as agent:
        # On startup, attempt to send a spoken welcome if the runtime supports agent.say()
        welcome = "Hello! I'm your virtual sales assistant. How can I help you today?"
        if hasattr(agent, "say") and asyncio.iscoroutinefunction(getattr(agent, "say")):
            try:
                log.info("Sending agent welcome (voice)...")
                await agent.say(welcome)
            except Exception as e:
                log.warning("agent.say failed; falling back to log. %s", e)
                log.info("Would say: %s", welcome)
        else:
            # If no say() support, just log the welcome
            log.info("Agent (no TTS available) - welcome: %s", welcome)

        log.info("🗣️ Agent is live and listening...")

        # Keep the agent alive. LiveKit runtime will route media/events in background.
        # We block here until the process is signaled to shut down.
        try:
            # wait forever (or until cancelled)
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            log.info("Agent shutdown requested, exiting entry.")

# --- CLI runner: construct WorkerOptions robustly and run the CLI ---
def build_worker_options_for_entry(entry_fn):
    """
    WorkerOptions constructors changed across versions (entry, entrypoint, entrypoint_fnc).
    Try common signatures in order and return a constructed instance.
    """
    last_exc = None
    for kw in ("entrypoint_fnc", "entry", "entrypoint"):
        try:
            return WorkerOptions(**{kw: entry_fn})
        except TypeError as e:
            last_exc = e
            continue
    # if none worked, raise a helpful message
    raise TypeError("Unable to construct WorkerOptions with known parameter names. Last error: %s" % last_exc)

if __name__ == "__main__":
    # create options and run CLI
    try:
        options = build_worker_options_for_entry(entry)
    except Exception as e:
        raise SystemExit(f"Failed to construct WorkerOptions: {e}")

    # run the CLI runner (dev / console / start etc.)
    cli.run_app(options)
