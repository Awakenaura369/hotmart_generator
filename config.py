"""
Configuration file for Hotmart Social Media Generator
Customize these settings to match your preferences
"""

# Groq API Settings
GROQ_MODEL = "llama-3.3-70b-versatile"  # Options: llama-3.3-70b-versatile, mixtral-8x7b-32768, etc.
GROQ_TEMPERATURE = 0.8  # Range: 0.0 (conservative) to 1.0 (creative)
GROQ_MAX_TOKENS = 1500

# Platform Settings
PLATFORMS = {
    'facebook': {
        'enabled': True,
        'max_length': 2000,
        'style': 'friendly and engaging, use emojis',
        'format': 'short paragraphs with strong call-to-action'
    },
    'instagram': {
        'enabled': True,
        'max_length': 2200,
        'style': 'visual and inspiring, use emojis and hashtags',
        'format': 'short paragraphs + 10-15 relevant hashtags'
    },
    'twitter': {
        'enabled': True,
        'max_length': 280,
        'style': 'concise and impactful',
        'format': 'brief message with 2-3 hashtags'
    },
    'linkedin': {
        'enabled': True,
        'max_length': 3000,
        'style': 'professional and educational',
        'format': 'long-form post with clear benefit points'
    },
    'tiktok': {
        'enabled': True,
        'max_length': 2200,
        'style': 'energetic and trendy',
        'format': 'video script with strong hook and call-to-action'
    }
}

# Language Settings
DEFAULT_LANGUAGE = 'en'
SUPPORTED_LANGUAGES = ['en', 'ar', 'es', 'pt', 'fr']

# Extraction Settings
REQUEST_TIMEOUT = 10  # seconds
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# Output Settings
AUTO_SAVE = False  # Automatically save to JSON after generation
OUTPUT_DIRECTORY = 'outputs'
JSON_INDENT = 2

# Streamlit Settings
STREAMLIT_THEME = 'light'  # Options: light, dark
PAGE_TITLE = 'Hotmart Social Media Generator'
PAGE_ICON = '🚀'

# Custom Instructions (Optional)
CUSTOM_SYSTEM_PROMPT = """
You are an expert social media marketing content creator, 
specialized in writing engaging and effective posts.
"""

# Additional features you can add:
# - Custom emoji sets per platform
# - Specific hashtag strategies
# - Brand voice guidelines
# - Industry-specific templates
