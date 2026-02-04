import axios from 'axios'

const API_BASE = import.meta.env.DEV ? '' : 'http://localhost:8000'

const api = axios.create({
    baseURL: API_BASE,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// Request interceptor for auth
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => Promise.reject(error)
)

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

// Upload APIs
export const uploadDocument = async (file, options = {}) => {
    const formData = new FormData()
    formData.append('file', file)
    if (options.businessId) formData.append('business_id', options.businessId)
    if (options.statementType) formData.append('statement_type', options.statementType)

    return api.post('/api/upload/document', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    })
}

export const validateData = async (data) => {
    return api.post('/api/upload/validate', data)
}

// Analysis APIs
export const runFullAnalysis = async (financialData, industry = 'services', language = 'en') => {
    return api.post('/api/analysis/full', {
        financial_data: financialData,
        industry,
        language
    })
}

export const calculateMetrics = async (financialData, industry = 'services') => {
    return api.post('/api/analysis/metrics', {
        financial_data: financialData,
        industry
    })
}

export const assessRisk = async (financialData, metrics = null) => {
    return api.post('/api/analysis/risk', {
        financial_data: financialData,
        metrics
    })
}

export const getCreditScore = async (financialData, businessInfo = null) => {
    return api.post('/api/analysis/credit-score', {
        financial_data: financialData,
        business_info: businessInfo
    })
}

export const generateForecast = async (financialData, periods = 12) => {
    return api.post('/api/analysis/forecast', {
        financial_data: financialData,
        periods
    })
}

export const benchmarkAnalysis = async (metrics, industry = 'services') => {
    return api.post('/api/analysis/benchmark', {
        metrics,
        industry
    })
}

// Reports APIs
export const generateReport = async (business, analysis, reportType = 'full', language = 'en') => {
    return api.post('/api/reports/generate', {
        business,
        analysis,
        report_type: reportType,
        language
    })
}

export const downloadReport = async (filename) => {
    return api.get(`/api/reports/download/${filename}`, {
        responseType: 'blob'
    })
}

// Integration APIs
export const verifyGSTIN = async (gstin) => {
    return api.get(`/api/integrations/gst/verify/${gstin}`)
}

export const getGSTCompliance = async (gstin) => {
    return api.get(`/api/integrations/gst/compliance/${gstin}`)
}

export const getLoanProducts = async (businessProfile) => {
    return api.post('/api/integrations/bank/loan-products', businessProfile)
}

export const getProductRecommendations = async (creditScore, financialNeeds, industry) => {
    return api.post('/api/integrations/bank/product-recommendations', {
        credit_score: creditScore,
        financial_needs: financialNeeds,
        industry
    })
}

// Config APIs
export const getTranslations = async (language = 'en') => {
    return api.get(`/api/translations/${language}`)
}

export const getConfig = async () => {
    return api.get('/api/config')
}

export const healthCheck = async () => {
    return api.get('/api/health')
}

export default api
