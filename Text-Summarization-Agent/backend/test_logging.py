"""
Test script to verify the logging system is working correctly
Run this script to generate sample log entries
"""

from logger_config import logger, access_logger
import time

def test_logging():
    """Test all logging levels and features"""
    
    print("\n" + "="*60)
    print("Testing Logging System")
    print("="*60 + "\n")
    
    # Test different log levels
    logger.debug("This is a DEBUG message - detailed diagnostic info")
    time.sleep(0.5)
    
    logger.info("This is an INFO message - general information")
    time.sleep(0.5)
    
    logger.warning("This is a WARNING message - potential issue detected")
    time.sleep(0.5)
    
    logger.error("This is an ERROR message - something went wrong")
    time.sleep(0.5)
    
    # Test logging with extra context
    logger.info(
        "Request processed successfully",
        extra={
            "request_id": "test-123-456",
            "duration_ms": 234,
            "status_code": 200
        }
    )
    time.sleep(0.5)
    
    # Test error logging with exception
    try:
        # Intentionally cause an error
        result = 1 / 0
    except Exception as e:
        logger.error(
            "Test exception caught",
            exc_info=True,
            extra={
                "request_id": "test-error-789",
                "error_type": type(e).__name__
            }
        )
    
    time.sleep(0.5)
    
    # Test access logger
    access_logger.info(
        "API request completed",
        extra={
            "request_id": "access-test-001",
            "method": "POST",
            "path": "/summarize",
            "status_code": 200,
            "duration_ms": 1234
        }
    )
    
    print("\n" + "="*60)
    print("Logging Test Complete!")
    print("="*60)
    print("\nCheck the following log files:")
    print("  - backend/logs/error.log")
    print("  - backend/logs/info.log")
    print("  - backend/logs/debug.log")
    print("  - backend/logs/access.log")
    print("\nYou should see:")
    print("  ✓ Colored output in this console")
    print("  ✓ JSON-formatted entries in log files")
    print("  ✓ Exception stack trace in error.log")
    print("  ✓ Request context in access.log")
    print("\n")

if __name__ == "__main__":
    test_logging()
