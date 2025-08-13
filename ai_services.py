"""
AI Services Module - Modular architecture for multiple AI providers
Easily switch between Hugging Face, OpenAI, Google Gemini, etc.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import os
import requests
import json
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AIResponse:
    """Standard response format for all AI providers"""
    content: str
    provider: str
    model: str
    success: bool
    error: Optional[str] = None
    tokens_used: Optional[int] = None

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def query_data(self, query: str, context: Dict[str, Any]) -> AIResponse:
        """Process natural language queries about supply chain data"""
        pass
    
    @abstractmethod
    def generate_insights(self, data: Dict[str, Any]) -> AIResponse:
        """Generate smart analytics and insights from supply chain data"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured"""
        pass

class HuggingFaceProvider(AIProvider):
    """Hugging Face AI Provider - Free tier available"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "microsoft/DialoGPT-medium"):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.model = model
        self.base_url = "https://api-inference.huggingface.co/models"
        
    def query_data(self, query: str, context: Dict[str, Any]) -> AIResponse:
        """Process natural language queries"""
        try:
            # Build context for the AI
            context_str = self._build_context_string(context)
            
            prompt = f"""You are a supply chain analyst. Based on this data:
{context_str}

User Query: {query}

Provide a helpful, specific answer about the supply chain data. Be concise and actionable."""

            response = self._make_request(prompt)
            
            if response:
                return AIResponse(
                    content=response,
                    provider="HuggingFace",
                    model=self.model,
                    success=True
                )
            else:
                return AIResponse(
                    content="I couldn't process your query at the moment.",
                    provider="HuggingFace", 
                    model=self.model,
                    success=False,
                    error="API request failed"
                )
                
        except Exception as e:
            logger.error(f"HuggingFace query error: {e}")
            return AIResponse(
                content="Sorry, I encountered an error processing your query.",
                provider="HuggingFace",
                model=self.model, 
                success=False,
                error=str(e)
            )
    
    def generate_insights(self, data: Dict[str, Any]) -> AIResponse:
        """Generate smart analytics and insights"""
        try:
            # Analyze the data and generate insights
            stats = self._calculate_stats(data)
            
            prompt = f"""As a supply chain expert, analyze this data and provide 3-5 key insights:

Supply Chain Statistics:
- Total Shipments: {stats['total_shipments']}
- Delayed Shipments: {stats['delayed_shipments']} ({stats['delay_rate']:.1f}%)
- Active Trucks: {stats['active_trucks']}
- Distribution Centers: {stats['distribution_centers']}
- Stores: {stats['stores']}
- Open Events: {stats['open_events']}
- Weather Alerts: {stats['weather_alerts']}

Provide actionable insights about performance, risks, and optimization opportunities. Keep it professional and concise."""

            response = self._make_request(prompt)
            
            if response:
                return AIResponse(
                    content=response,
                    provider="HuggingFace",
                    model=self.model,
                    success=True
                )
            else:
                # Fallback to rule-based insights
                return self._generate_fallback_insights(stats)
                
        except Exception as e:
            logger.error(f"HuggingFace insights error: {e}")
            stats = self._calculate_stats(data)
            return self._generate_fallback_insights(stats)
    
    def is_available(self) -> bool:
        """Check if HuggingFace is available"""
        try:
            # Simple availability check
            response = requests.get(f"{self.base_url}/{self.model}", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _make_request(self, prompt: str) -> Optional[str]:
        """Make request to HuggingFace API"""
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 200,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(
                f"{self.base_url}/{self.model}",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').replace(prompt, '').strip()
                elif isinstance(result, dict):
                    return result.get('generated_text', '').replace(prompt, '').strip()
            
            return None
            
        except Exception as e:
            logger.error(f"HuggingFace API request failed: {e}")
            return None
    
    def _build_context_string(self, context: Dict[str, Any]) -> str:
        """Build context string from supply chain data"""
        lines = []
        
        if 'shipments' in context:
            shipments = context['shipments']
            lines.append(f"Shipments: {len(shipments)} total")
            delayed = len([s for s in shipments if s.get('status') == 'Delayed'])
            lines.append(f"Delayed shipments: {delayed}")
        
        if 'stores' in context:
            lines.append(f"Stores: {len(context['stores'])}")
        
        if 'trucks' in context:
            trucks = context['trucks']
            active = len([t for t in trucks if t.get('status') == 'In Transit'])
            lines.append(f"Active trucks: {active}/{len(trucks)}")
        
        return "; ".join(lines)
    
    def _calculate_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate statistics from supply chain data"""
        shipments = data.get('shipments', [])
        trucks = data.get('trucks', [])
        events = data.get('events', [])
        weather_alerts = data.get('weather_alerts', [])
        
        delayed_shipments = len([s for s in shipments if s.get('status') == 'Delayed'])
        active_trucks = len([t for t in trucks if t.get('status') == 'In Transit'])
        open_events = len([e for e in events if e.get('resolution_status') != 'Resolved'])
        
        return {
            'total_shipments': len(shipments),
            'delayed_shipments': delayed_shipments,
            'delay_rate': (delayed_shipments / len(shipments) * 100) if shipments else 0,
            'active_trucks': active_trucks,
            'distribution_centers': len(data.get('distribution_centers', [])),
            'stores': len(data.get('stores', [])),
            'open_events': open_events,
            'weather_alerts': len(weather_alerts)
        }
    
    def _generate_fallback_insights(self, stats: Dict[str, Any]) -> AIResponse:
        """Generate rule-based insights as fallback"""
        insights = []
        
        # Delay analysis
        if stats['delay_rate'] > 20:
            insights.append(f"⚠️ High delay rate: {stats['delay_rate']:.1f}% of shipments are delayed")
        elif stats['delay_rate'] < 5:
            insights.append(f"✅ Excellent on-time performance: Only {stats['delay_rate']:.1f}% delays")
        
        # Truck utilization
        truck_utilization = (stats['active_trucks'] / max(stats['active_trucks'], 1)) * 100
        if truck_utilization > 80:
            insights.append("🚛 High truck utilization - consider expanding fleet")
        
        # Events analysis
        if stats['open_events'] > 5:
            insights.append(f"🔴 {stats['open_events']} unresolved events require attention")
        
        # Weather impact
        if stats['weather_alerts'] > 0:
            insights.append(f"🌦️ {stats['weather_alerts']} weather alerts may impact operations")
        
        if not insights:
            insights.append("📊 Supply chain operations appear stable")
        
        return AIResponse(
            content="\n".join(insights),
            provider="HuggingFace",
            model="fallback",
            success=True
        )

class OpenAIProvider(AIProvider):
    """OpenAI GPT Provider - Paid service"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        
    def query_data(self, query: str, context: Dict[str, Any]) -> AIResponse:
        # TODO: Implement OpenAI integration
        return AIResponse(
            content="OpenAI provider not yet implemented",
            provider="OpenAI",
            model=self.model,
            success=False,
            error="Not implemented"
        )
    
    def generate_insights(self, data: Dict[str, Any]) -> AIResponse:
        # TODO: Implement OpenAI insights
        return AIResponse(
            content="OpenAI insights not yet implemented", 
            provider="OpenAI",
            model=self.model,
            success=False,
            error="Not implemented"
        )
    
    def is_available(self) -> bool:
        return self.api_key is not None

class GeminiProvider(AIProvider):
    """Google Gemini Provider - Free tier available"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        
    def query_data(self, query: str, context: Dict[str, Any]) -> AIResponse:
        # TODO: Implement Gemini integration
        return AIResponse(
            content="Gemini provider not yet implemented",
            provider="Gemini", 
            model=self.model,
            success=False,
            error="Not implemented"
        )
    
    def generate_insights(self, data: Dict[str, Any]) -> AIResponse:
        # TODO: Implement Gemini insights
        return AIResponse(
            content="Gemini insights not yet implemented",
            provider="Gemini",
            model=self.model,
            success=False,
            error="Not implemented" 
        )
    
    def is_available(self) -> bool:
        return self.api_key is not None

class AIService:
    """Main AI service that manages different providers"""
    
    def __init__(self, primary_provider: str = "huggingface"):
        self.providers = {
            "huggingface": HuggingFaceProvider(),
            "openai": OpenAIProvider(),
            "gemini": GeminiProvider()
        }
        self.primary_provider = primary_provider
        
    def get_active_provider(self) -> AIProvider:
        """Get the currently active AI provider"""
        provider = self.providers.get(self.primary_provider)
        
        # Fallback to available provider if primary is not available
        if not provider or not provider.is_available():
            for name, p in self.providers.items():
                if p.is_available():
                    logger.info(f"Falling back to {name} provider")
                    return p
            
            # If no providers available, return HuggingFace as default
            logger.warning("No AI providers available, using HuggingFace")
            return self.providers["huggingface"]
        
        return provider
    
    def switch_provider(self, provider_name: str) -> bool:
        """Switch to a different AI provider"""
        if provider_name in self.providers:
            self.primary_provider = provider_name
            logger.info(f"Switched to {provider_name} provider")
            return True
        return False
    
    def query_data(self, query: str, context: Dict[str, Any]) -> AIResponse:
        """Process natural language query using active provider"""
        provider = self.get_active_provider()
        return provider.query_data(query, context)
    
    def generate_insights(self, data: Dict[str, Any]) -> AIResponse:
        """Generate insights using active provider"""
        provider = self.get_active_provider()
        return provider.generate_insights(data)
    
    def get_provider_status(self) -> Dict[str, bool]:
        """Get status of all providers"""
        return {
            name: provider.is_available() 
            for name, provider in self.providers.items()
        }

# Global AI service instance
ai_service = AIService("openai")
