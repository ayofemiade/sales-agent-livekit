# sales_agent.py
import os
from pathlib import Path
from dotenv import load_dotenv
from livekit.agents import WorkerOptions, JobContext, cli
from livekit.plugins import openai, silero, cartesia


load_dotenv()

CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# --- Basic check for keys ---
if not CEREBRAS_API_KEY or not CARTESIA_API_KEY:
    raise SystemExit("❌ Please set CEREBRAS_API_KEY and CARTESIA_API_KEY in your .env file")

# --- Load context files (used to teach your agent what to say) ---
def load_context():
    context_dir = Path("context")
    context_dir.mkdir(exist_ok=True)
    all_content = ""
    for file_path in context_dir.glob("*"):
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding="utf-8")
                all_content += f"\n=== {file_path.name} ===\n{content}\n"
            except Exception as e:
                print(f"⚠️ Skipped {file_path.name}: {e}")
    return all_content.strip() or "No context files found"

# --- Entry function for LiveKit Agent ---
async def entry(ctx: JobContext):
    print("🚀 Sales Agent starting...")

    context_data = load_context()
    print(f"✅ Context loaded ({len(context_data)} characters)")

    # Initialize the tools (voice + LLM)
    llm = openai.LLM.with_cerebras(model="llama-3.3-70b")
    stt = cartesia.STT()
    tts = cartesia.TTS()
    vad = silero.VAD.load()

    # The agent’s core “personality”
    instructions = f"""
    You are a friendly, professional sales agent who speaks with warmth and clarity.
    Use ONLY the information provided in the context below.
    {context_data}
    RULES:
    - If something isn't in the context, say: "I don't have that information."
    - Keep replies short and natural for speech.
    """

    # Create a simple agent session using LiveKit plugins
    async with ctx.connect() as agent:
        # Speak an introduction when started
        await agent.say("Hello! I'm your virtual sales assistant. How can I help you today?")
        print("🗣️ Agent is live and listening...")

# --- Run locally ---
if __name__ == "__main__":
    cli.run_app(WorkerOptions(entry=entry))
