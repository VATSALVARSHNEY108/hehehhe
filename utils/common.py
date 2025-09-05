import streamlit as st
import time
import uuid
from typing import Dict, List, Any
import json


def init_session_state():
    """Initialize session state variables"""
    if 'recent_tools' not in st.session_state:
        st.session_state.recent_tools = []
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'settings' not in st.session_state:
        st.session_state.settings = {
            'theme': 'light',
            'auto_save': True,
            'show_tips': True
        }


def add_to_recent(tool_name: str):
    """Add tool to recent tools list"""
    if tool_name not in st.session_state.recent_tools:
        st.session_state.recent_tools.append(tool_name)
        if len(st.session_state.recent_tools) > 10:
            st.session_state.recent_tools.pop(0)


def add_to_history(operation: str, details: Dict[str, Any]):
    """Add operation to history"""
    history_entry = {
        'id': str(uuid.uuid4()),
        'timestamp': time.time(),
        'operation': operation,
        'details': details
    }
    st.session_state.history.append(history_entry)
    if len(st.session_state.history) > 100:
        st.session_state.history.pop(0)


def display_tool_grid(categories: Dict[str, Any]):
    """Display tool categories in a grid layout"""
    cols = st.columns(3)
    for i, (name, info) in enumerate(categories.items()):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                <div style="
                    border: 2px solid {info['color']};
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                    text-align: center;
                    background-color: {info['color']}20;
                    cursor: pointer;
                ">
                    <h3 style="margin: 0; color: {info['color']};">
                        {info['icon']} {name}
                    </h3>
                    <p style="margin: 10px 0; color: #666;">
                        {info['description']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Open {name}", key=f"cat_{i}"):
                    st.session_state.selected_category = name
                    st.rerun()


def search_tools(query: str, categories: Dict[str, Any]) -> Dict[str, List[str]]:
    """Search for tools across categories"""
    results = {}
    query = query.lower()

    for category_name, category_info in categories.items():
        # This would be expanded with actual tool lists from each module
        matching_tools = []

        # Basic category name matching
        if query in category_name.lower() or query in category_info['description'].lower():
            matching_tools.append(f"All {category_name}")

        if matching_tools:
            results[category_name] = matching_tools

    return results


def show_progress_bar(text: str, duration: int = 3):
    """Show a progress bar with given text and duration"""
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(duration * 10):
        progress = (i + 1) / (duration * 10)
        progress_bar.progress(progress)
        status_text.text(f"{text}... {int(progress * 100)}%")
        time.sleep(0.1)

    status_text.text(f"{text} completed!")
    return True


def create_download_button(data: bytes, filename: str, mime_type: str = "application/octet-stream"):
    """Create a download button for processed data"""
    return st.download_button(
        label=f"📥 Download {filename}",
        data=data,
        file_name=filename,
        mime=mime_type
    )


def display_comparison(original_data, processed_data, title: str = "Comparison"):
    """Display before/after comparison"""
    st.subheader(title)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Before:**")
        if isinstance(original_data, str):
            st.text_area("Original", original_data, height=200, disabled=True)
        else:
            st.write(original_data)

    with col2:
        st.markdown("**After:**")
        if isinstance(processed_data, str):
            st.text_area("Processed", processed_data, height=200, disabled=True)
        else:
            st.write(processed_data)


def validate_file_type(uploaded_file, allowed_types: List[str]) -> bool:
    """Validate uploaded file type"""
    if uploaded_file is None:
        return False

    file_extension = uploaded_file.name.split('.')[-1].lower()
    return file_extension in allowed_types


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} TB"


def show_error_message(error: str, details: str = None):
    """Display formatted error message"""
    st.error(f"❌ {error}")
    if details:
        st.exception(details)


def show_success_message(message: str):
    """Display formatted success message"""
    st.success(f"✅ {message}")


def show_info_message(message: str):
    """Display formatted info message"""
    st.info(f"ℹ️ {message}")


def create_tool_header(title: str, description: str, icon: str = "🛠️"):
    """Create consistent tool header"""
    st.markdown(f"## {icon} {title}")
    st.markdown(f"*{description}*")
    st.markdown("---")


def save_to_favorites(tool_name: str, settings: Dict[str, Any]):
    """Save tool configuration to favorites"""
    favorite = {
        'id': str(uuid.uuid4()),
        'name': tool_name,
        'settings': settings,
        'timestamp': time.time()
    }
    st.session_state.favorites.append(favorite)
    show_success_message(f"Saved {tool_name} to favorites!")


def load_from_favorites():
    """Load and display favorite configurations"""
    if not st.session_state.favorites:
        st.info("No favorites saved yet.")
        return None

    favorite_names = [f"{fav['name']} ({time.strftime('%Y-%m-%d', time.localtime(fav['timestamp']))})"
                      for fav in st.session_state.favorites]

    selected = st.selectbox("Select favorite configuration:", favorite_names)
    if selected:
        index = favorite_names.index(selected)
        return st.session_state.favorites[index]
    return None
