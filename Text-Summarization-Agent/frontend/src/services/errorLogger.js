/**
 * Error logging service for frontend
 * Sends errors to backend for centralized logging
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Log error to backend
 * @param {Object} errorData - Error information
 * @param {string} errorData.message - Error message
 * @param {string} [errorData.stack] - Stack trace
 * @param {string} [errorData.componentStack] - React component stack
 * @param {string} [errorData.severity='error'] - Error severity (error, warning, info)
 * @param {Object} [errorData.context] - Additional context
 */
export async function logError({
    message,
    stack = null,
    componentStack = null,
    severity = 'error',
    context = {}
}) {
    try {
        const errorPayload = {
            message,
            stack,
            componentStack,
            url: window.location.href,
            userAgent: navigator.userAgent,
            timestamp: new Date().toISOString(),
            severity,
            context: {
                ...context,
                viewport: {
                    width: window.innerWidth,
                    height: window.innerHeight
                },
                screen: {
                    width: window.screen.width,
                    height: window.screen.height
                }
            }
        };

        // Send to backend
        const response = await fetch(`${API_BASE_URL}/log-error`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(errorPayload),
        });

        if (!response.ok) {
            console.error('Failed to log error to backend:', response.statusText);
        }
    } catch (err) {
        // Fallback: log to console if backend logging fails
        console.error('Error logging service failed:', err);
        console.error('Original error:', message, stack);
    }
}

/**
 * Log warning to backend
 * @param {string} message - Warning message
 * @param {Object} [context] - Additional context
 */
export function logWarning(message, context = {}) {
    return logError({
        message,
        severity: 'warning',
        context
    });
}

/**
 * Log info to backend
 * @param {string} message - Info message
 * @param {Object} [context] - Additional context
 */
export function logInfo(message, context = {}) {
    return logError({
        message,
        severity: 'info',
        context
    });
}

/**
 * Setup global error handlers
 */
export function setupGlobalErrorHandlers() {
    // Handle unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled promise rejection:', event.reason);

        logError({
            message: `Unhandled Promise Rejection: ${event.reason?.message || event.reason}`,
            stack: event.reason?.stack,
            severity: 'error',
            context: {
                type: 'unhandledRejection',
                promise: event.promise
            }
        });
    });

    // Handle global errors
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);

        // Don't log errors from browser extensions or external scripts
        if (event.filename && !event.filename.includes(window.location.origin)) {
            return;
        }

        logError({
            message: event.message || 'Unknown error',
            stack: event.error?.stack,
            severity: 'error',
            context: {
                type: 'globalError',
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno
            }
        });
    });

    console.log('Global error handlers initialized');
}

/**
 * Log API errors with request/response details
 * @param {Error} error - Error object
 * @param {Object} requestDetails - Request details
 */
export function logApiError(error, requestDetails = {}) {
    return logError({
        message: `API Error: ${error.message}`,
        stack: error.stack,
        severity: 'error',
        context: {
            type: 'apiError',
            ...requestDetails,
            errorName: error.name
        }
    });
}

/**
 * Log performance issues
 * @param {string} operation - Operation name
 * @param {number} duration - Duration in milliseconds
 * @param {Object} [context] - Additional context
 */
export function logPerformance(operation, duration, context = {}) {
    if (duration > 3000) { // Log if operation takes more than 3 seconds
        return logWarning(`Slow operation: ${operation} took ${duration}ms`, {
            type: 'performance',
            operation,
            duration,
            ...context
        });
    }
}
