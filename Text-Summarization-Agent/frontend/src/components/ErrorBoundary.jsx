import React from 'react';
import { logError } from '../services/errorLogger';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
            errorInfo: null
        };
    }

    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        // Log error to backend
        logError({
            message: error.toString(),
            stack: error.stack,
            componentStack: errorInfo.componentStack,
            severity: 'error',
            context: {
                component: 'ErrorBoundary',
                errorName: error.name
            }
        });

        // Update state with error details
        this.setState({
            error: error,
            errorInfo: errorInfo
        });

        // Also log to console for development
        console.error('Error caught by boundary:', error, errorInfo);
    }

    handleReset = () => {
        this.setState({
            hasError: false,
            error: null,
            errorInfo: null
        });
        // Reload the page to reset the app
        window.location.reload();
    };

    render() {
        if (this.state.hasError) {
            // Fallback UI
            return (
                <div className="min-h-screen w-full flex items-center justify-center bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900 p-4">
                    <div className="glass-card p-8 max-w-2xl w-full space-y-6">
                        {/* Error Icon */}
                        <div className="flex justify-center">
                            <div className="w-20 h-20 rounded-full bg-red-500/20 flex items-center justify-center">
                                <svg
                                    className="w-10 h-10 text-red-500"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                                    />
                                </svg>
                            </div>
                        </div>

                        {/* Error Title */}
                        <div className="text-center">
                            <h1 className="text-2xl font-display font-bold text-white mb-2">
                                Oops! Something went wrong
                            </h1>
                            <p className="text-dark-400">
                                We've encountered an unexpected error. The error has been logged and we'll look into it.
                            </p>
                        </div>

                        {/* Error Details (Development) */}
                        {process.env.NODE_ENV === 'development' && this.state.error && (
                            <div className="space-y-3">
                                <details className="bg-white/5 rounded-lg p-4">
                                    <summary className="text-sm font-semibold text-white cursor-pointer hover:text-primary-400 transition-colors">
                                        Error Details
                                    </summary>
                                    <div className="mt-3 space-y-2">
                                        <div>
                                            <p className="text-xs text-dark-400 mb-1">Error Message:</p>
                                            <p className="text-sm text-red-400 font-mono">
                                                {this.state.error.toString()}
                                            </p>
                                        </div>
                                        {this.state.error.stack && (
                                            <div>
                                                <p className="text-xs text-dark-400 mb-1">Stack Trace:</p>
                                                <pre className="text-xs text-dark-300 font-mono overflow-x-auto bg-black/30 p-3 rounded">
                                                    {this.state.error.stack}
                                                </pre>
                                            </div>
                                        )}
                                        {this.state.errorInfo?.componentStack && (
                                            <div>
                                                <p className="text-xs text-dark-400 mb-1">Component Stack:</p>
                                                <pre className="text-xs text-dark-300 font-mono overflow-x-auto bg-black/30 p-3 rounded">
                                                    {this.state.errorInfo.componentStack}
                                                </pre>
                                            </div>
                                        )}
                                    </div>
                                </details>
                            </div>
                        )}

                        {/* Actions */}
                        <div className="flex gap-4 justify-center">
                            <button
                                onClick={this.handleReset}
                                className="btn-primary px-6 py-3"
                            >
                                <svg
                                    className="w-5 h-5 mr-2"
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                                    />
                                </svg>
                                Reload Application
                            </button>
                            <button
                                onClick={() => window.history.back()}
                                className="btn-secondary px-6 py-3"
                            >
                                Go Back
                            </button>
                        </div>

                        {/* Help Text */}
                        <div className="text-center text-sm text-dark-400">
                            <p>
                                If this problem persists, please contact support with the error details above.
                            </p>
                        </div>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
