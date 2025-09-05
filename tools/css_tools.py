import streamlit as st
import re
import json
import colorsys
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler


def display_tools():
    """Display all CSS tools"""

    tool_categories = {
        "CSS Generators": [
            "Gradient Generator", "Shadow Generator", "Border Radius Generator", "Flexbox Generator", "Grid Generator"
        ],
        "CSS Preprocessors": [
            "SASS/SCSS Compiler", "LESS Processor", "Stylus Compiler", "CSS Variables Generator"
        ],
        "CSS Validators": [
            "Syntax Validator", "Property Checker", "Browser Compatibility", "CSS Linter"
        ],
        "CSS Minifiers": [
            "Code Minifier", "Whitespace Remover", "Comment Stripper", "Property Optimizer"
        ],
        "CSS Beautifiers": [
            "Code Formatter", "Indentation Fixer", "Property Organizer", "Structure Improver"
        ],
        "CSS Color Tools": [
            "Color Picker", "Palette Generator", "Color Scheme Creator", "Accessibility Checker"
        ],
        "CSS Layout Tools": [
            "Flexbox Layout", "Grid Layout", "Responsive Layout", "CSS Framework Tools"
        ],
        "CSS Animation Tools": [
            "Keyframe Generator", "Transition Builder", "Animation Preview", "Easing Functions"
        ],
        "CSS Framework Utilities": [
            "Bootstrap Helper", "Tailwind Utilities", "Foundation Tools", "Custom Framework"
        ],
        "CSS Debugging Tools": [
            "Selector Tester", "Specificity Calculator", "Cascade Analyzer", "Property Inspector"
        ]
    }

    selected_category = st.selectbox("Select CSS Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"CSS Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Gradient Generator":
        gradient_generator()
    elif selected_tool == "Shadow Generator":
        shadow_generator()
    elif selected_tool == "Border Radius Generator":
        border_radius_generator()
    elif selected_tool == "Flexbox Generator":
        flexbox_generator()
    elif selected_tool == "Code Minifier":
        css_minifier()
    elif selected_tool == "Code Formatter":
        css_formatter()
    elif selected_tool == "Color Picker":
        css_color_picker()
    elif selected_tool == "Syntax Validator":
        css_validator()
    elif selected_tool == "Keyframe Generator":
        keyframe_generator()
    elif selected_tool == "Selector Tester":
        selector_tester()
    elif selected_tool == "Specificity Calculator":
        specificity_calculator()
    elif selected_tool == "Grid Generator":
        grid_generator()
    elif selected_tool == "Responsive Layout":
        responsive_layout()
    elif selected_tool == "Bootstrap Helper":
        bootstrap_helper()
    elif selected_tool == "Transition Builder":
        transition_builder()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def gradient_generator():
    """CSS gradient generator"""
    create_tool_header("Gradient Generator", "Create beautiful CSS gradients", "🌈")

    gradient_type = st.selectbox("Gradient Type", ["Linear", "Radial", "Conic"])

    if gradient_type == "Linear":
        direction = st.selectbox("Direction", [
            "to right", "to left", "to top", "to bottom",
            "to top right", "to top left", "to bottom right", "to bottom left",
            "45deg", "90deg", "135deg", "180deg", "270deg"
        ])
    elif gradient_type == "Radial":
        shape = st.selectbox("Shape", ["circle", "ellipse"])
        position = st.selectbox("Position", ["center", "top", "bottom", "left", "right"])

    # Color stops
    st.subheader("Color Stops")

    num_colors = st.slider("Number of colors", 2, 8, 2)
    colors = []
    positions = []

    for i in range(num_colors):
        col1, col2 = st.columns(2)
        with col1:
            color = st.color_picker(f"Color {i + 1}", f"#{'ff0000' if i == 0 else '00ff00' if i == 1 else 'ff00ff'}",
                                    key=f"grad_color_{i}")
            colors.append(color)
        with col2:
            if i == 0:
                position = st.number_input(f"Position {i + 1} (%)", 0, 100, 0, key=f"grad_pos_{i}")
            elif i == num_colors - 1:
                position = st.number_input(f"Position {i + 1} (%)", 0, 100, 100, key=f"grad_pos_{i}")
            else:
                position = st.number_input(f"Position {i + 1} (%)", 0, 100, (100 // (num_colors - 1)) * i,
                                           key=f"grad_pos_{i}")
            positions.append(position)

    # Generate gradient CSS
    if gradient_type == "Linear":
        color_stops = [f"{colors[i]} {positions[i]}%" for i in range(num_colors)]
        gradient_css = f"background: linear-gradient({direction}, {', '.join(color_stops)});"
    elif gradient_type == "Radial":
        color_stops = [f"{colors[i]} {positions[i]}%" for i in range(num_colors)]
        gradient_css = f"background: radial-gradient({shape} at {position}, {', '.join(color_stops)});"
    else:  # Conic
        color_stops = [f"{colors[i]} {positions[i]}%" for i in range(num_colors)]
        gradient_css = f"background: conic-gradient({', '.join(color_stops)});"

    # Display preview
    st.subheader("Preview")
    preview_html = f"""
    <div style="{gradient_css} width: 300px; height: 200px; border: 1px solid #ccc; border-radius: 10px; margin: 20px 0;"></div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)

    # Display CSS code
    st.subheader("CSS Code")
    st.code(gradient_css, language="css")

    # Additional CSS variations
    st.subheader("Complete CSS (with vendor prefixes)")
    complete_css = f"""/* Gradient CSS */
.gradient-element {{
    {gradient_css}
    /* Fallback for older browsers */
    background: {colors[0]};
}}"""

    st.code(complete_css, language="css")

    # Download
    FileHandler.create_download_link(complete_css.encode(), "gradient.css", "text/css")


def shadow_generator():
    """CSS box shadow generator"""
    create_tool_header("Shadow Generator", "Create CSS box shadows", "📦")

    shadow_type = st.selectbox("Shadow Type", ["Box Shadow", "Text Shadow", "Drop Shadow (filter)"])

    if shadow_type == "Box Shadow":
        st.subheader("Box Shadow Properties")

        col1, col2 = st.columns(2)
        with col1:
            h_offset = st.slider("Horizontal Offset (px)", -100, 100, 10)
            v_offset = st.slider("Vertical Offset (px)", -100, 100, 10)
            blur_radius = st.slider("Blur Radius (px)", 0, 100, 10)
            spread_radius = st.slider("Spread Radius (px)", -100, 100, 0)

        with col2:
            shadow_color = st.color_picker("Shadow Color", "#000000")
            opacity = st.slider("Opacity", 0.0, 1.0, 0.5, 0.1)
            inset = st.checkbox("Inset Shadow")

        # Convert color to rgba
        hex_color = shadow_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        rgba_color = f"rgba({r}, {g}, {b}, {opacity})"

        # Generate shadow CSS
        inset_text = "inset " if inset else ""
        shadow_css = f"box-shadow: {inset_text}{h_offset}px {v_offset}px {blur_radius}px {spread_radius}px {rgba_color};"

        # Preview
        st.subheader("Preview")
        preview_html = f"""
        <div style="width: 200px; height: 150px; background: #f0f0f0; margin: 50px auto; {shadow_css} border-radius: 10px; display: flex; align-items: center; justify-content: center;">
            <span style="color: #666;">Preview Box</span>
        </div>
        """
        st.markdown(preview_html, unsafe_allow_html=True)

    elif shadow_type == "Text Shadow":
        st.subheader("Text Shadow Properties")

        col1, col2 = st.columns(2)
        with col1:
            h_offset = st.slider("Horizontal Offset (px)", -50, 50, 2)
            v_offset = st.slider("Vertical Offset (px)", -50, 50, 2)
            blur_radius = st.slider("Blur Radius (px)", 0, 50, 4)

        with col2:
            shadow_color = st.color_picker("Shadow Color", "#000000")
            text_color = st.color_picker("Text Color", "#333333")
            font_size = st.slider("Font Size (px)", 16, 72, 36)

        shadow_css = f"text-shadow: {h_offset}px {v_offset}px {blur_radius}px {shadow_color};"

        # Preview
        st.subheader("Preview")
        preview_html = f"""
        <div style="text-align: center; padding: 30px;">
            <h2 style="color: {text_color}; font-size: {font_size}px; {shadow_css} margin: 0;">
                Sample Text
            </h2>
        </div>
        """
        st.markdown(preview_html, unsafe_allow_html=True)

    # Display CSS
    st.subheader("CSS Code")
    st.code(shadow_css, language="css")

    FileHandler.create_download_link(shadow_css.encode(), "shadow.css", "text/css")


def border_radius_generator():
    """CSS border radius generator"""
    create_tool_header("Border Radius Generator", "Create custom border radius", "📐")

    mode = st.radio("Mode", ["Simple", "Advanced"])

    if mode == "Simple":
        radius = st.slider("Border Radius (px)", 0, 100, 10)
        border_radius_css = f"border-radius: {radius}px;"
    else:
        st.subheader("Individual Corner Control")

        col1, col2 = st.columns(2)
        with col1:
            top_left = st.slider("Top Left (px)", 0, 100, 10)
            bottom_left = st.slider("Bottom Left (px)", 0, 100, 10)
        with col2:
            top_right = st.slider("Top Right (px)", 0, 100, 10)
            bottom_right = st.slider("Bottom Right (px)", 0, 100, 10)

        border_radius_css = f"border-radius: {top_left}px {top_right}px {bottom_right}px {bottom_left}px;"

    # Preview
    st.subheader("Preview")
    preview_html = f"""
    <div style="width: 200px; height: 150px; background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
                margin: 30px auto; {border_radius_css} display: flex; align-items: center; justify-content: center;">
        <span style="color: white; font-weight: bold;">Preview</span>
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)

    # CSS Code
    st.subheader("CSS Code")
    st.code(border_radius_css, language="css")

    # Additional examples
    st.subheader("Common Shapes")
    examples = {
        "Circle": "border-radius: 50%;",
        "Pill": "border-radius: 25px;",
        "Rounded Rectangle": "border-radius: 15px;",
        "Leaf": "border-radius: 0 100% 0 100%;"
    }

    for shape, css in examples.items():
        if st.button(f"Use {shape}"):
            st.code(css, language="css")


def flexbox_generator():
    """CSS Flexbox generator"""
    create_tool_header("Flexbox Generator", "Generate CSS Flexbox layouts", "📏")

    st.subheader("Container Properties")

    col1, col2 = st.columns(2)
    with col1:
        flex_direction = st.selectbox("Flex Direction", ["row", "row-reverse", "column", "column-reverse"])
        flex_wrap = st.selectbox("Flex Wrap", ["nowrap", "wrap", "wrap-reverse"])
        justify_content = st.selectbox("Justify Content", [
            "flex-start", "flex-end", "center", "space-between", "space-around", "space-evenly"
        ])

    with col2:
        align_items = st.selectbox("Align Items", [
            "stretch", "flex-start", "flex-end", "center", "baseline"
        ])
        align_content = st.selectbox("Align Content", [
            "stretch", "flex-start", "flex-end", "center", "space-between", "space-around"
        ])
        gap = st.slider("Gap (px)", 0, 50, 10)

    # Generate container CSS
    container_css = f"""display: flex;
flex-direction: {flex_direction};
flex-wrap: {flex_wrap};
justify-content: {justify_content};
align-items: {align_items};
align-content: {align_content};
gap: {gap}px;"""

    # Item properties
    st.subheader("Item Properties")
    num_items = st.slider("Number of Items", 1, 6, 3)

    item_properties = []
    for i in range(num_items):
        with st.expander(f"Item {i + 1} Properties"):
            col1, col2, col3 = st.columns(3)
            with col1:
                flex_grow = st.number_input(f"Flex Grow", 0, 10, 1, key=f"grow_{i}")
            with col2:
                flex_shrink = st.number_input(f"Flex Shrink", 0, 10, 1, key=f"shrink_{i}")
            with col3:
                align_self = st.selectbox(f"Align Self",
                                          ["auto", "flex-start", "flex-end", "center", "baseline", "stretch"],
                                          key=f"align_{i}")

            item_properties.append({
                "flex_grow": flex_grow,
                "flex_shrink": flex_shrink,
                "align_self": align_self
            })

    # Preview
    st.subheader("Preview")

    items_html = ""
    for i, props in enumerate(item_properties):
        item_style = f"""
        flex: {props['flex_grow']} {props['flex_shrink']} auto;
        align-self: {props['align_self']};
        background: hsl({i * 60}, 70%, 60%);
        padding: 20px;
        margin: 5px;
        border-radius: 5px;
        color: white;
        text-align: center;
        """
        items_html += f'<div style="{item_style}">Item {i + 1}</div>'

    preview_html = f"""
    <div style="{container_css} border: 2px dashed #ccc; padding: 20px; min-height: 200px;">
        {items_html}
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)

    # CSS Output
    st.subheader("CSS Code")

    complete_css = f""".flex-container {{
{container_css}
}}

/* Item styles */"""

    for i, props in enumerate(item_properties):
        complete_css += f"""
.flex-item-{i + 1} {{
    flex: {props['flex_grow']} {props['flex_shrink']} auto;
    align-self: {props['align_self']};
}}"""

    st.code(complete_css, language="css")

    FileHandler.create_download_link(complete_css.encode(), "flexbox.css", "text/css")


def css_minifier():
    """CSS minification tool"""
    create_tool_header("CSS Minifier", "Minify CSS code for production", "🗜️")

    # File upload option
    uploaded_file = FileHandler.upload_files(['css'], accept_multiple=False)

    if uploaded_file:
        css_content = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded CSS", css_content, height=200, disabled=True)
    else:
        css_content = st.text_area("Enter CSS code to minify:", height=300, value="""/* Sample CSS */
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    margin: 10px;
    background-color: #f0f0f0;
    border-radius: 5px;
}

.button {
    background: linear-gradient(45deg, #007bff, #0056b3);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}""")

    if css_content:
        # Minification options
        col1, col2 = st.columns(2)
        with col1:
            remove_comments = st.checkbox("Remove Comments", True)
            remove_whitespace = st.checkbox("Remove Whitespace", True)
            remove_empty_rules = st.checkbox("Remove Empty Rules", True)
        with col2:
            merge_selectors = st.checkbox("Merge Identical Selectors", True)
            shorten_colors = st.checkbox("Shorten Color Values", True)
            remove_semicolons = st.checkbox("Remove Last Semicolons", True)

        if st.button("Minify CSS"):
            minified_css = minify_css(css_content, {
                'remove_comments': remove_comments,
                'remove_whitespace': remove_whitespace,
                'remove_empty_rules': remove_empty_rules,
                'merge_selectors': merge_selectors,
                'shorten_colors': shorten_colors,
                'remove_semicolons': remove_semicolons
            })

            # Show results
            st.subheader("Minified CSS")
            st.code(minified_css, language="css")

            # Statistics
            original_size = len(css_content)
            minified_size = len(minified_css)
            reduction = ((original_size - minified_size) / original_size * 100) if original_size > 0 else 0

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Original Size", f"{original_size:,} bytes")
            with col2:
                st.metric("Minified Size", f"{minified_size:,} bytes")
            with col3:
                st.metric("Size Reduction", f"{reduction:.1f}%")

            FileHandler.create_download_link(minified_css.encode(), "minified.css", "text/css")


def css_formatter():
    """CSS code formatter"""
    create_tool_header("CSS Formatter", "Format and beautify CSS code", "✨")

    # File upload option
    uploaded_file = FileHandler.upload_files(['css'], accept_multiple=False)

    if uploaded_file:
        css_content = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded CSS", css_content, height=200, disabled=True)
    else:
        css_content = st.text_area("Enter CSS code to format:", height=300,
                                   value=""".container{display:flex;justify-content:center;align-items:center;padding:20px;margin:10px;}.button{background:#007bff;color:white;padding:10px 20px;border:none;border-radius:4px;cursor:pointer;}.button:hover{background:#0056b3;}""")

    if css_content:
        # Formatting options
        col1, col2 = st.columns(2)
        with col1:
            indent_size = st.selectbox("Indent Size", [2, 4, 8], index=1)
            indent_type = st.selectbox("Indent Type", ["Spaces", "Tabs"])
            brace_style = st.selectbox("Brace Style", ["Same Line", "New Line"])
        with col2:
            sort_properties = st.checkbox("Sort Properties Alphabetically", False)
            add_missing_semicolons = st.checkbox("Add Missing Semicolons", True)
            normalize_quotes = st.checkbox("Normalize Quotes", True)

        if st.button("Format CSS"):
            formatted_css = format_css(css_content, {
                'indent_size': indent_size,
                'indent_type': indent_type,
                'brace_style': brace_style,
                'sort_properties': sort_properties,
                'add_missing_semicolons': add_missing_semicolons,
                'normalize_quotes': normalize_quotes
            })

            st.subheader("Formatted CSS")
            st.code(formatted_css, language="css")

            FileHandler.create_download_link(formatted_css.encode(), "formatted.css", "text/css")


def css_color_picker():
    """Advanced CSS color picker and palette generator"""
    create_tool_header("CSS Color Picker", "Pick colors and generate palettes", "🎨")

    tab1, tab2, tab3 = st.tabs(["Color Picker", "Palette Generator", "Color Converter"])

    with tab1:
        st.subheader("Color Selection")

        color = st.color_picker("Pick a color", "#007bff")

        # Convert to different formats
        hex_color = color
        hex_short = shorten_hex_color(hex_color)
        rgb = hex_to_rgb(hex_color)
        hsl = rgb_to_hsl(rgb)

        col1, col2 = st.columns(2)
        with col1:
            st.code(f"HEX: {hex_color}")
            st.code(f"HEX (short): {hex_short}")
            st.code(f"RGB: rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")
        with col2:
            st.code(f"HSL: hsl({hsl[0]}, {hsl[1]}%, {hsl[2]}%)")
            st.code(f"CSS Variable: var(--primary-color)")
            st.code(f"RGBA: rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 1)")

        # Color variations
        st.subheader("Color Variations")
        variations = generate_color_variations(hex_color)

        for variation_name, variation_color in variations.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(
                    f'<div style="width:50px;height:30px;background-color:{variation_color};border:1px solid #000;"></div>',
                    unsafe_allow_html=True)
            with col2:
                st.code(f"{variation_name}: {variation_color}")

    with tab2:
        st.subheader("Color Palette Generator")

        base_color = st.color_picker("Base color", "#007bff", key="palette_base")
        palette_type = st.selectbox("Palette Type", [
            "Monochromatic", "Analogous", "Complementary", "Triadic", "Tetradic"
        ])

        if st.button("Generate Palette"):
            palette = generate_color_palette(base_color, palette_type)

            st.subheader(f"{palette_type} Palette")

            # Display palette
            palette_html = '<div style="display: flex; margin: 20px 0;">'
            for i, color in enumerate(palette):
                palette_html += f'''
                <div style="width: 80px; height: 80px; background-color: {color}; 
                           border: 1px solid #ccc; margin-right: 10px; 
                           display: flex; align-items: end; justify-content: center; color: white;">
                    <small style="background: rgba(0,0,0,0.7); padding: 2px 4px; margin: 5px;">{color}</small>
                </div>
                '''
            palette_html += '</div>'

            st.markdown(palette_html, unsafe_allow_html=True)

            # CSS Variables
            css_vars = ":root {\n"
            for i, color in enumerate(palette):
                css_vars += f"  --color-{i + 1}: {color};\n"
            css_vars += "}"

            st.subheader("CSS Variables")
            st.code(css_vars, language="css")

            FileHandler.create_download_link(css_vars.encode(), "color-palette.css", "text/css")

    with tab3:
        st.subheader("Color Format Converter")

        input_format = st.selectbox("Input Format", ["HEX", "RGB", "HSL"])

        if input_format == "HEX":
            hex_input = st.text_input("HEX Color", "#007bff")
            if hex_input:
                try:
                    rgb = hex_to_rgb(hex_input)
                    hsl = rgb_to_hsl(rgb)

                    st.write(f"**RGB**: rgb({rgb[0]}, {rgb[1]}, {rgb[2]})")
                    st.write(f"**HSL**: hsl({hsl[0]}, {hsl[1]}%, {hsl[2]}%)")
                except:
                    st.error("Invalid HEX color format")

        elif input_format == "RGB":
            col1, col2, col3 = st.columns(3)
            with col1:
                r = st.number_input("Red", 0, 255, 0)
            with col2:
                g = st.number_input("Green", 0, 255, 123)
            with col3:
                b = st.number_input("Blue", 0, 255, 255)

            hex_result = rgb_to_hex((r, g, b))
            hsl_result = rgb_to_hsl((r, g, b))

            st.write(f"**HEX**: {hex_result}")
            st.write(f"**HSL**: hsl({hsl_result[0]}, {hsl_result[1]}%, {hsl_result[2]}%)")


def css_validator():
    """CSS syntax validator"""
    create_tool_header("CSS Validator", "Validate CSS syntax and properties", "✅")

    # File upload option
    uploaded_file = FileHandler.upload_files(['css'], accept_multiple=False)

    if uploaded_file:
        css_content = FileHandler.process_text_file(uploaded_file[0])
        st.text_area("Uploaded CSS", css_content, height=200, disabled=True)
    else:
        css_content = st.text_area("Enter CSS code to validate:", height=300)

    if css_content and st.button("Validate CSS"):
        validation_results = validate_css(css_content)

        # Display results
        if validation_results['errors']:
            st.subheader("❌ Errors Found")
            for error in validation_results['errors']:
                st.error(f"Line {error['line']}: {error['message']}")

        if validation_results['warnings']:
            st.subheader("⚠️ Warnings")
            for warning in validation_results['warnings']:
                st.warning(f"Line {warning['line']}: {warning['message']}")

        if not validation_results['errors'] and not validation_results['warnings']:
            st.success("✅ No issues found! Your CSS is valid.")

        # Statistics
        st.subheader("Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rules", validation_results['stats']['rules'])
        with col2:
            st.metric("Properties", validation_results['stats']['properties'])
        with col3:
            st.metric("Selectors", validation_results['stats']['selectors'])
        with col4:
            st.metric("Errors", len(validation_results['errors']))


def keyframe_generator():
    """CSS keyframe animation generator"""
    create_tool_header("Keyframe Generator", "Create CSS keyframe animations", "🎬")

    animation_name = st.text_input("Animation Name", "myAnimation")

    # Keyframes
    st.subheader("Animation Keyframes")

    num_keyframes = st.slider("Number of Keyframes", 2, 10, 3)
    keyframes = []

    for i in range(num_keyframes):
        with st.expander(f"Keyframe {i + 1}"):
            col1, col2 = st.columns(2)
            with col1:
                if i == 0:
                    percentage = st.number_input("Percentage", 0, 100, 0, key=f"kf_pct_{i}", disabled=True)
                elif i == num_keyframes - 1:
                    percentage = st.number_input("Percentage", 0, 100, 100, key=f"kf_pct_{i}", disabled=True)
                else:
                    percentage = st.number_input("Percentage", 0, 100, (100 // (num_keyframes - 1)) * i,
                                                 key=f"kf_pct_{i}")

            with col2:
                properties = st.text_area("CSS Properties", "transform: translateX(0px);\nopacity: 1;",
                                          height=100, key=f"kf_props_{i}")

            keyframes.append({
                'percentage': percentage,
                'properties': properties
            })

    # Animation properties
    st.subheader("Animation Properties")
    col1, col2 = st.columns(2)
    with col1:
        duration = st.number_input("Duration (seconds)", 0.1, 60.0, 2.0, 0.1)
        iteration_count = st.selectbox("Iteration Count", ["1", "2", "3", "infinite"])
        direction = st.selectbox("Direction", ["normal", "reverse", "alternate", "alternate-reverse"])
    with col2:
        timing_function = st.selectbox("Timing Function", [
            "ease", "ease-in", "ease-out", "ease-in-out", "linear",
            "cubic-bezier(0.25, 0.1, 0.25, 1)"
        ])
        fill_mode = st.selectbox("Fill Mode", ["none", "forwards", "backwards", "both"])
        delay = st.number_input("Delay (seconds)", 0.0, 10.0, 0.0, 0.1)

    # Generate CSS
    if st.button("Generate Animation CSS"):
        # Sort keyframes by percentage
        keyframes.sort(key=lambda x: x['percentage'])

        # Generate keyframes CSS
        keyframes_css = f"@keyframes {animation_name} {{\n"
        for kf in keyframes:
            keyframes_css += f"  {kf['percentage']}% {{\n"
            for prop in kf['properties'].strip().split('\n'):
                if prop.strip():
                    keyframes_css += f"    {prop.strip()}\n"
            keyframes_css += "  }\n"
        keyframes_css += "}"

        # Generate animation property
        animation_css = f"""animation: {animation_name} {duration}s {timing_function} {delay}s {iteration_count} {direction} {fill_mode};"""

        complete_css = f"""{keyframes_css}

.animated-element {{
  {animation_css}
}}"""

        st.subheader("Generated CSS")
        st.code(complete_css, language="css")

        # Preview (simple)
        st.subheader("Preview")
        st.info(
            "Preview functionality would require JavaScript. Use the generated CSS in your project to see the animation.")

        FileHandler.create_download_link(complete_css.encode(), f"{animation_name}.css", "text/css")


# Helper functions
def minify_css(css_content, options):
    """Minify CSS content based on options"""
    result = css_content

    if options['remove_comments']:
        # Remove CSS comments
        result = re.sub(r'/\*.*?\*/', '', result, flags=re.DOTALL)

    if options['remove_whitespace']:
        # Remove unnecessary whitespace
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r';\s*}', '}', result)
        result = re.sub(r'{\s*', '{', result)
        result = re.sub(r'}\s*', '}', result)
        result = re.sub(r':\s*', ':', result)
        result = re.sub(r';\s*', ';', result)
        result = result.strip()

    if options['shorten_colors']:
        # Shorten hex colors
        result = re.sub(r'#([0-9a-fA-F])\1([0-9a-fA-F])\2([0-9a-fA-F])\3', r'#\1\2\3', result)

    if options['remove_semicolons']:
        # Remove last semicolon before closing brace
        result = re.sub(r';(\s*})', r'\1', result)

    return result


def format_css(css_content, options):
    """Format CSS content based on options"""
    indent_char = '\t' if options['indent_type'] == 'Tabs' else ' ' * options['indent_size']

    # Basic formatting
    result = css_content

    # Remove existing formatting
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()

    # Add proper spacing and indentation
    formatted_lines = []
    indent_level = 0

    i = 0
    while i < len(result):
        char = result[i]

        if char == '{':
            formatted_lines.append(char)
            if options['brace_style'] == 'New Line':
                formatted_lines.append('\n')
            formatted_lines.append('\n')
            indent_level += 1
        elif char == '}':
            if formatted_lines and formatted_lines[-1] != '\n':
                formatted_lines.append('\n')
            indent_level -= 1
            formatted_lines.append(indent_char * indent_level + char + '\n')
        elif char == ';':
            formatted_lines.append(char + '\n')
        else:
            # Add indentation at start of line
            if formatted_lines and formatted_lines[-1] == '\n':
                formatted_lines.append(indent_char * indent_level)
            formatted_lines.append(char)

        i += 1

    return ''.join(formatted_lines)


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def rgb_to_hsl(rgb):
    """Convert RGB to HSL"""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (int(h * 360), int(s * 100), int(l * 100))


def shorten_hex_color(hex_color):
    """Shorten hex color if possible"""
    if len(hex_color) == 7:
        if hex_color[1] == hex_color[2] and hex_color[3] == hex_color[4] and hex_color[5] == hex_color[6]:
            return f"#{hex_color[1]}{hex_color[3]}{hex_color[5]}"
    return hex_color


def generate_color_variations(base_color):
    """Generate color variations"""
    rgb = hex_to_rgb(base_color)
    variations = {}

    # Lighter variations
    for i, percent in enumerate([20, 40, 60], 1):
        lighter_rgb = tuple(min(255, int(c + (255 - c) * percent / 100)) for c in rgb)
        variations[f"Lighter {percent}%"] = rgb_to_hex(lighter_rgb)

    # Darker variations
    for i, percent in enumerate([20, 40, 60], 1):
        darker_rgb = tuple(max(0, int(c * (100 - percent) / 100)) for c in rgb)
        variations[f"Darker {percent}%"] = rgb_to_hex(darker_rgb)

    return variations


def generate_color_palette(base_color, palette_type):
    """Generate color palette based on type"""
    base_rgb = hex_to_rgb(base_color)
    base_hsl = rgb_to_hsl(base_rgb)

    palette = [base_color]

    if palette_type == "Monochromatic":
        # Different lightness values
        for lightness in [30, 50, 70, 90]:
            if lightness != base_hsl[2]:
                new_hsl = (base_hsl[0], base_hsl[1], lightness)
                new_rgb = colorsys.hls_to_rgb(new_hsl[0] / 360, new_hsl[2] / 100, new_hsl[1] / 100)
                new_rgb = tuple(int(c * 255) for c in new_rgb)
                palette.append(rgb_to_hex(new_rgb))

    elif palette_type == "Analogous":
        # Adjacent hues
        for offset in [-30, -15, 15, 30]:
            new_hue = (base_hsl[0] + offset) % 360
            new_hsl = (new_hue, base_hsl[1], base_hsl[2])
            new_rgb = colorsys.hls_to_rgb(new_hsl[0] / 360, new_hsl[2] / 100, new_hsl[1] / 100)
            new_rgb = tuple(int(c * 255) for c in new_rgb)
            palette.append(rgb_to_hex(new_rgb))

    elif palette_type == "Complementary":
        # Opposite hue
        comp_hue = (base_hsl[0] + 180) % 360
        comp_hsl = (comp_hue, base_hsl[1], base_hsl[2])
        comp_rgb = colorsys.hls_to_rgb(comp_hsl[0] / 360, comp_hsl[2] / 100, comp_hsl[1] / 100)
        comp_rgb = tuple(int(c * 255) for c in comp_rgb)
        palette.append(rgb_to_hex(comp_rgb))

        # Add variations
        for lightness in [30, 70]:
            for hue in [base_hsl[0], comp_hue]:
                new_hsl = (hue, base_hsl[1], lightness)
                new_rgb = colorsys.hls_to_rgb(new_hsl[0] / 360, new_hsl[2] / 100, new_hsl[1] / 100)
                new_rgb = tuple(int(c * 255) for c in new_rgb)
                palette.append(rgb_to_hex(new_rgb))

    return list(set(palette))[:6]  # Return unique colors, max 6


def validate_css(css_content):
    """Basic CSS validation"""
    errors = []
    warnings = []
    stats = {'rules': 0, 'properties': 0, 'selectors': 0}

    lines = css_content.split('\n')

    # Basic syntax checking
    brace_count = 0
    in_rule = False

    for line_num, line in enumerate(lines, 1):
        line = line.strip()

        if not line or line.startswith('/*'):
            continue

        # Count braces
        open_braces = line.count('{')
        close_braces = line.count('}')
        brace_count += open_braces - close_braces

        if open_braces > 0:
            stats['rules'] += open_braces
            in_rule = True

        if close_braces > 0:
            in_rule = False

        # Check for properties
        if in_rule and ':' in line and not line.endswith('{'):
            stats['properties'] += 1

            # Check for missing semicolon
            if not line.rstrip().endswith(';') and not line.rstrip().endswith('{') and not line.rstrip().endswith('}'):
                warnings.append({
                    'line': line_num,
                    'message': 'Missing semicolon'
                })

        # Check for invalid characters
        if re.search(r'[^\w\s\-_.:;{}()#,>+~\[\]="\'@%/\*]', line):
            errors.append({
                'line': line_num,
                'message': 'Invalid characters detected'
            })

    # Check for unmatched braces
    if brace_count != 0:
        errors.append({
            'line': len(lines),
            'message': f'Unmatched braces (difference: {brace_count})'
        })

    return {
        'errors': errors,
        'warnings': warnings,
        'stats': stats
    }


# Additional placeholder functions for remaining tools
def grid_generator():
    """CSS Grid generator"""
    st.info("CSS Grid Generator - Coming soon!")


def responsive_layout():
    """Responsive layout generator"""
    st.info("Responsive Layout Generator - Coming soon!")


def bootstrap_helper():
    """Bootstrap helper tools"""
    st.info("Bootstrap Helper - Coming soon!")


def transition_builder():
    """CSS transition builder"""
    st.info("CSS Transition Builder - Coming soon!")


def specificity_calculator():
    """CSS specificity calculator"""
    st.info("CSS Specificity Calculator - Coming soon!")


def selector_tester():
    """CSS selector tester"""
    st.info("CSS Selector Tester - Coming soon!")
