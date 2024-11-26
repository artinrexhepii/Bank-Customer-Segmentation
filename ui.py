import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import numpy as np
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set Page Configuration with a cleaner layout
st.set_page_config(
    page_title="Raiffeisen Bank Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    /* Modern color palette */
    :root {
        --raiffeisen-yellow: #FFE600;
        --raiffeisen-black: #000000;
        --raiffeisen-gray-100: #F8F9FA;
        --raiffeisen-gray-200: #E9ECEF;
        --raiffeisen-gray-300: #DEE2E6;
        --raiffeisen-white: #FFFFFF;
        --shadow-sm: 0 2px 4px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
        --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
    }

    /* Force light mode and consistent styling */
    .stApp {
        background-color: var(--raiffeisen-gray-100) !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--raiffeisen-black) !important;
        padding: 1.5rem 1rem !important;
    }

    /* Remove default radio button styling */
    [data-testid="stSidebar"] .stRadio input {
        display: none !important;  /* Force hide radio buttons */
    }

    /* Button container */
    [data-testid="stSidebar"] .stRadio {
        display: block;
        width: 100%;
        margin: 0.5rem 0;
    }

    /* Button styling */
    [data-testid="stSidebar"] .stRadio > label {
        display: flex;
        align-items: center;
        width: 100%;
        padding: 0.8rem 1.2rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.08);
        color: var(--raiffeisen-white) !important;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Hover state */
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(255, 230, 0, 0.15);
        border-color: var(--raiffeisen-yellow);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Selected/Active state */
    [data-testid="stSidebar"] .stRadio input:checked + label {
        background: #FFE600 !important;
        color: var(--raiffeisen-black) !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 230, 0, 0.3) !important;
    }

    /* Icon styling */
    [data-testid="stSidebar"] .stRadio > label::before {
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        margin-right: 12px;
        background-size: 20px;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.8;
        transition: all 0.3s ease;
    }

    /* Section headers */
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {
        color: var(--raiffeisen-gray-300) !important;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 1.5rem 0 0.5rem;
        margin-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        font-weight: 600;
    }

    /* Main navigation buttons */
    [data-testid="stSidebar"] .stRadio > label:has-text("OVERVIEW")::before {
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23FFFFFF"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>');
    }

    [data-testid="stSidebar"] .stRadio > label:has-text("Customer")::before {
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23FFFFFF"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>');
    }

    [data-testid="stSidebar"] .stRadio > label:has-text("Products")::before {
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23FFFFFF"><path d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/></svg>');
    }

    /* Account menu buttons */
    [data-testid="stSidebar"] .stRadio[data-testid="account_menu"] > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
    }

    /* Icon color change on active state */
    [data-testid="stSidebar"] .stRadio input:checked + label::before {
        filter: brightness(0) saturate(100%);
    }

    /* Logo section */
    .sidebar-logo {
        display: flex;
        align-items: center;
        padding: 1rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255, 230, 0, 0.1);
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
    }
    
    .sidebar-logo img {
        width: 32px;
        height: 32px;
        margin-right: 12px;
    }
    
    .sidebar-logo-text {
        color: var(--raiffeisen-yellow);
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Footer styling */
    .sidebar-footer {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        font-size: 0.8rem;
        color: var(--raiffeisen-gray-300);
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Header styles */
    h1 {
        color: var(--raiffeisen-black);
        font-family: 'Arial', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid var(--raiffeisen-yellow);
    }

    h2, h3 {
        color: var(--raiffeisen-black);
        font-family: 'Arial', sans-serif;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Card styling */
    .card {
        background-color: var(--raiffeisen-white);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid var(--raiffeisen-gray-200);
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    .card-title {
        font-size: 1.1rem;
        color: var(--raiffeisen-black);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .card-value {
        font-size: 2rem;
        color: var(--raiffeisen-black);
        font-weight: 700;
    }

    /* Button styling */
    .stButton button {
        background-color: var(--raiffeisen-yellow);
        color: var(--raiffeisen-black);
        border: none;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9rem;
    }
    .stButton button:hover {
        background-color: #FFD700;
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }

    /* Input fields styling */
    [data-testid="stTextInput"] input, 
    [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] {
        border-radius: 8px;
        border: 2px solid var(--raiffeisen-gray-200);
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }
    [data-testid="stTextInput"] input:focus, 
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stSelectbox"]:focus {
        border-color: var(--raiffeisen-yellow);
        box-shadow: 0 0 0 2px rgba(255, 230, 0, 0.2);
    }

    /* Table styling */
    [data-testid="stTable"] {
        background-color: var(--raiffeisen-white);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
    }
    [data-testid="stTable"] th {
        background-color: var(--raiffeisen-black);
        color: var(--raiffeisen-white);
        padding: 1rem;
    }
    [data-testid="stTable"] td {
        padding: 1rem;
        border-bottom: 1px solid var(--raiffeisen-gray-200);
    }

    /* Chart styling */
    [data-testid="stPlotlyChart"] {
        background-color: var(--raiffeisen-white);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: var(--shadow-sm);
    }

    /* Main Navigation Section Title */
    [data-testid="stSidebar"] h3 {
        color: var(--raiffeisen-white) !important;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 2rem 0 1rem;
        padding: 0 1rem;
        font-weight: 600;
    }

    /* Remove default radio appearance */
    [data-testid="stSidebar"] .stRadio input {
        display: none;
    }

    /* Button Container */
    [data-testid="stSidebar"] .stRadio {
        margin: 0.5rem 0;
    }

    /* Navigation Button Styling */
    [data-testid="stSidebar"] .stRadio > label {
        display: flex;
        align-items: center;
        width: 100%;
        padding: 0.9rem 1.2rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.08);
        color: var(--raiffeisen-white) !important;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-transform: none;  /* Reset text transform for buttons */
    }

    /* Hover Effect */
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(255, 230, 0, 0.15);
        border-color: var(--raiffeisen-yellow);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Selected/Active State */
    [data-testid="stSidebar"] .stRadio input:checked + label {
        background: #FFE600 !important;
        color: var(--raiffeisen-black) !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 230, 0, 0.3) !important;
    }

    /* Icon Styling */
    [data-testid="stSidebar"] .stRadio > label::before {
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        margin-right: 12px;
        background-size: 20px;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.8;
        transition: all 0.3s ease;
    }

    /* Custom icons for each navigation item */
    [data-testid="stSidebar"] .stRadio > label:has-text("OVERVIEW")::before {
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23FFFFFF"><path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/></svg>');
    }

    [data-testid="stSidebar"] .stRadio > label:has-text("Customer")::before {
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23FFFFFF"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>');
    }

    [data-testid="stSidebar"] .stRadio > label:has-text("Products")::before {
        background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23FFFFFF"><path d="M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14z"/></svg>');
    }

    /* Icon color change on active state */
    [data-testid="stSidebar"] .stRadio input:checked + label::before {
        filter: brightness(0) saturate(100%);
    }

    /* Add to your existing CSS */
    .stExpander {
        background-color: var(--raiffeisen-white);
        border-radius: 8px;
        border: 1px solid var(--raiffeisen-gray-200);
        margin-bottom: 0.5rem;
    }

    .stExpander:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    /* Metric cards */
    .metric-card {
        background: var(--raiffeisen-white);
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: var(--shadow-sm);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--raiffeisen-black);
    }

    .metric-label {
        font-size: 0.9rem;
        color: var(--raiffeisen-gray-300);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox select, div[data-baseweb="select"] {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ddd !important;
        padding: 0.5rem !important;
        border-radius: 5px !important;
        width: 100% !important;
    }
    
    /* Style for selectbox dropdown */
    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
    }
    
    /* Style for selectbox options */
    div[data-baseweb="popover"] div[role="listbox"] {
        background-color: white !important;
    }
    
    div[data-baseweb="popover"] div[role="option"] {
        background-color: white !important;
        color: black !important;
    }
    
    div[data-baseweb="popover"] div[role="option"]:hover {
        background-color: #f8f9fa !important;
    }
    
    /* Style for selected option */
    div[data-baseweb="select"] div[aria-selected="true"] {
        background-color: white !important;
        color: black !important;
    }
    
    .stSlider {
        padding: 1rem 0 !important;
    }
    
    .input-label {
        color: #333;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        padding: 10px 16px;
        color: black !important;
        font-weight: 500;
        background-color: #f8f9fa;
        border-radius: 6px;
        border: 1px solid #dee2e6;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e9ecef;
        border-color: #ced4da;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFE600 !important;
        color: black !important;
        font-weight: 600;
        border: none !important;
    }
    
    /* Ensure text color remains black */
    .stTabs [role="tabpanel"] p {
        color: black !important;
    }
    
    /* Style the tab content area */
    .stTabs [role="tabpanel"] {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
    }

    /* Radio button container - more specific selector */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    /* Radio button label - more specific selector */
    .stRadio > div > div > label {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        padding: 0.8rem 1.2rem !important;
        margin: 0.5rem 0 !important;
        border-radius: 8px !important;
        background: rgba(255, 255, 255, 0.08) !important;
        color: var(--raiffeisen-white) !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }

    /* Hide default radio button */
    .stRadio > div > div > label > div:first-child {
        display: none !important;
    }

    /* Hover state */
    .stRadio > div > div > label:hover {
        background: rgba(255, 230, 0, 0.15) !important;
        border-color: var(--raiffeisen-yellow) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }

    /* Selected state */
    .stRadio > div > div[aria-checked="true"] > label {
        background: #FFE600 !important;
        color: var(--raiffeisen-black) !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 230, 0, 0.3) !important;
    }

    /* Update the radio button CSS styling */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        background: transparent !important;
    }

    /* Individual radio button label */
    .stRadio > div > div > label {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        padding: 0.8rem 1.2rem !important;
        margin: 0.3rem 0 !important;
        border-radius: 8px !important;
        background: rgba(255, 255, 255, 0.08) !important;
        color: var(--raiffeisen-white) !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }

    /* Hide the default radio button circle */
    .stRadio > div > div > label > div:first-child {
        display: none !important;
    }

    /* Hover state */
    .stRadio > div > div > label:hover {
        background: rgba(255, 230, 0, 0.15) !important;
        border-color: var(--raiffeisen-yellow) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }

    /* Selected state */
    .stRadio > div > div[aria-checked="true"] > label {
        background: #FFE600 !important;
        color: var(--raiffeisen-black) !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 230, 0, 0.3) !important;
    }

    /* Reset and base styles */
    .stRadio [role="radiogroup"] {
        gap: 0.5rem !important;
    }
    
    /* Style for all radio buttons */
    .stRadio label {
        width: 100% !important;
        background: rgba(255, 255, 255, 0.1) !important;
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
        color: white !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin: 0.2rem 0 !important;
    }
    
    /* Hide the default radio button */
    .stRadio input {
        display: none !important;
    }
    
    /* Hover effect */
    .stRadio label:hover {
        background: rgba(255, 230, 0, 0.2) !important;
        transform: translateX(4px) !important;
    }
    
    /* Selected state */
    .stRadio [data-checked=true] label {
        background: #FFE600 !important;
        color: black !important;
        font-weight: 600 !important;
        transform: translateX(4px) !important;
    }
    
    /* Section headers */
    [data-testid="stSidebar"] h3 {
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.1rem !important;
        padding-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
        text-transform: uppercase !important;
    }
    
    /* Container adjustments */
    [data-testid="stSidebar"] > div {
        padding: 1.5rem 1rem !important;
    }
    
    /* Add icons to options */
    .stRadio label {
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }

    /* Consistent sizing for all input fields */
    .stNumberInput,
    .stSelectbox,
    div[data-baseweb="select"],
    div[data-baseweb="input"] {
        width: 100% !important;
    }

    /* Input field containers */
    .stNumberInput > div,
    .stSelectbox > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        width: 100% !important;
    }

    /* Actual input elements */
    .stNumberInput input,
    .stSelectbox select,
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] input {
        height: 42px !important;
        min-height: 42px !important;
        max-height: 42px !important;
        width: 100% !important;
        padding: 0.5rem 1rem !important;
        box-sizing: border-box !important;
        margin: 0 !important;
        line-height: 1.5 !important;
    }

    /* Select box specific styling */
    div[data-baseweb="select"] > div {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Input label styling */
    .input-label {
        margin-bottom: 0.5rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #333 !important;
    }

    /* Container spacing */
    .stColumn > div {
        padding: 0.5rem !important;
    }

    /* Remove any default margins that might affect alignment */
    .stNumberInput, .stSelectbox {
        margin: 0 !important;
    }

    /* Ensure select boxes match number input height */
    div[data-baseweb="select"] span {
        line-height: 42px !important;
    }

    /* Style for the dropdown arrow in select boxes */
    div[data-baseweb="select"] svg {
        height: 42px !important;
    }

    /* Ensure consistent spacing between rows */
    .row-widget {
        margin-bottom: 1rem !important;
    }

    /* Radio button styling */
    .stRadio [role="radiogroup"] {
        gap: 0.5rem !important;
    }
    
    /* Style for all radio buttons */
    .stRadio label {
        width: 100% !important;
        background: rgba(255, 255, 255, 0.1) !important;
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
        color: white !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin: 0.2rem 0 !important;
    }
    
    /* Hide the default radio button */
    .stRadio input {
        display: none !important;
    }
    
    /* Hover effect */
    .stRadio label:hover {
        background: rgba(255, 230, 0, 0.2) !important;
        transform: translateX(4px) !important;
    }
    
    /* Selected state */
    .stRadio [data-checked=true] label {
        background: #FFE600 !important;
        color: black !important;
        font-weight: 600 !important;
        transform: translateX(4px) !important;
    }

    /* Additional specificity for radio buttons */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] > div[role="radiogroup"] > div[data-checked="true"] {
        background-color: #FFE600 !important;
        color: black !important;
    }

    /* Radio button when checked */
    .stRadio > div > div[data-checked="true"] {
        background-color: #FFE600 !important;
        color: black !important;
    }

    .st-az {
        background-color: #FFE600 !important;
    }

    .st-emotion-cache-1dp5vir {
        position: absolute;
        top: 0px;
        right: 0px;
        left: 0px;
        height: 0.125rem;
        background-image: none;  /* Remove gradient */
        background-color: #FFE600 !important;  /* Add solid Raiffeisen yellow */
        z-index: 999990;
    }
    </style>
""", unsafe_allow_html=True)

# Add logo and brand name to sidebar
st.sidebar.markdown("""
    <div class="sidebar-logo">
        <img src="https://companieslogo.com/img/orig/RAW.F-6920c4d1.png?t=1720244493" alt="Raiffeisen Logo">
        <span class="sidebar-logo-text">Raiffeisen Bank</span>
    </div>
""", unsafe_allow_html=True)

# Main Navigation
st.sidebar.markdown("<h3>MAIN NAVIGATION</h3>", unsafe_allow_html=True)
nav_options = {
    "Overview": "📊",
    "Customer": "👥",
    "Products": "🛍️"
}

menu = st.sidebar.radio(
    label="Navigation",
    options=list(nav_options.keys()),
    label_visibility="collapsed",
    format_func=lambda x: f"{nav_options[x]} {x}"
)

# Account Navigation
st.sidebar.markdown("<h3>ACCOUNT</h3>", unsafe_allow_html=True)
account_options = {
    "Settings": "⚙️",
    "Profile": "👤",
    "Help": "❓"
}

account_menu = st.sidebar.radio(
    label="Account",
    options=list(account_options.keys()),
    label_visibility="collapsed",
    format_func=lambda x: f"{account_options[x]} {x}",
    key="account_section"
)

# Add footer to sidebar
st.sidebar.markdown("""
    <div class="sidebar-footer">
        © 2024 Raiffeisen Bank<br>
        All rights reserved
    </div>
""", unsafe_allow_html=True)

# Load the scaler and model (add this near your other initializations)
with open('scaler_and_model.pkl', 'rb') as f:
    saved_objects = pickle.load(f)
    scaler = saved_objects['scaler']
    kmeans5 = saved_objects['model']

# Add this before the button click handler
clusters = {
    "Engaged Mid-Tier Customers": {
        "description": "Middle-aged customers with very low tenure and average balance. Moderately active with 1-2 products and higher engagement. Slight exit risk.",
        "icon": "🎯",
        "products": [
            {"name": "Loyalty Rewards Program", "description": "Rewards for higher product usage to increase engagement"},
            {"name": "Customized Investment Plans", "description": "Mid-range investments targeting moderate balance"},
            {"name": "Flexible Credit Card Options", "description": "Cash-back and travel rewards"},
            {"name": "Personalized Financial Coaching", "description": "Maximize engagement and benefits"},
            {"name": "Bundle Discounts", "description": "Package multiple products to increase loyalty"}
        ]
    },
    "Low-Balance Loyalists": {
        "description": "Middle-aged customers with moderate tenure and very low balances. Hold more products, less active but high salary. Rarely leave the bank.",
        "icon": "💎",
        "products": [
            {"name": "Low-Threshold Savings Plans", "description": "No minimum balance requirements"},
            {"name": "No-Fee Credit Cards", "description": "Increase product adoption without financial burden"},
            {"name": "Budget Management Tools", "description": "Plan and grow financial assets"},
            {"name": "Exclusive Discounts", "description": "Incentives for everyday transactions"},
            {"name": "Loyalty Recognition Programs", "description": "Acknowledge loyalty to maintain engagement"}
        ]
    },
    "High-Balance At-Risk Customers": {
        "description": "Middle-aged customers with moderate tenure and highest average balance. Fewer products, less active. Highest exit risk requiring attention.",
        "icon": "⚡",
        "products": [
            {"name": "Premium Relationship Manager", "description": "Dedicated support for personalized attention"},
            {"name": "Priority Services", "description": "Faster loan approvals and priority customer service"},
            {"name": "High-Yield Savings Accounts", "description": "Higher interest rates for substantial balances"},
            {"name": "Exit Prevention Offers", "description": "Targeted retention offers and waived fees"},
            {"name": "Financial Goal Consultations", "description": "Tailored consultations to address dissatisfaction"}
        ]
    }
}

# Add these constants at the top of your file
SENDER_EMAIL = "artinrexhepi03@gmail.com"
SENDER_PASSWORD = "gitr wahh gmrd syye"  # Replace with your App Password

def send_product_email(receiver_email, product_name, product_description, customer_surname):
    # Email setup
    msg = MIMEMultipart('alternative')
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = f"Raiffeisen Bank: Information about {product_name}"

    # HTML Email template
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #000000;
                padding: 20px;
                text-align: center;
            }}
            .header img {{
                max-width: 200px;
                height: auto;
            }}
            .content {{
                background-color: #ffffff;
                padding: 30px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .product-name {{
                color: #000000;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .product-description {{
                background-color: #f9f9f9;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                color: #666666;
                font-size: 12px;
            }}
            .button {{
                display: inline-block;
                background-color: #FFE600;
                color: #000000;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
                font-weight: bold;
            }}
            .contact-info {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eeeeee;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://companieslogo.com/img/orig/RAW.F-6920c4d1.png?t=1720244493" alt="Raiffeisen Bank Logo">
            </div>
            <div class="content">
                <p>Dear {customer_surname},</p>
                
                <p>Thank you for your interest in our financial products. We're excited to provide you with information about our:</p>
                
                <div class="product-name">{product_name}</div>
                
                <div class="product-description">
                    {product_description}
                </div>
                
                <p>This product has been specifically recommended based on your profile and financial needs.</p>
                
                <a href="#" class="button">Learn More</a>
                
                <div class="contact-info">
                    <p>If you have any questions or would like to proceed with this product, please don't hesitate to:</p>
                    <ul>
                        <li>Call us at: <strong>+383 38 222 222</strong></li>
                        <li>Visit your nearest branch</li>
                        <li>Reply to this email</li>
                    </ul>
                </div>
            </div>
            <div class="footer">
                <p>© 2024 Raiffeisen Bank Kosovo. All rights reserved.</p>
                <p>This email was sent to {receiver_email}</p>
                <p>Raiffeisen Bank Kosovo J.S.C. | Prishtina, Kosovo</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Attach HTML version
    msg.attach(MIMEText(html, 'html'))

    try:
        # Create SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, receiver_email, text)
        
        # Close session
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

if menu == "Customer":
    # Header with modern design
    st.markdown("""
        <div style='background: #000000; 
                    padding: 2.5rem; 
                    border-radius: 15px; 
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h1 style='color: #FFE600; margin: 0; font-size: 2.8rem; font-weight: 700;'>Customer Profile & Analytics</h1>
            <p style='color: #ffffff; margin-top: 0.8rem; font-size: 1.2rem; opacity: 0.9;'>
                Analyze and predict customer segments based on their profile
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Instead of separate cards in col1 and col2, create a single full-width card
    st.markdown("""
        <div style='background: white; 
                    padding: 2rem; 
                    border-radius: 12px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                    margin-bottom: 1rem;'>
            <h3 style='color: #000000; 
                      font-size: 1.3rem; 
                      margin-bottom: 1.5rem; 
                      border-bottom: 2px solid #FFE600; 
                      padding-bottom: 0.5rem;'>
                Client Details
            </h3>
    """, unsafe_allow_html=True)

    # Create two columns for the inputs
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<p class='input-label'>Surname</p>", unsafe_allow_html=True)
        surname = st.text_input("",
            value="",
            key="surname",
            help="Customer's surname",
            label_visibility="collapsed")
        
        st.markdown("<p class='input-label'>Credit Score</p>", unsafe_allow_html=True)
        credit_score = st.number_input("",
            min_value=300, max_value=850, value=650,
            key="credit_score",
            help="Customer's credit score (300-850)",
            label_visibility="collapsed")
            
        st.markdown("<p class='input-label'>Balance ($)</p>", unsafe_allow_html=True)
        balance = st.number_input("",
            min_value=0, value=0,
            key="balance",
            format="%d",
            help="Current account balance",
            label_visibility="collapsed")
            
        st.markdown("<p class='input-label'>Products Per Year</p>", unsafe_allow_html=True)
        products_per_year = st.number_input("",
            min_value=0, max_value=10, value=1,
            key="products_per_year",
            help="Number of products purchased per year",
            label_visibility="collapsed")
            
        st.markdown("<p class='input-label'>Has Credit Card</p>", unsafe_allow_html=True)
        has_cr_card = st.selectbox("",
            ["No", "Yes"],
            key="has_cr_card",
            help="Whether the customer has a credit card",
            label_visibility="collapsed")
        has_cr_card = 1 if has_cr_card == "Yes" else 0
            
        st.markdown("<p class='input-label'>Is Active Member</p>", unsafe_allow_html=True)
        is_active = st.selectbox("",
            ["No", "Yes"],
            key="is_active",
            help="Whether the customer is actively using services",
            label_visibility="collapsed")
        is_active = 1 if is_active == "Yes" else 0

    with col2:
        st.markdown("<p class='input-label'>Email</p>", unsafe_allow_html=True)
        email = st.text_input("",
            value="",
            key="email",
            help="Customer's email address",
            label_visibility="collapsed")
        
        st.markdown("<p class='input-label'>Age</p>", unsafe_allow_html=True)
        age = st.number_input("",
            min_value=18, max_value=100, value=35,
            key="age",
            help="Customer's age",
            label_visibility="collapsed")
            
        st.markdown("<p class='input-label'>Estimated Salary ($)</p>", unsafe_allow_html=True)
        estimated_salary = st.number_input("",
            min_value=0, value=50000, step=1000,
            key="estimated_salary",
            format="%d",
            help="Customer's estimated annual salary",
            label_visibility="collapsed")
            
        st.markdown("<p class='input-label'>Tenure (Years)</p>", unsafe_allow_html=True)
        tenure = st.number_input("",
            min_value=0, max_value=50, value=5,
            key="tenure",
            help="Years as a customer",
            label_visibility="collapsed")
            
        st.markdown("<p class='input-label'>Gender</p>", unsafe_allow_html=True)
        gender = st.selectbox("",
            ["Male", "Female"],
            key="gender",
            help="Customer's gender",
            label_visibility="collapsed")
            
        st.markdown("<p class='input-label'>Number of Products</p>", unsafe_allow_html=True)
        num_products = st.selectbox("",
            options=list(range(11)),
            key="num_products",
            help="Number of bank products currently used",
            label_visibility="collapsed")

    # Close the card div
    st.markdown("</div>", unsafe_allow_html=True)

    # Generate Analysis Button with enhanced styling
    st.markdown("""
        <div style='background: white; 
                    padding: 2rem; 
                    border-radius: 12px; 
                    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                    margin-top: 1rem;'>
    """, unsafe_allow_html=True)
    
    if st.button("Generate Customer Analysis", 
                 type="primary",
                 use_container_width=True,
                 key="generate_analysis"):
        
        # Convert gender to binary
        gender_binary = 1 if gender == "Male" else 0
        
        # Create array with values in specified order
        customer_data = [
            credit_score, gender_binary, age, tenure, balance,
            num_products, has_cr_card, is_active, estimated_salary,
            products_per_year
        ]
        
        # Convert to DataFrame
        columns = ['CreditScore', 'Gender', 'Age', 'Tenure', 'Balance',
                  'NumOfProducts', 'HasCrCard', 'IsActiveMember',
                  'EstimatedSalary', 'ProductsPerYear']
        
        customer_array = np.array(customer_data).reshape(1, -1)
        customer_df = pd.DataFrame(customer_array, columns=columns)
        
        # Scale and predict
        customer_scaled = scaler.transform(customer_df)
        predicted_cluster = kmeans5.predict(customer_scaled)[0]
        
        # Map cluster numbers to names
        cluster_keys = {
            0: "Engaged Mid-Tier Customers",
            1: "Low-Balance Loyalists",
            2: "High-Balance At-Risk Customers"
        }
        
        cluster_key = cluster_keys[predicted_cluster]
        
        # Store the results in session state so they persist
        st.session_state.predicted_cluster = predicted_cluster
        st.session_state.cluster_key = cluster_key
        st.session_state.cluster_info = clusters[cluster_key]

# Check if we have results to display (either from button click or stored in session)
if hasattr(st.session_state, 'predicted_cluster'):
    cluster_key = st.session_state.cluster_key
    
    # Display result with enhanced styling
    st.markdown(f"""
        <div style='background: #000000; 
                    padding: 2rem; 
                    border-radius: 15px; 
                    margin: 2rem 0;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <h2 style='color: #FFE600; 
                      margin: 0; 
                      font-size: 2rem; 
                      display: flex; 
                      align-items: center;'>
                <span style='background: rgba(255,230,0,0.2); 
                           padding: 0.5rem; 
                           border-radius: 8px; 
                           margin-right: 1rem;'>
                    {clusters[cluster_key]['icon']}
                </span>
                Customer Segment: {cluster_key}
            </h2>
            <p style='color: #ffffff; 
                      margin-top: 1rem; 
                      font-size: 1.1rem; 
                      opacity: 0.9;'>
                {clusters[cluster_key]['description']}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display recommended products with enhanced styling
    st.markdown("""
        <h3 style='color: #000000; 
                  font-size: 1.5rem; 
                  margin: 2rem 0 1rem; 
                  padding-bottom: 0.5rem; 
                  border-bottom: 2px solid #FFE600;'>
            Recommended Products
        </h3>
    """, unsafe_allow_html=True)
    
    # Display products in an enhanced grid
    cols = st.columns(2)
    for idx, product in enumerate(clusters[cluster_key]['products']):
        with cols[idx % 2]:
            st.markdown(f"""
                <div style='background: white; 
                              padding: 1.5rem; 
                              border-radius: 12px; 
                              margin-bottom: 1rem; 
                              box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                              border: 1px solid #eee;
                              transition: transform 0.2s ease, box-shadow 0.2s ease;'>
                    <div style='font-size: 1.1rem; 
                              font-weight: 600; 
                              color: #000; 
                              margin-bottom: 0.8rem;
                              display: flex;
                              align-items: center;'>
                        <span style='background: #FFE600;
                                   padding: 0.4rem;
                                   border-radius: 6px;
                                   margin-right: 0.8rem;
                                   font-size: 0.9rem;'>
                            {idx + 1}
                        </span>
                        {product['name']}
                    </div>
                    <div style='color: #666;
                              line-height: 1.5;
                              margin-bottom: 1rem;'>
                        {product['description']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
                
            # Only show email button if email is provided and not empty
            if email and email.strip():
                if st.button(f"📧 Send Product Info", key=f"email_{idx}"):
                    if send_product_email(email, product['name'], product['description'], surname):
                        st.markdown("""
                            <div style='color: white; 
                                      font-weight: bold; 
                                      background-color: #00C853; 
                                      padding: 0.75rem; 
                                      border-radius: 6px; 
                                      text-align: center;'>
                                Product information sent successfully!
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("Failed to send email. Please try again later.")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Overview":
    # Load the CSV data
    df = pd.read_csv('clustered_data.csv')

    # Header with gradient background
    st.markdown("""
        <div style='background: #000000; 
                    padding: 2rem; 
                    border-radius: 10px; 
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='color: #FFE600; margin: 0; font-size: 2.5rem;'>Dashboard Overview</h1>
            <p style='color: #ffffff; margin-top: 0.5rem; font-size: 1.1rem;'>Customer Segmentation Analysis</p>
        </div>
    """, unsafe_allow_html=True)

    # Calculate metrics from the CSV data
    total_customers = len(df.index)
    avg_balance = df['Balance'].mean()
    avg_tenure = df['Tenure'].mean()
    active_users = len(df[df['Exited'] == 0])

    # Define metrics with dynamic values
    metrics = [
        {
            'title': 'Total Customers',
            'value': f"{total_customers:,}",
            'delta': '2.1% vs last month',
            'icon': '👥'
        },
        {
            'title': 'Average Balance',
            'value': f"${avg_balance:,.2f}",
            'delta': '3.2% vs last month',
            'icon': '💰'
        },
        {
            'title': 'Average Tenure',
            'value': f"{avg_tenure:.1f} years",
            'delta': '1.8% vs last month',
            'icon': '⏳'
        },
        {
            'title': 'Active Users',
            'value': f"{active_users:,}",
            'delta': '4.3% vs last month',
            'icon': '✨'
        }
    ]

    # Display metrics in a grid
    col1, col2, col3, col4 = st.columns(4)
    
    for metric, col in zip(metrics, [col1, col2, col3, col4]):
        col.markdown(f"""
            <div style='background-color: white; 
                        padding: 1.5rem; 
                        border-radius: 10px; 
                        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                        transition: transform 0.3s ease;
                        border: 1px solid #eee;'
                 onmouseover="this.style.transform='translateY(-5px)'"
                 onmouseout="this.style.transform='translateY(0)'">
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                    <span style='color: #666; font-size: 0.9rem;'>{metric['title']}</span>
                    <span style='font-size: 1.5rem;'>{metric['icon']}</span>
                </div>
                <div style='font-size: 1.8rem; font-weight: 600; color: #000; margin-bottom: 0.5rem;'>
                    {metric['value']}
                </div>
                <div style='color: #00C853; font-size: 0.8rem; display: flex; align-items: center;'>
                    ↑ {metric['delta']}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Charts section with single tab (removed financial metrics tab)
    st.markdown("<br>", unsafe_allow_html=True)
    tab1 = st.tabs(["📊 Distribution Analysis"])[0]  # Changed to single tab
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            # Calculate cluster distribution
            cluster_dist = df['Cluster'].value_counts().reset_index()
            cluster_dist.columns = ['Clusters', 'Users']
            
            # Map cluster numbers to their names
            cluster_names = {
                0: "Engaged Mid-Tier",
                1: "Low-Balance Loyalists",
                2: "High-Balance At-Risk"
            }
            cluster_dist['Clusters'] = cluster_dist['Clusters'].map(cluster_names)
            
            # Customer Distribution Chart with black axis labels
            fig1 = px.bar(cluster_dist, 
                         x="Clusters", 
                         y="Users",
                         color="Clusters",
                         title="Customer Distribution by Segment",
                         color_discrete_sequence=["#FFE600", "#000000", "#666666"])
            
            fig1.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=50, l=10, r=10, b=10),
                showlegend=False,
                title_x=0.5,
                title_font_size=16,
                xaxis=dict(tickfont=dict(color='black')),
                yaxis=dict(tickfont=dict(color='black'))
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            # Calculate average balance by cluster
            balance_by_cluster = df.groupby('Cluster')['Balance'].mean().reset_index()
            
            # Map cluster numbers to their names
            cluster_names = {
                0: "Engaged Mid-Tier",
                1: "Low-Balance Loyalists",
                2: "High-Balance At-Risk"
            }
            balance_by_cluster['Cluster'] = balance_by_cluster['Cluster'].map(cluster_names)
            
            # Balance Distribution Chart
            fig2 = px.pie(balance_by_cluster, 
                         names="Cluster", 
                         values="Balance",
                         title="Average Balance Distribution by Segment",
                         color_discrete_sequence=["#FFE600", "#000000", "#666666"])
            
            fig2.update_traces(textinfo='label+percent+value', 
                             texttemplate='%{label}<br>$%{value:,.2f}<br>(%{percent})')
            
            fig2.update_layout(
                margin=dict(t=50, l=10, r=10, b=10),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                title_x=0.5,
                title_font_size=16
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Bottom section with additional insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 10px; height: 100%;'>
                <h3 style='color: #000; margin-bottom: 1rem;'>Key Insights</h3>
                <ul style='color: #666; margin: 0; padding-left: 1.2rem;'>
                    <li style='margin-bottom: 0.5rem;'>High-Balance At-Risk segment holds the highest average balance but shows concerning exit patterns</li>
                    <li style='margin-bottom: 0.5rem;'>Low-Balance Loyalists demonstrate strong retention despite lower balances</li>
                    <li style='margin-bottom: 0.5rem;'>Engaged Mid-Tier customers show balanced product usage and moderate activity</li>
                    <li>Customer engagement correlates strongly with product diversity and tenure</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 10px; height: 100%;'>
                <h3 style='color: #000; margin-bottom: 1rem;'>Recommendations</h3>
                <ul style='color: #666; margin: 0; padding-left: 1.2rem;'>
                    <li style='margin-bottom: 0.5rem;'>Implement targeted retention strategies for High-Balance At-Risk segment</li>
                    <li style='margin-bottom: 0.5rem;'>Develop product upgrade paths for Low-Balance Loyalists to increase their value</li>
                    <li style='margin-bottom: 0.5rem;'>Create engagement programs for Mid-Tier customers to prevent churn</li>
                    <li>Focus on cross-selling opportunities to increase product adoption across segments</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

elif menu == "Products":
    st.markdown("""
        <div style='background: linear-gradient(90deg, #000000 0%, #333333 100%); 
                    padding: 2rem; 
                    border-radius: 10px; 
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='color: #FFE600; margin: 0; font-size: 2.5rem;'>Cluster-Specific Products</h1>
            <p style='color: #ffffff; margin-top: 0.5rem; font-size: 1.1rem;'>Tailored financial solutions for each customer segment</p>
        </div>
    """, unsafe_allow_html=True)

    # Create tabs for each cluster
    tabs = st.tabs(list(clusters.keys()))
    
    # Load the CSV data
    df = pd.read_csv('clustered_data.csv')

    # Update the customer table section in the cluster tab loop
    for tab, (cluster_name, cluster_data) in zip(tabs, clusters.items()):
        with tab:
            # Display cluster information
            st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;'>
                    <div style='display: flex; align-items: center; margin-bottom: 1rem;'>
                        <div style='font-size: 2rem; margin-right: 1rem;'>{cluster_data['icon']}</div>
                        <div>
                            <div style='font-size: 1.3rem; font-weight: 600; color: #000;'>{cluster_name}</div>
                            <div style='color: #666;'>{cluster_data['description']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Display recommended products
            st.markdown("<h3 style='color: #000; margin-bottom: 1rem;'>Recommended Products</h3>", unsafe_allow_html=True)
            
            cols = st.columns(2)
            for idx, product in enumerate(cluster_data['products']):
                with cols[idx % 2]:
                    st.markdown(f"""
                        <div style='background: white; 
                                  padding: 1.5rem; 
                                  border-radius: 12px; 
                                  margin-bottom: 1rem; 
                                  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                                  border: 1px solid #eee;'>
                            <div style='font-size: 1.1rem; 
                                      font-weight: 600; 
                                      color: #000; 
                                      margin-bottom: 0.8rem;
                                      display: flex;
                                      align-items: center;'>
                                <span style='background: #FFE600;
                                           padding: 0.4rem;
                                           border-radius: 6px;
                                           margin-right: 0.8rem;
                                           font-size: 0.9rem;'>
                                    {idx + 1}
                                </span>
                                {product['name']}
                            </div>
                            <div style='color: #666;
                                      line-height: 1.5;'>
                                {product['description']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            # Show customer table
            st.markdown("""
                <div style='margin-top: 2rem; margin-bottom: 1rem;'>
                    <h3 style='color: #000; font-size: 1.3rem;'>Cluster Customer Overview</h3>
                </div>
            """, unsafe_allow_html=True)

            # Map segment names to cluster numbers
            cluster_mapping = {
                "Engaged Mid-Tier Customers": 0,
                "Low-Balance Loyalists": 1,
                "High-Balance At-Risk Customers": 2
            }
            
            # Get cluster number from the mapping
            cluster_num = cluster_mapping[cluster_name]
            
            # Filter data for this cluster
            cluster_df = df[df['Cluster'] == cluster_num].copy()
            
            # Select columns for display
            display_columns = ['CustomerId', 'Surname', 'CreditScore', 'Geography', 
                             'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 
                             'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Exited']
            
            display_df = cluster_df[display_columns].copy()
            
            # Format the columns
            display_df['Balance'] = display_df['Balance'].apply(lambda x: f"${x:,.2f}")
            display_df['EstimatedSalary'] = display_df['EstimatedSalary'].apply(lambda x: f"${x:,.2f}")
            display_df['HasCrCard'] = display_df['HasCrCard'].map({1: 'Yes', 0: 'No'})
            display_df['IsActiveMember'] = display_df['IsActiveMember'].map({1: 'Yes', 0: 'No'})
            display_df['Exited'] = display_df['Exited'].map({1: 'Yes', 0: 'No'})
            
            # Display the table
            st.dataframe(
                display_df,
                hide_index=True,
                use_container_width=True
            )

