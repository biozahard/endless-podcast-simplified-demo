#!/usr/bin/env python3
"""LLM Client for Ollama API interaction."""

import json
import requests
from typing import List


class LLMClient:
    """Client for interacting with local Ollama server."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.generate_endpoint = "/api/generate"
        self.tags_endpoint = "/api/tags"
    
    def list_models(self) -> List[str]:
        """Get list of available models from Ollama."""
        try:
            r = requests.get(self.base_url + self.tags_endpoint, timeout=5)
            r.raise_for_status()
            data = r.json()
            return [m.get('name') for m in data.get('models', [])]
        except Exception:
            return []

    def generate(self, prompt: str, model: str, stream_output: bool = True) -> str:
        """Generate text with streaming output to console."""
        payload = {"model": model, "prompt": prompt, "stream": True}
        chunks = []
        
        with requests.post(
            self.base_url + self.generate_endpoint, 
            json=payload, 
            stream=True, 
            timeout=600
        ) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                    
                if 'response' in data:
                    part = data['response']
                    if stream_output:
                        print(part, end='', flush=True)
                    chunks.append(part)
                    
                if data.get('done'):
                    break
        
        if stream_output:
            print()
        return ''.join(chunks).strip()

    def generate_quiet(self, prompt: str, model: str, max_length: int = 240) -> str:
        """Generate text without console output, with length limit."""
        payload = {"model": model, "prompt": prompt, "stream": True}
        chunks = []
        
        with requests.post(
            self.base_url + self.generate_endpoint, 
            json=payload, 
            stream=True, 
            timeout=120
        ) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                    
                if 'response' in data:
                    chunks.append(data['response'])
                    
                if data.get('done'):
                    break
        
        text = ' '.join(''.join(chunks).split())
        
        # Limit length
        if len(text) > max_length:
            cut = text[:max_length]
            cut = cut.rsplit(' ', 1)[0] + '…'
            return cut
        
        return text.strip()
