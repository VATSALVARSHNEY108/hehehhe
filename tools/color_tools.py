import streamlit as st
import colorsys
import re
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all color tools"""

    tool_categories = {
        "Color Converters": [
            "RGB to HEX", "HEX to RGB", "HSL Converter", "CMYK Converter", "Color Name Finder"
        ],
        "Palette Tools": [
            "Color Palette Generator", "Gradient Creator", "Complementary Colors", "Analogous Colors", "Triadic Colors"
        ],
        "Color Analysis": [
            "Color Contrast Checker", "Accessibility Validator", "Color Blindness Simulator", "Color Harmony Analyzer"
        ],
        "Image Color Tools": [
            "Dominant Color Extractor", "Color Replacement", "Color Filter", "Monochrome Converter"
        ],
        "Design Tools": [
            "Material Design Colors", "Flat UI Colors", "Web Safe Colors", "Brand Color Extractor"
        ],
        "Color Schemes": [
            "Random Color Generator", "Seasonal Palettes", "Trending Colors", "Custom Scheme Builder"
        ]
    }

    selected_category = st.selectbox("Select Color Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Color Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "RGB to HEX":
        rgb_to_hex()
    elif selected_tool == "HEX to RGB":
        hex_to_rgb()
    elif selected_tool == "Color Palette Generator":
        palette_generator()
    elif selected_tool == "Color Contrast Checker":
        contrast_checker()
    elif selected_tool == "Dominant Color Extractor":
        dominant_color_extractor()
    elif selected_tool == "Random Color Generator":
        random_color_generator()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def rgb_to_hex():
    """Convert RGB values to HEX"""
    create_tool_header("RGB to HEX Converter", "Convert RGB color values to hexadecimal format", "🎨")

    col1, col2, col3 = st.columns(3)
    with col1:
        r = st.slider("Red", 0, 255, 128)
    with col2:
        g = st.slider("Green", 0, 255, 128)
    with col3:
        b = st.slider("Blue", 0, 255, 128)

    hex_color = f"#{r:02x}{g:02x}{b:02x}"

    st.markdown(f"### HEX Color: `{hex_color}`")
    st.color_picker("Color Preview", hex_color, disabled=True)


def hex_to_rgb():
    """Convert HEX to RGB values"""
    create_tool_header("HEX to RGB Converter", "Convert hexadecimal color values to RGB format", "🎨")

    hex_input = st.text_input("Enter HEX color (e.g., #FF5733 or FF5733):", "#FF5733")

    # Clean hex input
    hex_clean = hex_input.strip().lstrip('#')

    if len(hex_clean) == 6 and all(c in '0123456789ABCDEFabcdef' for c in hex_clean):
        r = int(hex_clean[0:2], 16)
        g = int(hex_clean[2:4], 16)
        b = int(hex_clean[4:6], 16)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Red", r)
        with col2:
            st.metric("Green", g)
        with col3:
            st.metric("Blue", b)

        st.color_picker("Color Preview", f"#{hex_clean}", disabled=True)
    else:
        st.error("Please enter a valid HEX color code")


def palette_generator():
    """Generate color palettes"""
    create_tool_header("Color Palette Generator", "Generate beautiful color palettes", "🌈")

    base_color = st.color_picker("Choose base color:", "#3498db")
    palette_type = st.selectbox("Palette Type:", ["Monochromatic", "Complementary", "Triadic", "Analogous"])

    if st.button("Generate Palette"):
        colors = generate_palette(base_color, palette_type)

        col1, col2, col3, col4, col5 = st.columns(5)
        for i, color in enumerate(colors):
            with [col1, col2, col3, col4, col5][i]:
                st.color_picker(f"Color {i + 1}", color, disabled=True)
                st.code(color)


def generate_palette(base_color, palette_type):
    """Generate color palette based on type"""
    # Convert hex to HSV
    hex_clean = base_color.lstrip('#')
    r, g, b = int(hex_clean[0:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

    colors = [base_color]

    if palette_type == "Monochromatic":
        for i in range(1, 5):
            new_s = max(0.1, s - i * 0.15)
            new_v = min(1.0, v + i * 0.1)
            rgb = colorsys.hsv_to_rgb(h, new_s, new_v)
            hex_color = f"#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}"
            colors.append(hex_color)
    elif palette_type == "Complementary":
        comp_h = (h + 0.5) % 1.0
        rgb = colorsys.hsv_to_rgb(comp_h, s, v)
        hex_color = f"#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}"
        colors.append(hex_color)
        # Add variations
        for i in range(3):
            var_s = max(0.1, s - i * 0.2)
            var_v = min(1.0, v + i * 0.15)
            rgb = colorsys.hsv_to_rgb(comp_h, var_s, var_v)
            hex_color = f"#{int(rgb[0] * 255):02x}{int(rgb[1] * 255):02x}{int(rgb[2] * 255):02x}"
            colors.append(hex_color)

    return colors[:5]


def contrast_checker():
    """Check color contrast for accessibility"""
    create_tool_header("Color Contrast Checker", "Check color contrast ratios for accessibility", "♿")

    col1, col2 = st.columns(2)
    with col1:
        fg_color = st.color_picker("Foreground Color:", "#000000")
    with col2:
        bg_color = st.color_picker("Background Color:", "#FFFFFF")

    # Calculate contrast ratio
    ratio = calculate_contrast_ratio(fg_color, bg_color)

    st.markdown(f"### Contrast Ratio: {ratio:.2f}:1")

    # WCAG compliance
    if ratio >= 7:
        st.success("✅ AAA compliant (excellent accessibility)")
    elif ratio >= 4.5:
        st.success("✅ AA compliant (good accessibility)")
    elif ratio >= 3:
        st.warning("⚠️ AA Large compliant (acceptable for large text)")
    else:
        st.error("❌ Does not meet accessibility standards")

    # Preview
    st.markdown(f"""
    <div style="background-color: {bg_color}; color: {fg_color}; padding: 20px; border-radius: 8px;">
        <h3>Sample Text Preview</h3>
        <p>This is how your text will look with these colors.</p>
    </div>
    """, unsafe_allow_html=True)


def calculate_contrast_ratio(fg_color, bg_color):
    """Calculate the contrast ratio between two colors"""

    def hex_to_rgb(hex_color):
        hex_clean = hex_color.lstrip('#')
        return tuple(int(hex_clean[i:i + 2], 16) for i in (0, 2, 4))

    def luminance(rgb):
        rgb_normalized = [c / 255.0 for c in rgb]
        rgb_gamma = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb_normalized]
        return 0.2126 * rgb_gamma[0] + 0.7152 * rgb_gamma[1] + 0.0722 * rgb_gamma[2]

    fg_rgb = hex_to_rgb(fg_color)
    bg_rgb = hex_to_rgb(bg_color)

    fg_lum = luminance(fg_rgb)
    bg_lum = luminance(bg_rgb)

    lighter = max(fg_lum, bg_lum)
    darker = min(fg_lum, bg_lum)

    return (lighter + 0.05) / (darker + 0.05)


def dominant_color_extractor():
    """Extract dominant colors from an image"""
    create_tool_header("Dominant Color Extractor", "Extract the main colors from any image", "🖼️")

    uploaded_file = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=False)

    if uploaded_file:
        image = FileHandler.process_image_file(uploaded_file[0])
        if image:
            st.image(image, caption="Uploaded Image", use_column_width=True)

            num_colors = st.slider("Number of colors to extract:", 2, 10, 5)

            if st.button("Extract Colors"):
                colors = extract_dominant_colors(image, num_colors)

                st.markdown("### Dominant Colors:")
                cols = st.columns(len(colors))
                for i, color in enumerate(colors):
                    hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                    with cols[i]:
                        st.color_picker(f"Color {i + 1}", hex_color, disabled=True)
                        st.code(hex_color)


def extract_dominant_colors(image, num_colors):
    """Extract dominant colors using k-means clustering"""
    from sklearn.cluster import KMeans

    # Convert image to numpy array
    img_array = np.array(image)
    img_data = img_array.reshape((-1, 3))

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=num_colors, random_state=42)
    kmeans.fit(img_data)

    # Get the colors
    colors = kmeans.cluster_centers_.astype(int)
    return colors


def random_color_generator():
    """Generate random colors"""
    create_tool_header("Random Color Generator", "Generate random colors for inspiration", "🎲")

    if st.button("Generate Random Colors"):
        colors = []
        for _ in range(5):
            r = np.random.randint(0, 256)
            g = np.random.randint(0, 256)
            b = np.random.randint(0, 256)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            colors.append(hex_color)

        cols = st.columns(5)
        for i, color in enumerate(colors):
            with cols[i]:
                st.color_picker(f"Color {i + 1}", color, disabled=True)
                st.code(color)