import React from 'react';

const LengthSelector = ({ selectedLength, onChange, disabled = false }) => {
    const options = [
        {
            value: 'short',
            label: 'Short',
            description: '2-3 sentences',
            icon: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                </svg>
            )
        },
        {
            value: 'medium',
            label: 'Medium',
            description: '4-6 sentences',
            icon: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            )
        },
        {
            value: 'detailed',
            label: 'Detailed',
            description: '8-12 sentences',
            icon: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                </svg>
            )
        },
    ];

    return (
        <div className="space-y-2">
            <label className="block text-sm font-semibold text-dark-300">
                Summary Length
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {options.map((option) => (
                    <button
                        key={option.value}
                        type="button"
                        onClick={() => onChange(option.value)}
                        disabled={disabled}
                        className={`
              relative p-4 rounded-xl border-2 transition-all duration-200
              ${selectedLength === option.value
                                ? 'border-primary-500 bg-primary-500/10 shadow-lg shadow-primary-500/20'
                                : 'border-white/10 bg-white/5 hover:bg-white/10 hover:border-white/20'
                            }
              ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer active:scale-95'}
            `}
                        aria-label={`Select ${option.label} summary length`}
                    >
                        <div className="flex items-center space-x-3">
                            <div className={`
                p-2 rounded-lg transition-colors
                ${selectedLength === option.value
                                    ? 'bg-primary-500 text-white'
                                    : 'bg-white/10 text-dark-300'
                                }
              `}>
                                {option.icon}
                            </div>
                            <div className="flex-1 text-left">
                                <div className={`
                  font-semibold transition-colors
                  ${selectedLength === option.value ? 'text-primary-400' : 'text-white'}
                `}>
                                    {option.label}
                                </div>
                                <div className="text-xs text-dark-400 mt-0.5">
                                    {option.description}
                                </div>
                            </div>
                        </div>

                        {/* Selection indicator */}
                        {selectedLength === option.value && (
                            <div className="absolute top-2 right-2">
                                <svg className="w-5 h-5 text-primary-400" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                </svg>
                            </div>
                        )}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default LengthSelector;
