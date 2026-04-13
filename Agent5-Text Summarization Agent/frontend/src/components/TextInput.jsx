import React from 'react';

const TextInput = ({
    value,
    onChange,
    placeholder,
    minLength = 200,
    maxLength = 50000,
    disabled = false
}) => {
    const charCount = value.length;
    const isValid = charCount >= minLength && charCount <= maxLength;
    const percentage = (charCount / maxLength) * 100;

    return (
        <div className="w-full space-y-3">
            <div className="relative">
                <textarea
                    id="text-input"
                    value={value}
                    onChange={onChange}
                    placeholder={placeholder}
                    disabled={disabled}
                    className="input-field min-h-[300px] sm:min-h-[400px] w-full"
                    aria-label="Text input for summarization"
                />

                {/* Character counter overlay */}
                <div className="absolute bottom-4 right-4 glass-card px-3 py-1.5">
                    <span className={`text-sm font-semibold ${charCount < minLength
                            ? 'text-yellow-400'
                            : charCount > maxLength
                                ? 'text-red-400'
                                : 'text-green-400'
                        }`}>
                        {charCount.toLocaleString()} / {maxLength.toLocaleString()}
                    </span>
                </div>
            </div>

            {/* Progress bar */}
            <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                <div
                    className={`h-full transition-all duration-300 ${charCount < minLength
                            ? 'bg-yellow-400'
                            : charCount > maxLength
                                ? 'bg-red-400'
                                : 'bg-gradient-to-r from-primary-500 to-accent-500'
                        }`}
                    style={{ width: `${Math.min(percentage, 100)}%` }}
                />
            </div>

            {/* Validation message */}
            {charCount > 0 && (
                <div className="flex items-center space-x-2">
                    {charCount < minLength ? (
                        <>
                            <svg className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                            </svg>
                            <span className="text-sm text-yellow-400">
                                Minimum {minLength} characters required ({minLength - charCount} more needed)
                            </span>
                        </>
                    ) : charCount > maxLength ? (
                        <>
                            <svg className="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                            </svg>
                            <span className="text-sm text-red-400">
                                Maximum {maxLength.toLocaleString()} characters exceeded ({charCount - maxLength} over limit)
                            </span>
                        </>
                    ) : (
                        <>
                            <svg className="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            <span className="text-sm text-green-400">
                                Ready to summarize
                            </span>
                        </>
                    )}
                </div>
            )}
        </div>
    );
};

export default TextInput;
