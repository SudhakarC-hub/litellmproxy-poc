"""
Proxy Configuration for ADK Agent

This module provides configuration for connecting to LiteLLM proxy.
All models are managed through the proxy admin UI.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LiteLLM Proxy configuration
LITELLM_PROXY_URL = os.getenv("LITELLM_PROXY_URL", "http://localhost:4000")
LITELLM_MASTER_KEY = os.getenv("LITELLM_MASTER_KEY", "sk-1234")

# Model selection (any model configured in proxy admin UI)
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-flash")


def get_proxy_config():
    """
    Get LiteLLM proxy configuration.
    
    Returns:
        Dictionary with proxy URL, authentication, and selected model
    """
    return {
        "proxy_url": LITELLM_PROXY_URL,
        "api_key": LITELLM_MASTER_KEY,
        "model": MODEL_NAME
    }
