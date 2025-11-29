from livekit import agents
print("Available in agents:", dir(agents))
try:
    from livekit.agents import pipeline
    print("\nAvailable in pipeline:", dir(pipeline))
except:
    print("\nNo pipeline module")
