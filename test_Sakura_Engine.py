from SRC.Systems.AssistantEngines.SakuraEngine import SakuraEngine

# Create the engine
engine = SakuraEngine()

# Test message
user_message = "I'm feeling a little overwhelmed today."

# Generate Sakura's response
response = engine.generate_response(user_message)

print("\n=== SAKURA ENGINE OUTPUT ===\n")
print(response)
