"""
Multilingual translations for the platform.
Supports English and Hindi with extensible structure.
"""

TRANSLATIONS = {
    'en': {
        # General
        'app_name': 'Financial Health Assessment Platform',
        'welcome': 'Welcome',
        'dashboard': 'Dashboard',
        'upload': 'Upload Documents',
        'analysis': 'Financial Analysis',
        'reports': 'Reports',
        'settings': 'Settings',
        
        # Health Score
        'health_score': 'Financial Health Score',
        'overall_score': 'Overall Score',
        'excellent': 'Excellent',
        'good': 'Good',
        'fair': 'Fair',
        'needs_attention': 'Needs Attention',
        'critical': 'Critical',
        
        # Metrics
        'liquidity': 'Liquidity',
        'profitability': 'Profitability',
        'solvency': 'Solvency',
        'efficiency': 'Efficiency',
        'current_ratio': 'Current Ratio',
        'quick_ratio': 'Quick Ratio',
        'gross_margin': 'Gross Profit Margin',
        'net_margin': 'Net Profit Margin',
        'debt_to_equity': 'Debt to Equity Ratio',
        'roe': 'Return on Equity',
        'roa': 'Return on Assets',
        
        # Risk
        'risk_assessment': 'Risk Assessment',
        'risk_level': 'Risk Level',
        'low_risk': 'Low Risk',
        'medium_risk': 'Medium Risk',
        'high_risk': 'High Risk',
        'critical_risk': 'Critical Risk',
        
        # Recommendations
        'recommendations': 'Recommendations',
        'action_items': 'Action Items',
        'priority': 'Priority',
        'high_priority': 'High Priority',
        'medium_priority': 'Medium Priority',
        'low_priority': 'Low Priority',
        
        # Reports
        'generate_report': 'Generate Report',
        'download_pdf': 'Download PDF',
        'investor_report': 'Investor Report',
        'quick_summary': 'Quick Summary',
        
        # Business
        'business_name': 'Business Name',
        'industry': 'Industry',
        'gstin': 'GSTIN',
        'annual_turnover': 'Annual Turnover',
        
        # Actions
        'save': 'Save',
        'cancel': 'Cancel',
        'submit': 'Submit',
        'analyze': 'Analyze',
        'export': 'Export',
        
        # Messages
        'loading': 'Loading...',
        'success': 'Success',
        'error': 'Error',
        'no_data': 'No data available',
    },
    
    'hi': {
        # General
        'app_name': 'वित्तीय स्वास्थ्य मूल्यांकन मंच',
        'welcome': 'स्वागत है',
        'dashboard': 'डैशबोर्ड',
        'upload': 'दस्तावेज़ अपलोड करें',
        'analysis': 'वित्तीय विश्लेषण',
        'reports': 'रिपोर्ट',
        'settings': 'सेटिंग्स',
        
        # Health Score
        'health_score': 'वित्तीय स्वास्थ्य स्कोर',
        'overall_score': 'कुल स्कोर',
        'excellent': 'उत्कृष्ट',
        'good': 'अच्छा',
        'fair': 'ठीक',
        'needs_attention': 'ध्यान देने की आवश्यकता',
        'critical': 'गंभीर',
        
        # Metrics
        'liquidity': 'तरलता',
        'profitability': 'लाभप्रदता',
        'solvency': 'शोधन क्षमता',
        'efficiency': 'दक्षता',
        'current_ratio': 'चालू अनुपात',
        'quick_ratio': 'त्वरित अनुपात',
        'gross_margin': 'सकल लाभ मार्जिन',
        'net_margin': 'शुद्ध लाभ मार्जिन',
        'debt_to_equity': 'ऋण से इक्विटी अनुपात',
        'roe': 'इक्विटी पर प्रतिफल',
        'roa': 'संपत्ति पर प्रतिफल',
        
        # Risk
        'risk_assessment': 'जोखिम मूल्यांकन',
        'risk_level': 'जोखिम स्तर',
        'low_risk': 'कम जोखिम',
        'medium_risk': 'मध्यम जोखिम',
        'high_risk': 'उच्च जोखिम',
        'critical_risk': 'गंभीर जोखिम',
        
        # Recommendations
        'recommendations': 'सिफारिशें',
        'action_items': 'कार्य बिंदु',
        'priority': 'प्राथमिकता',
        'high_priority': 'उच्च प्राथमिकता',
        'medium_priority': 'मध्यम प्राथमिकता',
        'low_priority': 'कम प्राथमिकता',
        
        # Reports
        'generate_report': 'रिपोर्ट बनाएं',
        'download_pdf': 'PDF डाउनलोड करें',
        'investor_report': 'निवेशक रिपोर्ट',
        'quick_summary': 'त्वरित सारांश',
        
        # Business
        'business_name': 'व्यवसाय का नाम',
        'industry': 'उद्योग',
        'gstin': 'जीएसटीआईएन',
        'annual_turnover': 'वार्षिक कारोबार',
        
        # Actions
        'save': 'सहेजें',
        'cancel': 'रद्द करें',
        'submit': 'जमा करें',
        'analyze': 'विश्लेषण करें',
        'export': 'निर्यात करें',
        
        # Messages
        'loading': 'लोड हो रहा है...',
        'success': 'सफल',
        'error': 'त्रुटि',
        'no_data': 'कोई डेटा उपलब्ध नहीं',
    }
}


def get_translation(key: str, language: str = 'en') -> str:
    """Get translation for a key."""
    lang_dict = TRANSLATIONS.get(language, TRANSLATIONS['en'])
    return lang_dict.get(key, TRANSLATIONS['en'].get(key, key))


def get_all_translations(language: str = 'en') -> dict:
    """Get all translations for a language."""
    return TRANSLATIONS.get(language, TRANSLATIONS['en'])
