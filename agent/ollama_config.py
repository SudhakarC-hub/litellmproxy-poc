"""
Ollama Configuration for ADK Agent

This module provides configuration and utilities for connecting to Ollama.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral")


def get_ollama_config():
    """
    Get Ollama configuration.
    
    Returns:
        Dictionary with Ollama configuration
    """
    return {
        "base_url": OLLAMA_BASE_URL,
        "model": MODEL_NAME
    }


def get_model_endpoint():
    """
    Get the full Ollama model endpoint.
    
    Returns:
        Full endpoint URL for Ollama
    """
    return f"{OLLAMA_BASE_URL}/v1"
