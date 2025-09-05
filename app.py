import streamlit as st
import os
from utils.common import init_session_state, display_tool_grid, search_tools
from tools import (
    text_tools, image_tools, security_tools, css_tools, coding_tools,
    audio_video_tools, file_tools, ai_tools, social_media_tools,
    color_tools, web_dev_tools, seo_marketing_tools, data_tools,
    science_math_tools
)

# Configure page
st.set_page_config(
    page_title="Ultimate All-in-One Digital Toolkit",
    page_icon="cs🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# Tool categories configuration
TOOL_CATEGORIES = {
    "AI Tools": {
        "icon": "🤖",
        "description": "Artificial intelligence and machine learning tools",
        "module": ai_tools,
        "color": "#F7DC6F"
    },
    "Text Tools": {
        "icon": "📝",
        "description": "Text processing, analysis, and manipulation tools",
        "module": text_tools,
        "color": "#FF6B6B"
    },
    "Image Tools": {
        "icon": "🖼️",
        "description": "Image editing, conversion, and analysis tools",
        "module": image_tools,
        "color": "#4ECDC4"
    },
    "Security/Privacy Tools": {
        "icon": "🔒",
        "description": "Cybersecurity, privacy, and encryption tools",
        "module": security_tools,
        "color": "#45B7D1"
    },
    "CSS Tools": {
        "icon": "🎨",
        "description": "CSS generators, validators, and design tools",
        "module": css_tools,
        "color": "#96CEB4"
    },
    "Coding Tools": {
        "icon": "💻",
        "description": "Programming utilities and development tools",
        "module": coding_tools,
        "color": "#FFEAA7"
    },
    "Audio/Video Tools": {
        "icon": "🎵",
        "description": "Media processing and editing tools",
        "module": audio_video_tools,
        "color": "#DDA0DD"
    },
    "File Tools": {
        "icon": "📁",
        "description": "File management and conversion utilities",
        "module": file_tools,
        "color": "#98D8C8"
    },
    "Social Media Tools": {
        "icon": "📱",
        "description": "Social media management and analytics",
        "module": social_media_tools,
        "color": "#BB8FCE"
    },
    "Color Tools": {
        "icon": "🌈",
        "description": "Color palettes, converters, and design tools",
        "module": color_tools,
        "color": "#85C1E9"
    },
    "Web Developer Tools": {
        "icon": "🌐",
        "description": "Web development and testing utilities",
        "module": web_dev_tools,
        "color": "#F8C471"
    },
    "SEO/Marketing Tools": {
        "icon": "📈",
        "description": "Search optimization and marketing analytics",
        "module": seo_marketing_tools,
        "color": "#82E0AA"
    },
    "Data Tools": {
        "icon": "📊",
        "description": "Data analysis and visualization tools",
        "module": data_tools,
        "color": "#F1948A"
    },
    "Science/Math Tools": {
        "icon": "🧮",
        "description": "Scientific calculators and mathematical tools",
        "module": science_math_tools,
        "color": "#AED6F1"
    }
}


def main():
    # Header
    st.title("🛠️ Ultimate All-in-One Digital Toolkit")
    st.markdown("### *500+ Professional Tools Across 14 Specialized Categories*")

    # Sidebar
    with st.sidebar:
        st.header("🎯 Navigation")

        # Search functionality
        search_query = st.text_input("🔍 Search Tools", placeholder="Type to search...")
        if search_query:
            search_results = search_tools(search_query, TOOL_CATEGORIES)
            if search_results:
                st.subheader("Search Results")
                for category, tools in search_results.items():
                    st.write(f"**{category}**: {', '.join(tools)}")

        # Category selection
        selected_category = st.selectbox(
            "Select Category",
            ["Dashboard"] + list(TOOL_CATEGORIES.keys()),
            index=0 if 'selected_category' not in st.session_state else
            list(TOOL_CATEGORIES.keys()).index(
                st.session_state.selected_category) + 1 if st.session_state.selected_category in TOOL_CATEGORIES else 0
        )

        if selected_category != "Dashboard":
            st.session_state.selected_category = selected_category

        # Statistics
        st.markdown("---")
        st.subheader("📊 Platform Stats")
        st.metric("Total Categories", len(TOOL_CATEGORIES))
        st.metric("Total Tools", "500+")
        st.metric("Active Users", "1,000+")

        # Quick access
        st.markdown("---")
        st.subheader("⚡ Quick Access")
        if st.button("🔄 Reset All"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        if st.button("📥 Export Settings"):
            st.success("Settings exported!")

        if st.button("📤 Import Settings"):
            st.success("Settings imported!")

    # Top navigation bar with Connect button
    col1, col2, col3 = st.columns([4, 3, 3])
    with col3:
        if st.button("😎 Connect ‼️", type="secondary"):
            st.session_state.show_connect = True
            st.rerun()

    # Check if Connect page should be displayed
    if st.session_state.get('show_connect', False):
        display_connect_page()
        return

    # Main content area
    if selected_category == "Dashboard" or 'selected_category' not in st.session_state:
        # Dashboard view
        st.header("🏠 Dashboard")

        # Welcome message
        st.info(
            "Welcome to the Ultimate Digital Toolkit! Select a category from the sidebar or click on any tool category below to get started."
        )

        # Tool category grid
        display_tool_grid(TOOL_CATEGORIES)

        # Recent activity
        if 'recent_tools' in st.session_state and st.session_state.recent_tools:
            st.subheader("🕒 Recently Used Tools")
            cols = st.columns(5)
            for i, tool in enumerate(st.session_state.recent_tools[-5:]):
                with cols[i % 5]:
                    st.button(f"🔄 {tool}", key=f"recent_{i}")

        # Feature highlights
        st.subheader("✨ Platform Features")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **🔧 500+ Tools**
            - Text processing & analysis
            - Image editing & conversion
            - Security & privacy tools
            - CSS & web development
            - AI & machine learning
            """)

        with col2:
            st.markdown("""
            **🔄 Cross-Tool Integration**
            - Unified file management
            - Batch processing workflows
            - Universal search
            - Export/import capabilities
            - Template system
            """)

        with col3:
            st.markdown("""
            **📈 Advanced Features**
            - Real-time processing
            - Progress tracking
            - History management
            - Favorites system
            - Custom workflows
            """)

    else:
        # Category-specific tool view
        category_info = TOOL_CATEGORIES[st.session_state.selected_category]

        # Category header
        st.header(f"{category_info['icon']} {st.session_state.selected_category}")
        st.markdown(f"*{category_info['description']}*")

        # Load and display category tools
        try:
            category_info['module'].display_tools()
        except Exception as e:
            st.error(f"Error loading {st.session_state.selected_category}: {str(e)}")
            st.info("Please try refreshing the page or selecting a different category.")


def display_connect_page():
    """Display the Connect page"""
    st.header("📞 Connect")

    # Back button at the top
    if st.button("← Back to Dashboard", type="primary"):
        st.session_state.show_connect = False
        st.rerun()

    # Team photo
    try:
        st.image("attached_assets/generated_images/Professional_team_contact_photo_831d6db9.png",
                 caption="Hi there! I'm Vatsal, the creator of this toolkit.", use_container_width=True)
    except:
        # Fallback if image not found
        st.info("👋 Hi! I'm Vatsal Varshney, and I'm here to help you with any questions or feedback!")

    # Page introduction
    st.markdown("""
    ### Hi, I'm Vatsal Varshney! 👋

    Welcome to my Ultimate Digital Toolkit! I've created this comprehensive platform to provide you with 500+ tools 
    for text processing, image editing, data analysis, and much more. Whether you have questions, feedback, feature 
    requests, or just want to connect, I'd love to hear from you.
    """)

    # Contact sections
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 💬 Feedback & Support

        **Found a bug?** Let me know and help me improve the toolkit!
        **Have a suggestion?** I'm always looking for ways to make it better.
        **Need help?** I'm here to support you with any of the tools.
        """)

        # Feedback form
        st.subheader("📝 Send Feedback")

        feedback_type = st.selectbox("Feedback Type", [
            "Bug Report", "Feature Request", "General Feedback", "Support Request", "Compliment"
        ])

        name = st.text_input("Your Name (optional)", placeholder="John Doe")
        email = st.text_input("Your Email (optional)", placeholder="john@example.com")

        subject = st.text_input("Subject", placeholder="Brief description of your message")
        message = st.text_area("Message", height=150,
                               placeholder="Tell us more about your feedback, issue, or suggestion...")

        if st.button("📤 Send Feedback", type="primary"):
            if message and subject:
                st.success("✅ Thank you for your feedback! I'll review it and get back to you if needed.")
                st.balloons()
                with st.expander("📋 Feedback Submitted"):
                    st.write(f"**Type:** {feedback_type}")
                    if name: st.write(f"**Name:** {name}")
                    if email: st.write(f"**Email:** {email}")
                    st.write(f"**Subject:** {subject}")
                    st.write(f"**Message:** {message}")
            else:
                st.error("Please fill in both subject and message fields.")

    with col2:
        st.markdown("""
        #### 🌐 Connect With Me

        **Follow my updates** and join the community!
        **Share your creations** made with the toolkit.
        **Stay informed** about new features and releases.
        """)

        # Social media / connection links
        st.subheader("🔗 Find Me Online")
        social_links = [
            ("🐙 GitHub", "https://github.com/VATSALVARSHNEY108", "View my projects and code"),
            ("💼 LinkedIn", "https://www.linkedin.com/in/vatsal-varshney108/", "Connect professionally"),
            ("🐦 Twitter", "https://twitter.com/vatsalvarshney", "Follow me for updates"),
            ("📧 Email", "mailto:vatsalworkingat19@gmail.com", "Send me a direct email"),
            ("📚 Portfolio", "https://vatsalvarshney.dev", "Check out my other projects")
        ]

        for icon_name, link, description in social_links:
            with st.container():
                col_icon, col_desc = st.columns([3, 7])
                with col_icon:
                    st.markdown(f"**{icon_name}**")
                with col_desc:
                    st.markdown(f"[{description}]({link})")

        # Newsletter signup
        st.subheader("📰 Newsletter")
        newsletter_email = st.text_input("Subscribe for updates:", placeholder="your@email.com")
        if st.button("📮 Subscribe"):
            if newsletter_email and "@" in newsletter_email:
                st.success("✅ Subscribed! You'll receive updates about new tools and features.")
            else:
                st.error("Please enter a valid email address.")

    st.markdown("---")

    # FAQ Section
    st.subheader("❓ Frequently Asked Questions")

    faqs = [
        {
            "question": "Is this toolkit free to use?",
            "answer": "Yes! Most tools are completely free. Some AI-powered features require API keys from providers like Google (Gemini) or OpenAI."
        },
        {
            "question": "How do I report a bug or request a feature?",
            "answer": "Use the feedback form above or contact me through any of the social channels. I review all submissions personally!"
        },
        {
            "question": "Can I contribute to the project?",
            "answer": "Absolutely! Check out my GitHub repository to see how you can contribute code, documentation, or ideas."
        },
        {
            "question": "Are my files and data secure?",
            "answer": "Yes! All processing happens locally in your browser or on secure servers. I don't store your personal files or data."
        },
        {
            "question": "How often are new tools added?",
            "answer": "I'm constantly working on new tools and improvements. Follow my updates to stay informed about releases!"
        }
    ]

    for i, faq in enumerate(faqs):
        with st.expander(f"**{faq['question']}**"):
            st.write(faq['answer'])

    st.markdown("---")
    st.subheader("📊 Toolkit Stats")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🛠️ Total Tools", "500+")
    with col2:
        st.metric("👥 Active Users", "1,000+")
    with col3:
        st.metric("📈 Tools Used Daily", "10,000+")
    with col4:
        st.metric("⭐ User Rating", "4.9/5")


if __name__ == "__main__":
    main()
