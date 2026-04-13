import axios from 'axios';
import { logApiError, logPerformance } from './errorLogger';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000, // 30 seconds
});

// Request interceptor for logging
api.interceptors.request.use(
    (config) => {
        // Add timestamp to track request duration
        config.metadata = { startTime: new Date() };
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('Request interceptor error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor for logging
api.interceptors.response.use(
    (response) => {
        // Calculate request duration
        const duration = new Date() - response.config.metadata.startTime;
        console.log(`API Response: ${response.config.url} - ${response.status} (${duration}ms)`);

        // Log slow requests
        logPerformance(
            `API ${response.config.method?.toUpperCase()} ${response.config.url}`,
            duration,
            { status: response.status }
        );

        return response;
    },
    (error) => {
        // Calculate request duration even for errors
        const duration = error.config?.metadata?.startTime
            ? new Date() - error.config.metadata.startTime
            : 0;

        console.error(`API Error: ${error.config?.url} (${duration}ms)`, error);

        // Log API error with details
        logApiError(error, {
            url: error.config?.url,
            method: error.config?.method,
            status: error.response?.status,
            duration,
            requestData: error.config?.data,
            responseData: error.response?.data
        });

        return Promise.reject(error);
    }
);

/**
 * Summarize text using the backend API
 * @param {string} text - The text to summarize
 * @param {string} length - Summary length: 'short', 'medium', or 'detailed'
 * @param {boolean} regenerate - Whether this is a regeneration request
 * @returns {Promise} API response with summary data
 */
export const summarizeText = async (text, length = 'medium', regenerate = false) => {
    try {
        const response = await api.post('/summarize', {
            text,
            length,
            regenerate,
        });
        return response.data;
    } catch (error) {
        let errorMessage = 'An unexpected error occurred';

        if (error.response) {
            // Server responded with error
            errorMessage = error.response.data.detail || 'Failed to generate summary';
            console.error('Server error:', error.response.status, error.response.data);
        } else if (error.request) {
            // Request made but no response
            errorMessage = 'Unable to connect to the server. Please ensure the backend is running.';
            console.error('No response received:', error.request);
        } else {
            // Something else happened
            console.error('Request setup error:', error.message);
        }

        throw new Error(errorMessage);
    }
};

/**
 * Check API health status
 * @returns {Promise} Health check response
 */
export const checkHealth = async () => {
    try {
        const response = await api.get('/health');
        return response.data;
    } catch (error) {
        console.error('Health check failed:', error);
        throw new Error('Backend service is unavailable');
    }
};

export default api;
