import React from 'react';

const Header = () => {
    return (
        <header className="w-full py-6 px-4 sm:px-6 lg:px-8 animate-fade-in">
            <div className="max-w-7xl mx-auto">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                        <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/30 animate-gradient">
                            <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                        </div>
                        <div>
                            <h1 className="text-2xl sm:text-3xl font-display font-bold gradient-text text-shadow">
                                AI Text Summarizer
                            </h1>
                            <p className="text-xs sm:text-sm text-dark-400 font-medium">
                                Powered by Gemini 2.5 Flash
                            </p>
                        </div>
                    </div>

                    <div className="hidden sm:flex items-center space-x-2 glass-card px-4 py-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        <span className="text-sm text-dark-300 font-medium">Active</span>
                    </div>
                </div>
            </div>
        </header>
    );
};

export default Header;
