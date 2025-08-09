"""
AI Service Module - Flexible provider abstraction
Easily switch between Hugging Face, OpenAI, Gemini, etc.
"""
import os
import json
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import aiohttp

@dataclass
class AIResponse:
    """Standardized AI response format"""
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    confidence: Optional[float] = None

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def generate_text(self, prompt: str, max_tokens: int = 150) -> AIResponse:
        pass
    
    @abstractmethod
    async def analyze_data(self, data: Dict, query: str) -> AIResponse:
        pass

class HuggingFaceProvider(AIProvider):
    """Hugging Face AI provider (FREE)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY", "")
        self.base_url = "https://api-inference.huggingface.co/models"
        self.model = "microsoft/DialoGPT-medium"  # Free model
        
    async def generate_text(self, prompt: str, max_tokens: int = 150) -> AIResponse:
        """Generate text using Hugging Face"""
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/{self.model}",
                    headers=headers,
                    json={"inputs": prompt, "parameters": {"max_length": max_tokens}}
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result[0].get("generated_text", "").replace(prompt, "").strip()
                        return AIResponse(
                            content=content,
                            provider="HuggingFace",
                            model=self.model
                        )
                    else:
                        return AIResponse(
                            content="Sorry, I couldn't process that request.",
                            provider="HuggingFace",
                            model=self.model
                        )
            except Exception as e:
                return AIResponse(
                    content=f"Error: {str(e)}",
                    provider="HuggingFace",
                    model=self.model
                )
    
    async def analyze_data(self, data: Dict, query: str) -> AIResponse:
        """Analyze supply chain data"""
        # Prepare context for analysis
        context = f"""
        Supply Chain Data Analysis:
        - Total Shipments: {len(data.get('shipments', []))}
        - Active Shipments: {len([s for s in data.get('shipments', []) if s.get('status') == 'In Transit'])}
        - Delayed Shipments: {len([s for s in data.get('shipments', []) if s.get('status') == 'Delayed'])}
        - Distribution Centers: {len(data.get('distribution_centers', []))}
        - Stores: {len(data.get('stores', []))}
        - Active Events: {len(data.get('events', []))}
        
        Query: {query}
        
        Provide a brief analysis:
        """
        
        return await self.generate_text(context, max_tokens=200)

class OpenAIProvider(AIProvider):
    """OpenAI GPT provider (PAID)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = "gpt-3.5-turbo"
        
    async def generate_text(self, prompt: str, max_tokens: int = 150) -> AIResponse:
        """Generate text using OpenAI GPT"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result["choices"][0]["message"]["content"]
                        tokens = result["usage"]["total_tokens"]
                        return AIResponse(
                            content=content,
                            provider="OpenAI",
                            model=self.model,
                            tokens_used=tokens
                        )
                    else:
                        return AIResponse(
                            content="OpenAI request failed.",
                            provider="OpenAI",
                            model=self.model
                        )
            except Exception as e:
                return AIResponse(
                    content=f"OpenAI Error: {str(e)}",
                    provider="OpenAI",
                    model=self.model
                )
    
    async def analyze_data(self, data: Dict, query: str) -> AIResponse:
        """Analyze supply chain data with GPT"""
        context = f"""
        You are a supply chain analyst. Analyze this data and answer the query:
        
        Supply Chain Metrics:
        - Total Shipments: {len(data.get('shipments', []))}
        - In Transit: {len([s for s in data.get('shipments', []) if s.get('status') == 'In Transit'])}
        - Delayed: {len([s for s in data.get('shipments', []) if s.get('status') == 'Delayed'])}
        - Distribution Centers: {len(data.get('distribution_centers', []))}
        - Stores: {len(data.get('stores', []))}
        - Active Issues: {len([e for e in data.get('events', []) if e.get('resolution_status') != 'Resolved'])}
        
        Query: {query}
        
        Provide actionable insights in 2-3 sentences:
        """
        
        return await self.generate_text(context, max_tokens=200)

class GeminiProvider(AIProvider):
    """Google Gemini provider (FREE TIER)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = "gemini-pro"
        
    async def generate_text(self, prompt: str, max_tokens: int = 150) -> AIResponse:
        """Generate text using Gemini"""
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": max_tokens}
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        content = result["candidates"][0]["content"]["parts"][0]["text"]
                        return AIResponse(
                            content=content,
                            provider="Gemini",
                            model=self.model
                        )
                    else:
                        return AIResponse(
                            content="Gemini request failed.",
                            provider="Gemini",
                            model=self.model
                        )
            except Exception as e:
                return AIResponse(
                    content=f"Gemini Error: {str(e)}",
                    provider="Gemini",
                    model=self.model
                )
    
    async def analyze_data(self, data: Dict, query: str) -> AIResponse:
        """Analyze supply chain data with Gemini"""
        context = f"""
        As a supply chain expert, analyze this operational data:
        
        Current Status:
        - Shipments: {len(data.get('shipments', []))} total
        - Active: {len([s for s in data.get('shipments', []) if s.get('status') == 'In Transit'])}
        - Delayed: {len([s for s in data.get('shipments', []) if s.get('status') == 'Delayed'])}
        - Network: {len(data.get('distribution_centers', []))} DCs, {len(data.get('stores', []))} stores
        - Open Issues: {len([e for e in data.get('events', []) if e.get('resolution_status') != 'Resolved'])}
        
        User Question: {query}
        
        Provide a concise, actionable analysis:
        """
        
        return await self.generate_text(context, max_tokens=200)

class AIService:
    """Main AI service with provider switching"""
    
    def __init__(self, provider: str = "huggingface"):
        self.provider_name = provider
        self.provider = self._create_provider(provider)
    
    def _create_provider(self, provider: str) -> AIProvider:
        """Factory method to create AI providers"""
        providers = {
            "huggingface": HuggingFaceProvider,
            "openai": OpenAIProvider,
            "gemini": GeminiProvider
        }
        
        if provider not in providers:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(providers.keys())}")
        
        return providers[provider]()
    
    def switch_provider(self, provider: str):
        """Switch AI provider at runtime"""
        print(f"🔄 Switching AI provider from {self.provider_name} to {provider}")
        self.provider_name = provider
        self.provider = self._create_provider(provider)
    
    async def query_supply_chain(self, data: Dict, query: str) -> AIResponse:
        """Smart query interface for supply chain data"""
        return await self.provider.analyze_data(data, query)
    
    async def generate_insights(self, data: Dict) -> List[AIResponse]:
        """Generate multiple insights about supply chain performance"""
        insights = []
        
        insight_prompts = [
            "What are the main performance issues in this supply chain?",
            "What optimization opportunities do you see?",
            "Are there any concerning patterns or trends?",
            "What should management focus on first?"
        ]
        
        for prompt in insight_prompts:
            response = await self.provider.analyze_data(data, prompt)
            insights.append(response)
        
        return insights
    
    def get_provider_status(self) -> Dict:
        """Get current provider information"""
        return {
            "current_provider": self.provider_name,
            "model": getattr(self.provider, 'model', 'unknown'),
            "available_providers": ["huggingface", "openai", "gemini"]
        }

# Global AI service instance
ai_service = AIService("huggingface")  # Start with free Hugging Face