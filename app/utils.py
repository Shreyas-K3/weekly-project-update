import streamlit as st

def load_css(file_name):
    """Loads custom CSS file."""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def roadmap_svg(size="24"):
    """Returns a simple SVG icon for a roadmap/journey."""
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="#FF0000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="roadmap-icon">
        <path d="M12 22s-8-4-8-10c0-4.4 3.6-8 8-8s8 3.6 8 8c0 6-8 10-8 10z"></path>
        <circle cx="12" cy="10" r="3"></circle>
        <path d="M12 10l0 12"></path>
    </svg>
    """

def create_circular_meter(label, value, max_value, color):
    """Generates custom HTML/CSS for a circular meter."""
    percentage = (value / max_value) * 100
    if percentage > 100: percentage = 100 # Cap at 100% for progress
    
    # CSS for the meter is in style.css, this just generates the HTML structure
    return f"""
    <div class="meter-card">
        <div class="circular-meter" style="--p:{percentage}; --c:{color};">
            <div class="meter-label">{label}</div>
            <div class="meter-value">{value}{'%' if max_value == 100 else ''}</div>
        </div>
    </div>
    """
