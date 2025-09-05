import os
import json
import streamlit as st
from typing import Optional, Dict, Any, List
import requests
import base64

# Import AI libraries
try:
    from google import genai
    from google.genai import types

    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIClient:
    """Unified AI client for multiple providers"""

    def __init__(self):
        self.gemini_client = None
        self.openai_client = None
        self._init_clients()

    def _init_clients(self):
        """Initialize AI clients with API keys"""
        # Initialize Gemini
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key and GEMINI_AVAILABLE:
            try:
                self.gemini_client = genai.Client(api_key=gemini_key)
            except Exception as e:
                st.error(f"Failed to initialize Gemini: {str(e)}")

        # Initialize OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and OPENAI_AVAILABLE:
            try:
                self.openai_client = OpenAI(api_key=openai_key)
            except Exception as e:
                st.error(f"Failed to initialize OpenAI: {str(e)}")

    def generate_text(self, prompt: str, model: str = "gemini", max_tokens: int = 1000) -> str:
        """Generate text using specified AI model"""
        try:
            if model == "gemini" and self.gemini_client:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                return response.text or "No response generated"

            elif model == "openai" and self.openai_client:
                # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
                # do not change this unless explicitly requested by the user
                response = self.openai_client.chat.completions.create(
                    model="gpt-5",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content

            else:
                return "AI model not available. Please check API keys."

        except Exception as e:
            return f"Error generating text: {str(e)}"

    def analyze_image(self, image_data: bytes, prompt: str = "Analyze this image") -> str:
        """Analyze image using AI"""
        try:
            if self.gemini_client:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=[
                        types.Part.from_bytes(
                            data=image_data,
                            mime_type="image/jpeg",
                        ),
                        prompt
                    ],
                )
                return response.text if response.text else "No analysis available"

            elif self.openai_client:
                base64_image = base64.b64encode(image_data).decode('utf-8')
                response = self.openai_client.chat.completions.create(
                    model="gpt-5",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                                }
                            ],
                        }
                    ],
                    max_tokens=500,
                )
                return response.choices[0].message.content

            else:
                return "Image analysis not available. Please check API keys."

        except Exception as e:
            return f"Error analyzing image: {str(e)}"

    def generate_image(self, prompt: str, model: str = "gemini") -> Optional[bytes]:
        """Generate image using AI"""
        try:
            if model == "gemini" and self.gemini_client:
                response = self.gemini_client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )

                if response.candidates and response.candidates[0].content:
                    for part in response.candidates[0].content.parts:
                        if part.inline_data and part.inline_data.data:
                            return part.inline_data.data

            elif model == "openai" and self.openai_client:
                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    n=1,
                    size="1024x1024",
                )

                # Download image from URL
                image_url = response.data[0].url
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    return img_response.content

            return None

        except Exception as e:
            st.error(f"Error generating image: {str(e)}")
            return None

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        try:
            if self.gemini_client:
                prompt = f"""
                Analyze the sentiment of the following text and provide:
                1. Overall sentiment (positive/negative/neutral)
                2. Confidence score (0-1)
                3. Key emotional indicators
                4. Brief explanation

                Text: {text}

                Respond in JSON format.
                """

                response = self.gemini_client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                    ),
                )

                if response.text:
                    return json.loads(response.text)

            elif self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-5",
                    messages=[
                        {
                            "role": "system",
                            "content": "Analyze sentiment and respond with JSON containing sentiment, confidence, indicators, and explanation."
                        },
                        {"role": "user", "content": text}
                    ],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)

            return {"error": "No AI model available"}

        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}

    def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language"""
        try:
            prompt = f"Translate the following text to {target_language}: {text}"
            return self.generate_text(prompt)
        except Exception as e:
            return f"Translation failed: {str(e)}"

    def summarize_text(self, text: str, max_sentences: int = 3) -> str:
        """Summarize text to specified number of sentences"""
        try:
            prompt = f"Summarize the following text in {max_sentences} sentences: {text}"
            return self.generate_text(prompt)
        except Exception as e:
            return f"Summarization failed: {str(e)}"

    def get_available_models(self) -> List[str]:
        """Get list of available AI models"""
        models = []
        if self.gemini_client:
            models.append("gemini")
        if self.openai_client:
            models.append("openai")
        return models


# Global AI client instance
ai_client = AIClient()
