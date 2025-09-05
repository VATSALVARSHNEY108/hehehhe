import streamlit as st
import re
import base64
import hashlib
import html
import urllib.parse
import uuid
import random
import string
from collections import Counter
import qrcode
from io import BytesIO
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler
from utils.ai_client import ai_client


def display_tools():
    """Display all text processing tools"""

    # Tool selection
    tool_categories = {
        "Text Conversion": [
            "Case Converter", "Base Converter", "Encoding Converter", "Format Converter"
        ],
        "Text Formatting": [
            "Whitespace Manager", "Line Break Handler", "Character Remover", "Text Normalizer"
        ],
        "Text Analysis": [
            "Word Counter", "Readability Analyzer", "Language Detector", "Sentiment Analyzer"
        ],
        "Encoding & Encryption": [
            "Base64 Encoder/Decoder", "URL Encoder/Decoder", "HTML Entity Converter", "Hash Generator"
        ],
        "Text Generation": [
            "Lorem Ipsum Generator", "Random Text Generator", "Password Generator", "UUID Generator"
        ],
        "Language Tools": [
            "Text Translator", "Spell Checker", "Grammar Analyzer", "Text-to-Speech"
        ],
        "Text Extraction": [
            "Email Extractor", "URL Extractor", "Phone Extractor", "Regex Matcher"
        ],
        "Text Editing": [
            "Find and Replace", "Text Merger", "Text Splitter", "Duplicate Remover"
        ],
        "Text Styling": [
            "Markdown Converter", "HTML Formatter", "Text Decorator", "Font Styler"
        ],
        "Miscellaneous": [
            "QR Code Generator", "Text to Image", "Word Cloud", "Text Comparison"
        ]
    }

    selected_category = st.selectbox("Select Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    # Add to recent tools
    add_to_recent(f"Text Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Case Converter":
        case_converter()
    elif selected_tool == "Base Converter":
        base_converter()
    elif selected_tool == "Word Counter":
        word_counter()
    elif selected_tool == "Base64 Encoder/Decoder":
        base64_converter()
    elif selected_tool == "Hash Generator":
        hash_generator()
    elif selected_tool == "Password Generator":
        password_generator()
    elif selected_tool == "QR Code Generator":
        qr_generator()
    elif selected_tool == "Find and Replace":
        find_replace()
    elif selected_tool == "Sentiment Analyzer":
        sentiment_analyzer()
    elif selected_tool == "Text Translator":
        text_translator()
    elif selected_tool == "Email Extractor":
        email_extractor()
    elif selected_tool == "URL Extractor":
        url_extractor()
    elif selected_tool == "Lorem Ipsum Generator":
        lorem_generator()
    elif selected_tool == "UUID Generator":
        uuid_generator()
    elif selected_tool == "Markdown Converter":
        markdown_converter()
    elif selected_tool == "Text Comparison":
        text_comparison()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def case_converter():
    """Text case conversion tool"""
    create_tool_header("Case Converter", "Convert text between different cases", "🔤")

    # File upload option
    uploaded_file = FileHandler.upload_files(['txt'], accept_multiple=False)

    if uploaded_file:
        text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Text", text, height=100, disabled=True)
    else:
        text = st.text_area("Enter text to convert:", height=150)

    if text:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("UPPERCASE"):
                result = text.upper()
                st.text_area("Result:", result, height=150)
                FileHandler.create_download_link(result.encode(), "uppercase.txt", "text/plain")

        with col2:
            if st.button("lowercase"):
                result = text.lower()
                st.text_area("Result:", result, height=150)
                FileHandler.create_download_link(result.encode(), "lowercase.txt", "text/plain")

        col3, col4 = st.columns(2)

        with col3:
            if st.button("Title Case"):
                result = text.title()
                st.text_area("Result:", result, height=150)
                FileHandler.create_download_link(result.encode(), "titlecase.txt", "text/plain")

        with col4:
            if st.button("Sentence case"):
                sentences = text.split('. ')
                result = '. '.join([s.capitalize() for s in sentences])
                st.text_area("Result:", result, height=150)
                FileHandler.create_download_link(result.encode(), "sentencecase.txt", "text/plain")


def base_converter():
    """Number base conversion tool"""
    create_tool_header("Base Converter", "Convert numbers between different bases", "🔢")

    number = st.text_input("Enter number:")
    from_base = st.selectbox("From base:", [2, 8, 10, 16], index=2)
    to_base = st.selectbox("To base:", [2, 8, 10, 16], index=0)

    if number and st.button("Convert"):
        try:
            # Convert to decimal first
            decimal_value = int(number, from_base)

            # Convert to target base
            if to_base == 2:
                result = bin(decimal_value)[2:]
            elif to_base == 8:
                result = oct(decimal_value)[2:]
            elif to_base == 10:
                result = str(decimal_value)
            elif to_base == 16:
                result = hex(decimal_value)[2:].upper()

            st.success(f"Result: {result}")

        except ValueError:
            st.error("Invalid number for the selected base!")


def word_counter():
    """Word and character counting tool"""
    create_tool_header("Word Counter", "Count words, characters, and analyze text", "📊")

    # File upload option
    uploaded_file = FileHandler.upload_files(['txt', 'docx'], accept_multiple=False)

    if uploaded_file:
        text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Text", text, height=100, disabled=True)
    else:
        text = st.text_area("Enter text to analyze:", height=200)

    if text:
        # Basic counts
        char_count = len(text)
        char_count_no_spaces = len(text.replace(' ', ''))
        word_count = len(text.split())
        sentence_count = len([s for s in text.split('.') if s.strip()])
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])

        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Characters", char_count)
        col2.metric("Characters (no spaces)", char_count_no_spaces)
        col3.metric("Words", word_count)
        col4.metric("Sentences", sentence_count)
        col5.metric("Paragraphs", paragraph_count)

        # Word frequency
        if st.checkbox("Show word frequency"):
            words = re.findall(r'\b\w+\b', text.lower())
            word_freq = Counter(words)
            most_common = word_freq.most_common(10)

            st.subheader("Most Common Words")
            for word, count in most_common:
                st.write(f"**{word}**: {count}")

        # Reading time estimate
        reading_speed = 200  # words per minute
        reading_time = word_count / reading_speed
        st.info(f"Estimated reading time: {reading_time:.1f} minutes")


def base64_converter():
    """Base64 encoding and decoding tool"""
    create_tool_header("Base64 Converter", "Encode and decode Base64 text", "🔐")

    operation = st.radio("Select operation:", ["Encode", "Decode"])

    if operation == "Encode":
        text = st.text_area("Enter text to encode:")
        if text and st.button("Encode"):
            encoded = base64.b64encode(text.encode()).decode()
            st.text_area("Encoded result:", encoded, height=100)
            FileHandler.create_download_link(encoded.encode(), "encoded.txt", "text/plain")

    else:  # Decode
        encoded_text = st.text_area("Enter Base64 text to decode:")
        if encoded_text and st.button("Decode"):
            try:
                decoded = base64.b64decode(encoded_text).decode()
                st.text_area("Decoded result:", decoded, height=100)
                FileHandler.create_download_link(decoded.encode(), "decoded.txt", "text/plain")
            except Exception as e:
                st.error(f"Invalid Base64 input: {str(e)}")


def hash_generator():
    """Hash generation tool"""
    create_tool_header("Hash Generator", "Generate various types of hashes", "🔒")

    text = st.text_area("Enter text to hash:")
    hash_type = st.selectbox("Select hash type:", ["MD5", "SHA1", "SHA256", "SHA512"])

    if text and st.button("Generate Hash"):
        text_bytes = text.encode()

        if hash_type == "MD5":
            hash_result = hashlib.md5(text_bytes).hexdigest()
        elif hash_type == "SHA1":
            hash_result = hashlib.sha1(text_bytes).hexdigest()
        elif hash_type == "SHA256":
            hash_result = hashlib.sha256(text_bytes).hexdigest()
        elif hash_type == "SHA512":
            hash_result = hashlib.sha512(text_bytes).hexdigest()

        st.code(hash_result)
        FileHandler.create_download_link(hash_result.encode(), f"hash_{hash_type.lower()}.txt", "text/plain")


def password_generator():
    """Password generation tool"""
    create_tool_header("Password Generator", "Generate secure passwords", "🔑")

    col1, col2 = st.columns(2)

    with col1:
        length = st.slider("Password length:", 4, 128, 12)
        include_uppercase = st.checkbox("Include uppercase letters", True)
        include_lowercase = st.checkbox("Include lowercase letters", True)
        include_numbers = st.checkbox("Include numbers", True)
        include_symbols = st.checkbox("Include symbols", True)

    with col2:
        exclude_ambiguous = st.checkbox("Exclude ambiguous characters (0, O, l, I)", True)
        num_passwords = st.slider("Number of passwords:", 1, 20, 1)

    if st.button("Generate Passwords"):
        chars = ""
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_numbers:
            chars += string.digits
        if include_symbols:
            chars += "!@#$%^&*"

        if exclude_ambiguous:
            chars = chars.replace('0', '').replace('O', '').replace('l', '').replace('I', '')

        if not chars:
            st.error("Please select at least one character type!")
        else:
            passwords = []
            for _ in range(num_passwords):
                password = ''.join(random.choice(chars) for _ in range(length))
                passwords.append(password)
                st.code(password)

            # Create downloadable file
            password_text = '\n'.join(passwords)
            FileHandler.create_download_link(password_text.encode(), "passwords.txt", "text/plain")


def qr_generator():
    """QR code generation tool"""
    create_tool_header("QR Code Generator", "Generate QR codes from text", "📱")

    text = st.text_area("Enter text for QR code:")

    col1, col2 = st.columns(2)
    with col1:
        size = st.slider("Size (pixels):", 100, 1000, 300)
    with col2:
        border = st.slider("Border size:", 1, 10, 4)

    if text and st.button("Generate QR Code"):
        qr = qrcode.QRCode(version=1, box_size=10, border=border)
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size))

        # Display QR code
        st.image(img, caption="Generated QR Code")

        # Prepare download
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        FileHandler.create_download_link(img_buffer.getvalue(), "qrcode.png", "image/png")


def find_replace():
    """Find and replace tool"""
    create_tool_header("Find and Replace", "Find and replace text patterns", "🔍")

    # File upload option
    uploaded_file = FileHandler.upload_files(['txt'], accept_multiple=False)

    if uploaded_file:
        text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Text", text, height=100, disabled=True)
    else:
        text = st.text_area("Enter text:", height=200)

    find_text = st.text_input("Find:")
    replace_text = st.text_input("Replace with:")

    col1, col2, col3 = st.columns(3)
    with col1:
        case_sensitive = st.checkbox("Case sensitive")
    with col2:
        whole_words = st.checkbox("Whole words only")
    with col3:
        use_regex = st.checkbox("Use regular expressions")

    if text and find_text and st.button("Replace"):
        try:
            if use_regex:
                flags = 0 if case_sensitive else re.IGNORECASE
                if whole_words:
                    pattern = r'\b' + re.escape(find_text) + r'\b'
                else:
                    pattern = find_text
                result = re.sub(pattern, replace_text, text, flags=flags)
            else:
                if not case_sensitive:
                    # Case insensitive replacement
                    def replace_func(match):
                        return replace_text

                    pattern = re.escape(find_text)
                    if whole_words:
                        pattern = r'\b' + pattern + r'\b'
                    result = re.sub(pattern, replace_func, text, flags=re.IGNORECASE)
                else:
                    if whole_words:
                        pattern = r'\b' + re.escape(find_text) + r'\b'
                        result = re.sub(pattern, replace_text, text)
                    else:
                        result = text.replace(find_text, replace_text)

            st.text_area("Result:", result, height=200)

            # Count replacements
            original_count = len(re.findall(re.escape(find_text), text, re.IGNORECASE if not case_sensitive else 0))
            st.info(f"Replaced {original_count} occurrences")

            FileHandler.create_download_link(result.encode(), "replaced_text.txt", "text/plain")

        except re.error as e:
            st.error(f"Regular expression error: {str(e)}")


def sentiment_analyzer():
    """AI-powered sentiment analysis"""
    create_tool_header("Sentiment Analyzer", "Analyze text sentiment using AI", "😊")

    # File upload option
    uploaded_file = FileHandler.upload_files(['txt'], accept_multiple=False)

    if uploaded_file:
        text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Text", text, height=100, disabled=True)
    else:
        text = st.text_area("Enter text to analyze:", height=150)

    if text and st.button("Analyze Sentiment"):
        with st.spinner("Analyzing sentiment..."):
            result = ai_client.analyze_sentiment(text)

            if 'error' not in result:
                st.subheader("Sentiment Analysis Results")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Sentiment", result.get('sentiment', 'Unknown'))
                with col2:
                    confidence = result.get('confidence', 0)
                    st.metric("Confidence", f"{confidence:.2%}")

                if 'explanation' in result:
                    st.write("**Analysis:**", result['explanation'])

                if 'indicators' in result:
                    st.write("**Key Indicators:**", ', '.join(result['indicators']))
            else:
                st.error(result['error'])


def text_translator():
    """AI-powered text translation"""
    create_tool_header("Text Translator", "Translate text using AI", "🌍")

    text = st.text_area("Enter text to translate:", height=150)
    target_language = st.selectbox("Target language:", [
        "Spanish", "French", "German", "Italian", "Portuguese", "Russian",
        "Chinese", "Japanese", "Korean", "Arabic", "Hindi", "Dutch"
    ])

    if text and st.button("Translate"):
        with st.spinner("Translating..."):
            result = ai_client.translate_text(text, target_language)
            st.text_area("Translation:", result, height=150)
            FileHandler.create_download_link(result.encode(), f"translation_{target_language.lower()}.txt",
                                             "text/plain")


def email_extractor():
    """Extract email addresses from text"""
    create_tool_header("Email Extractor", "Extract email addresses from text", "📧")

    # File upload option
    uploaded_file = FileHandler.upload_files(['txt'], accept_multiple=False)

    if uploaded_file:
        text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Text", text, height=100, disabled=True)
    else:
        text = st.text_area("Enter text containing emails:", height=200)

    if text and st.button("Extract Emails"):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)

        if emails:
            st.success(f"Found {len(emails)} email(s):")
            for email in emails:
                st.write(f"• {email}")

            # Create downloadable list
            email_list = '\n'.join(emails)
            FileHandler.create_download_link(email_list.encode(), "extracted_emails.txt", "text/plain")
        else:
            st.info("No email addresses found.")


def url_extractor():
    """Extract URLs from text"""
    create_tool_header("URL Extractor", "Extract URLs from text", "🔗")

    # File upload option
    uploaded_file = FileHandler.upload_files(['txt'], accept_multiple=False)

    if uploaded_file:
        text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Text", text, height=100, disabled=True)
    else:
        text = st.text_area("Enter text containing URLs:", height=200)

    if text and st.button("Extract URLs"):
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)

        if urls:
            st.success(f"Found {len(urls)} URL(s):")
            for url in urls:
                st.write(f"• {url}")

            # Create downloadable list
            url_list = '\n'.join(urls)
            FileHandler.create_download_link(url_list.encode(), "extracted_urls.txt", "text/plain")
        else:
            st.info("No URLs found.")


def lorem_generator():
    """Lorem ipsum text generator"""
    create_tool_header("Lorem Ipsum Generator", "Generate placeholder text", "📄")

    col1, col2 = st.columns(2)
    with col1:
        num_paragraphs = st.slider("Number of paragraphs:", 1, 10, 3)
    with col2:
        start_with_lorem = st.checkbox("Start with 'Lorem ipsum...'", True)

    if st.button("Generate Text"):
        lorem_words = [
            "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
            "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore",
            "magna", "aliqua", "enim", "ad", "minim", "veniam", "quis", "nostrud",
            "exercitation", "ullamco", "laboris", "nisi", "aliquip", "ex", "ea", "commodo",
            "consequat", "duis", "aute", "irure", "in", "reprehenderit", "voluptate",
            "velit", "esse", "cillum", "fugiat", "nulla", "pariatur", "excepteur", "sint",
            "occaecat", "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
            "deserunt", "mollit", "anim", "id", "est", "laborum"
        ]

        paragraphs = []

        for i in range(num_paragraphs):
            if i == 0 and start_with_lorem:
                paragraph = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                remaining_words = random.randint(30, 80)
            else:
                paragraph = ""
                remaining_words = random.randint(40, 100)

            words = []
            for _ in range(remaining_words):
                words.append(random.choice(lorem_words))

            paragraph += ' '.join(words) + '.'
            paragraph = paragraph.capitalize()
            paragraphs.append(paragraph)

        result = '\n\n'.join(paragraphs)
        st.text_area("Generated Lorem Ipsum:", result, height=300)
        FileHandler.create_download_link(result.encode(), "lorem_ipsum.txt", "text/plain")


def uuid_generator():
    """UUID generation tool"""
    create_tool_header("UUID Generator", "Generate universally unique identifiers", "🆔")

    col1, col2 = st.columns(2)
    with col1:
        num_uuids = st.slider("Number of UUIDs:", 1, 100, 1)
    with col2:
        uuid_version = st.selectbox("UUID Version:", [1, 4], index=1)

    if st.button("Generate UUIDs"):
        uuids = []
        for _ in range(num_uuids):
            if uuid_version == 1:
                new_uuid = str(uuid.uuid1())
            else:  # Version 4
                new_uuid = str(uuid.uuid4())
            uuids.append(new_uuid)
            st.code(new_uuid)

        # Create downloadable file
        uuid_text = '\n'.join(uuids)
        FileHandler.create_download_link(uuid_text.encode(), "uuids.txt", "text/plain")


def markdown_converter():
    """Markdown to HTML converter"""
    create_tool_header("Markdown Converter", "Convert Markdown to HTML", "📝")

    # File upload option
    uploaded_file = FileHandler.upload_files(['md', 'txt'], accept_multiple=False)

    if uploaded_file:
        markdown_text = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Markdown", markdown_text, height=100, disabled=True)
    else:
        markdown_text = st.text_area("Enter Markdown text:", height=200)

    if markdown_text and st.button("Convert to HTML"):
        # Simple markdown to HTML conversion
        html_text = markdown_text

        # Headers
        html_text = re.sub(r'^### (.*)', r'<h3>\1</h3>', html_text, flags=re.MULTILINE)
        html_text = re.sub(r'^## (.*)', r'<h2>\1</h2>', html_text, flags=re.MULTILINE)
        html_text = re.sub(r'^# (.*)', r'<h1>\1</h1>', html_text, flags=re.MULTILINE)

        # Bold and italic
        html_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_text)
        html_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_text)

        # Links
        html_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html_text)

        # Line breaks
        html_text = html_text.replace('\n', '<br>\n')

        st.text_area("HTML Output:", html_text, height=200)
        st.subheader("Preview:")
        st.markdown(html_text, unsafe_allow_html=True)

        FileHandler.create_download_link(html_text.encode(), "converted.html", "text/html")


def text_comparison():
    """Compare two texts"""
    create_tool_header("Text Comparison", "Compare two texts for differences", "🔍")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Text 1")
        text1 = st.text_area("Enter first text:", height=200, key="text1")

    with col2:
        st.subheader("Text 2")
        text2 = st.text_area("Enter second text:", height=200, key="text2")

    if text1 and text2 and st.button("Compare Texts"):
        # Basic comparison metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Length Difference", abs(len(text1) - len(text2)))
        with col2:
            similarity = calculate_similarity(text1, text2)
            st.metric("Similarity", f"{similarity:.1%}")
        with col3:
            word_diff = abs(len(text1.split()) - len(text2.split()))
            st.metric("Word Count Difference", word_diff)

        # Character-by-character comparison
        st.subheader("Detailed Comparison")

        if len(text1) == len(text2):
            differences = []
            for i, (c1, c2) in enumerate(zip(text1, text2)):
                if c1 != c2:
                    differences.append(f"Position {i}: '{c1}' vs '{c2}'")

            if differences:
                st.write(f"Found {len(differences)} character differences:")
                for diff in differences[:20]:  # Show first 20 differences
                    st.write(f"• {diff}")
                if len(differences) > 20:
                    st.write(f"... and {len(differences) - 20} more")
            else:
                st.success("Texts are identical!")
        else:
            st.info("Texts have different lengths. Exact character comparison not possible.")


def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts"""
    # Simple similarity based on common words
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())

    if not words1 and not words2:
        return 1.0
    if not words1 or not words2:
        return 0.0

    common_words = words1.intersection(words2)
    total_words = words1.union(words2)

    return len(common_words) / len(total_words)
