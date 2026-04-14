import React, { useState } from 'react';
import Header from './components/Header';
import TextInput from './components/TextInput';
import LengthSelector from './components/LengthSelector';
import ActionButtons from './components/ActionButtons';
import SummaryOutput from './components/SummaryOutput';
import Notification from './components/Notification';
import { summarizeText } from './services/api';

function App() {
    // State management
    const [inputText, setInputText] = useState('');
    const [summaryLength, setSummaryLength] = useState('medium');
    const [summary, setSummary] = useState('');
    const [stats, setStats] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [notification, setNotification] = useState(null);

    // Constants
    const MIN_LENGTH = 200;
    const MAX_LENGTH = 50000;

    // Validation
    const isValidInput = inputText.length >= MIN_LENGTH && inputText.length <= MAX_LENGTH;
    const canSummarize = isValidInput && !isLoading;
    const canClear = inputText.length > 0 || summary.length > 0;
    const canCopy = summary.length > 0;
    const canRegenerate = summary.length > 0;

    // Show notification helper
    const showNotification = (message, type = 'success') => {
        setNotification({ message, type });
    };

    // Handle text input change
    const handleTextChange = (e) => {
        setInputText(e.target.value);
    };

    // Handle summarize
    const handleSummarize = async () => {
        if (!canSummarize) return;

        setIsLoading(true);
        setSummary('');
        setStats(null);

        try {
            const result = await summarizeText(inputText, summaryLength, false);
            setSummary(result.summary);
            setStats({
                original_length: result.original_length,
                summary_length: result.summary_length,
                compression_ratio: result.compression_ratio,
            });
            showNotification('Summary generated successfully!', 'success');
        } catch (error) {
            showNotification(error.message || 'Failed to generate summary', 'error');
            console.error('Summarization error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Handle regenerate
    const handleRegenerate = async () => {
        if (!canRegenerate || !isValidInput) return;

        setIsLoading(true);

        try {
            const result = await summarizeText(inputText, summaryLength, true);
            setSummary(result.summary);
            setStats({
                original_length: result.original_length,
                summary_length: result.summary_length,
                compression_ratio: result.compression_ratio,
            });
            showNotification('Summary regenerated with variation!', 'success');
        } catch (error) {
            showNotification(error.message || 'Failed to regenerate summary', 'error');
            console.error('Regeneration error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Handle clear
    const handleClear = () => {
        setInputText('');
        setSummary('');
        setStats(null);
        showNotification('Content cleared', 'info');
    };

    // Handle copy to clipboard
    const handleCopy = async () => {
        if (!canCopy) return;

        try {
            await navigator.clipboard.writeText(summary);
            showNotification('Summary copied to clipboard!', 'success');
        } catch (error) {
            showNotification('Failed to copy to clipboard', 'error');
            console.error('Copy error:', error);
        }
    };

    // Handle Enter key for submission (Ctrl+Enter)
    const handleKeyDown = (e) => {
        if (e.ctrlKey && e.key === 'Enter' && canSummarize) {
            handleSummarize();
        }
    };

    return (
        <div className="min-h-screen w-full" onKeyDown={handleKeyDown}>
            {/* Background decorative elements */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl animate-pulse-slow"></div>
                <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-accent-500/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }}></div>
            </div>

            {/* Main content */}
            <div className="relative z-10">
                <Header />

                <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
                    {/* Input Section */}
                    <section className="glass-card p-6 sm:p-8 space-y-6">
                        <div className="flex items-center justify-between">
                            <h2 className="text-xl font-display font-semibold text-white">
                                Input Text
                            </h2>
                            <span className="text-sm text-dark-400 hidden sm:block">
                                Tip: Press <kbd className="px-2 py-1 bg-white/10 rounded text-xs">Ctrl</kbd> + <kbd className="px-2 py-1 bg-white/10 rounded text-xs">Enter</kbd> to summarize
                            </span>
                        </div>

                        <TextInput
                            value={inputText}
                            onChange={handleTextChange}
                            placeholder="Paste your text here (minimum 200 characters)..."
                            minLength={MIN_LENGTH}
                            maxLength={MAX_LENGTH}
                            disabled={isLoading}
                        />

                        <LengthSelector
                            selectedLength={summaryLength}
                            onChange={setSummaryLength}
                            disabled={isLoading}
                        />

                        <ActionButtons
                            onSummarize={handleSummarize}
                            onClear={handleClear}
                            onCopy={handleCopy}
                            onRegenerate={handleRegenerate}
                            canSummarize={canSummarize}
                            canClear={canClear}
                            canCopy={canCopy}
                            canRegenerate={canRegenerate}
                            isLoading={isLoading}
                        />
                    </section>

                    {/* Output Section */}
                    <section>
                        <h2 className="text-xl font-display font-semibold text-white mb-4">
                            Summary Output
                        </h2>
                        <SummaryOutput
                            summary={summary}
                            stats={stats}
                            isLoading={isLoading}
                        />
                    </section>

                    {/* Footer */}
                    <footer className="text-center py-8 text-dark-400 text-sm">
                        <p>
                            Powered by{' '}
                            <span className="gradient-text font-semibold">Gemini 2.5 Flash</span>
                            {' '}• Built with React & Tailwind CSS
                        </p>
                    </footer>
                </main>
            </div>

            {/* Notification */}
            {notification && (
                <Notification
                    message={notification.message}
                    type={notification.type}
                    onClose={() => setNotification(null)}
                />
            )}
        </div>
    );
}

export default App;
