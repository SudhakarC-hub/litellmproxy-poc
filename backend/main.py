"""
FastAPI Backend for PDF Summarizer Agent

This module provides the REST API endpoints for uploading PDFs and generating summaries
using the Google ADK agent with Ollama.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv

from backend.pdf_extractor import PDFExtractor
from agent.agent import get_pdf_summary

# Load environment variables
load_dotenv()

# Configuration
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

# Initialize FastAPI app
app = FastAPI(
    title="PDF Summarizer Agent API",
    description="API for uploading PDFs and generating summaries using Google ADK with Ollama",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummaryResponse(BaseModel):
    """Response model for PDF summary"""
    summary: str
    page_count: int
    file_name: str


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PDF Summarizer Agent API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "pdf-summarizer-agent"
    }


@app.post("/upload", response_model=SummaryResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file and generate a summary.
    
    Args:
        file: PDF file to process
        
    Returns:
        SummaryResponse with the generated summary
        
    Raises:
        HTTPException: For various error conditions
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    # Read file content
    content = await file.read()
    file_size = len(content)
    
    # Validate file size
    if file_size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE_MB}MB"
        )
    
    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )
    
    # Create temporary file to store the PDF
    temp_file = None
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Extract text from PDF
        try:
            pdf_text = PDFExtractor.extract_text(temp_file_path)
            page_count = PDFExtractor.get_page_count(temp_file_path)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
        
        # Generate summary using ADK agent
        try:
            summary = await get_pdf_summary(pdf_text)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating summary: {str(e)}"
            )
        
        return SummaryResponse(
            summary=summary,
            page_count=page_count,
            file_name=file.filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=BACKEND_HOST,
        port=BACKEND_PORT,
        reload=True
    )
