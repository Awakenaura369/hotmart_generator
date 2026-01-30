import streamlit as st
import json
from datetime import datetime
from hotmart_generator import HotmartSocialMediaGenerator
import os

# Page configuration
st.set_page_config(
    page_title="Hotmart Social Media Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .platform-header {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
    }
    .stButton>button:hover {
        background-color: #764ba2;
    }
    .product-info-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 20px 0;
    }
    .post-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_posts' not in st.session_state:
    st.session_state.generated_posts = None
if 'product_info' not in st.session_state:
    st.session_state.product_info = None
if 'generation_complete' not in st.session_state:
    st.session_state.generation_complete = False

# Main header
st.markdown('<h1 class="main-header">🚀 Hotmart Social Media Generator</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Generate professional social media posts for your Hotmart products using AI</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key input
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=os.environ.get('GROQ_API_KEY', ''),
        help="Get your free API key from console.groq.com"
    )
    
    st.markdown("---")
    
    # Language selection
    language = st.selectbox(
        "🌍 Content Language",
        options=['en', 'ar', 'es', 'pt', 'fr'],
        format_func=lambda x: {
            'en': '🇬🇧 English',
            'ar': '🇸🇦 Arabic',
            'es': '🇪🇸 Spanish',
            'pt': '🇧🇷 Portuguese',
            'fr': '🇫🇷 French'
        }[x],
        index=0
    )
    
    st.markdown("---")
    
    # Platform selection
    st.subheader("📱 Platforms")
    platforms = {
        'Facebook': st.checkbox('Facebook', value=True),
        'Instagram': st.checkbox('Instagram', value=True),
        'Twitter': st.checkbox('Twitter', value=True),
        'LinkedIn': st.checkbox('LinkedIn', value=True),
        'TikTok': st.checkbox('TikTok', value=True)
    }
    
    st.markdown("---")
    
    # Info section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Hotmart Social Media Generator** uses AI to create 
        engaging social media posts for your products.
        
        **Features:**
        - 5 social media platforms
        - Multi-language support
        - Automatic product info extraction
        - Professional copywriting
        - Easy export to JSON
        
        **How to use:**
        1. Enter your Groq API key
        2. Paste your Hotmart product URL
        3. Click Generate
        4. Copy and use your posts!
        """)

# Main content area
tab1, tab2 = st.tabs(["🎯 Generate Posts", "📚 Manual Input"])

with tab1:
    st.subheader("Generate from Hotmart URL")
    
    hotmart_url = st.text_input(
        "Hotmart Product URL",
        placeholder="https://hotmart.com/product/your-product",
        help="Paste the full URL of your Hotmart product page"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        generate_button = st.button("🚀 Generate Posts", type="primary", use_container_width=True)
    
    if generate_button:
        if not groq_api_key:
            st.error("❌ Please enter your Groq API key in the sidebar")
        elif not hotmart_url:
            st.error("❌ Please enter a Hotmart product URL")
        else:
            try:
                with st.spinner("🔍 Extracting product information..."):
                    generator = HotmartSocialMediaGenerator(groq_api_key)
                    product_info = generator.extract_product_info(hotmart_url)
                
                if not product_info['title']:
                    st.warning("⚠️ Could not extract product information automatically. Please use the Manual Input tab.")
                else:
                    st.success(f"✅ Found product: {product_info['title']}")
                    
                    # Display product info
                    with st.container():
                        st.markdown('<div class="product-info-box">', unsafe_allow_html=True)
                        st.markdown("### 📦 Product Information")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Title:** {product_info['title']}")
                            st.write(f"**Price:** {product_info['price'] or 'Not found'}")
                        with col2:
                            st.write(f"**URL:** {product_info['url']}")
                        if product_info['description']:
                            st.write(f"**Description:** {product_info['description'][:200]}...")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Generate posts
                    selected_platforms = [p.lower() for p, selected in platforms.items() if selected]
                    
                    if not selected_platforms:
                        st.warning("⚠️ Please select at least one platform in the sidebar")
                    else:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        posts = {}
                        total_platforms = len(selected_platforms)
                        
                        for idx, platform in enumerate(selected_platforms):
                            status_text.text(f"✍️ Generating {platform.upper()} post... ({idx+1}/{total_platforms})")
                            post = generator.generate_post(product_info, platform, language)
                            posts[platform] = post
                            progress_bar.progress((idx + 1) / total_platforms)
                        
                        status_text.text("✅ All posts generated successfully!")
                        
                        st.session_state.generated_posts = posts
                        st.session_state.product_info = product_info
                        st.session_state.generation_complete = True
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.subheader("Manual Product Information Entry")
    
    with st.form("manual_input_form"):
        manual_title = st.text_input("Product Title *", placeholder="Enter product title")
        manual_description = st.text_area("Product Description", placeholder="Enter product description")
        manual_price = st.text_input("Price", placeholder="e.g., $97 or R$ 197")
        manual_url = st.text_input("Product URL", placeholder="https://hotmart.com/product/...")
        
        submit_manual = st.form_submit_button("🚀 Generate Posts", type="primary", use_container_width=True)
        
        if submit_manual:
            if not groq_api_key:
                st.error("❌ Please enter your Groq API key in the sidebar")
            elif not manual_title:
                st.error("❌ Product title is required")
            else:
                try:
                    product_info = {
                        'title': manual_title,
                        'description': manual_description,
                        'price': manual_price,
                        'url': manual_url or '',
                        'benefits': []
                    }
                    
                    generator = HotmartSocialMediaGenerator(groq_api_key)
                    
                    selected_platforms = [p.lower() for p, selected in platforms.items() if selected]
                    
                    if not selected_platforms:
                        st.warning("⚠️ Please select at least one platform in the sidebar")
                    else:
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        posts = {}
                        total_platforms = len(selected_platforms)
                        
                        for idx, platform in enumerate(selected_platforms):
                            status_text.text(f"✍️ Generating {platform.upper()} post... ({idx+1}/{total_platforms})")
                            post = generator.generate_post(product_info, platform, language)
                            posts[platform] = post
                            progress_bar.progress((idx + 1) / total_platforms)
                        
                        status_text.text("✅ All posts generated successfully!")
                        
                        st.session_state.generated_posts = posts
                        st.session_state.product_info = product_info
                        st.session_state.generation_complete = True
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Display generated posts
if st.session_state.generation_complete and st.session_state.generated_posts:
    st.markdown("---")
    st.markdown("## 📱 Generated Posts")
    
    # Platform emojis
    platform_emojis = {
        'facebook': '📘',
        'instagram': '📸',
        'twitter': '🐦',
        'linkedin': '💼',
        'tiktok': '🎵'
    }
    
    for platform, post in st.session_state.generated_posts.items():
        with st.expander(f"{platform_emojis.get(platform, '📱')} {platform.upper()}", expanded=True):
            st.markdown('<div class="post-container">', unsafe_allow_html=True)
            st.text_area(
                f"{platform}_post",
                value=post,
                height=200,
                label_visibility="collapsed",
                key=f"textarea_{platform}"
            )
            
            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"📋 Copy", key=f"copy_{platform}"):
                    st.success("Copied to clipboard! (Use Ctrl+C)")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Export section
    st.markdown("---")
    st.subheader("💾 Export")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        export_data = {
            'product_info': st.session_state.product_info,
            'posts': st.session_state.generated_posts,
            'language': language,
            'generated_at': datetime.now().isoformat()
        }
        
        json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
        
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"hotmart_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            type="primary",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #666;">Made with ❤️ using Groq AI | '
    '<a href="https://console.groq.com" target="_blank">Get API Key</a></p>',
    unsafe_allow_html=True
)
