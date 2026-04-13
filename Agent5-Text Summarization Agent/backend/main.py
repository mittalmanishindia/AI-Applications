from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Literal, Optional, Dict, Any
import time
import uuid
from datetime import datetime
from google.api_core.exceptions import ResourceExhausted

# Import logging configuration
from logger_config import logger, access_logger

# Load environment variables
load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.critical("GEMINI_API_KEY not found in environment variables")
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)
logger.info("Gemini API configured successfully")

# Initialize FastAPI app
app = FastAPI(title="AI Text Summarization Agent", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses with timing"""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Log incoming request
    logger.info(
        f"Incoming request: {request.method} {request.url.path}",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )
    
    # Process request
    try:
        response = await call_next(request)
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log successful response
        access_logger.info(
            f"Request completed: {request.method} {request.url.path} - Status: {response.status_code}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "client_ip": request.client.host if request.client else "unknown"
            }
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        return response
        
    except Exception as e:
        duration_ms = int((time.time() - start_time) * 1000)
        
        # Log error
        logger.error(
            f"Request failed: {request.method} {request.url.path} - Error: {str(e)}",
            exc_info=True,
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": duration_ms,
                "client_ip": request.client.host if request.client else "unknown"
            }
        )
        raise

# Request/Response models
class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=200, max_length=50000)
    length: Literal["short", "medium", "detailed"] = "medium"
    regenerate: bool = False

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float

# Prompt templates for different summary lengths
PROMPT_TEMPLATES = {
    "short": "Provide a brief, concise summary of the following text in 2-3 sentences. Focus on the main points only:\n\n{text}",
    "medium": "Summarize the following text in a clear and comprehensive manner. Include key points and important details in 4-6 sentences:\n\n{text}",
    "detailed": "Provide a detailed and thorough summary of the following text. Include all important points, key details, and context. Aim for 8-12 sentences:\n\n{text}"
}

@app.get("/")
async def root():
    logger.debug("Root endpoint accessed")
    return {
        "message": "AI Text Summarization Agent API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    health_status = {"status": "healthy", "gemini_configured": bool(GEMINI_API_KEY)}
    logger.debug(f"Health check performed: {health_status}")
    return health_status

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    start_time = time.time()
    
    logger.info(
        f"Summarization request received - Length: {request.length}, Regenerate: {request.regenerate}, Text length: {len(request.text)} chars"
    )
    
    try:
        # Select prompt template based on length
        prompt = PROMPT_TEMPLATES[request.length].format(text=request.text)
        
        logger.debug(f"Using prompt template: {request.length}")
        
        # Configure temperature based on regenerate flag
        # Higher temperature for regeneration to get variation
        temperature = 0.9 if request.regenerate else 0.7
        
        logger.debug(f"Temperature set to: {temperature}")
        
        # Initialize Gemini model
        # Default to gemini-2.0-flash as requested by user, allow override via env
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        model = genai.GenerativeModel(model_name)
        
        logger.info(f"Using Gemini model: {model_name}")
        
        logger.info("Calling Gemini API for summarization...")
        api_start = time.time()
        
        # Generate summary
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=1024,
            )
        )
        
        api_duration = int((time.time() - api_start) * 1000)
        logger.info(f"Gemini API call completed in {api_duration}ms")
        
        summary = response.text.strip()
        
        # Calculate metrics
        original_length = len(request.text)
        summary_length = len(summary)
        compression_ratio = round((1 - summary_length / original_length) * 100, 2)
        
        total_duration = int((time.time() - start_time) * 1000)
        
        logger.info(
            f"Summarization successful - Original: {original_length} chars, "
            f"Summary: {summary_length} chars, Compression: {compression_ratio}%, "
            f"Total time: {total_duration}ms"
        )
        
        return SummarizeResponse(
            summary=summary,
            original_length=original_length,
            summary_length=summary_length,
            compression_ratio=compression_ratio
        )
        
    except ValueError as e:
        # Validation errors
        logger.warning(f"Validation error in summarization: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )

    except ResourceExhausted as e:
        # Handle quota exceeded/rate limit errors
        duration = int((time.time() - start_time) * 1000)
        logger.warning(
            f"Quota exceeded after {duration}ms - Error: {str(e)}",
            extra={
                "text_length": len(request.text),
                "summary_length": request.length,
                "duration_ms": duration,
                "error_type": "ResourceExhausted"
            }
        )
        raise HTTPException(
            status_code=429,
            detail="Service quota exceeded. Please try again later."
        )
    
    except Exception as e:
        # Log detailed error information
        duration = int((time.time() - start_time) * 1000)
        
        logger.error(
            f"Summarization failed after {duration}ms - Error: {str(e)}",
            exc_info=True,
            extra={
                "text_length": len(request.text),
                "summary_length": request.length,
                "regenerate": request.regenerate,
                "duration_ms": duration,
                "error_type": type(e).__name__
            }
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )

# Frontend error logging model
class FrontendError(BaseModel):
    message: str
    stack: Optional[str] = None
    componentStack: Optional[str] = None
    url: str
    userAgent: str
    timestamp: str
    severity: Literal["error", "warning", "info"] = "error"
    context: Optional[Dict[str, Any]] = None


@app.post("/log-error")
async def log_frontend_error(error: FrontendError):
    """Endpoint to receive and log frontend errors"""
    try:
        log_message = f"Frontend Error: {error.message} | URL: {error.url}"
        
        extra_data = {
            "source": "frontend",
            "url": error.url,
            "user_agent": error.userAgent,
            "timestamp": error.timestamp,
            "severity": error.severity
        }
        
        if error.context:
            extra_data["context"] = error.context
        
        # Log based on severity
        if error.severity == "error":
            logger.error(
                log_message,
                extra=extra_data
            )
            if error.stack:
                logger.error(f"Stack trace: {error.stack}")
            if error.componentStack:
                logger.error(f"Component stack: {error.componentStack}")
        elif error.severity == "warning":
            logger.warning(log_message, extra=extra_data)
        else:
            logger.info(log_message, extra=extra_data)
        
        return {"status": "logged", "message": "Error logged successfully"}
        
    except Exception as e:
        logger.error(f"Failed to log frontend error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to log error"
        )


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Text Summarization Agent server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
