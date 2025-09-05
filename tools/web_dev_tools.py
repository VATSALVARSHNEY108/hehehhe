import streamlit as st
import re
import json
import requests
import html
from urllib.parse import urlparse, urljoin
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all web development tools"""

    tool_categories = {
        "HTML Tools": [
            "HTML Validator", "HTML Minifier", "HTML Beautifier", "Tag Analyzer", "Meta Tag Generator"
        ],
        "JavaScript Tools": [
            "JS Validator", "JS Minifier", "JS Beautifier", "Console Logger", "Function Analyzer"
        ],
        "Performance Tools": [
            "Speed Test", "Bundle Analyzer", "Image Optimizer", "Cache Analyzer", "Loading Simulator"
        ],
        "Responsive Design": [
            "Viewport Tester", "Media Query Generator", "Breakpoint Analyzer", "Mobile Simulator"
        ],
        "Accessibility Tools": [
            "A11y Checker", "ARIA Validator", "Color Contrast", "Screen Reader Test", "Keyboard Navigation"
        ],
        "SEO Tools": [
            "Meta Tag Checker", "Sitemap Generator", "Robots.txt Validator", "Schema Markup", "OpenGraph Generator"
        ],
        "API Tools": [
            "REST API Tester", "JSON Formatter", "API Documentation", "Request Builder", "Response Analyzer"
        ],
        "Code Generators": [
            "Lorem Ipsum", "Placeholder Images", "Dummy Data", "Color Palettes", "Icon Sets"
        ],
        "Development Utilities": [
            "URL Encoder/Decoder", "Base64 Converter", "Timestamp Converter", "Hash Generator", "UUID Generator"
        ],
        "Testing Tools": [
            "Form Validator", "Link Checker", "Cross-Browser Test", "Performance Monitor", "Error Logger"
        ]
    }

    selected_category = st.selectbox("Select Web Dev Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Web Dev Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "HTML Validator":
        html_validator()
    elif selected_tool == "JS Validator":
        js_validator()
    elif selected_tool == "JSON Formatter":
        json_formatter()
    elif selected_tool == "Meta Tag Generator":
        meta_tag_generator()
    elif selected_tool == "URL Encoder/Decoder":
        url_encoder_decoder()
    elif selected_tool == "Sitemap Generator":
        sitemap_generator()
    elif selected_tool == "REST API Tester":
        api_tester()
    elif selected_tool == "Performance Monitor":
        performance_monitor()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def html_validator():
    """Validate HTML code"""
    create_tool_header("HTML Validator", "Validate your HTML code for errors and best practices", "🏷️")

    uploaded_file = FileHandler.upload_files(['html', 'htm'], accept_multiple=False)

    if uploaded_file:
        html_code = FileHandler.process_text_file(uploaded_file[0])
        st.code(html_code, language='html')
    else:
        html_code = st.text_area("Enter HTML code:", height=200,
                                 placeholder="<html>\n  <head>\n    <title>My Page</title>\n  </head>\n  <body>\n    <h1>Hello World!</h1>\n  </body>\n</html>")

    if html_code and st.button("Validate HTML"):
        errors = validate_html(html_code)

        if not errors:
            st.success("✅ Valid HTML! No errors found.")
        else:
            st.error(f"❌ Found {len(errors)} errors:")
            for i, error in enumerate(errors, 1):
                st.write(f"{i}. {error}")


def validate_html(html_code):
    """Basic HTML validation"""
    errors = []

    # Check for basic structure
    if not re.search(r'<!DOCTYPE\s+html>', html_code, re.IGNORECASE):
        errors.append("Missing DOCTYPE declaration")

    if not re.search(r'<html[^>]*>', html_code, re.IGNORECASE):
        errors.append("Missing <html> tag")

    if not re.search(r'<head[^>]*>', html_code, re.IGNORECASE):
        errors.append("Missing <head> tag")

    if not re.search(r'<body[^>]*>', html_code, re.IGNORECASE):
        errors.append("Missing <body> tag")

    # Check for unclosed tags
    tags = re.findall(r'<(\w+)[^>]*>', html_code)
    closing_tags = re.findall(r'</(\w+)>', html_code)

    self_closing = {'img', 'br', 'hr', 'input', 'meta', 'link'}

    for tag in tags:
        if tag.lower() not in self_closing and tag.lower() not in [t.lower() for t in closing_tags]:
            errors.append(f"Unclosed tag: <{tag}>")

    return errors


def js_validator():
    """Validate JavaScript code"""
    create_tool_header("JavaScript Validator", "Check your JavaScript code for syntax errors", "⚡")

    uploaded_file = FileHandler.upload_files(['js'], accept_multiple=False)

    if uploaded_file:
        js_code = FileHandler.process_text_file(uploaded_file[0])
        st.code(js_code, language='javascript')
    else:
        js_code = st.text_area("Enter JavaScript code:", height=200,
                               placeholder="function greet(name) {\n  console.log('Hello, ' + name + '!');\n}")

    if js_code and st.button("Validate JavaScript"):
        errors = validate_javascript(js_code)

        if not errors:
            st.success("✅ Valid JavaScript! No obvious syntax errors found.")
        else:
            st.warning(f"⚠️ Found {len(errors)} potential issues:")
            for i, error in enumerate(errors, 1):
                st.write(f"{i}. {error}")


def validate_javascript(js_code):
    """Basic JavaScript validation"""
    errors = []

    # Check for common syntax issues
    if js_code.count('(') != js_code.count(')'):
        errors.append("Mismatched parentheses")

    if js_code.count('{') != js_code.count('}'):
        errors.append("Mismatched braces")

    if js_code.count('[') != js_code.count(']'):
        errors.append("Mismatched brackets")

    # Check for semicolons at end of statements
    lines = js_code.split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line and not line.endswith((';', '{', '}', ')', ']')) and not line.startswith(
                ('if', 'for', 'while', 'function', '//')):
            errors.append(f"Line {i}: Missing semicolon")

    return errors


def json_formatter():
    """Format and validate JSON"""
    create_tool_header("JSON Formatter", "Format, validate, and beautify JSON data", "📄")

    uploaded_file = FileHandler.upload_files(['json'], accept_multiple=False)

    if uploaded_file:
        json_text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded JSON:", json_text, height=150, disabled=True)
    else:
        json_text = st.text_area("Enter JSON data:", height=200,
                                 placeholder='{"name": "John", "age": 30, "city": "New York"}')

    if json_text:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Format JSON"):
                try:
                    parsed = json.loads(json_text)
                    formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
                    st.code(formatted, language='json')
                    st.success("✅ Valid JSON!")
                    FileHandler.create_download_link(formatted.encode(), "formatted.json", "application/json")
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON: {str(e)}")

        with col2:
            if st.button("Minify JSON"):
                try:
                    parsed = json.loads(json_text)
                    minified = json.dumps(parsed, separators=(',', ':'))
                    st.code(minified, language='json')
                    st.success("✅ JSON minified!")
                    FileHandler.create_download_link(minified.encode(), "minified.json", "application/json")
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON: {str(e)}")


def meta_tag_generator():
    """Generate meta tags for HTML"""
    create_tool_header("Meta Tag Generator", "Generate HTML meta tags for SEO and social media", "🏷️")

    title = st.text_input("Page Title:", placeholder="My Awesome Website")
    description = st.text_area("Description:", placeholder="A comprehensive description of your website", height=100)
    keywords = st.text_input("Keywords (comma-separated):", placeholder="web, development, tools")
    author = st.text_input("Author:", placeholder="Your Name")

    st.markdown("### Social Media")
    og_title = st.text_input("Open Graph Title:", value=title)
    og_description = st.text_area("Open Graph Description:", value=description, height=80)
    og_image = st.text_input("Open Graph Image URL:", placeholder="https://example.com/image.jpg")

    if st.button("Generate Meta Tags"):
        meta_tags = generate_meta_tags(title, description, keywords, author, og_title, og_description, og_image)

        st.markdown("### Generated Meta Tags")
        st.code(meta_tags, language='html')
        FileHandler.create_download_link(meta_tags.encode(), "meta_tags.html", "text/html")


def generate_meta_tags(title, description, keywords, author, og_title, og_description, og_image):
    """Generate HTML meta tags"""
    tags = []

    if title:
        tags.append(f'<title>{html.escape(title)}</title>')
        tags.append(f'<meta name="title" content="{html.escape(title)}">')

    if description:
        tags.append(f'<meta name="description" content="{html.escape(description)}">')

    if keywords:
        tags.append(f'<meta name="keywords" content="{html.escape(keywords)}">')

    if author:
        tags.append(f'<meta name="author" content="{html.escape(author)}">')

    # Standard meta tags
    tags.append('<meta charset="UTF-8">')
    tags.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')

    # Open Graph tags
    if og_title:
        tags.append(f'<meta property="og:title" content="{html.escape(og_title)}">')

    if og_description:
        tags.append(f'<meta property="og:description" content="{html.escape(og_description)}">')

    if og_image:
        tags.append(f'<meta property="og:image" content="{html.escape(og_image)}">')

    tags.append('<meta property="og:type" content="website">')

    # Twitter Card tags
    tags.append('<meta name="twitter:card" content="summary_large_image">')
    if og_title:
        tags.append(f'<meta name="twitter:title" content="{html.escape(og_title)}">')
    if og_description:
        tags.append(f'<meta name="twitter:description" content="{html.escape(og_description)}">')
    if og_image:
        tags.append(f'<meta name="twitter:image" content="{html.escape(og_image)}">')

    return '\n'.join(tags)


def url_encoder_decoder():
    """Encode and decode URLs"""
    create_tool_header("URL Encoder/Decoder", "Encode and decode URL components", "🔗")

    operation = st.radio("Operation:", ["Encode", "Decode"])

    if operation == "Encode":
        text = st.text_area("Enter text to encode:", placeholder="Hello World! This is a test.")
        if text and st.button("Encode"):
            from urllib.parse import quote
            encoded = quote(text)
            st.code(encoded)
            st.success("Text encoded successfully!")
    else:
        text = st.text_area("Enter URL-encoded text to decode:", placeholder="Hello%20World%21%20This%20is%20a%20test.")
        if text and st.button("Decode"):
            from urllib.parse import unquote
            try:
                decoded = unquote(text)
                st.code(decoded)
                st.success("Text decoded successfully!")
            except Exception as e:
                st.error(f"Error decoding: {str(e)}")


def sitemap_generator():
    """Generate XML sitemap"""
    create_tool_header("Sitemap Generator", "Generate XML sitemap for your website", "🗺️")

    st.info("Enter your website URLs to generate a sitemap:")

    urls = st.text_area("Enter URLs (one per line):", height=200,
                        placeholder="https://example.com/\nhttps://example.com/about\nhttps://example.com/contact")

    if urls and st.button("Generate Sitemap"):
        sitemap = generate_sitemap(urls)
        st.code(sitemap, language='xml')
        FileHandler.create_download_link(sitemap.encode(), "sitemap.xml", "application/xml")


def generate_sitemap(urls_text):
    """Generate XML sitemap from URLs"""
    from datetime import datetime

    urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
    current_date = datetime.now().strftime('%Y-%m-%d')

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in urls:
        sitemap.append('  <url>')
        sitemap.append(f'    <loc>{html.escape(url)}</loc>')
        sitemap.append(f'    <lastmod>{current_date}</lastmod>')
        sitemap.append('    <changefreq>weekly</changefreq>')
        sitemap.append('    <priority>0.8</priority>')
        sitemap.append('  </url>')

    sitemap.append('</urlset>')

    return '\n'.join(sitemap)


def api_tester():
    """Test REST APIs"""
    create_tool_header("REST API Tester", "Test and debug REST API endpoints", "🔌")

    method = st.selectbox("HTTP Method:", ["GET", "POST", "PUT", "DELETE", "PATCH"])
    url = st.text_input("API Endpoint:", placeholder="https://api.example.com/users")

    # Headers
    st.markdown("### Headers")
    headers_text = st.text_area("Headers (JSON format):", height=100,
                                placeholder='{"Content-Type": "application/json", "Authorization": "Bearer token"}')

    # Body (for POST, PUT, PATCH)
    if method in ["POST", "PUT", "PATCH"]:
        st.markdown("### Request Body")
        body = st.text_area("Request Body (JSON):", height=150,
                            placeholder='{"name": "John", "email": "john@example.com"}')
    else:
        body = ""

    if st.button("Send Request"):
        if url:
            response = test_api(method, url, headers_text, body)
            display_api_response(response)
        else:
            st.error("Please enter an API endpoint")


def test_api(method, url, headers_text, body):
    """Test API endpoint"""
    try:
        headers = {}
        if headers_text:
            headers = json.loads(headers_text)

        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=body, timeout=30)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data=body, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, data=body, timeout=30)

        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text,
            'success': True
        }
    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }


def display_api_response(response):
    """Display API response"""
    if response['success']:
        col1, col2 = st.columns(2)

        with col1:
            if response['status_code'] < 300:
                st.success(f"✅ Status: {response['status_code']}")
            elif response['status_code'] < 400:
                st.warning(f"⚠️ Status: {response['status_code']}")
            else:
                st.error(f"❌ Status: {response['status_code']}")

        with col2:
            st.metric("Response Time", "< 30s")

        st.markdown("### Response Headers")
        st.json(response['headers'])

        st.markdown("### Response Body")
        try:
            # Try to format as JSON
            json_response = json.loads(response['content'])
            st.json(json_response)
        except:
            # Display as text if not JSON
            st.code(response['content'])
    else:
        st.error(f"❌ Request failed: {response['error']}")


def performance_monitor():
    """Monitor website performance"""
    create_tool_header("Performance Monitor", "Test website speed and performance", "⚡")

    url = st.text_input("Website URL:", placeholder="https://example.com")

    if url and st.button("Test Performance"):
        if url.startswith(('http://', 'https://')):
            performance = test_performance(url)
            display_performance_results(performance)
        else:
            st.error("Please enter a valid URL starting with http:// or https://")


def test_performance(url):
    """Test website performance"""
    import time

    try:
        start_time = time.time()
        response = requests.get(url, timeout=30)
        end_time = time.time()

        load_time = end_time - start_time

        return {
            'load_time': load_time,
            'status_code': response.status_code,
            'size': len(response.content),
            'headers': dict(response.headers),
            'success': True
        }
    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }


def display_performance_results(performance):
    """Display performance test results"""
    if performance['success']:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Load Time", f"{performance['load_time']:.2f}s")

        with col2:
            st.metric("Status Code", performance['status_code'])

        with col3:
            size_mb = performance['size'] / (1024 * 1024)
            st.metric("Page Size", f"{size_mb:.2f} MB")

        # Performance rating
        if performance['load_time'] < 1:
            st.success("🚀 Excellent performance!")
        elif performance['load_time'] < 3:
            st.success("✅ Good performance")
        elif performance['load_time'] < 5:
            st.warning("⚠️ Average performance")
        else:
            st.error("❌ Slow performance")

        # Recommendations
        st.markdown("### Recommendations")
        if performance['load_time'] > 3:
            st.write("- Consider optimizing images")
            st.write("- Enable compression")
            st.write("- Use a Content Delivery Network (CDN)")
        if size_mb > 5:
            st.write("- Reduce page size by optimizing assets")
            st.write("- Minify CSS and JavaScript")
    else:
        st.error(f"❌ Performance test failed: {performance['error']}")