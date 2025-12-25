"""
PDF Summarizer Agent using Google ADK

This module implements an ADK agent that generates summaries of PDF documents
using a locally hosted Ollama LLM (Mistral model) via Google ADK framework.
"""

import os
from google.adk.agents import Agent
from google.adk.models import LiteLlm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "mistral")
OLLAMA_API_BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


def summarize_pdf_text(pdf_text: str) -> str:
    """
    Tool function to summarize PDF text.
    
    Args:
        pdf_text: The extracted text from the PDF document
        
    Returns:
        A comprehensive summary of the PDF content
    """
    # This function will be called by the agent
    # The actual summarization is handled by the LLM
    return pdf_text


# Create the PDF Summarizer Agent using Google ADK
pdf_summarizer_agent = Agent(
    model=LiteLlm(model=f"ollama_chat/{MODEL_NAME}"),
    name="pdf_summarizer_agent",
    description=(
        "An expert document summarizer that analyzes PDF documents and generates "
        "comprehensive, well-structured summaries highlighting key points, findings, "
        "and conclusions."
    ),
    instruction="""
You are an expert document summarizer with deep analytical skills. Your task is to:

1. Carefully read and analyze the provided PDF document text
2. Identify the main themes, key points, and important details
3. Create a comprehensive yet concise summary that captures:
   - The document's primary purpose and main arguments
   - Key findings, data, or evidence presented
   - Important conclusions or recommendations
   - Any significant implications or takeaways

4. Structure your summary clearly with:
   - An opening statement about the document's topic
   - Well-organized paragraphs covering main points
   - A concluding statement if applicable

5. Keep the summary between 100-200 words depending on the document's length and complexity
6. Use clear, professional language that is accessible to a general audience
7. Maintain objectivity and accuracy - don't add information not present in the original text

Provide your summary directly without any preamble or meta-commentary.
""",
    tools=[summarize_pdf_text]
)


async def get_pdf_summary(pdf_text: str) -> str:
    """
    Generate a summary of PDF text using the ADK agent with Ollama.
    
    This function uses ONLY Google ADK framework - no fallback.
    If ADK fails, it will raise an exception to help debug ADK issues.
    
    Args:
        pdf_text: Extracted text from the PDF
        
    Returns:
        Generated summary as a string
        
    Raises:
        Exception: If summary generation fails (for debugging ADK)
    """
    import uuid
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google import genai
    from google.genai import types
    
    # Create the prompt for summarization
    prompt_text = f"""Please summarize the following PDF document:

{pdf_text}

Provide a comprehensive summary following the guidelines in your instructions."""

    try:
        # Create session service (required by ADK Runner)
        session_service = InMemorySessionService()
        
        # Generate unique session ID for this request
        user_id = "pdf_user"
        session_id = f"pdf_session_{uuid.uuid4().hex[:8]}"
        app_name = "pdf_summarizer"
        
        # Create the session first (app_name is required)
        # Note: create_session is async, so we need to await it
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id
        )
        
        # Use Google ADK Runner to execute the agent
        # When providing an agent, we must also provide app_name
        runner = Runner(
            app_name=app_name,
            agent=pdf_summarizer_agent,
            session_service=session_service
        )
        
        # Create the message in ADK Content format
        new_message = types.Content(
            role='user',
            parts=[types.Part(text=prompt_text)]
        )
        
        # Run the agent with proper parameters (using async version)
        # user_id and session_id are required for session management
        response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            # Check for agent response events
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts'):
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
        
        if response_text.strip():
            return response_text.strip()
        
        # If no response collected, raise error
        raise Exception(
            f"ADK did not generate any response. "
            f"Check if Ollama is running and the model is available."
        )
        
    except Exception as e:
        # Re-raise with more context for debugging ADK issues
        raise Exception(
            f"Google ADK failed to generate summary. "
            f"Error: {str(e)}. "
            f"This helps identify ADK configuration or integration issues."
        )
