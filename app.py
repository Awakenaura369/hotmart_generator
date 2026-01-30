#!/usr/bin/env python3
"""
Hotmart Social Media Posts Generator
Generates social media posts from Hotmart product links using Groq AI
"""

import os
import json
import re
from groq import Groq
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class HotmartSocialMediaGenerator:
    def __init__(self, groq_api_key):
        """Initialize the generator with Groq API key"""
        self.client = Groq(api_key=groq_api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def extract_product_info(self, url):
        """Extract product information from Hotmart page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_info = {
                'url': url,
                'title': '',
                'description': '',
                'price': '',
                'benefits': []
            }
            
            # Try to extract title
            title_selectors = [
                'h1',
                'meta[property="og:title"]',
                'title'
            ]
            for selector in title_selectors:
                if selector.startswith('meta'):
                    tag = soup.select_one(selector)
                    if tag and tag.get('content'):
                        product_info['title'] = tag['content']
                        break
                else:
                    tag = soup.select_one(selector)
                    if tag:
                        product_info['title'] = tag.get_text(strip=True)
                        break
            
            # Try to extract description
            desc_selectors = [
                'meta[property="og:description"]',
                'meta[name="description"]',
                '.description',
                '.product-description'
            ]
            for selector in desc_selectors:
                if selector.startswith('meta'):
                    tag = soup.select_one(selector)
                    if tag and tag.get('content'):
                        product_info['description'] = tag['content']
                        break
                else:
                    tag = soup.select_one(selector)
                    if tag:
                        product_info['description'] = tag.get_text(strip=True)
                        break
            
            # Try to extract price
            price_patterns = [
                r'R\$\s*[\d,.]+',
                r'\$\s*[\d,.]+',
                r'USD\s*[\d,.]+',
                r'EUR\s*[\d,.]+',
            ]
            page_text = soup.get_text()
            for pattern in price_patterns:
                match = re.search(pattern, page_text)
                if match:
                    product_info['price'] = match.group()
                    break
            
            return product_info
            
        except Exception as e:
            return {
                'url': url,
                'title': 'Hotmart Product',
                'description': '',
                'price': '',
                'benefits': []
            }
    
    def generate_post(self, product_info, platform, language='en'):
        """Generate a post for a specific platform"""
        
        platform_specs = {
            'facebook': {
                'max_length': 2000,
                'style': 'friendly and engaging, use emojis',
                'format': 'short paragraphs with strong call-to-action'
            },
            'instagram': {
                'max_length': 2200,
                'style': 'visual and inspiring, use emojis and hashtags',
                'format': 'short paragraphs + 10-15 relevant hashtags'
            },
            'twitter': {
                'max_length': 280,
                'style': 'concise and impactful',
                'format': 'brief message with 2-3 hashtags'
            },
            'linkedin': {
                'max_length': 3000,
                'style': 'professional and educational',
                'format': 'long-form post with clear benefit points'
            },
            'tiktok': {
                'max_length': 2200,
                'style': 'energetic and trendy',
                'format': 'video script with strong hook and call-to-action'
            }
        }
        
        spec = platform_specs.get(platform.lower(), platform_specs['facebook'])
        
        language_instructions = {
            'en': 'Write in English',
            'ar': 'Write in Arabic (Modern Standard Arabic or Moroccan Darija if appropriate)',
            'es': 'Write in Spanish',
            'pt': 'Write in Portuguese',
            'fr': 'Write in French'
        }
        
        lang_instruction = language_instructions.get(language, 'Write in English')
        
        prompt = f"""You are an expert in digital marketing and social media content creation.

Product Information:
- Title: {product_info['title']}
- Description: {product_info['description']}
- Price: {product_info['price']}
- URL: {product_info['url']}

Create a professional marketing post for {platform} with these specifications:
- Maximum length: {spec['max_length']} characters
- Style: {spec['style']}
- Format: {spec['format']}

The post must:
1. Grab attention from the first line
2. Highlight key benefits
3. Include a clear call-to-action
4. {lang_instruction}
5. Use emojis strategically

Write ONLY the post without any preambles or additional explanations."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert social media marketing content creator, specialized in writing engaging and effective posts."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.8,
                max_tokens=1500,
            )
            
            return chat_completion.choices[0].message.content.strip()
        
        except Exception as e:
            return f"Error generating post: {e}"
    
    def generate_all_posts(self, hotmart_url, language='en', product_info_override=None):
        """Generate posts for all platforms"""
        
        if product_info_override:
            product_info = product_info_override
        else:
            product_info = self.extract_product_info(hotmart_url)
        
        platforms = ['facebook', 'instagram', 'twitter', 'linkedin', 'tiktok']
        posts = {}
        
        for platform in platforms:
            post = self.generate_post(product_info, platform, language)
            posts[platform] = post
        
        return posts, product_info


def main():
    """Main program for CLI usage"""
    print("=" * 60)
    print("🚀 Hotmart Social Media Posts Generator")
    print("=" * 60)
    print()
    
    groq_api_key = os.environ.get('GROQ_API_KEY')
    
    if not groq_api_key:
        groq_api_key = input("🔑 Enter your Groq API key: ").strip()
        
        if not groq_api_key:
            print("❌ Please provide a valid API key")
            return
    
    generator = HotmartSocialMediaGenerator(groq_api_key)
    
    hotmart_url = input("\n🔗 Enter Hotmart product URL: ").strip()
    
    if not hotmart_url:
        print("❌ Please provide a valid URL")
        return
    
    language = input("\n🌍 Language (en/ar/es/pt/fr) [default: en]: ").strip() or 'en'
    
    print("\n" + "=" * 60)
    print("🔍 Extracting product information...")
    
    posts, product_info = generator.generate_all_posts(hotmart_url, language)
    
    print(f"✅ Product: {product_info['title']}\n")
    
    print("=" * 60)
    print("📱 Generated Posts:")
    print("=" * 60)
    
    for platform, post in posts.items():
        print(f"\n{'='*60}")
        print(f"📌 {platform.upper()}")
        print(f"{'='*60}")
        print(post)
        print()
    
    save = input("\n💾 Save results to JSON file? (y/n): ").strip().lower()
    
    if save == 'y':
        output = {
            'product_info': product_info,
            'posts': posts,
            'language': language
        }
        
        filename = f"hotmart_posts_{product_info['title'][:30].replace(' ', '_')}.json"
        filename = re.sub(r'[^\w\s-]', '', filename)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Saved to: {filename}")
    
    print("\n🎉 Done!")


if __name__ == "__main__":
    main()
