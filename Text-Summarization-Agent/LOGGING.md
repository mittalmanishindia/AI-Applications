# Error Logging System Documentation

## Overview

The AI Text Summarization Agent includes a comprehensive error logging system that captures errors from both the backend (FastAPI) and frontend (React) applications. All errors are logged to structured files for easy debugging and monitoring.

---

## Backend Logging (Python/FastAPI)

### Log Files Location

All backend logs are stored in: `backend/logs/`

| Log File | Purpose | Level | Rotation |
|----------|---------|-------|----------|
| `error.log` | Critical errors and exceptions | ERROR | 10 MB, 5 backups |
| `info.log` | General application info | INFO | 10 MB, 5 backups |
| `debug.log` | Detailed debugging information | DEBUG | 10 MB, 3 backups |
| `access.log` | API request/response logs | INFO | 20 MB, 10 backups |

### Log Format

Logs are stored in **JSON format** for easy parsing and analysis:

```json
{
  "timestamp": "2025-12-09T12:09:51.123456",
  "level": "ERROR",
  "logger": "summarization_agent",
  "message": "Summarization failed after 1234ms - Error: API timeout",
  "module": "main",
  "function": "summarize_text",
  "line": 145,
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "duration_ms": 1234,
  "error_type": "TimeoutError",
  "exception": "Traceback (most recent call last)..."
}
```

### What Gets Logged

#### 1. **Request/Response Logging**
- All incoming HTTP requests
- Response status codes
- Request duration (in milliseconds)
- Client IP addresses
- Request IDs for tracing

#### 2. **Summarization Operations**
- Input text length
- Summary length preference
- Gemini API call duration
- Compression ratio achieved
- Success/failure status

#### 3. **Errors**
- Full exception stack traces
- Error type and message
- Request context (what was being processed)
- Duration before failure
- Input parameters

#### 4. **Application Events**
- Server startup
- Configuration loading
- API key validation
- Health check requests

### Console Output

The backend also outputs **colored logs** to the console for real-time monitoring:

- 🔵 **DEBUG** - Cyan
- 🟢 **INFO** - Green
- 🟡 **WARNING** - Yellow
- 🔴 **ERROR** - Red
- 🟣 **CRITICAL** - Magenta

---

## Frontend Logging (React)

### Error Logging Service

The frontend includes a comprehensive error logging service (`errorLogger.js`) that sends errors to the backend for centralized logging.

### What Gets Logged

#### 1. **React Component Errors**
- Caught by Error Boundary
- Component stack traces
- Props and state context
- Automatically sent to backend

#### 2. **API Errors**
- Request/response details
- HTTP status codes
- Request duration
- Failed endpoints
- Request payload

#### 3. **Global JavaScript Errors**
- Unhandled exceptions
- Unhandled promise rejections
- Script errors
- Runtime errors

#### 4. **Performance Issues**
- Operations taking > 3 seconds
- Slow API calls
- Rendering performance

### Error Severity Levels

- **error**: Critical errors requiring attention
- **warning**: Non-critical issues
- **info**: Informational messages

### Error Context

Each frontend error includes:
- Error message and stack trace
- Current URL
- User agent (browser info)
- Viewport dimensions
- Screen resolution
- Timestamp
- Custom context data

---

## Error Boundary

The application includes a React Error Boundary that:

1. **Catches React errors** during rendering, lifecycle methods, and constructors
2. **Displays user-friendly error UI** instead of crashing
3. **Logs errors automatically** to the backend
4. **Provides recovery options** (reload, go back)
5. **Shows error details** in development mode

### Error UI Features

- Clean, branded error page
- Error details (development only)
- Reload application button
- Go back button
- Support contact information

---

## Global Error Handlers

The application sets up global error handlers for:

### 1. Unhandled Promise Rejections
```javascript
window.addEventListener('unhandledrejection', ...)
```
Catches async errors that weren't properly handled.

### 2. Global JavaScript Errors
```javascript
window.addEventListener('error', ...)
```
Catches runtime errors not caught by try-catch blocks.

---

## API Interceptors

### Request Interceptor
- Logs all outgoing API requests
- Adds timestamp for duration tracking
- Logs request method and URL

### Response Interceptor
- Logs successful responses with duration
- Tracks slow API calls (> 3s)
- Logs failed requests with full context

---

## Using the Logging System

### Backend (Python)

```python
from logger_config import logger

# Info logging
logger.info("Operation completed successfully")

# Error logging with context
logger.error(
    "Failed to process request",
    exc_info=True,  # Include stack trace
    extra={
        "request_id": request_id,
        "user_id": user_id,
        "duration_ms": duration
    }
)

# Warning
logger.warning("Slow operation detected")

# Debug
logger.debug("Processing step 1 of 5")
```

### Frontend (JavaScript)

```javascript
import { logError, logWarning, logInfo, logApiError } from './services/errorLogger';

// Log error
logError({
    message: 'Failed to load data',
    stack: error.stack,
    severity: 'error',
    context: {
        component: 'DataLoader',
        userId: currentUser.id
    }
});

// Log warning
logWarning('Slow network detected', { latency: 5000 });

// Log API error
logApiError(error, {
    endpoint: '/summarize',
    method: 'POST',
    payload: requestData
});
```

---

## Monitoring and Analysis

### Viewing Logs

1. **Real-time Console Logs**
   - Backend: Check terminal running FastAPI
   - Frontend: Check browser console (F12)

2. **Log Files**
   - Navigate to `backend/logs/`
   - Open `.log` files with any text editor
   - Use JSON parsers for structured analysis

### Analyzing Logs

#### Using `jq` (JSON processor)
```bash
# View all errors
cat backend/logs/error.log | jq 'select(.level=="ERROR")'

# Find slow requests
cat backend/logs/access.log | jq 'select(.duration_ms > 3000)'

# Filter by request ID
cat backend/logs/info.log | jq 'select(.request_id=="abc-123")'
```

#### Using Python
```python
import json

with open('backend/logs/error.log', 'r') as f:
    for line in f:
        log = json.loads(line)
        if log['level'] == 'ERROR':
            print(f"{log['timestamp']}: {log['message']}")
```

### Common Debugging Scenarios

#### 1. **Tracking a Specific Request**
- Find the `request_id` from the error
- Search all log files for that request ID
- Follow the request lifecycle

#### 2. **Finding Performance Issues**
- Check `access.log` for high `duration_ms` values
- Look for patterns in slow requests
- Identify bottlenecks

#### 3. **Debugging Frontend Errors**
- Check browser console first
- Look at `error.log` for backend-logged frontend errors
- Review component stack traces

#### 4. **API Integration Issues**
- Check `access.log` for failed requests
- Review request/response payloads
- Verify API endpoint availability

---

## Log Rotation

Logs automatically rotate when they reach size limits:

- **Error logs**: 10 MB, keeps 5 backups
- **Info logs**: 10 MB, keeps 5 backups
- **Debug logs**: 10 MB, keeps 3 backups
- **Access logs**: 20 MB, keeps 10 backups

Old logs are renamed with `.1`, `.2`, etc. suffixes.

---

## Best Practices

### 1. **Don't Log Sensitive Data**
- Never log API keys, passwords, or tokens
- Sanitize user input before logging
- Be careful with personal information

### 2. **Use Appropriate Log Levels**
- **DEBUG**: Detailed diagnostic info
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error events that might still allow the app to continue
- **CRITICAL**: Serious errors causing the application to abort

### 3. **Include Context**
- Add relevant context to error logs
- Include request IDs for tracing
- Log user actions leading to errors

### 4. **Monitor Regularly**
- Check error logs daily
- Set up alerts for critical errors
- Review performance metrics weekly

### 5. **Clean Up Old Logs**
- Archive old logs periodically
- Keep only necessary backups
- Consider log aggregation tools for production

---

## Production Considerations

For production deployment, consider:

1. **Log Aggregation Services**
   - Sentry for error tracking
   - LogRocket for session replay
   - ELK Stack (Elasticsearch, Logstash, Kibana)
   - Datadog, New Relic, or similar

2. **Alerting**
   - Set up alerts for error rate spikes
   - Monitor API response times
   - Track application health metrics

3. **Privacy Compliance**
   - Ensure logs comply with GDPR/privacy laws
   - Implement log retention policies
   - Anonymize user data in logs

4. **Performance**
   - Consider async logging for high-traffic apps
   - Use log sampling for very high volumes
   - Optimize log storage and rotation

---

## Troubleshooting

### Logs Not Being Created

1. Check write permissions on `backend/logs/` directory
2. Verify logger is imported correctly
3. Check for errors in `logger_config.py`

### Logs Too Large

1. Reduce log level (e.g., INFO instead of DEBUG)
2. Decrease rotation size limits
3. Reduce backup count
4. Implement log sampling

### Missing Frontend Errors

1. Verify Error Boundary is wrapping App
2. Check global error handlers are initialized
3. Ensure backend `/log-error` endpoint is accessible
4. Check browser console for error logging failures

---

## Summary

The logging system provides:

✅ **Comprehensive Coverage**: Backend + Frontend  
✅ **Structured Logging**: JSON format for easy parsing  
✅ **Automatic Rotation**: Prevents disk space issues  
✅ **Request Tracing**: Track requests across the stack  
✅ **Performance Monitoring**: Identify slow operations  
✅ **Error Context**: Full stack traces and context  
✅ **User-Friendly**: Error Boundary for graceful failures  
✅ **Production-Ready**: Scalable and maintainable  

For questions or issues, refer to the code comments in:
- `backend/logger_config.py`
- `frontend/src/services/errorLogger.js`
- `frontend/src/components/ErrorBoundary.jsx`
