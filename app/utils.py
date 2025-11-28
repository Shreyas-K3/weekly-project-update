import streamlit as st
import base64
import pandas as pd

def load_css(file_name):
    """Loads custom CSS file."""
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Provides a gentle warning if the CSS file isn't found
        print(f"CSS file not found at {file_name}. Displaying without custom styles.")


def get_base64_image_data(uploaded_file):
    """Converts an uploaded file to a Base64 string suitable for HTML/CSS img src."""
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        base64_encoded = base64.b64encode(file_bytes).decode('utf-8')
        mime_type = uploaded_file.type
        # Return the complete data URL string
        return f"data:{mime_type};base64,{base64_encoded}"
    return None

def roadmap_svg(size="32"): 
    """Returns a simple SVG icon for a roadmap/journey, used for Current Progress/Next Week Plan."""
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#FF0000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="roadmap-icon" style="vertical-align: middle; margin-right: 8px;">
        <path d="M12 22s-8-4-8-10c0-4.4 3.6-8 8-8s8 3.6 8 8c0 6-8 10-8 10z"></path>
        <circle cx="12" cy="10" r="3"></circle>
        <path d="M12 10l0 12"></path>
    </svg>
    """

def kshitij_logo_svg(size="32"):
    """
    Returns a placeholder SVG icon for Kshitij logo (a red circle with a white 'K').
    This is used as a fallback when no logo is uploaded by the admin.
    """
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 100 100" style="vertical-align: middle; margin-left: 8px;">
        <rect width="100" height="100" fill="#FF0000" rx="50" ry="50"/>
        <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="AvantGarde, sans-serif" font-size="60" fill="white">K</text>
    </svg>
    """

def create_circular_meter(label, value, max_value, color, size="200px"):
    """Generates custom HTML/CSS for a circular meter (gauge)."""
    # Safety check to prevent ZeroDivisionError if max_value is 0
    if max_value == 0:
        percentage = 0
    else:
        percentage = (value / max_value) * 100
        
    if percentage > 100: percentage = 100 # Cap at 100% for display
    
    # Generate HTML structure with CSS variables for dynamic sizing and coloring
    return f"""
    <div class="meter-card">
        <div class="circular-meter large-gauge" style="--p:{percentage}; --c:{color}; --size: {size};">
            <div class="meter-label">{label}</div>
            <div class="meter-value">{value}{'%' if max_value == 100 else ''}</div>
        </div>
    </div>
    """
