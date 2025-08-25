#!/usr/bin/env python3
"""Ultra-simple podcast conversation demo."""
import time
import signal
import sys
import argparse
from dataclasses import dataclass

from llm_client import LLMClient

# --- Configuration ---
DEFAULT_MODEL = "gpt-oss:20b"
llm = LLMClient()

# --- Simple models ---
@dataclass
class Persona:
    name: str
    personality: str

# --- CLI argument parsing ---
def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Ultra-simple podcast conversation demo")
    parser.add_argument("--topic", default="AI and the future", help="Conversation topic")
    parser.add_argument("--host-name", default="Joe Rogan", help="Host name")
    parser.add_argument("--host-personality", default="Curious interviewer who asks direct questions and shares personal experiences", help="Host personality description")
    parser.add_argument("--guest-name", default="Alex Chen", help="Guest name")
    parser.add_argument("--guest-personality", default="Tech entrepreneur with strong opinions about AI and the future", help="Guest personality description")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Language model to use")
    parser.add_argument("--language", default="English", help="Conversation language (en, uk, es, fr, etc.)")
    parser.add_argument("--history", type=int, default=10, help="Number of recent messages to include in context (default: 10)")
    return parser.parse_args()

# --- Simple conversation demo ---
def run_conversation():
    """Run a simple 2-person conversation demo."""
    args = parse_args()
    
    # Use CLI args directly
    topic = args.topic
    host_name = args.host_name
    host_personality = args.host_personality
    guest_name = args.guest_name
    guest_personality = args.guest_personality
    model_to_use = args.model
    language_name = args.language
    history_limit = args.history
    
    # Create host and guest with custom names and personalities
    host = Persona(name=host_name, personality=host_personality)
    guest = Persona(name=guest_name, personality=guest_personality)
    participants = [host, guest]
    history = []
    
    print(f"\n=== Podcast: {topic} ===")
    print(f"Model: {model_to_use}")
    print(f"Language: {language_name}")
    print(f"Participants: {host.name} (host), {guest.name} (guest)")
    print(f"Host: {host.personality}")
    print(f"Guest: {guest.personality}")
    print("Press Ctrl+C to stop\n")
    
    turn = 0
    try:
        while True:
            speaker = participants[turn % 2]
            
            # Build simple prompt
            recent_chat = "\n".join(history[-history_limit:]) if history else "(start)"
            prompt = (
                f"Podcast conversation in {language_name}. Topic: {topic}. "
                f"Participants: {host.name} ({host.personality}) is a host and interviewer, {guest.name} ({guest.personality}). "
                f"Recent turns:\n{recent_chat}\n"
                f"Your turn: {speaker.name}. Be conversational, ~30 words max. Respond in {language_name}."
            )
            
            print(f"[{speaker.name}]: ", end="", flush=True)
            reply = llm.generate(prompt, model=model_to_use)
            history.append(f"{speaker.name}: {reply}")
            print()
            
            turn += 1
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\nConversation ended after {turn} turns.")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    run_conversation()
