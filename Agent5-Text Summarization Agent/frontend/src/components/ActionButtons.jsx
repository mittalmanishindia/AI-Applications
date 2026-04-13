import React from 'react';

const ActionButtons = ({
    onSummarize,
    onClear,
    onCopy,
    onRegenerate,
    canSummarize,
    canClear,
    canCopy,
    canRegenerate,
    isLoading
}) => {
    return (
        <div className="flex flex-wrap gap-3">
            {/* Summarize Button */}
            <button
                onClick={onSummarize}
                disabled={!canSummarize || isLoading}
                className="btn-primary flex items-center space-x-2 flex-1 sm:flex-initial justify-center"
                aria-label="Generate summary"
            >
                {isLoading ? (
                    <>
                        <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <span>Generating...</span>
                    </>
                ) : (
                    <>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                        </svg>
                        <span>Summarize</span>
                    </>
                )}
            </button>

            {/* Clear Button */}
            <button
                onClick={onClear}
                disabled={!canClear || isLoading}
                className="btn-secondary flex items-center space-x-2"
                aria-label="Clear input"
            >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                <span>Clear</span>
            </button>

            {/* Regenerate Button */}
            {canRegenerate && (
                <button
                    onClick={onRegenerate}
                    disabled={isLoading}
                    className="btn-secondary flex items-center space-x-2"
                    aria-label="Regenerate summary"
                >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                    <span>Regenerate</span>
                </button>
            )}

            {/* Copy Button */}
            {canCopy && (
                <button
                    onClick={onCopy}
                    disabled={isLoading}
                    className="btn-secondary flex items-center space-x-2"
                    aria-label="Copy summary to clipboard"
                >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    <span>Copy</span>
                </button>
            )}
        </div>
    );
};

export default ActionButtons;
