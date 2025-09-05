import streamlit as st
import json
import csv
import io
from datetime import datetime, timedelta
import calendar
import random
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler
from utils.ai_client import ai_client


def display_tools():
    """Display all social media tools"""

    tool_categories = {
        "Content Schedulers": [
            "Multi-Platform Scheduler", "Content Calendar", "Post Optimizer", "Timing Analyzer", "Bulk Scheduler"
        ],
        "Analytics Dashboards": [
            "Engagement Analytics", "Reach Analysis", "Performance Tracker", "Competitor Analysis", "Growth Metrics"
        ],
        "Hashtag Generators": [
            "Hashtag Research", "Trending Hashtags", "Niche Discovery", "Hashtag Analytics", "Tag Optimizer"
        ],
        "Engagement Tools": [
            "Comment Manager", "Follower Analysis", "Interaction Tracker", "Community Builder", "Response Automation"
        ],
        "Multi-Platform Managers": [
            "Cross-Platform Posting", "Unified Dashboard", "Account Manager", "Content Distributor", "Platform Sync"
        ],
        "Content Creation": [
            "Post Generator", "Caption Writer", "Visual Content", "Story Creator", "Video Scripts"
        ],
        "Audience Analysis": [
            "Demographics Analyzer", "Behavior Insights", "Audience Segmentation", "Growth Tracking",
            "Engagement Patterns"
        ],
        "Campaign Management": [
            "Campaign Planner", "A/B Testing", "Performance Monitor", "ROI Tracker", "Campaign Analytics"
        ],
        "Social Listening": [
            "Mention Monitor", "Brand Tracking", "Sentiment Analysis", "Trend Detection", "Competitor Monitoring"
        ],
        "Influencer Tools": [
            "Influencer Finder", "Collaboration Manager", "Performance Tracker", "Outreach Automation", "ROI Calculator"
        ]
    }

    selected_category = st.selectbox("Select Social Media Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Social Media Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Multi-Platform Scheduler":
        multi_platform_scheduler()
    elif selected_tool == "Content Calendar":
        content_calendar()
    elif selected_tool == "Hashtag Research":
        hashtag_research()
    elif selected_tool == "Engagement Analytics":
        engagement_analytics()
    elif selected_tool == "Post Generator":
        post_generator()
    elif selected_tool == "Caption Writer":
        caption_writer()
    elif selected_tool == "Audience Segmentation":
        audience_segmentation()
    elif selected_tool == "Campaign Planner":
        campaign_planner()
    elif selected_tool == "Mention Monitor":
        mention_monitor()
    elif selected_tool == "Influencer Finder":
        influencer_finder()
    elif selected_tool == "Cross-Platform Posting":
        cross_platform_posting()
    elif selected_tool == "Trending Hashtags":
        trending_hashtags()
    elif selected_tool == "Performance Tracker":
        performance_tracker()
    elif selected_tool == "A/B Testing":
        ab_testing()
    elif selected_tool == "Brand Tracking":
        brand_tracking()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def multi_platform_scheduler():
    """Schedule posts across multiple social media platforms"""
    create_tool_header("Multi-Platform Scheduler", "Schedule posts across multiple social media platforms", "📅")

    # Platform selection
    st.subheader("Select Platforms")
    platforms = st.multiselect("Choose Platforms", [
        "Twitter", "Facebook", "Instagram", "LinkedIn", "TikTok", "YouTube", "Pinterest", "Reddit"
    ], default=["Twitter", "Facebook", "Instagram"])

    if not platforms:
        st.warning("Please select at least one platform.")
        return

    # Content creation
    st.subheader("Create Content")

    content_type = st.selectbox("Content Type", [
        "Text Post", "Image Post", "Video Post", "Link Post", "Story", "Carousel"
    ])

    # Main content
    main_content = st.text_area("Main Content", height=150,
                                placeholder="Write your post content here...")

    # Platform-specific customization
    st.subheader("Platform-Specific Content")
    platform_content = {}

    for platform in platforms:
        with st.expander(f"{platform} Customization"):
            custom_content = st.text_area(f"Custom content for {platform}",
                                          value=main_content,
                                          key=f"content_{platform}",
                                          help=f"Customize content specifically for {platform}")

            # Platform-specific settings
            if platform == "Twitter":
                thread_mode = st.checkbox("Create Thread", key=f"thread_{platform}")
                if thread_mode:
                    thread_count = st.number_input("Number of tweets", 1, 10, 1, key=f"thread_count_{platform}")

            elif platform == "Instagram":
                use_carousel = st.checkbox("Carousel Post", key=f"carousel_{platform}")
                story_post = st.checkbox("Also post to Story", key=f"story_{platform}")

            elif platform == "LinkedIn":
                professional_tone = st.checkbox("Use Professional Tone", True, key=f"prof_{platform}")

            # Hashtags for each platform
            hashtags = st.text_input(f"Hashtags for {platform}",
                                     placeholder="#hashtag1 #hashtag2",
                                     key=f"hashtags_{platform}")

            platform_content[platform] = {
                'content': custom_content,
                'hashtags': hashtags,
                'settings': {}
            }

    # Scheduling
    st.subheader("Schedule Settings")

    col1, col2 = st.columns(2)
    with col1:
        schedule_option = st.selectbox("Schedule Option", [
            "Post Now", "Schedule for Later", "Optimal Time", "Custom Schedule"
        ])

    with col2:
        if schedule_option in ["Schedule for Later", "Custom Schedule"]:
            schedule_date = st.date_input("Schedule Date", datetime.now().date())
            schedule_time = st.time_input("Schedule Time", datetime.now().time())
        elif schedule_option == "Optimal Time":
            timezone = st.selectbox("Timezone", [
                "UTC", "EST", "PST", "GMT", "CET", "JST", "IST"
            ])

    # Media attachments
    if content_type in ["Image Post", "Video Post", "Carousel"]:
        st.subheader("Media Attachments")
        media_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov'], accept_multiple=True)

        if media_files:
            st.success(f"Uploaded {len(media_files)} media file(s)")

    # Preview and schedule
    if st.button("Preview & Schedule Posts"):
        if main_content:
            preview_posts(platform_content, platforms, schedule_option)

            # Create scheduling data
            schedule_data = {
                'platforms': platforms,
                'content': platform_content,
                'schedule_option': schedule_option,
                'schedule_datetime': f"{schedule_date} {schedule_time}" if schedule_option != "Post Now" else "Immediate",
                'content_type': content_type,
                'created_at': datetime.now().isoformat()
            }

            # Export schedule
            if st.button("Export Schedule"):
                schedule_json = json.dumps(schedule_data, indent=2)
                FileHandler.create_download_link(
                    schedule_json.encode(),
                    f"social_media_schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    "application/json"
                )
        else:
            st.error("Please enter some content for your post.")


def content_calendar():
    """Create and manage social media content calendar"""
    create_tool_header("Content Calendar", "Plan and organize your social media content", "📅")

    # Calendar view options
    view_type = st.selectbox("Calendar View", ["Monthly", "Weekly", "Daily"])

    if view_type == "Monthly":
        selected_date = st.date_input("Select Month", datetime.now().date())
        year = selected_date.year
        month = selected_date.month

        # Display monthly calendar
        st.subheader(f"Content Calendar - {calendar.month_name[month]} {year}")

        # Calendar grid
        cal = calendar.monthcalendar(year, month)

        # Create calendar layout
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                with cols[i]:
                    if day == 0:
                        st.write("")
                    else:
                        date_obj = datetime(year, month, day).date()

                        # Check if content is scheduled for this day
                        has_content = check_scheduled_content(date_obj)

                        if has_content:
                            st.markdown(f"**{day}** 📝")
                            if st.button(f"View {day}", key=f"day_{day}"):
                                show_day_content(date_obj)
                        else:
                            st.write(f"{day}")
                            if st.button(f"+ {day}", key=f"add_{day}"):
                                add_content_to_day(date_obj)

    # Content planning
    st.subheader("Plan New Content")

    col1, col2 = st.columns(2)
    with col1:
        content_date = st.date_input("Content Date")
        content_time = st.time_input("Content Time")
        platform = st.selectbox("Platform", [
            "All Platforms", "Twitter", "Facebook", "Instagram", "LinkedIn", "TikTok"
        ])

    with col2:
        content_type = st.selectbox("Content Type", [
            "Promotional", "Educational", "Entertainment", "Behind-the-Scenes", "User-Generated", "News"
        ])
        priority = st.selectbox("Priority", ["High", "Medium", "Low"])

    content_title = st.text_input("Content Title")
    content_description = st.text_area("Content Description", height=100)
    content_notes = st.text_area("Notes/Ideas", height=80)

    if st.button("Add to Calendar"):
        if content_title and content_description:
            calendar_entry = create_calendar_entry(
                content_date, content_time, platform, content_type,
                priority, content_title, content_description, content_notes
            )

            st.success(f"Content added to calendar for {content_date}")

            # Export calendar entry
            entry_json = json.dumps(calendar_entry, indent=2)
            FileHandler.create_download_link(
                entry_json.encode(),
                f"calendar_entry_{content_date}.json",
                "application/json"
            )


def hashtag_research():
    """Research and analyze hashtags"""
    create_tool_header("Hashtag Research", "Research hashtags for better reach", "#️⃣")

    # Research input
    st.subheader("Hashtag Research")

    col1, col2 = st.columns(2)
    with col1:
        research_method = st.selectbox("Research Method", [
            "Topic-Based", "Competitor Analysis", "Trending Discovery", "Niche Research"
        ])
        platform = st.selectbox("Target Platform", [
            "Instagram", "Twitter", "TikTok", "LinkedIn", "Facebook"
        ])

    with col2:
        topic = st.text_input("Topic/Keyword", placeholder="Enter your topic or keyword")
        industry = st.selectbox("Industry", [
            "Technology", "Fashion", "Food", "Travel", "Fitness", "Business",
            "Art", "Music", "Education", "Health", "Other"
        ])

    if st.button("Research Hashtags") and topic:
        with st.spinner("Researching hashtags..."):
            # Generate hashtag research using AI
            hashtag_data = research_hashtags_ai(topic, platform, industry, research_method)

            if hashtag_data:
                st.subheader("Hashtag Research Results")

                # Display recommended hashtags
                tabs = st.tabs(["Recommended", "Popular", "Niche", "Trending"])

                with tabs[0]:  # Recommended
                    st.write("**Recommended Hashtags:**")
                    recommended = hashtag_data.get('recommended', [])
                    display_hashtag_list(recommended, "recommended")

                with tabs[1]:  # Popular
                    st.write("**Popular Hashtags:**")
                    popular = hashtag_data.get('popular', [])
                    display_hashtag_list(popular, "popular")

                with tabs[2]:  # Niche
                    st.write("**Niche Hashtags:**")
                    niche = hashtag_data.get('niche', [])
                    display_hashtag_list(niche, "niche")

                with tabs[3]:  # Trending
                    st.write("**Trending Hashtags:**")
                    trending = hashtag_data.get('trending', [])
                    display_hashtag_list(trending, "trending")

                # Hashtag strategy
                st.subheader("Hashtag Strategy Recommendations")
                strategy = generate_hashtag_strategy(hashtag_data, platform)

                for recommendation in strategy:
                    st.write(f"• {recommendation}")

                # Export hashtags
                if st.button("Export Hashtag Research"):
                    export_data = {
                        'topic': topic,
                        'platform': platform,
                        'industry': industry,
                        'research_method': research_method,
                        'hashtags': hashtag_data,
                        'strategy': strategy,
                        'research_date': datetime.now().isoformat()
                    }

                    export_json = json.dumps(export_data, indent=2)
                    FileHandler.create_download_link(
                        export_json.encode(),
                        f"hashtag_research_{topic.replace(' ', '_')}.json",
                        "application/json"
                    )


def engagement_analytics():
    """Analyze social media engagement metrics"""
    create_tool_header("Engagement Analytics", "Analyze engagement metrics and performance", "📊")

    # Data input method
    data_method = st.selectbox("Data Input Method", [
        "Upload CSV Data", "Manual Entry", "Sample Data"
    ])

    if data_method == "Upload CSV Data":
        uploaded_file = FileHandler.upload_files(['csv'], accept_multiple=False)

        if uploaded_file:
            df = FileHandler.process_csv_file(uploaded_file[0])
            if df is not None:
                st.subheader("Uploaded Data Preview")
                st.dataframe(df.head())

                engagement_data = df.to_dict('records')
        else:
            engagement_data = None

    elif data_method == "Sample Data":
        engagement_data = generate_sample_engagement_data()
        st.success("Using sample engagement data for demonstration")

    else:  # Manual Entry
        st.subheader("Enter Engagement Data")

        posts = []
        num_posts = st.number_input("Number of Posts to Analyze", 1, 20, 5)

        for i in range(num_posts):
            with st.expander(f"Post {i + 1}"):
                col1, col2 = st.columns(2)

                with col1:
                    post_type = st.selectbox(f"Post Type", ["Image", "Video", "Text", "Carousel"], key=f"type_{i}")
                    platform = st.selectbox(f"Platform", ["Instagram", "Twitter", "Facebook", "LinkedIn"],
                                            key=f"platform_{i}")
                    date = st.date_input(f"Post Date", key=f"date_{i}")

                with col2:
                    likes = st.number_input(f"Likes", 0, 100000, 0, key=f"likes_{i}")
                    comments = st.number_input(f"Comments", 0, 10000, 0, key=f"comments_{i}")
                    shares = st.number_input(f"Shares", 0, 10000, 0, key=f"shares_{i}")

                posts.append({
                    'post_type': post_type,
                    'platform': platform,
                    'date': date.isoformat(),
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'engagement_rate': calculate_engagement_rate(likes, comments, shares)
                })

        engagement_data = posts

    # Analytics
    if engagement_data:
        st.subheader("Engagement Analytics")

        # Overall metrics
        total_posts = len(engagement_data)
        total_likes = sum(post.get('likes', 0) for post in engagement_data)
        total_comments = sum(post.get('comments', 0) for post in engagement_data)
        total_shares = sum(post.get('shares', 0) for post in engagement_data)
        avg_engagement = sum(
            post.get('engagement_rate', 0) for post in engagement_data) / total_posts if total_posts > 0 else 0

        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Posts", total_posts)
        with col2:
            st.metric("Total Likes", f"{total_likes:,}")
        with col3:
            st.metric("Total Comments", f"{total_comments:,}")
        with col4:
            st.metric("Total Shares", f"{total_shares:,}")
        with col5:
            st.metric("Avg Engagement", f"{avg_engagement:.2%}")

        # Performance by platform
        st.subheader("Performance by Platform")
        platform_stats = analyze_platform_performance(engagement_data)

        for platform, stats in platform_stats.items():
            with st.expander(f"{platform} Performance"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Posts", stats['posts'])
                with col2:
                    st.metric("Avg Likes", f"{stats['avg_likes']:.0f}")
                with col3:
                    st.metric("Engagement Rate", f"{stats['avg_engagement']:.2%}")

        # Best performing posts
        st.subheader("Top Performing Posts")
        top_posts = sorted(engagement_data, key=lambda x: x.get('engagement_rate', 0), reverse=True)[:5]

        for i, post in enumerate(top_posts, 1):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**#{i}** {post.get('post_type', 'Unknown')}")
            with col2:
                st.write(f"Platform: {post.get('platform', 'Unknown')}")
            with col3:
                st.write(f"Date: {post.get('date', 'Unknown')}")
            with col4:
                st.write(f"Engagement: {post.get('engagement_rate', 0):.2%}")

        # Generate report
        if st.button("Generate Analytics Report"):
            report = generate_engagement_report(engagement_data, platform_stats)

            FileHandler.create_download_link(
                report.encode(),
                f"engagement_analytics_{datetime.now().strftime('%Y%m%d')}.txt",
                "text/plain"
            )


def post_generator():
    """Generate social media posts using AI"""
    create_tool_header("Post Generator", "Generate engaging social media posts with AI", "✍️")

    # Post parameters
    st.subheader("Post Configuration")

    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Target Platform", [
            "Instagram", "Twitter", "Facebook", "LinkedIn", "TikTok", "Pinterest"
        ])
        post_type = st.selectbox("Post Type", [
            "Promotional", "Educational", "Entertaining", "Inspirational", "Behind-the-Scenes", "Question/Poll"
        ])
        topic = st.text_input("Topic/Subject", placeholder="What should the post be about?")

    with col2:
        tone = st.selectbox("Tone", [
            "Professional", "Casual", "Friendly", "Humorous", "Inspirational", "Educational"
        ])
        target_audience = st.selectbox("Target Audience", [
            "General", "Young Adults", "Professionals", "Students", "Parents", "Entrepreneurs"
        ])
        include_hashtags = st.checkbox("Include Hashtags", True)

    # Additional options
    with st.expander("Advanced Options"):
        call_to_action = st.text_input("Call to Action", placeholder="e.g., Visit our website, Like and share")
        keywords = st.text_input("Keywords to Include", placeholder="keyword1, keyword2, keyword3")
        post_length = st.selectbox("Post Length", ["Short", "Medium", "Long"])
        emoji_style = st.selectbox("Emoji Usage", ["None", "Minimal", "Moderate", "Heavy"])

    if st.button("Generate Post") and topic:
        with st.spinner("Generating social media post..."):
            # Create prompt for AI
            prompt = create_post_generation_prompt(
                platform, post_type, topic, tone, target_audience,
                include_hashtags, call_to_action, keywords, post_length, emoji_style
            )

            generated_post = ai_client.generate_text(prompt, max_tokens=500)

            if generated_post:
                st.subheader("Generated Post")
                st.text_area("", generated_post, height=200, disabled=True)

                # Post analysis
                st.subheader("Post Analysis")
                analysis = analyze_generated_post(generated_post, platform)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Character Count", analysis['char_count'])
                with col2:
                    st.metric("Word Count", analysis['word_count'])
                with col3:
                    st.metric("Hashtag Count", analysis['hashtag_count'])

                # Platform-specific feedback
                feedback = get_platform_feedback(generated_post, platform)
                if feedback:
                    st.subheader("Platform Optimization Feedback")
                    for item in feedback:
                        st.write(f"• {item}")

                # Download post
                FileHandler.create_download_link(
                    generated_post.encode(),
                    f"social_post_{platform.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    "text/plain"
                )

                # Generate variations
                if st.button("Generate Variations"):
                    variations = generate_post_variations(generated_post, platform)

                    st.subheader("Post Variations")
                    for i, variation in enumerate(variations, 1):
                        with st.expander(f"Variation {i}"):
                            st.write(variation)


def caption_writer():
    """AI-powered caption writing tool"""
    create_tool_header("Caption Writer", "Write engaging captions for your content", "💬")

    # Content input
    st.subheader("Content Information")

    # Image upload for context
    uploaded_image = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=False)

    if uploaded_image:
        image = FileHandler.process_image_file(uploaded_image[0])
        if image:
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Analyze image for context
            if st.button("Analyze Image for Context"):
                with st.spinner("Analyzing image..."):
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format='PNG')
                    img_bytes.seek(0)

                    image_description = ai_client.analyze_image(
                        img_bytes.getvalue(),
                        "Describe this image in detail for social media caption writing."
                    )

                    if image_description:
                        st.text_area("Image Analysis", image_description, height=100, disabled=True)

    # Caption parameters
    col1, col2 = st.columns(2)
    with col1:
        content_theme = st.text_input("Content Theme/Topic")
        platform = st.selectbox("Platform", ["Instagram", "Facebook", "Twitter", "LinkedIn", "TikTok"])
        caption_style = st.selectbox("Caption Style", [
            "Storytelling", "Question-based", "List-format", "Behind-the-scenes", "Motivational", "Humorous"
        ])

    with col2:
        brand_voice = st.selectbox("Brand Voice", [
            "Professional", "Casual", "Playful", "Inspirational", "Educational", "Luxury"
        ])
        target_mood = st.selectbox("Target Mood", [
            "Engaging", "Informative", "Entertaining", "Inspiring", "Promotional", "Community-building"
        ])
        caption_length = st.selectbox("Caption Length", ["Short", "Medium", "Long"])

    # Additional context
    brand_info = st.text_area("Brand/Business Information (optional)",
                              placeholder="Tell us about your brand, values, or business...")

    specific_message = st.text_area("Specific Message/CTA",
                                    placeholder="Any specific message or call-to-action you want to include...")

    if st.button("Generate Caption"):
        if content_theme:
            with st.spinner("Creating engaging caption..."):
                caption_prompt = create_caption_prompt(
                    content_theme, platform, caption_style, brand_voice,
                    target_mood, caption_length, brand_info, specific_message
                )

                generated_caption = ai_client.generate_text(caption_prompt, max_tokens=800)

                if generated_caption:
                    st.subheader("Generated Caption")
                    st.text_area("", generated_caption, height=250, disabled=True)

                    # Caption metrics
                    st.subheader("Caption Metrics")
                    metrics = analyze_caption_metrics(generated_caption, platform)

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Characters", metrics['characters'])
                    with col2:
                        st.metric("Words", metrics['words'])
                    with col3:
                        st.metric("Hashtags", metrics['hashtags'])
                    with col4:
                        st.metric("Mentions", metrics['mentions'])

                    # Platform optimization
                    optimization = get_caption_optimization(generated_caption, platform)
                    if optimization:
                        st.subheader("Optimization Tips")
                        for tip in optimization:
                            st.write(f"• {tip}")

                    # Export caption
                    FileHandler.create_download_link(
                        generated_caption.encode(),
                        f"caption_{platform.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        "text/plain"
                    )


# Helper Functions

def preview_posts(platform_content, platforms, schedule_option):
    """Preview posts for all platforms"""
    st.subheader("Post Preview")

    for platform in platforms:
        with st.expander(f"{platform} Post Preview"):
            content = platform_content[platform]['content']
            hashtags = platform_content[platform]['hashtags']

            # Show platform-specific preview
            st.write(f"**{platform} Post:**")
            st.write(content)
            if hashtags:
                st.write(f"**Hashtags:** {hashtags}")

            st.write(f"**Schedule:** {schedule_option}")


def check_scheduled_content(date):
    """Check if content is scheduled for a specific date"""
    # This would check against a database or storage
    # For demo, randomly return True/False
    return random.choice([True, False, False])  # 33% chance of having content


def show_day_content(date):
    """Show content scheduled for a specific day"""
    st.write(f"Content scheduled for {date}")
    # This would fetch actual content from storage


def add_content_to_day(date):
    """Add content to a specific day"""
    st.write(f"Add content for {date}")
    # This would open a form to add content


def create_calendar_entry(date, time, platform, content_type, priority, title, description, notes):
    """Create a calendar entry"""
    return {
        'date': date.isoformat(),
        'time': time.isoformat(),
        'platform': platform,
        'content_type': content_type,
        'priority': priority,
        'title': title,
        'description': description,
        'notes': notes,
        'created_at': datetime.now().isoformat()
    }


def research_hashtags_ai(topic, platform, industry, method):
    """Research hashtags using AI"""
    prompt = f"""
    Research hashtags for the topic "{topic}" on {platform} in the {industry} industry.
    Method: {method}

    Provide:
    1. 10 recommended hashtags (mix of popular and niche)
    2. 5 popular hashtags (high volume)
    3. 5 niche hashtags (specific to topic)
    4. 5 trending hashtags (currently popular)

    Format as JSON with categories: recommended, popular, niche, trending
    """

    try:
        response = ai_client.generate_text(prompt, max_tokens=1000)
        # Try to parse as JSON, fallback to text processing
        if response.strip().startswith('{'):
            return json.loads(response)
        else:
            # Parse text response into hashtag categories
            return parse_hashtag_response(response)
    except:
        # Fallback hashtag data
        return generate_fallback_hashtags(topic, platform, industry)


def display_hashtag_list(hashtags, category):
    """Display hashtag list with copy functionality"""
    if hashtags:
        hashtag_text = ' '.join([f"#{tag}" if not tag.startswith('#') else tag for tag in hashtags])
        st.code(hashtag_text)

        if st.button(f"Copy {category.title()} Hashtags", key=f"copy_{category}"):
            st.success(f"{category.title()} hashtags copied to clipboard!")


def generate_hashtag_strategy(hashtag_data, platform):
    """Generate hashtag strategy recommendations"""
    strategies = [
        f"Use a mix of popular and niche hashtags for optimal reach on {platform}",
        "Include 3-5 popular hashtags to increase discoverability",
        "Add 5-7 niche hashtags to target specific audiences",
        "Monitor trending hashtags and incorporate when relevant",
        "Create a branded hashtag for community building"
    ]

    if platform == "Instagram":
        strategies.append("Use up to 30 hashtags, but 11-15 often perform best")
    elif platform == "Twitter":
        strategies.append("Limit to 1-2 hashtags to maintain readability")
    elif platform == "TikTok":
        strategies.append("Use trending sounds and hashtags for algorithm boost")

    return strategies


def generate_sample_engagement_data():
    """Generate sample engagement data for analytics"""
    platforms = ["Instagram", "Twitter", "Facebook", "LinkedIn"]
    post_types = ["Image", "Video", "Text", "Carousel"]

    data = []
    for i in range(20):
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        likes = random.randint(50, 1000)
        comments = random.randint(5, 100)
        shares = random.randint(1, 50)

        data.append({
            'post_type': random.choice(post_types),
            'platform': random.choice(platforms),
            'date': date.isoformat(),
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'engagement_rate': calculate_engagement_rate(likes, comments, shares)
        })

    return data


def calculate_engagement_rate(likes, comments, shares, followers=1000):
    """Calculate engagement rate"""
    total_engagement = likes + comments + shares
    return total_engagement / followers


def analyze_platform_performance(engagement_data):
    """Analyze performance by platform"""
    platform_stats = {}

    for post in engagement_data:
        platform = post.get('platform')
        if platform not in platform_stats:
            platform_stats[platform] = {
                'posts': 0,
                'total_likes': 0,
                'total_engagement': 0
            }

        platform_stats[platform]['posts'] += 1
        platform_stats[platform]['total_likes'] += post.get('likes', 0)
        platform_stats[platform]['total_engagement'] += post.get('engagement_rate', 0)

    # Calculate averages
    for platform, stats in platform_stats.items():
        stats['avg_likes'] = stats['total_likes'] / stats['posts'] if stats['posts'] > 0 else 0
        stats['avg_engagement'] = stats['total_engagement'] / stats['posts'] if stats['posts'] > 0 else 0

    return platform_stats


def generate_engagement_report(engagement_data, platform_stats):
    """Generate engagement analytics report"""
    report = "SOCIAL MEDIA ENGAGEMENT ANALYTICS REPORT\n"
    report += "=" * 50 + "\n\n"
    report += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"Analysis Period: Last 30 days\n\n"

    # Overall stats
    total_posts = len(engagement_data)
    total_likes = sum(post.get('likes', 0) for post in engagement_data)
    total_comments = sum(post.get('comments', 0) for post in engagement_data)
    total_shares = sum(post.get('shares', 0) for post in engagement_data)

    report += "OVERALL PERFORMANCE:\n"
    report += f"Total Posts: {total_posts}\n"
    report += f"Total Likes: {total_likes:,}\n"
    report += f"Total Comments: {total_comments:,}\n"
    report += f"Total Shares: {total_shares:,}\n\n"

    # Platform breakdown
    report += "PLATFORM PERFORMANCE:\n"
    for platform, stats in platform_stats.items():
        report += f"\n{platform}:\n"
        report += f"  Posts: {stats['posts']}\n"
        report += f"  Avg Likes: {stats['avg_likes']:.0f}\n"
        report += f"  Avg Engagement Rate: {stats['avg_engagement']:.2%}\n"

    return report


def create_post_generation_prompt(platform, post_type, topic, tone, audience, hashtags, cta, keywords, length, emoji):
    """Create prompt for post generation"""
    prompt = f"""
    Create a {post_type.lower()} social media post for {platform} about "{topic}".

    Requirements:
    - Tone: {tone}
    - Target Audience: {audience}
    - Post Length: {length}
    - Emoji Usage: {emoji}
    """

    if hashtags:
        prompt += f"\n- Include relevant hashtags"

    if cta:
        prompt += f"\n- Include this call to action: {cta}"

    if keywords:
        prompt += f"\n- Include these keywords: {keywords}"

    prompt += f"\n\nMake it engaging and optimized for {platform}."

    return prompt


def analyze_generated_post(post, platform):
    """Analyze generated post metrics"""
    char_count = len(post)
    word_count = len(post.split())
    hashtag_count = post.count('#')

    return {
        'char_count': char_count,
        'word_count': word_count,
        'hashtag_count': hashtag_count
    }


def get_platform_feedback(post, platform):
    """Get platform-specific optimization feedback"""
    feedback = []
    char_count = len(post)

    if platform == "Twitter" and char_count > 280:
        feedback.append("Post exceeds Twitter's 280 character limit")
    elif platform == "Instagram" and char_count > 2200:
        feedback.append("Post exceeds Instagram's caption limit")

    if platform == "LinkedIn" and not any(word in post.lower() for word in ['professional', 'business', 'career']):
        feedback.append("Consider adding professional context for LinkedIn")

    return feedback


def generate_post_variations(original_post, platform):
    """Generate variations of the original post"""
    variations = []

    # This would use AI to create variations
    variations.append(f"Variation 1: {original_post[:100]}... (shortened)")
    variations.append(f"Variation 2: {original_post} (with different hashtags)")
    variations.append(f"Variation 3: Question format - What do you think about {original_post[:50]}?")

    return variations


def create_caption_prompt(theme, platform, style, voice, mood, length, brand_info, message):
    """Create prompt for caption generation"""
    prompt = f"""
    Write a {length.lower()} {style.lower()} caption for {platform} about "{theme}".

    Style Requirements:
    - Brand Voice: {voice}
    - Target Mood: {mood}
    - Caption Style: {style}
    """

    if brand_info:
        prompt += f"\n- Brand Context: {brand_info}"

    if message:
        prompt += f"\n- Include Message/CTA: {message}"

    prompt += f"\n\nMake it engaging and authentic for {platform}."

    return prompt


def analyze_caption_metrics(caption, platform):
    """Analyze caption metrics"""
    return {
        'characters': len(caption),
        'words': len(caption.split()),
        'hashtags': caption.count('#'),
        'mentions': caption.count('@')
    }


def get_caption_optimization(caption, platform):
    """Get caption optimization tips"""
    tips = []

    if platform == "Instagram":
        if caption.count('#') < 5:
            tips.append("Consider adding more hashtags (5-11 recommended for Instagram)")
        if len(caption) < 100:
            tips.append("Instagram captions can be longer - consider expanding your story")

    elif platform == "Twitter":
        if len(caption) > 240:
            tips.append("Consider shortening for Twitter (280 char limit)")
        if caption.count('#') > 2:
            tips.append("Twitter posts work better with 1-2 hashtags")

    return tips


# Placeholder functions for remaining tools
def parse_hashtag_response(response):
    """Parse text response into hashtag categories"""
    return {
        'recommended': ['example1', 'example2', 'example3'],
        'popular': ['popular1', 'popular2', 'popular3'],
        'niche': ['niche1', 'niche2', 'niche3'],
        'trending': ['trending1', 'trending2', 'trending3']
    }


def generate_fallback_hashtags(topic, platform, industry):
    """Generate fallback hashtag data"""
    return {
        'recommended': [f'{topic}', f'{industry}', f'{platform}content'],
        'popular': ['trending', 'viral', 'popular'],
        'niche': [f'{topic}community', f'{industry}life', 'niche'],
        'trending': ['trend1', 'trend2', 'trend3']
    }


# Additional placeholder functions
def audience_segmentation():
    """Audience segmentation tool"""
    st.info("Audience Segmentation - Coming soon!")


def campaign_planner():
    """Campaign planning tool"""
    st.info("Campaign Planner - Coming soon!")


def mention_monitor():
    """Social media mention monitor"""
    st.info("Mention Monitor - Coming soon!")


def influencer_finder():
    """Influencer discovery tool"""
    st.info("Influencer Finder - Coming soon!")


def cross_platform_posting():
    """Cross-platform posting tool"""
    st.info("Cross-Platform Posting - Coming soon!")


def trending_hashtags():
    """Trending hashtag discovery"""
    st.info("Trending Hashtags - Coming soon!")


def performance_tracker():
    """Performance tracking tool"""
    st.info("Performance Tracker - Coming soon!")


def ab_testing():
    """A/B testing tool"""
    st.info("A/B Testing - Coming soon!")


def brand_tracking():
    """Brand tracking tool"""
    st.info("Brand Tracking - Coming soon!")
