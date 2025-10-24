#!/usr/bin/env python3
"""
Ollama Turbo Client for AI Research Daily

Enhanced with capabilities specifically for research analysis:
- Vision: Analyze paper diagrams, charts, figures
- Thinking: Deep reasoning for research synthesis
- Web Search: Fallback when arXiv/HuggingFace APIs fail
- Structured Outputs: Clean JSON for paper metadata

Author: The Lab - AI Research Daily
"""

import aiohttp
import asyncio
import json
from typing import List, Dict, Optional
from datetime import datetime


class OllamaTurboClient:
    """
    Ollama Cloud API Client optimized for AI research analysis
    
    Works in GitHub Actions and locally
    Uses Ollama Cloud API (https://api.ollama.ai)
    """

    def __init__(self, api_key: str, base_url: str = "https://api.ollama.ai"):
        self.api_key = api_key
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def generate(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        thinking: bool = False,
        web_search: bool = False,
        structured_output: Optional[Dict] = None,
        images: Optional[List[str]] = None
    ) -> str:
        """Generate text using Ollama Cloud"""
        
        url = f"{self.base_url}/api/chat"
        message_content = prompt
        if images:
            message_content = {'text': prompt, 'images': images}

        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': message_content}],
            'stream': False,
            'options': {'num_predict': max_tokens, 'temperature': temperature}
        }

        if thinking:
            payload['options']['thinking'] = True
        if web_search:
            payload['web_search'] = True
        if structured_output:
            payload['format'] = structured_output

        async with self.session.post(url, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            return data['message']['content']

    async def web_search_fallback(self, query: str, max_tokens: int = 2000) -> str:
        """Web search fallback when APIs fail"""
        return await self.generate(
            model='deepseek-v3.1:671b-cloud',
            prompt=query,
            max_tokens=max_tokens,
            temperature=0.7,
            web_search=True
        )


# Recommended models
MODELS = {
    'reasoning': 'deepseek-v3.1:671b-cloud',
    'vision': 'qwen3-vl:235b-cloud',
    'creative': 'qwen3-coder:30b-cloud',
    'embedding': 'nomic-embed-text'
}
