import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
import cv2
import io
import zipfile
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from utils.common import create_tool_header, show_progress_bar, add_to_recent
from utils.file_handler import FileHandler
from utils.ai_client import ai_client


def display_tools():
    """Display all image processing tools"""

    tool_categories = {
        "Conversion Tools": [
            "Format Converter", "Batch Converter", "Animated GIF Creator", "PDF to Image", "SVG Converter"
        ],
        "Editing Tools": [
            "Image Resizer", "Image Cropper", "Rotate & Flip", "Brightness/Contrast", "Color Adjustment"
        ],
        "Design Tools": [
            "Canvas Creator", "Text Overlay", "Watermark Tool", "Collage Maker", "Border Tool"
        ],
        "Color Tools": [
            "Palette Extractor", "Color Replacer", "Histogram Analyzer", "Color Balance", "Hue Adjuster"
        ],
        "Analysis Tools": [
            "Metadata Extractor", "Image Comparison", "Face Detection", "Object Detection", "Image Statistics"
        ],
        "Compression Tools": [
            "Image Compressor", "Quality Optimizer", "Batch Compression", "Format-Specific Compression"
        ],
        "Effects Tools": [
            "Blur Effects", "Artistic Filters", "Vintage Effects", "Edge Detection", "Noise Reduction"
        ],
        "Annotation Tools": [
            "Shape Drawer", "Text Annotations", "Highlighting Tool", "Redaction Tool", "Markup Tool"
        ],
        "AI Tools": [
            "Image Enhancement", "Background Removal", "Style Transfer", "Image Analysis", "Object Recognition"
        ],
        "Miscellaneous": [
            "Icon Generator", "Placeholder Creator", "Image Statistics", "Format Info", "EXIF Viewer"
        ]
    }

    selected_category = st.selectbox("Select Tool Category", list(tool_categories.keys()))
    selected_tool = st.selectbox("Select Tool", tool_categories[selected_category])

    st.markdown("---")

    add_to_recent(f"Image Tools - {selected_tool}")

    # Display selected tool
    if selected_tool == "Format Converter":
        format_converter()
    elif selected_tool == "Image Resizer":
        image_resizer()
    elif selected_tool == "Image Cropper":
        image_cropper()
    elif selected_tool == "Palette Extractor":
        palette_extractor()
    elif selected_tool == "Image Compressor":
        image_compressor()
    elif selected_tool == "Watermark Tool":
        watermark_tool()
    elif selected_tool == "Batch Converter":
        batch_converter()
    elif selected_tool == "Brightness/Contrast":
        brightness_contrast()
    elif selected_tool == "Blur Effects":
        blur_effects()
    elif selected_tool == "Metadata Extractor":
        metadata_extractor()
    elif selected_tool == "Background Removal":
        background_removal()
    elif selected_tool == "Text Overlay":
        text_overlay()
    elif selected_tool == "Image Enhancement":
        image_enhancement()
    elif selected_tool == "Collage Maker":
        collage_maker()
    elif selected_tool == "Icon Generator":
        icon_generator()
    else:
        st.info(f"{selected_tool} tool is being implemented. Please check back soon!")


def format_converter():
    """Convert image formats"""
    create_tool_header("Format Converter", "Convert images between different formats", "🔄")

    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                              accept_multiple=True)

    if uploaded_files:
        target_format = st.selectbox("Target Format", ["PNG", "JPEG", "GIF", "BMP", "TIFF", "WEBP"])

        if target_format == "JPEG":
            quality = st.slider("JPEG Quality", 1, 100, 85)
        else:
            quality = None

        if st.button("Convert Images"):
            converted_files = {}
            progress_bar = st.progress(0)

            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    image = FileHandler.process_image_file(uploaded_file)
                    if image:
                        # Convert RGBA to RGB for JPEG
                        if target_format == "JPEG" and image.mode in ("RGBA", "P"):
                            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                            rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
                            image = rgb_image

                        # Save converted image
                        output = io.BytesIO()
                        save_kwargs = {"format": target_format}
                        if quality and target_format == "JPEG":
                            save_kwargs["quality"] = quality

                        image.save(output, **save_kwargs)

                        # Generate filename
                        base_name = uploaded_file.name.rsplit('.', 1)[0]
                        new_filename = f"{base_name}.{target_format.lower()}"
                        converted_files[new_filename] = output.getvalue()

                        progress_bar.progress((i + 1) / len(uploaded_files))

                except Exception as e:
                    st.error(f"Error converting {uploaded_file.name}: {str(e)}")

            if converted_files:
                if len(converted_files) == 1:
                    filename, data = next(iter(converted_files.items()))
                    FileHandler.create_download_link(data, filename, f"image/{target_format.lower()}")
                else:
                    # Create ZIP archive for multiple files
                    zip_data = FileHandler.create_zip_archive(converted_files)
                    FileHandler.create_download_link(zip_data, "converted_images.zip", "application/zip")

                st.success(f"Converted {len(converted_files)} image(s) to {target_format}")


def image_resizer():
    """Resize images"""
    create_tool_header("Image Resizer", "Resize images with various options", "📐")

    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                              accept_multiple=True)

    if uploaded_files:
        resize_method = st.selectbox("Resize Method",
                                     ["Exact Dimensions", "Scale by Percentage", "Fit to Width", "Fit to Height"])

        if resize_method == "Exact Dimensions":
            col1, col2 = st.columns(2)
            with col1:
                width = st.number_input("Width (pixels)", min_value=1, value=800)
            with col2:
                height = st.number_input("Height (pixels)", min_value=1, value=600)
        elif resize_method == "Scale by Percentage":
            scale = st.slider("Scale Percentage", 10, 500, 100)
        elif resize_method == "Fit to Width":
            width = st.number_input("Target Width (pixels)", min_value=1, value=800)
        elif resize_method == "Fit to Height":
            height = st.number_input("Target Height (pixels)", min_value=1, value=600)

        maintain_aspect = st.checkbox("Maintain Aspect Ratio", True)
        resampling = st.selectbox("Resampling Algorithm", ["LANCZOS", "BILINEAR", "BICUBIC", "NEAREST"])

        if st.button("Resize Images"):
            resized_files = {}
            progress_bar = st.progress(0)

            resampling_map = {
                "LANCZOS": Image.Resampling.LANCZOS,
                "BILINEAR": Image.Resampling.BILINEAR,
                "BICUBIC": Image.Resampling.BICUBIC,
                "NEAREST": Image.Resampling.NEAREST
            }

            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    image = FileHandler.process_image_file(uploaded_file)
                    if image:
                        original_width, original_height = image.size

                        if resize_method == "Exact Dimensions":
                            if maintain_aspect:
                                image.thumbnail((width, height), resampling_map[resampling])
                                new_image = image
                            else:
                                new_image = image.resize((width, height), resampling_map[resampling])
                        elif resize_method == "Scale by Percentage":
                            new_width = int(original_width * scale / 100)
                            new_height = int(original_height * scale / 100)
                            new_image = image.resize((new_width, new_height), resampling_map[resampling])
                        elif resize_method == "Fit to Width":
                            aspect_ratio = original_height / original_width
                            new_height = int(width * aspect_ratio)
                            new_image = image.resize((width, new_height), resampling_map[resampling])
                        elif resize_method == "Fit to Height":
                            aspect_ratio = original_width / original_height
                            new_width = int(height * aspect_ratio)
                            new_image = image.resize((new_width, height), resampling_map[resampling])

                        # Save resized image
                        output = io.BytesIO()
                        format_name = image.format if image.format else "PNG"
                        new_image.save(output, format=format_name)

                        base_name = uploaded_file.name.rsplit('.', 1)[0]
                        extension = uploaded_file.name.rsplit('.', 1)[1]
                        new_filename = f"{base_name}_resized.{extension}"
                        resized_files[new_filename] = output.getvalue()

                        progress_bar.progress((i + 1) / len(uploaded_files))

                except Exception as e:
                    st.error(f"Error resizing {uploaded_file.name}: {str(e)}")

            if resized_files:
                if len(resized_files) == 1:
                    filename, data = next(iter(resized_files.items()))
                    FileHandler.create_download_link(data, filename, "image/png")
                else:
                    zip_data = FileHandler.create_zip_archive(resized_files)
                    FileHandler.create_download_link(zip_data, "resized_images.zip", "application/zip")

                st.success(f"Resized {len(resized_files)} image(s)")


def image_cropper():
    """Crop images"""
    create_tool_header("Image Cropper", "Crop images with precise control", "✂️")

    uploaded_file = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                             accept_multiple=False)

    if uploaded_file:
        image = FileHandler.process_image_file(uploaded_file[0])

        if image:
            st.subheader("Original Image")
            st.image(image, caption="Original Image", use_column_width=True)

            width, height = image.size
            st.write(f"Image dimensions: {width} × {height} pixels")

            # Crop parameters
            col1, col2 = st.columns(2)
            with col1:
                left = st.slider("Left", 0, width - 1, 0)
                top = st.slider("Top", 0, height - 1, 0)
            with col2:
                right = st.slider("Right", left + 1, width, width)
                bottom = st.slider("Bottom", top + 1, height, height)

            # Preview crop area
            preview_image = image.copy()
            draw = ImageDraw.Draw(preview_image)
            draw.rectangle([left, top, right, bottom], outline="red", width=3)
            st.image(preview_image, caption="Crop Preview (red rectangle)", use_column_width=True)

            if st.button("Crop Image"):
                try:
                    cropped_image = image.crop((left, top, right, bottom))

                    st.subheader("Cropped Image")
                    st.image(cropped_image, caption="Cropped Image", use_column_width=True)

                    # Save cropped image
                    output = io.BytesIO()
                    format_name = image.format if image.format else "PNG"
                    cropped_image.save(output, format=format_name)

                    base_name = uploaded_file[0].name.rsplit('.', 1)[0]
                    extension = uploaded_file[0].name.rsplit('.', 1)[1]
                    filename = f"{base_name}_cropped.{extension}"

                    FileHandler.create_download_link(output.getvalue(), filename, "image/png")
                    st.success("Image cropped successfully!")

                except Exception as e:
                    st.error(f"Error cropping image: {str(e)}")


def palette_extractor():
    """Extract color palette from images"""
    create_tool_header("Palette Extractor", "Extract dominant colors from images", "🎨")

    uploaded_file = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                             accept_multiple=False)

    if uploaded_file:
        image = FileHandler.process_image_file(uploaded_file[0])

        if image:
            st.image(image, caption="Source Image", use_column_width=True)

            num_colors = st.slider("Number of colors to extract", 2, 20, 8)

            if st.button("Extract Palette"):
                try:
                    # Convert image to RGB and resize for faster processing
                    rgb_image = image.convert('RGB')
                    rgb_image.thumbnail((200, 200))

                    # Convert to numpy array
                    img_array = np.array(rgb_image)
                    img_array = img_array.reshape(-1, 3)

                    # Use KMeans to find dominant colors
                    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
                    kmeans.fit(img_array)

                    colors = kmeans.cluster_centers_.astype(int)

                    # Create palette visualization
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

                    # Show original image
                    ax1.imshow(rgb_image)
                    ax1.set_title("Original Image")
                    ax1.axis('off')

                    # Show color palette
                    palette_height = 100
                    palette_width = len(colors) * 50
                    palette_image = np.zeros((palette_height, palette_width, 3), dtype=np.uint8)

                    for i, color in enumerate(colors):
                        start_x = i * 50
                        end_x = (i + 1) * 50
                        palette_image[:, start_x:end_x] = color

                    ax2.imshow(palette_image)
                    ax2.set_title("Extracted Palette")
                    ax2.axis('off')

                    # Display color information
                    st.subheader("Color Palette")
                    st.pyplot(fig)
                    plt.close()

                    # Show color codes
                    st.subheader("Color Codes")
                    for i, color in enumerate(colors):
                        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                        rgb_color = f"rgb({color[0]}, {color[1]}, {color[2]})"

                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.markdown(
                                f'<div style="width:50px;height:30px;background-color:{hex_color};border:1px solid #000;"></div>',
                                unsafe_allow_html=True)
                        with col2:
                            st.code(hex_color)
                        with col3:
                            st.code(rgb_color)
                        with col4:
                            st.code(f"HSV: {cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]}")

                    # Create downloadable palette data
                    palette_data = []
                    for i, color in enumerate(colors):
                        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                        rgb_color = f"rgb({color[0]}, {color[1]}, {color[2]})"
                        palette_data.append(f"Color {i + 1}: {hex_color} | {rgb_color}")

                    palette_text = '\n'.join(palette_data)
                    FileHandler.create_download_link(palette_text.encode(), "color_palette.txt", "text/plain")

                except Exception as e:
                    st.error(f"Error extracting palette: {str(e)}")


def image_compressor():
    """Compress images with quality control"""
    create_tool_header("Image Compressor", "Reduce image file sizes", "🗜️")

    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                              accept_multiple=True)

    if uploaded_files:
        compression_method = st.selectbox("Compression Method",
                                          ["Quality Reduction", "Resize + Quality", "Format Optimization"])

        if compression_method in ["Quality Reduction", "Resize + Quality"]:
            quality = st.slider("Quality", 1, 100, 75)

        if compression_method == "Resize + Quality":
            scale_factor = st.slider("Scale Factor", 0.1, 1.0, 0.8)

        target_format = st.selectbox("Output Format", ["Keep Original", "JPEG", "PNG", "WEBP"])

        if st.button("Compress Images"):
            compressed_files = {}
            progress_bar = st.progress(0)
            total_original_size = 0
            total_compressed_size = 0

            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    image = FileHandler.process_image_file(uploaded_file)
                    if image:
                        total_original_size += uploaded_file.size

                        # Apply compression method
                        if compression_method == "Resize + Quality":
                            new_width = int(image.width * scale_factor)
                            new_height = int(image.height * scale_factor)
                            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

                        # Determine output format
                        if target_format == "Keep Original":
                            output_format = image.format if image.format else "PNG"
                        else:
                            output_format = target_format

                        # Handle format-specific requirements
                        if output_format == "JPEG" and image.mode in ("RGBA", "P"):
                            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                            rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
                            image = rgb_image

                        # Save compressed image
                        output = io.BytesIO()
                        save_kwargs = {"format": output_format}

                        if compression_method in ["Quality Reduction", "Resize + Quality"] and output_format == "JPEG":
                            save_kwargs["quality"] = quality
                            save_kwargs["optimize"] = True
                        elif output_format == "PNG":
                            save_kwargs["optimize"] = True
                        elif output_format == "WEBP":
                            save_kwargs["quality"] = quality if compression_method in ["Quality Reduction",
                                                                                       "Resize + Quality"] else 80
                            save_kwargs["optimize"] = True

                        image.save(output, **save_kwargs)
                        compressed_data = output.getvalue()
                        total_compressed_size += len(compressed_data)

                        # Generate filename
                        base_name = uploaded_file.name.rsplit('.', 1)[0]
                        extension = output_format.lower() if target_format != "Keep Original" else \
                        uploaded_file.name.rsplit('.', 1)[1]
                        new_filename = f"{base_name}_compressed.{extension}"
                        compressed_files[new_filename] = compressed_data

                        progress_bar.progress((i + 1) / len(uploaded_files))

                except Exception as e:
                    st.error(f"Error compressing {uploaded_file.name}: {str(e)}")

            if compressed_files:
                # Show compression statistics
                compression_ratio = (total_original_size - total_compressed_size) / total_original_size * 100
                st.success(f"Compression complete! Reduced size by {compression_ratio:.1f}%")
                st.write(f"Original total size: {total_original_size:,} bytes")
                st.write(f"Compressed total size: {total_compressed_size:,} bytes")

                if len(compressed_files) == 1:
                    filename, data = next(iter(compressed_files.items()))
                    FileHandler.create_download_link(data, filename, "image/jpeg")
                else:
                    zip_data = FileHandler.create_zip_archive(compressed_files)
                    FileHandler.create_download_link(zip_data, "compressed_images.zip", "application/zip")


def watermark_tool():
    """Add watermarks to images"""
    create_tool_header("Watermark Tool", "Add text or image watermarks", "💧")

    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                              accept_multiple=True)

    if uploaded_files:
        watermark_type = st.selectbox("Watermark Type", ["Text", "Image"])

        if watermark_type == "Text":
            watermark_text = st.text_input("Watermark Text", "© Your Name")
            font_size = st.slider("Font Size", 10, 200, 36)
            opacity = st.slider("Opacity", 10, 100, 50)
            color = st.color_picker("Text Color", "#FFFFFF")
        else:
            watermark_image = FileHandler.upload_files(['png'], accept_multiple=False)
            if watermark_image:
                opacity = st.slider("Opacity", 10, 100, 50)
                scale = st.slider("Scale", 10, 100, 20)

        position = st.selectbox("Position", ["Bottom Right", "Bottom Left", "Top Right", "Top Left", "Center"])
        margin = st.slider("Margin", 0, 100, 20)

        if st.button("Add Watermark"):
            watermarked_files = {}
            progress_bar = st.progress(0)

            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    image = FileHandler.process_image_file(uploaded_file)
                    if image:
                        # Convert to RGBA for transparency support
                        if image.mode != 'RGBA':
                            image = image.convert('RGBA')

                        # Create watermark overlay
                        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
                        draw = ImageDraw.Draw(overlay)

                        if watermark_type == "Text":
                            # Calculate text size and position
                            try:
                                font = ImageFont.truetype("arial.ttf", font_size)
                            except:
                                font = ImageFont.load_default()

                            bbox = draw.textbbox((0, 0), watermark_text, font=font)
                            text_width = bbox[2] - bbox[0]
                            text_height = bbox[3] - bbox[1]

                            # Calculate position
                            x, y = calculate_position(position, image.size, (text_width, text_height), margin)

                            # Convert color and add opacity
                            hex_color = color.lstrip('#')
                            rgb_color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
                            rgba_color = rgb_color + (int(255 * opacity / 100),)

                            draw.text((x, y), watermark_text, font=font, fill=rgba_color)

                        else:  # Image watermark
                            if watermark_image:
                                wm_img = FileHandler.process_image_file(watermark_image[0])
                                if wm_img:
                                    # Scale watermark
                                    wm_width = int(wm_img.width * scale / 100)
                                    wm_height = int(wm_img.height * scale / 100)
                                    wm_img = wm_img.resize((wm_width, wm_height), Image.Resampling.LANCZOS)

                                    # Ensure RGBA mode
                                    if wm_img.mode != 'RGBA':
                                        wm_img = wm_img.convert('RGBA')

                                    # Apply opacity
                                    alpha = wm_img.split()[-1]
                                    alpha = alpha.point(lambda p: int(p * opacity / 100))
                                    wm_img.putalpha(alpha)

                                    # Calculate position
                                    x, y = calculate_position(position, image.size, wm_img.size, margin)

                                    overlay.paste(wm_img, (x, y), wm_img)

                        # Composite the watermark
                        watermarked = Image.alpha_composite(image, overlay)

                        # Convert back to original mode if needed
                        if uploaded_file.name.lower().endswith(('.jpg', '.jpeg')):
                            watermarked = watermarked.convert('RGB')

                        # Save watermarked image
                        output = io.BytesIO()
                        format_name = "JPEG" if uploaded_file.name.lower().endswith(('.jpg', '.jpeg')) else "PNG"
                        watermarked.save(output, format=format_name)

                        base_name = uploaded_file.name.rsplit('.', 1)[0]
                        extension = uploaded_file.name.rsplit('.', 1)[1]
                        new_filename = f"{base_name}_watermarked.{extension}"
                        watermarked_files[new_filename] = output.getvalue()

                        progress_bar.progress((i + 1) / len(uploaded_files))

                except Exception as e:
                    st.error(f"Error adding watermark to {uploaded_file.name}: {str(e)}")

            if watermarked_files:
                if len(watermarked_files) == 1:
                    filename, data = next(iter(watermarked_files.items()))
                    FileHandler.create_download_link(data, filename, "image/png")
                else:
                    zip_data = FileHandler.create_zip_archive(watermarked_files)
                    FileHandler.create_download_link(zip_data, "watermarked_images.zip", "application/zip")

                st.success(f"Added watermark to {len(watermarked_files)} image(s)")


def calculate_position(position, image_size, element_size, margin):
    """Calculate position for watermark or overlay"""
    img_width, img_height = image_size
    elem_width, elem_height = element_size

    if position == "Bottom Right":
        x = img_width - elem_width - margin
        y = img_height - elem_height - margin
    elif position == "Bottom Left":
        x = margin
        y = img_height - elem_height - margin
    elif position == "Top Right":
        x = img_width - elem_width - margin
        y = margin
    elif position == "Top Left":
        x = margin
        y = margin
    else:  # Center
        x = (img_width - elem_width) // 2
        y = (img_height - elem_height) // 2

    return max(0, x), max(0, y)


def batch_converter():
    """Batch process multiple images"""
    create_tool_header("Batch Converter", "Process multiple images at once", "⚡")

    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                              accept_multiple=True)

    if uploaded_files:
        st.subheader("Batch Operations")

        operations = st.multiselect("Select Operations", [
            "Format Conversion", "Resize", "Quality Adjustment", "Add Border", "Apply Filter"
        ])

        settings = {}

        if "Format Conversion" in operations:
            settings['target_format'] = st.selectbox("Target Format", ["PNG", "JPEG", "WEBP", "GIF"])

        if "Resize" in operations:
            col1, col2 = st.columns(2)
            with col1:
                settings['resize_width'] = st.number_input("Width", min_value=1, value=800)
            with col2:
                settings['resize_height'] = st.number_input("Height", min_value=1, value=600)
            settings['maintain_aspect'] = st.checkbox("Maintain Aspect Ratio", True)

        if "Quality Adjustment" in operations:
            settings['quality'] = st.slider("Quality", 1, 100, 85)

        if "Add Border" in operations:
            settings['border_width'] = st.slider("Border Width", 1, 50, 10)
            settings['border_color'] = st.color_picker("Border Color", "#000000")

        if "Apply Filter" in operations:
            settings['filter_type'] = st.selectbox("Filter Type", ["Blur", "Sharpen", "Enhance", "Grayscale"])

        if st.button("Process All Images"):
            processed_files = {}
            progress_bar = st.progress(0)

            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    image = FileHandler.process_image_file(uploaded_file)
                    if image:
                        processed_image = image.copy()

                        # Apply operations in sequence
                        for operation in operations:
                            if operation == "Resize":
                                if settings['maintain_aspect']:
                                    processed_image.thumbnail((settings['resize_width'], settings['resize_height']),
                                                              Image.Resampling.LANCZOS)
                                else:
                                    processed_image = processed_image.resize(
                                        (settings['resize_width'], settings['resize_height']), Image.Resampling.LANCZOS)

                            elif operation == "Add Border":
                                hex_color = settings['border_color'].lstrip('#')
                                border_color = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
                                processed_image = ImageOps.expand(processed_image, border=settings['border_width'],
                                                                  fill=border_color)

                            elif operation == "Apply Filter":
                                filter_type = settings['filter_type']
                                if filter_type == "Blur":
                                    processed_image = processed_image.filter(ImageFilter.BLUR)
                                elif filter_type == "Sharpen":
                                    processed_image = processed_image.filter(ImageFilter.SHARPEN)
                                elif filter_type == "Enhance":
                                    enhancer = ImageEnhance.Sharpness(processed_image)
                                    processed_image = enhancer.enhance(1.5)
                                elif filter_type == "Grayscale":
                                    processed_image = processed_image.convert('L').convert('RGB')

                        # Handle format conversion
                        output_format = settings.get('target_format', image.format if image.format else "PNG")

                        if output_format == "JPEG" and processed_image.mode in ("RGBA", "P"):
                            rgb_image = Image.new("RGB", processed_image.size, (255, 255, 255))
                            rgb_image.paste(processed_image, mask=processed_image.split()[
                                -1] if processed_image.mode == "RGBA" else None)
                            processed_image = rgb_image

                        # Save processed image
                        output = io.BytesIO()
                        save_kwargs = {"format": output_format}

                        if "Quality Adjustment" in operations and output_format in ["JPEG", "WEBP"]:
                            save_kwargs["quality"] = settings['quality']

                        processed_image.save(output, **save_kwargs)

                        base_name = uploaded_file.name.rsplit('.', 1)[0]
                        extension = output_format.lower()
                        new_filename = f"{base_name}_processed.{extension}"
                        processed_files[new_filename] = output.getvalue()

                        progress_bar.progress((i + 1) / len(uploaded_files))

                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")

            if processed_files:
                zip_data = FileHandler.create_zip_archive(processed_files)
                FileHandler.create_download_link(zip_data, "batch_processed_images.zip", "application/zip")
                st.success(f"Processed {len(processed_files)} image(s)")


def brightness_contrast():
    """Adjust brightness and contrast"""
    create_tool_header("Brightness/Contrast", "Adjust image brightness and contrast", "☀️")

    uploaded_file = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                             accept_multiple=False)

    if uploaded_file:
        image = FileHandler.process_image_file(uploaded_file[0])

        if image:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Original Image")
                st.image(image, use_column_width=True)

            # Adjustment controls
            brightness = st.slider("Brightness", 0.1, 3.0, 1.0, 0.1)
            contrast = st.slider("Contrast", 0.1, 3.0, 1.0, 0.1)

            # Apply adjustments in real-time
            enhancer_brightness = ImageEnhance.Brightness(image)
            temp_image = enhancer_brightness.enhance(brightness)

            enhancer_contrast = ImageEnhance.Contrast(temp_image)
            adjusted_image = enhancer_contrast.enhance(contrast)

            with col2:
                st.subheader("Adjusted Image")
                st.image(adjusted_image, use_column_width=True)

            if st.button("Download Adjusted Image"):
                output = io.BytesIO()
                format_name = image.format if image.format else "PNG"
                adjusted_image.save(output, format=format_name)

                base_name = uploaded_file[0].name.rsplit('.', 1)[0]
                extension = uploaded_file[0].name.rsplit('.', 1)[1]
                filename = f"{base_name}_adjusted.{extension}"

                FileHandler.create_download_link(output.getvalue(), filename, "image/png")


def blur_effects():
    """Apply blur effects to images"""
    create_tool_header("Blur Effects", "Apply various blur effects", "〰️")

    uploaded_file = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                             accept_multiple=False)

    if uploaded_file:
        image = FileHandler.process_image_file(uploaded_file[0])

        if image:
            blur_type = st.selectbox("Blur Type", ["Gaussian Blur", "Motion Blur", "Radial Blur", "Simple Blur"])

            if blur_type == "Gaussian Blur":
                radius = st.slider("Radius", 0.1, 10.0, 1.0, 0.1)
            elif blur_type == "Motion Blur":
                radius = st.slider("Radius", 1, 20, 5)
            else:
                radius = st.slider("Intensity", 1, 10, 2)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Original Image")
                st.image(image, use_column_width=True)

            with col2:
                st.subheader("Blurred Image")

                if blur_type == "Gaussian Blur":
                    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))
                elif blur_type == "Simple Blur":
                    blurred_image = image
                    for _ in range(int(radius)):
                        blurred_image = blurred_image.filter(ImageFilter.BLUR)
                elif blur_type == "Motion Blur":
                    # Simple motion blur simulation
                    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius / 2))
                else:  # Radial blur
                    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))

                st.image(blurred_image, use_column_width=True)

            if st.button("Download Blurred Image"):
                output = io.BytesIO()
                format_name = image.format if image.format else "PNG"
                blurred_image.save(output, format=format_name)

                base_name = uploaded_file[0].name.rsplit('.', 1)[0]
                extension = uploaded_file[0].name.rsplit('.', 1)[1]
                filename = f"{base_name}_blurred.{extension}"

                FileHandler.create_download_link(output.getvalue(), filename, "image/png")


def metadata_extractor():
    """Extract image metadata and EXIF data"""
    create_tool_header("Metadata Extractor", "Extract image metadata and EXIF data", "📋")

    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                              accept_multiple=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.subheader(f"Metadata for: {uploaded_file.name}")

            try:
                image = FileHandler.process_image_file(uploaded_file)
                if image:
                    # Basic image info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Width", f"{image.width} px")
                    with col2:
                        st.metric("Height", f"{image.height} px")
                    with col3:
                        st.metric("Mode", image.mode)

                    col4, col5, col6 = st.columns(3)
                    with col4:
                        st.metric("Format", image.format or "Unknown")
                    with col5:
                        st.metric("File Size", f"{uploaded_file.size:,} bytes")
                    with col6:
                        aspect_ratio = round(image.width / image.height, 2)
                        st.metric("Aspect Ratio", f"{aspect_ratio}:1")

                    # EXIF data (for JPEG images)
                    if hasattr(image, '_getexif') and image._getexif():
                        exif = image._getexif()
                        if exif:
                            st.subheader("EXIF Data")
                            exif_data = {}

                            # Common EXIF tags
                            exif_tags = {
                                256: 'ImageWidth',
                                257: 'ImageLength',
                                272: 'Make',
                                273: 'StripOffsets',
                                274: 'Orientation',
                                282: 'XResolution',
                                283: 'YResolution',
                                306: 'DateTime',
                                315: 'Artist'
                            }

                            for tag_id, value in exif.items():
                                tag_name = exif_tags.get(tag_id, f'Tag_{tag_id}')
                                exif_data[tag_name] = str(value)

                            if exif_data:
                                for key, value in exif_data.items():
                                    st.write(f"**{key}**: {value}")
                            else:
                                st.info("No readable EXIF data found")
                        else:
                            st.info("No EXIF data available")
                    else:
                        st.info("EXIF data not available for this format")

                    # Color analysis
                    st.subheader("Color Analysis")
                    if image.mode == 'RGB':
                        # Calculate average color
                        img_array = np.array(image)
                        avg_color = np.mean(img_array, axis=(0, 1)).astype(int)
                        hex_color = f"#{avg_color[0]:02x}{avg_color[1]:02x}{avg_color[2]:02x}"

                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Average Color**: {hex_color}")
                            st.markdown(
                                f'<div style="width:100px;height:50px;background-color:{hex_color};border:1px solid #000;"></div>',
                                unsafe_allow_html=True)

                        with col2:
                            # Calculate histogram
                            histogram = cv2.calcHist([cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)], [0, 1, 2], None,
                                                     [256, 256, 256], [0, 256, 0, 256, 0, 256])
                            st.write(f"**Total Pixels**: {image.width * image.height:,}")
                            st.write(f"**Color Depth**: {image.mode}")

            except Exception as e:
                st.error(f"Error extracting metadata from {uploaded_file.name}: {str(e)}")

            st.markdown("---")


def background_removal():
    """AI-powered background removal"""
    create_tool_header("Background Removal", "Remove backgrounds using AI", "🎭")

    uploaded_file = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=False)

    if uploaded_file:
        image = FileHandler.process_image_file(uploaded_file[0])

        if image:
            st.image(image, caption="Original Image", use_column_width=True)

            if st.button("Remove Background"):
                with st.spinner("Processing image with AI..."):
                    # Convert image to bytes for AI processing
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format='PNG')
                    img_bytes.seek(0)

                    # Use AI for analysis (simulated background removal instructions)
                    prompt = """
                    Analyze this image and provide detailed instructions for background removal:
                    1. Identify the main subject(s) in the image
                    2. Describe the background elements
                    3. Suggest color ranges or techniques for background removal
                    4. Provide step-by-step masking instructions

                    Format the response as JSON with sections for subject, background, and removal_steps.
                    """

                    analysis = ai_client.analyze_image(img_bytes.getvalue(), prompt)

                    if analysis and "error" not in analysis:
                        st.subheader("AI Analysis")
                        st.write(analysis)

                        # Simple background removal using color thresholding (basic implementation)
                        # This is a simplified version - in a real scenario, you'd use more sophisticated AI models

                        # Convert to HSV for better color separation
                        img_array = np.array(image)
                        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

                        # Create a simple mask based on edge detection
                        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                        edges = cv2.Canny(gray, 50, 150)

                        # Dilate edges to create a rough mask
                        kernel = np.ones((5, 5), np.uint8)
                        mask = cv2.dilate(edges, kernel, iterations=2)
                        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

                        # Create alpha channel
                        result_img = image.convert("RGBA")
                        result_array = np.array(result_img)

                        # Apply mask (simplified approach)
                        alpha_channel = 255 - mask
                        result_array[:, :, 3] = alpha_channel

                        result_image = Image.fromarray(result_array, 'RGBA')

                        st.subheader("Result (Simplified Background Removal)")
                        st.image(result_image, caption="Background Removed", use_column_width=True)
                        st.warning(
                            "This is a simplified background removal. For professional results, use dedicated AI services like Remove.bg or similar APIs.")

                        # Save result
                        output = io.BytesIO()
                        result_image.save(output, format='PNG')

                        base_name = uploaded_file[0].name.rsplit('.', 1)[0]
                        filename = f"{base_name}_no_bg.png"

                        FileHandler.create_download_link(output.getvalue(), filename, "image/png")
                    else:
                        st.error("Failed to analyze image with AI")


def text_overlay():
    """Add text overlay to images"""
    create_tool_header("Text Overlay", "Add customizable text to images", "📝")

    uploaded_file = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'],
                                             accept_multiple=False)

    if uploaded_file:
        image = FileHandler.process_image_file(uploaded_file[0])

        if image:
            st.image(image, caption="Original Image", use_column_width=True)

            # Text settings
            text_content = st.text_area("Text to add:", "Your Text Here")

            col1, col2, col3 = st.columns(3)
            with col1:
                font_size = st.slider("Font Size", 10, 200, 48)
                text_color = st.color_picker("Text Color", "#FFFFFF")
            with col2:
                outline_width = st.slider("Outline Width", 0, 10, 2)
                outline_color = st.color_picker("Outline Color", "#000000")
            with col3:
                opacity = st.slider("Opacity", 10, 100, 100)
                rotation = st.slider("Rotation", -180, 180, 0)

            position = st.selectbox("Position", ["Custom", "Top Left", "Top Center", "Top Right",
                                                 "Center Left", "Center", "Center Right",
                                                 "Bottom Left", "Bottom Center", "Bottom Right"])

            if position == "Custom":
                col1, col2 = st.columns(2)
                with col1:
                    x_pos = st.slider("X Position", 0, image.width, image.width // 2)
                with col2:
                    y_pos = st.slider("Y Position", 0, image.height, image.height // 2)

            shadow = st.checkbox("Add Shadow")
            if shadow:
                shadow_offset = st.slider("Shadow Offset", 1, 20, 5)
                shadow_color = st.color_picker("Shadow Color", "#808080")

            if st.button("Add Text"):
                try:
                    # Create a copy of the image
                    result_image = image.copy()
                    if result_image.mode != 'RGBA':
                        result_image = result_image.convert('RGBA')

                    # Create overlay for text
                    overlay = Image.new('RGBA', result_image.size, (0, 0, 0, 0))
                    draw = ImageDraw.Draw(overlay)

                    # Try to load a better font
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        try:
                            font = ImageFont.truetype("Arial.ttf", font_size)
                        except:
                            font = ImageFont.load_default()

                    # Calculate text position
                    bbox = draw.textbbox((0, 0), text_content, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]

                    if position == "Custom":
                        x, y = x_pos, y_pos
                    else:
                        position_map = {
                            "Top Left": (20, 20),
                            "Top Center": ((image.width - text_width) // 2, 20),
                            "Top Right": (image.width - text_width - 20, 20),
                            "Center Left": (20, (image.height - text_height) // 2),
                            "Center": ((image.width - text_width) // 2, (image.height - text_height) // 2),
                            "Center Right": (image.width - text_width - 20, (image.height - text_height) // 2),
                            "Bottom Left": (20, image.height - text_height - 20),
                            "Bottom Center": ((image.width - text_width) // 2, image.height - text_height - 20),
                            "Bottom Right": (image.width - text_width - 20, image.height - text_height - 20)
                        }
                        x, y = position_map.get(position, (50, 50))

                    # Convert colors
                    def hex_to_rgba(hex_color, alpha=255):
                        hex_color = hex_color.lstrip('#')
                        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)

                    text_rgba = hex_to_rgba(text_color, int(255 * opacity / 100))
                    outline_rgba = hex_to_rgba(outline_color, int(255 * opacity / 100))

                    # Add shadow if enabled
                    if shadow:
                        shadow_rgba = hex_to_rgba(shadow_color, int(128 * opacity / 100))
                        draw.text((x + shadow_offset, y + shadow_offset), text_content,
                                  font=font, fill=shadow_rgba)

                    # Add outline if enabled
                    if outline_width > 0:
                        for dx in range(-outline_width, outline_width + 1):
                            for dy in range(-outline_width, outline_width + 1):
                                if dx != 0 or dy != 0:
                                    draw.text((x + dx, y + dy), text_content,
                                              font=font, fill=outline_rgba)

                    # Add main text
                    draw.text((x, y), text_content, font=font, fill=text_rgba)

                    # Handle rotation if needed
                    if rotation != 0:
                        overlay = overlay.rotate(rotation, expand=True)

                    # Composite the overlay
                    result_image = Image.alpha_composite(result_image, overlay)

                    st.subheader("Result")
                    st.image(result_image, caption="Image with Text Overlay", use_column_width=True)

                    # Save result
                    output = io.BytesIO()
                    result_image.save(output, format='PNG')

                    base_name = uploaded_file[0].name.rsplit('.', 1)[0]
                    filename = f"{base_name}_with_text.png"

                    FileHandler.create_download_link(output.getvalue(), filename, "image/png")

                except Exception as e:
                    st.error(f"Error adding text overlay: {str(e)}")


def image_enhancement():
    """AI-powered image enhancement"""
    create_tool_header("Image Enhancement", "Enhance images using AI", "✨")

    uploaded_file = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=False)

    if uploaded_file:
        image = FileHandler.process_image_file(uploaded_file[0])

        if image:
            st.image(image, caption="Original Image", use_column_width=True)

            enhancement_type = st.selectbox("Enhancement Type", [
                "Auto Enhance", "Noise Reduction", "Sharpening", "Color Correction", "Upscaling"
            ])

            if st.button("Enhance Image"):
                with st.spinner("Enhancing image with AI..."):
                    # Get AI analysis and suggestions
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format='PNG')
                    img_bytes.seek(0)

                    prompt = f"""
                    Analyze this image for {enhancement_type} and provide specific enhancement recommendations:
                    1. Assess current image quality
                    2. Identify areas needing improvement
                    3. Suggest specific enhancement parameters
                    4. Recommend processing steps

                    Provide a detailed technical analysis.
                    """

                    analysis = ai_client.analyze_image(img_bytes.getvalue(), prompt)

                    st.subheader("AI Analysis")
                    st.write(analysis)

                    # Apply basic enhancements based on type
                    enhanced_image = image.copy()

                    if enhancement_type == "Auto Enhance":
                        # Apply multiple enhancements
                        enhancer = ImageEnhance.Sharpness(enhanced_image)
                        enhanced_image = enhancer.enhance(1.2)

                        enhancer = ImageEnhance.Contrast(enhanced_image)
                        enhanced_image = enhancer.enhance(1.1)

                        enhancer = ImageEnhance.Color(enhanced_image)
                        enhanced_image = enhancer.enhance(1.05)

                    elif enhancement_type == "Noise Reduction":
                        # Simple noise reduction using blur
                        enhanced_image = enhanced_image.filter(ImageFilter.SMOOTH)

                    elif enhancement_type == "Sharpening":
                        enhancer = ImageEnhance.Sharpness(enhanced_image)
                        enhanced_image = enhancer.enhance(1.5)
                        enhanced_image = enhanced_image.filter(ImageFilter.SHARPEN)

                    elif enhancement_type == "Color Correction":
                        enhancer = ImageEnhance.Color(enhanced_image)
                        enhanced_image = enhancer.enhance(1.2)

                        enhancer = ImageEnhance.Contrast(enhanced_image)
                        enhanced_image = enhancer.enhance(1.1)

                    elif enhancement_type == "Upscaling":
                        # Simple upscaling (2x)
                        new_size = (image.width * 2, image.height * 2)
                        enhanced_image = enhanced_image.resize(new_size, Image.Resampling.LANCZOS)

                    st.subheader("Enhanced Image")
                    st.image(enhanced_image, caption=f"Enhanced ({enhancement_type})", use_column_width=True)

                    # Save enhanced image
                    output = io.BytesIO()
                    enhanced_image.save(output, format='PNG')

                    base_name = uploaded_file[0].name.rsplit('.', 1)[0]
                    filename = f"{base_name}_enhanced.png"

                    FileHandler.create_download_link(output.getvalue(), filename, "image/png")


def collage_maker():
    """Create image collages"""
    create_tool_header("Collage Maker", "Create collages from multiple images", "🖼️")

    uploaded_files = FileHandler.upload_files(['jpg', 'jpeg', 'png', 'gif', 'bmp'], accept_multiple=True)

    if uploaded_files and len(uploaded_files) >= 2:
        st.write(f"Uploaded {len(uploaded_files)} images")

        # Collage settings
        col1, col2 = st.columns(2)
        with col1:
            layout = st.selectbox("Layout", ["Grid", "Mosaic", "Linear"])
            if layout == "Grid":
                cols = st.slider("Columns", 1, min(len(uploaded_files), 5), 2)
                rows = st.slider("Rows", 1, min(len(uploaded_files), 5), 2)

        with col2:
            canvas_width = st.number_input("Canvas Width", min_value=100, value=1200)
            canvas_height = st.number_input("Canvas Height", min_value=100, value=800)

        spacing = st.slider("Image Spacing", 0, 50, 10)
        background_color = st.color_picker("Background Color", "#FFFFFF")

        if st.button("Create Collage"):
            try:
                # Create canvas
                canvas = Image.new('RGB', (canvas_width, canvas_height), background_color)

                # Process images
                images = []
                for uploaded_file in uploaded_files:
                    img = FileHandler.process_image_file(uploaded_file)
                    if img:
                        images.append(img)

                if layout == "Grid":
                    # Calculate cell size
                    cell_width = (canvas_width - spacing * (cols + 1)) // cols
                    cell_height = (canvas_height - spacing * (rows + 1)) // rows

                    for i, img in enumerate(images[:cols * rows]):
                        row = i // cols
                        col = i % cols

                        # Resize image to fit cell
                        img.thumbnail((cell_width, cell_height), Image.Resampling.LANCZOS)

                        # Calculate position
                        x = spacing + col * (cell_width + spacing)
                        y = spacing + row * (cell_height + spacing)

                        # Center image in cell
                        x += (cell_width - img.width) // 2
                        y += (cell_height - img.height) // 2

                        canvas.paste(img, (x, y))

                elif layout == "Linear":
                    # Arrange images in a row
                    total_width = canvas_width - spacing * (len(images) + 1)
                    img_width = total_width // len(images)

                    for i, img in enumerate(images):
                        # Resize image
                        aspect_ratio = img.height / img.width
                        new_height = int(img_width * aspect_ratio)
                        img = img.resize((img_width, new_height), Image.Resampling.LANCZOS)

                        # Calculate position
                        x = spacing + i * (img_width + spacing)
                        y = (canvas_height - img.height) // 2

                        canvas.paste(img, (x, y))

                else:  # Mosaic
                    # Simple mosaic layout
                    positions = [
                        (spacing, spacing),
                        (canvas_width // 2, spacing),
                        (spacing, canvas_height // 2),
                        (canvas_width // 2, canvas_height // 2)
                    ]

                    cell_width = (canvas_width - spacing * 3) // 2
                    cell_height = (canvas_height - spacing * 3) // 2

                    for i, img in enumerate(images[:4]):
                        img.thumbnail((cell_width, cell_height), Image.Resampling.LANCZOS)

                        x, y = positions[i]
                        x += (cell_width - img.width) // 2
                        y += (cell_height - img.height) // 2

                        canvas.paste(img, (x, y))

                st.subheader("Collage Result")
                st.image(canvas, caption="Created Collage", use_column_width=True)

                # Save collage
                output = io.BytesIO()
                canvas.save(output, format='PNG')

                FileHandler.create_download_link(output.getvalue(), "collage.png", "image/png")

            except Exception as e:
                st.error(f"Error creating collage: {str(e)}")

    elif uploaded_files and len(uploaded_files) < 2:
        st.warning("Please upload at least 2 images to create a collage.")


def icon_generator():
    """Generate icons and favicons"""
    create_tool_header("Icon Generator", "Generate icons and favicons", "🔮")

    # Icon generation options
    generation_method = st.selectbox("Generation Method", ["From Text", "From Image", "AI Generated"])

    if generation_method == "From Text":
        text = st.text_input("Text for Icon", "AB")
        font_size = st.slider("Font Size", 10, 200, 64)
        text_color = st.color_picker("Text Color", "#FFFFFF")
        bg_color = st.color_picker("Background Color", "#007BFF")

    elif generation_method == "From Image":
        uploaded_file = FileHandler.upload_files(['jpg', 'jpeg', 'png'], accept_multiple=False)

    else:  # AI Generated
        prompt = st.text_input("Describe your icon", "A modern, minimalist app icon")

    # Icon sizes
    sizes = st.multiselect("Icon Sizes", [16, 32, 48, 64, 128, 256, 512], default=[32, 64, 128])

    if st.button("Generate Icons"):
        icon_files = {}

        try:
            if generation_method == "From Text":
                # Create base icon
                base_size = max(sizes)
                icon = Image.new('RGB', (base_size, base_size), bg_color)
                draw = ImageDraw.Draw(icon)

                # Try to load a font
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()

                # Calculate text position
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (base_size - text_width) // 2
                y = (base_size - text_height) // 2

                draw.text((x, y), text, font=font, fill=text_color)

                # Generate different sizes
                for size in sizes:
                    if size == base_size:
                        sized_icon = icon
                    else:
                        sized_icon = icon.resize((size, size), Image.Resampling.LANCZOS)

                    output = io.BytesIO()
                    sized_icon.save(output, format='PNG')
                    icon_files[f"icon_{size}x{size}.png"] = output.getvalue()

            elif generation_method == "From Image" and uploaded_file:
                source_image = FileHandler.process_image_file(uploaded_file[0])
                if source_image:
                    # Make square
                    min_dim = min(source_image.width, source_image.height)
                    left = (source_image.width - min_dim) // 2
                    top = (source_image.height - min_dim) // 2
                    square_image = source_image.crop((left, top, left + min_dim, top + min_dim))

                    # Generate different sizes
                    for size in sizes:
                        sized_icon = square_image.resize((size, size), Image.Resampling.LANCZOS)

                        output = io.BytesIO()
                        sized_icon.save(output, format='PNG')
                        icon_files[f"icon_{size}x{size}.png"] = output.getvalue()

            else:  # AI Generated
                with st.spinner("Generating AI icon..."):
                    ai_prompt = f"Create a clean, professional icon: {prompt}. Style: flat design, simple, modern, suitable for app icon"

                    # Generate image with AI
                    generated_bytes = ai_client.generate_image(ai_prompt)

                    if generated_bytes:
                        ai_image = Image.open(io.BytesIO(generated_bytes))

                        # Make square and generate sizes
                        min_dim = min(ai_image.width, ai_image.height)
                        left = (ai_image.width - min_dim) // 2
                        top = (ai_image.height - min_dim) // 2
                        square_image = ai_image.crop((left, top, left + min_dim, top + min_dim))

                        for size in sizes:
                            sized_icon = square_image.resize((size, size), Image.Resampling.LANCZOS)

                            output = io.BytesIO()
                            sized_icon.save(output, format='PNG')
                            icon_files[f"ai_icon_{size}x{size}.png"] = output.getvalue()
                    else:
                        st.error("Failed to generate AI icon")
                        return

            if icon_files:
                # Display generated icons
                st.subheader("Generated Icons")
                cols = st.columns(len(sizes))
                for i, size in enumerate(sizes):
                    with cols[i]:
                        filename = next((f for f in icon_files.keys() if f"_{size}x{size}" in f), None)
                        if filename:
                            img_data = icon_files[filename]
                            st.image(io.BytesIO(img_data), caption=f"{size}×{size}", width=size)

                # Create download
                if len(icon_files) == 1:
                    filename, data = next(iter(icon_files.items()))
                    FileHandler.create_download_link(data, filename, "image/png")
                else:
                    zip_data = FileHandler.create_zip_archive(icon_files)
                    FileHandler.create_download_link(zip_data, "icons.zip", "application/zip")

                st.success(f"Generated {len(icon_files)} icon(s)")

        except Exception as e:
            st.error(f"Error generating icons: {str(e)}")

