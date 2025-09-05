import streamlit as st
import re
import requests
from urllib.parse import urlparse, urljoin
import json
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all SEO and marketing tools"""

    tool_categories = {
        "SEO Analysis": [
            "Page SEO Analyzer", "Meta Tag Checker", "Keyword Density", "Heading Structure", "Internal Link Checker"
        ],
        "Content Marketing": [
            "Content Planner", "Keyword Research", "Competitor Analysis", "Content Calendar", "Topic Generator"
        ],
        "Social Media": [
            "Hashtag Generator", "Post Scheduler", "Engagement Calculator", "Handle Checker", "Bio Generator"
        ],
        "Email Marketing": [
            "Subject Line Tester", "Email Template", "List Segmentation", "A/B Test Calculator",
            "Deliverability Checker"
        ],
        "Analytics Tools": [
            "UTM Builder", "Click Tracker", "Conversion Calculator", "ROI Calculator", "Traffic Estimator"
        ],
        "Local SEO": [
            "Local Citation Checker", "GMB Optimizer", "Local Keyword Tool", "Review Generator", "NAP Consistency"
        ],
        "Technical SEO": [
            "Robots.txt Generator", "Sitemap Validator", "Schema Markup", "Canonical URL Checker", "Redirect Checker"
        ],
        "Link Building": [
            "Backlink Analyzer", "Anchor Text Analyzer", "Link Prospecting", "Outreach Templates",
            "Link Quality Checker"
        ],
        "PPC Tools": [
            "Ad Copy Generator", "Keyword Bid Calculator", "Quality Score Estimator", "Ad Preview",
            "Landing Page Analyzer"
        ],
        "Conversion Optimization": [
            "A/B Test Calculator", "Heatmap Analyzer", "Funnel Analyzer", "CRO Checklist", "Form Optimizer"
        ]
    }

    selected_category = st.selectbox("Select SEO/Marketing Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"SEO/Marketing Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Page SEO Analyzer":
        page_seo_analyzer()
    elif selected_tool == "Meta Tag Checker":
        meta_tag_checker()
    elif selected_tool == "Keyword Density":
        keyword_density()
    elif selected_tool == "UTM Builder":
        utm_builder()
    elif selected_tool == "Hashtag Generator":
        hashtag_generator()
    elif selected_tool == "Subject Line Tester":
        subject_line_tester()
    elif selected_tool == "Robots.txt Generator":
        robots_txt_generator()
    elif selected_tool == "Schema Markup":
        schema_markup_generator()
    elif selected_tool == "A/B Test Calculator":
        ab_test_calculator()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def page_seo_analyzer():
    """Analyze page SEO"""
    create_tool_header("Page SEO Analyzer", "Analyze your webpage for SEO optimization", "🔍")

    url = st.text_input("Enter webpage URL:", placeholder="https://example.com/page")

    if url and st.button("Analyze SEO"):
        if url.startswith(('http://', 'https://')):
            with st.spinner("Analyzing page..."):
                analysis = analyze_page_seo(url)
                display_seo_analysis(analysis)
        else:
            st.error("Please enter a valid URL starting with http:// or https://")


def analyze_page_seo(url):
    """Analyze webpage for SEO factors"""
    try:
        response = requests.get(url, timeout=30)
        html_content = response.text

        analysis = {
            'title': extract_title(html_content),
            'meta_description': extract_meta_description(html_content),
            'headings': extract_headings(html_content),
            'images': analyze_images(html_content),
            'links': analyze_links(html_content, url),
            'word_count': count_words(html_content),
            'success': True
        }

        return analysis
    except Exception as e:
        return {'error': str(e), 'success': False}


def extract_title(html):
    """Extract page title"""
    match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else None


def extract_meta_description(html):
    """Extract meta description"""
    match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    if not match:
        match = re.search(r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']', html, re.IGNORECASE)
    return match.group(1).strip() if match else None


def extract_headings(html):
    """Extract heading tags"""
    headings = {}
    for i in range(1, 7):
        pattern = f'<h{i}[^>]*>(.*?)</h{i}>'
        matches = re.findall(pattern, html, re.IGNORECASE | re.DOTALL)
        headings[f'h{i}'] = [re.sub(r'<[^>]+>', '', match).strip() for match in matches]
    return headings


def analyze_images(html):
    """Analyze images for alt text"""
    img_pattern = r'<img[^>]*>'
    images = re.findall(img_pattern, html, re.IGNORECASE)

    total_images = len(images)
    images_with_alt = 0

    for img in images:
        if re.search(r'alt=["\'][^"\']*["\']', img, re.IGNORECASE):
            images_with_alt += 1

    return {
        'total': total_images,
        'with_alt': images_with_alt,
        'without_alt': total_images - images_with_alt
    }


def analyze_links(html, base_url):
    """Analyze internal and external links"""
    link_pattern = r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>'
    links = re.findall(link_pattern, html, re.IGNORECASE)

    internal_links = 0
    external_links = 0

    domain = urlparse(base_url).netloc

    for link in links:
        if link.startswith(('http://', 'https://')):
            if urlparse(link).netloc == domain:
                internal_links += 1
            else:
                external_links += 1
        elif link.startswith('/') or not link.startswith(('mailto:', 'tel:')):
            internal_links += 1

    return {
        'total': len(links),
        'internal': internal_links,
        'external': external_links
    }


def count_words(html):
    """Count words in page content"""
    # Remove script and style elements
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Count words
    words = re.findall(r'\b\w+\b', text)
    return len(words)


def display_seo_analysis(analysis):
    """Display SEO analysis results"""
    if not analysis['success']:
        st.error(f"❌ Analysis failed: {analysis['error']}")
        return

    # Title analysis
    st.markdown("### 📝 Title Tag")
    if analysis['title']:
        title_length = len(analysis['title'])
        if 30 <= title_length <= 60:
            st.success(f"✅ Title length: {title_length} characters (optimal)")
        elif title_length < 30:
            st.warning(f"⚠️ Title length: {title_length} characters (too short)")
        else:
            st.error(f"❌ Title length: {title_length} characters (too long)")
        st.code(analysis['title'])
    else:
        st.error("❌ No title tag found")

    # Meta description analysis
    st.markdown("### 📄 Meta Description")
    if analysis['meta_description']:
        desc_length = len(analysis['meta_description'])
        if 150 <= desc_length <= 160:
            st.success(f"✅ Description length: {desc_length} characters (optimal)")
        elif desc_length < 150:
            st.warning(f"⚠️ Description length: {desc_length} characters (too short)")
        else:
            st.error(f"❌ Description length: {desc_length} characters (too long)")
        st.code(analysis['meta_description'])
    else:
        st.error("❌ No meta description found")

    # Headings analysis
    st.markdown("### 📋 Heading Structure")
    for heading, content in analysis['headings'].items():
        if content:
            st.write(f"**{heading.upper()}:** {len(content)} found")
            for i, text in enumerate(content[:3], 1):  # Show first 3
                st.write(f"  {i}. {text[:100]}...")

    # Images analysis
    st.markdown("### 🖼️ Images")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Images", analysis['images']['total'])
    with col2:
        st.metric("With Alt Text", analysis['images']['with_alt'])
    with col3:
        st.metric("Missing Alt Text", analysis['images']['without_alt'])

    if analysis['images']['without_alt'] > 0:
        st.warning(f"⚠️ {analysis['images']['without_alt']} images are missing alt text")
    else:
        st.success("✅ All images have alt text")

    # Links analysis
    st.markdown("### 🔗 Links")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Links", analysis['links']['total'])
    with col2:
        st.metric("Internal Links", analysis['links']['internal'])
    with col3:
        st.metric("External Links", analysis['links']['external'])

    # Content analysis
    st.markdown("### 📊 Content")
    st.metric("Word Count", analysis['word_count'])

    if analysis['word_count'] < 300:
        st.warning("⚠️ Content is quite short. Consider adding more valuable content.")
    elif analysis['word_count'] > 2000:
        st.info("ℹ️ Long content. Make sure it's well-structured with headings.")
    else:
        st.success("✅ Good content length")


def meta_tag_checker():
    """Check meta tags"""
    create_tool_header("Meta Tag Checker", "Check and validate meta tags", "🏷️")

    url = st.text_input("Enter webpage URL:", placeholder="https://example.com")

    if url and st.button("Check Meta Tags"):
        if url.startswith(('http://', 'https://')):
            meta_tags = check_meta_tags(url)
            display_meta_tags(meta_tags)
        else:
            st.error("Please enter a valid URL starting with http:// or https://")


def check_meta_tags(url):
    """Check meta tags of a webpage"""
    try:
        response = requests.get(url, timeout=30)
        html = response.text

        meta_tags = {
            'title': extract_title(html),
            'description': extract_meta_description(html),
            'keywords': extract_meta_keywords(html),
            'og_tags': extract_og_tags(html),
            'twitter_tags': extract_twitter_tags(html),
            'success': True
        }

        return meta_tags
    except Exception as e:
        return {'error': str(e), 'success': False}


def extract_meta_keywords(html):
    """Extract meta keywords"""
    match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']*)["\']', html, re.IGNORECASE)
    return match.group(1).strip() if match else None


def extract_og_tags(html):
    """Extract Open Graph tags"""
    og_tags = {}
    og_pattern = r'<meta[^>]*property=["\']og:([^"\']*)["\'][^>]*content=["\']([^"\']*)["\']'
    matches = re.findall(og_pattern, html, re.IGNORECASE)

    for prop, content in matches:
        og_tags[prop] = content

    return og_tags


def extract_twitter_tags(html):
    """Extract Twitter Card tags"""
    twitter_tags = {}
    twitter_pattern = r'<meta[^>]*name=["\']twitter:([^"\']*)["\'][^>]*content=["\']([^"\']*)["\']'
    matches = re.findall(twitter_pattern, html, re.IGNORECASE)

    for prop, content in matches:
        twitter_tags[prop] = content

    return twitter_tags


def display_meta_tags(meta_tags):
    """Display meta tags analysis"""
    if not meta_tags['success']:
        st.error(f"❌ Failed to check meta tags: {meta_tags['error']}")
        return

    # Basic meta tags
    st.markdown("### 📝 Basic Meta Tags")

    if meta_tags['title']:
        st.success(f"✅ Title: {meta_tags['title']}")
    else:
        st.error("❌ Title tag missing")

    if meta_tags['description']:
        st.success(f"✅ Description: {meta_tags['description']}")
    else:
        st.error("❌ Meta description missing")

    if meta_tags['keywords']:
        st.info(f"ℹ️ Keywords: {meta_tags['keywords']}")
    else:
        st.warning("⚠️ Meta keywords not found (not critical)")

    # Open Graph tags
    st.markdown("### 📱 Open Graph Tags")
    if meta_tags['og_tags']:
        for prop, content in meta_tags['og_tags'].items():
            st.write(f"**og:{prop}:** {content}")
    else:
        st.warning("⚠️ No Open Graph tags found")

    # Twitter tags
    st.markdown("### 🐦 Twitter Card Tags")
    if meta_tags['twitter_tags']:
        for prop, content in meta_tags['twitter_tags'].items():
            st.write(f"**twitter:{prop}:** {content}")
    else:
        st.warning("⚠️ No Twitter Card tags found")


def keyword_density():
    """Calculate keyword density"""
    create_tool_header("Keyword Density Analyzer", "Analyze keyword density in your content", "🔍")

    uploaded_file = FileHandler.upload_files(['txt', 'html'], accept_multiple=False)

    if uploaded_file:
        content = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded Content:", content[:500] + "...", height=100, disabled=True)
    else:
        content = st.text_area("Enter content to analyze:", height=200)

    if content and st.button("Analyze Keyword Density"):
        density = calculate_keyword_density(content)
        display_keyword_density(density)


def calculate_keyword_density(content):
    """Calculate keyword density"""
    # Remove HTML tags if present
    text = re.sub(r'<[^>]+>', '', content)

    # Convert to lowercase and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    total_words = len(words)

    # Count word frequency
    word_count = {}
    for word in words:
        if len(word) > 2:  # Ignore very short words
            word_count[word] = word_count.get(word, 0) + 1

    # Calculate density percentages
    density = {}
    for word, count in word_count.items():
        density[word] = {
            'count': count,
            'density': (count / total_words) * 100
        }

    # Sort by density
    sorted_density = dict(sorted(density.items(), key=lambda x: x[1]['density'], reverse=True))

    return {
        'total_words': total_words,
        'unique_words': len(word_count),
        'density': sorted_density
    }


def display_keyword_density(density):
    """Display keyword density results"""
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Words", density['total_words'])

    with col2:
        st.metric("Unique Words", density['unique_words'])

    st.markdown("### 📊 Top Keywords by Density")

    # Show top 20 keywords
    top_keywords = list(density['density'].items())[:20]

    for word, stats in top_keywords:
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(word)
        with col2:
            st.write(f"{stats['count']} times")
        with col3:
            st.write(f"{stats['density']:.2f}%")


def utm_builder():
    """Build UTM parameters"""
    create_tool_header("UTM Builder", "Create trackable campaign URLs", "📊")

    base_url = st.text_input("Website URL:", placeholder="https://example.com/page")
    source = st.text_input("Campaign Source:", placeholder="google, newsletter, social")
    medium = st.text_input("Campaign Medium:", placeholder="cpc, email, social")
    campaign = st.text_input("Campaign Name:", placeholder="spring_sale, product_launch")

    st.markdown("### Optional Parameters")
    term = st.text_input("Campaign Term (keywords):", placeholder="running shoes")
    content = st.text_input("Campaign Content:", placeholder="banner_ad, text_link")

    if base_url and source and medium and campaign:
        utm_url = build_utm_url(base_url, source, medium, campaign, term, content)

        st.markdown("### 🔗 Generated UTM URL")
        st.code(utm_url)

        # QR Code option
        if st.button("Generate QR Code"):
            import qrcode
            from io import BytesIO

            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(utm_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Convert to bytes
            img_buffer = BytesIO()
            img.save(img_buffer, format='PNG')
            img_bytes = img_buffer.getvalue()

            st.image(img_bytes, caption="QR Code for UTM URL")
            FileHandler.create_download_link(img_bytes, "utm_qr_code.png", "image/png")


def build_utm_url(base_url, source, medium, campaign, term="", content=""):
    """Build UTM URL with parameters"""
    from urllib.parse import quote

    # Ensure base URL has proper format
    if not base_url.startswith(('http://', 'https://')):
        base_url = 'https://' + base_url

    # Build UTM parameters
    params = [
        f"utm_source={quote(source)}",
        f"utm_medium={quote(medium)}",
        f"utm_campaign={quote(campaign)}"
    ]

    if term:
        params.append(f"utm_term={quote(term)}")

    if content:
        params.append(f"utm_content={quote(content)}")

    # Add parameters to URL
    separator = "&" if "?" in base_url else "?"
    utm_url = base_url + separator + "&".join(params)

    return utm_url


def hashtag_generator():
    """Generate hashtags for social media"""
    create_tool_header("Hashtag Generator", "Generate relevant hashtags for social media", "#️⃣")

    topic = st.text_input("Enter topic or keywords:", placeholder="fitness, workout, health")
    platform = st.selectbox("Social Media Platform:", ["Instagram", "Twitter", "LinkedIn", "TikTok"])

    if topic and st.button("Generate Hashtags"):
        hashtags = generate_hashtags(topic, platform)
        display_hashtags(hashtags, platform)


def generate_hashtags(topic, platform):
    """Generate hashtags based on topic and platform"""
    # Basic hashtag generation (in a real app, you might use an API)
    keywords = [word.strip().lower() for word in topic.split(',')]

    base_hashtags = []
    for keyword in keywords:
        base_hashtags.extend([
            f"#{keyword}",
            f"#{keyword}life",
            f"#{keyword}community",
            f"#{keyword}lover",
            f"#{keyword}daily"
        ])

    # Platform-specific hashtags
    platform_hashtags = {
        "Instagram": ["#instagood", "#photooftheday", "#instadaily", "#like4like", "#followme"],
        "Twitter": ["#trending", "#follow", "#retweet", "#engage", "#discussion"],
        "LinkedIn": ["#professional", "#networking", "#career", "#business", "#industry"],
        "TikTok": ["#fyp", "#viral", "#trending", "#foryou", "#tiktok"]
    }

    # Combine hashtags
    all_hashtags = base_hashtags + platform_hashtags.get(platform, [])

    return list(set(all_hashtags))  # Remove duplicates


def display_hashtags(hashtags, platform):
    """Display generated hashtags"""
    st.markdown(f"### #{platform} Hashtags")

    # Character limits by platform
    limits = {
        "Instagram": 30,
        "Twitter": 2,
        "LinkedIn": 3,
        "TikTok": 20
    }

    limit = limits.get(platform, 10)
    selected_hashtags = hashtags[:limit]

    # Display hashtags
    hashtag_text = " ".join(selected_hashtags)
    st.code(hashtag_text)

    # Copy button simulation
    st.success(f"✅ Generated {len(selected_hashtags)} hashtags")
    st.info(f"ℹ️ Recommended limit for {platform}: {limit} hashtags")

    # Show all hashtags in expandable section
    with st.expander("View All Generated Hashtags"):
        for hashtag in hashtags:
            st.write(hashtag)


def subject_line_tester():
    """Test email subject lines"""
    create_tool_header("Subject Line Tester", "Test and optimize email subject lines", "📧")

    subject_line = st.text_input("Enter subject line:", placeholder="Don't miss out on our amazing sale!")

    if subject_line and st.button("Test Subject Line"):
        analysis = analyze_subject_line(subject_line)
        display_subject_analysis(analysis)


def analyze_subject_line(subject_line):
    """Analyze email subject line"""
    length = len(subject_line)
    word_count = len(subject_line.split())

    # Check for spam words
    spam_words = ['free', 'urgent', 'limited time', 'act now', 'buy now', 'click here']
    spam_score = sum(1 for word in spam_words if word.lower() in subject_line.lower())

    # Check for personalization
    personalization = any(word in subject_line.lower() for word in ['you', 'your', 'name'])

    # Check for emojis
    emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF]', subject_line))

    # Check for urgency words
    urgency_words = ['urgent', 'hurry', 'fast', 'quick', 'limited', 'expires', 'deadline']
    urgency_score = sum(1 for word in urgency_words if word.lower() in subject_line.lower())

    return {
        'length': length,
        'word_count': word_count,
        'spam_score': spam_score,
        'personalization': personalization,
        'emoji_count': emoji_count,
        'urgency_score': urgency_score
    }


def display_subject_analysis(analysis):
    """Display subject line analysis"""
    # Length analysis
    st.markdown("### 📏 Length Analysis")
    col1, col2 = st.columns(2)

    with col1:
        if 30 <= analysis['length'] <= 50:
            st.success(f"✅ Character count: {analysis['length']} (optimal)")
        elif analysis['length'] < 30:
            st.warning(f"⚠️ Character count: {analysis['length']} (too short)")
        else:
            st.error(f"❌ Character count: {analysis['length']} (too long)")

    with col2:
        if 3 <= analysis['word_count'] <= 7:
            st.success(f"✅ Word count: {analysis['word_count']} (optimal)")
        else:
            st.warning(f"⚠️ Word count: {analysis['word_count']}")

    # Spam analysis
    st.markdown("### 🚫 Spam Risk")
    if analysis['spam_score'] == 0:
        st.success("✅ Low spam risk")
    elif analysis['spam_score'] <= 2:
        st.warning(f"⚠️ Medium spam risk ({analysis['spam_score']} spam words)")
    else:
        st.error(f"❌ High spam risk ({analysis['spam_score']} spam words)")

    # Other factors
    st.markdown("### 📊 Other Factors")

    if analysis['personalization']:
        st.success("✅ Contains personalization")
    else:
        st.info("ℹ️ Consider adding personalization (you, your)")

    if analysis['emoji_count'] > 0:
        st.info(f"📱 Contains {analysis['emoji_count']} emoji(s)")

    if analysis['urgency_score'] > 0:
        st.warning(f"⏰ Contains urgency words ({analysis['urgency_score']})")


def robots_txt_generator():
    """Generate robots.txt file"""
    create_tool_header("Robots.txt Generator", "Generate robots.txt file for your website", "🤖")

    st.markdown("### User-Agent Rules")

    user_agent = st.selectbox("User-Agent:", ["*", "Googlebot", "Bingbot", "Custom"])
    if user_agent == "Custom":
        user_agent = st.text_input("Custom User-Agent:")

    disallow_paths = st.text_area("Disallow paths (one per line):", placeholder="/admin/\n/private/\n/temp/")
    allow_paths = st.text_area("Allow paths (one per line):", placeholder="/public/\n/images/")

    sitemap_url = st.text_input("Sitemap URL:", placeholder="https://example.com/sitemap.xml")

    if st.button("Generate robots.txt"):
        robots_content = generate_robots_txt(user_agent, disallow_paths, allow_paths, sitemap_url)

        st.markdown("### 📄 Generated robots.txt")
        st.code(robots_content)
        FileHandler.create_download_link(robots_content.encode(), "robots.txt", "text/plain")


def generate_robots_txt(user_agent, disallow_paths, allow_paths, sitemap_url):
    """Generate robots.txt content"""
    lines = [f"User-agent: {user_agent}"]

    # Add disallow rules
    if disallow_paths:
        for path in disallow_paths.strip().split('\n'):
            if path.strip():
                lines.append(f"Disallow: {path.strip()}")

    # Add allow rules
    if allow_paths:
        for path in allow_paths.strip().split('\n'):
            if path.strip():
                lines.append(f"Allow: {path.strip()}")

    # Add empty line
    lines.append("")

    # Add sitemap
    if sitemap_url:
        lines.append(f"Sitemap: {sitemap_url}")

    return '\n'.join(lines)


def schema_markup_generator():
    """Generate Schema.org markup"""
    create_tool_header("Schema Markup Generator", "Generate structured data markup", "🏗️")

    schema_type = st.selectbox("Schema Type:", [
        "Organization", "Person", "LocalBusiness", "Product", "Article", "Event"
    ])

    if schema_type == "Organization":
        generate_organization_schema()
    elif schema_type == "Person":
        generate_person_schema()
    elif schema_type == "LocalBusiness":
        generate_local_business_schema()
    elif schema_type == "Product":
        generate_product_schema()
    elif schema_type == "Article":
        generate_article_schema()
    elif schema_type == "Event":
        generate_event_schema()


def generate_organization_schema():
    """Generate Organization schema"""
    name = st.text_input("Organization Name:", placeholder="Your Company")
    url = st.text_input("Website URL:", placeholder="https://yourcompany.com")
    logo = st.text_input("Logo URL:", placeholder="https://yourcompany.com/logo.png")
    description = st.text_area("Description:", placeholder="Company description")

    if name and st.button("Generate Schema"):
        schema = {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": name,
            "url": url,
            "logo": logo,
            "description": description
        }

        schema_json = json.dumps(schema, indent=2)
        st.code(schema_json, language='json')
        FileHandler.create_download_link(schema_json.encode(), "organization_schema.json", "application/json")


def generate_person_schema():
    """Generate Person schema"""
    name = st.text_input("Full Name:", placeholder="John Doe")
    job_title = st.text_input("Job Title:", placeholder="Software Engineer")
    company = st.text_input("Company:", placeholder="Tech Company")
    email = st.text_input("Email:", placeholder="john@example.com")

    if name and st.button("Generate Schema"):
        schema = {
            "@context": "https://schema.org",
            "@type": "Person",
            "name": name,
            "jobTitle": job_title,
            "worksFor": {
                "@type": "Organization",
                "name": company
            },
            "email": email
        }

        schema_json = json.dumps(schema, indent=2)
        st.code(schema_json, language='json')
        FileHandler.create_download_link(schema_json.encode(), "person_schema.json", "application/json")


def generate_local_business_schema():
    """Generate LocalBusiness schema"""
    st.info("LocalBusiness schema generation - implement based on needs")


def generate_product_schema():
    """Generate Product schema"""
    st.info("Product schema generation - implement based on needs")


def generate_article_schema():
    """Generate Article schema"""
    st.info("Article schema generation - implement based on needs")


def generate_event_schema():
    """Generate Event schema"""
    st.info("Event schema generation - implement based on needs")


def ab_test_calculator():
    """Calculate A/B test significance"""
    create_tool_header("A/B Test Calculator", "Calculate statistical significance of A/B tests", "📊")

    st.markdown("### Control Group (A)")
    visitors_a = st.number_input("Visitors:", min_value=1, value=1000, key="visitors_a")
    conversions_a = st.number_input("Conversions:", min_value=0, value=50, key="conversions_a")

    st.markdown("### Variant Group (B)")
    visitors_b = st.number_input("Visitors:", min_value=1, value=1000, key="visitors_b")
    conversions_b = st.number_input("Conversions:", min_value=0, value=60, key="conversions_b")

    if st.button("Calculate Results"):
        results = calculate_ab_test(visitors_a, conversions_a, visitors_b, conversions_b)
        display_ab_results(results)


def calculate_ab_test(visitors_a, conversions_a, visitors_b, conversions_b):
    """Calculate A/B test results"""
    import math

    # Conversion rates
    cr_a = conversions_a / visitors_a
    cr_b = conversions_b / visitors_b

    # Improvement
    improvement = ((cr_b - cr_a) / cr_a) * 100 if cr_a > 0 else 0

    # Standard error
    se_a = math.sqrt((cr_a * (1 - cr_a)) / visitors_a)
    se_b = math.sqrt((cr_b * (1 - cr_b)) / visitors_b)
    se_diff = math.sqrt(se_a ** 2 + se_b ** 2)

    # Z-score
    z_score = (cr_b - cr_a) / se_diff if se_diff > 0 else 0

    # Statistical significance (approximation)
    significant = abs(z_score) > 1.96  # 95% confidence

    return {
        'cr_a': cr_a,
        'cr_b': cr_b,
        'improvement': improvement,
        'z_score': z_score,
        'significant': significant
    }


def display_ab_results(results):
    """Display A/B test results"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Control Rate", f"{results['cr_a']:.2%}")

    with col2:
        st.metric("Variant Rate", f"{results['cr_b']:.2%}")

    with col3:
        improvement_color = "normal" if results['improvement'] >= 0 else "inverse"
        st.metric("Improvement", f"{results['improvement']:.2f}%")

    st.markdown("### 📊 Statistical Significance")

    if results['significant']:
        st.success(f"✅ Statistically significant (Z-score: {results['z_score']:.2f})")
        if results['improvement'] > 0:
            st.success("🎉 Variant B is performing better!")
        else:
            st.error("📉 Variant B is performing worse")
    else:
        st.warning(f"⚠️ Not statistically significant (Z-score: {results['z_score']:.2f})")
        st.info("Consider running the test longer or increasing sample size")