import React from 'react';

const SummaryOutput = ({ summary, stats, isLoading }) => {
    if (isLoading) {
        return (
            <div className="glass-card p-8 space-y-4 animate-slide-up">
                <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
                    <span className="text-lg font-semibold text-dark-200">Generating your summary...</span>
                </div>

                {/* Loading skeleton */}
                <div className="space-y-3">
                    <div className="h-4 bg-white/10 rounded loading-shimmer"></div>
                    <div className="h-4 bg-white/10 rounded loading-shimmer" style={{ width: '90%' }}></div>
                    <div className="h-4 bg-white/10 rounded loading-shimmer" style={{ width: '95%' }}></div>
                    <div className="h-4 bg-white/10 rounded loading-shimmer" style={{ width: '85%' }}></div>
                </div>
            </div>
        );
    }

    if (!summary) {
        return (
            <div className="glass-card p-8 text-center space-y-4">
                <div className="w-16 h-16 mx-auto bg-gradient-to-br from-primary-500/20 to-accent-500/20 rounded-2xl flex items-center justify-center">
                    <svg className="w-8 h-8 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                </div>
                <div>
                    <h3 className="text-xl font-semibold text-dark-200 mb-2">No Summary Yet</h3>
                    <p className="text-dark-400">
                        Enter your text above and click "Summarize" to generate an AI-powered summary.
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-4 animate-slide-up">
            {/* Summary content */}
            <div className="glass-card p-6 sm:p-8">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold gradient-text flex items-center space-x-2">
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        <span>AI-Generated Summary</span>
                    </h3>
                </div>

                <div className="prose prose-invert max-w-none">
                    <p className="text-dark-100 leading-relaxed whitespace-pre-wrap">
                        {summary}
                    </p>
                </div>
            </div>

            {/* Statistics */}
            {stats && (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div className="glass-card p-4">
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-primary-500/20 rounded-lg flex items-center justify-center">
                                <svg className="w-5 h-5 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                            </div>
                            <div>
                                <div className="text-xs text-dark-400 font-medium">Original</div>
                                <div className="text-lg font-bold text-white">{stats.original_length?.toLocaleString()}</div>
                            </div>
                        </div>
                    </div>

                    <div className="glass-card p-4">
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-accent-500/20 rounded-lg flex items-center justify-center">
                                <svg className="w-5 h-5 text-accent-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
                                </svg>
                            </div>
                            <div>
                                <div className="text-xs text-dark-400 font-medium">Summary</div>
                                <div className="text-lg font-bold text-white">{stats.summary_length?.toLocaleString()}</div>
                            </div>
                        </div>
                    </div>

                    <div className="glass-card p-4">
                        <div className="flex items-center space-x-3">
                            <div className="w-10 h-10 bg-green-500/20 rounded-lg flex items-center justify-center">
                                <svg className="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                </svg>
                            </div>
                            <div>
                                <div className="text-xs text-dark-400 font-medium">Compression</div>
                                <div className="text-lg font-bold text-white">{stats.compression_ratio}%</div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default SummaryOutput;
