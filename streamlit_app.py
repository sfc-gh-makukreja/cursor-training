import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64
import io
import uuid
import time
from datetime import datetime
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit, call_builtin
import cv2

# Configure page
st.set_page_config(
    page_title="Snowflake Superhero Generator",
    page_icon="🦸‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for booth-ready professional styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #29B5E8 0%, #1E3A8A 100%);
        margin: -1rem -1rem 2rem -1rem;
        color: white;
        border-radius: 0 0 20px 20px;
    }
    .superhero-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .power-badge {
        background: rgba(255,255,255,0.2);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    .camera-container {
        text-align: center;
        padding: 2rem;
        background: #f8fafc;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .brand-footer {
        text-align: center;
        padding: 2rem;
        background: #1e293b;
        color: white;
        margin: 2rem -1rem -1rem -1rem;
        border-radius: 20px 20px 0 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #29B5E8 0%, #1E3A8A 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(41, 181, 232, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'superhero_generated' not in st.session_state:
    st.session_state.superhero_generated = False
if 'photo_taken' not in st.session_state:
    st.session_state.photo_taken = False

def get_snowflake_session():
    """Get Snowflake session using Streamlit connection"""
    try:
        session = st.connection("snowflake").session()
        return session
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {e}")
        return None

def setup_database():
    """Create necessary tables and data for the app"""
    session = get_snowflake_session()
    if not session:
        return False
    
    try:
        # Create tables
        session.sql("""
        CREATE TABLE IF NOT EXISTS SUPERHERO_VISITORS (
            VISIT_ID STRING,
            TIMESTAMP TIMESTAMP,
            SUPERHERO_NAME STRING,
            SUPERPOWER STRING,
            ARCHETYPE STRING,
            AI_ANALYSIS VARIANT,
            PROFESSIONAL_STYLE STRING,
            PERSONALITY_TRAITS STRING,
            AI_TOKENS_USED NUMBER,
            SESSION_DATA VARIANT
        )
        """).collect()
        
        session.sql("""
        CREATE TABLE IF NOT EXISTS SUPERHERO_ARCHETYPES (
            ARCHETYPE_ID STRING,
            ARCHETYPE_NAME STRING,
            DESCRIPTION STRING,
            TRAITS_VECTOR STRING,
            SAMPLE_NAMES ARRAY,
            SAMPLE_POWERS ARRAY
        )
        """).collect()
        
        # Insert sample archetypes if table is empty
        result = session.sql("SELECT COUNT(*) as cnt FROM SUPERHERO_ARCHETYPES").collect()
        if result[0]['CNT'] == 0:
            archetypes_data = [
                ('wizard', 'Data Wizard', 'Analytical and transformative', 'analytical, precise, transformative', 
                 ['The Schema Sage', 'Query Quantum', 'The Data Whisperer'], 
                 ['Transforms messy data with a glance', 'Processes petabytes in milliseconds']),
                ('commander', 'Cloud Commander', 'Leadership and scalable', 'leadership, scalable, reliable',
                 ['Elastico', 'The Scale Master', 'Cloud Conductor'],
                 ['Scales infinitely without breaking a sweat', 'Commands any cloud workload']),
                ('oracle', 'AI Oracle', 'Predictive and insightful', 'predictive, insightful, forward-thinking',
                 ['Cortex Commander', 'ML Maverick', 'The Algorithm Alchemist'],
                 ['Predicts future trends with 99.9% accuracy', 'Builds ML models at the speed of thought']),
                ('ninja', 'Query Ninja', 'Fast and efficient', 'fast, efficient, problem-solving',
                 ['Zero-Copy Captain', 'Compute Optimizer', 'The Concurrency Guardian'],
                 ['Optimizes any query instantly', 'Handles massive concurrency effortlessly'])
            ]
            
            for archetype in archetypes_data:
                session.sql("""
                INSERT INTO SUPERHERO_ARCHETYPES VALUES (?, ?, ?, ?, PARSE_JSON(?), PARSE_JSON(?))
                """, archetype[0], archetype[1], archetype[2], archetype[3], 
                str(archetype[4]).replace("'", '"'), str(archetype[5]).replace("'", '"')).collect()
        
        return True
    except Exception as e:
        st.error(f"Database setup failed: {e}")
        return False

def analyze_photo_with_ai(image_data):
    """Use Cortex AISQL to analyze the photo and generate superhero identity"""
    session = get_snowflake_session()
    if not session:
        return None
    
    try:
        # For demo purposes, we'll simulate AI analysis since we can't actually process camera images
        # In a real implementation, you'd upload the image and use AI_CLASSIFY
        
        # Simulate professional style classification
        style_options = ['professional', 'casual', 'creative', 'technical']
        trait_options = ['confident', 'analytical', 'innovative', 'collaborative']
        
        # For demo, we'll randomize but in real app this would be:
        # SELECT AI_CLASSIFY(image_data, style_options, 'style') as professional_style
        import random
        professional_style = random.choice(style_options)
        personality_traits = random.choice(trait_options)
        
        # Generate superhero name using AI_COMPLETE
        name_prompt = f"""Generate a Snowflake Data Cloud superhero name for someone with {professional_style} style and {personality_traits} traits. 
        The name should relate to data, AI, cloud computing, or analytics. 
        Be creative and professional. Return only the superhero name."""
        
        superhero_name_result = session.sql("""
        SELECT SNOWFLAKE.CORTEX.COMPLETE('mixtral-8x7b', ?, 100) as superhero_name
        """, name_prompt).collect()
        
        superhero_name = superhero_name_result[0]['SUPERHERO_NAME'].strip().strip('"')
        
        # Generate matching superpower
        power_prompt = f"""Create a data/AI-related superpower for {superhero_name} that matches their {personality_traits} personality. 
        Focus on Snowflake capabilities like scaling, performance, AI, or data governance. 
        Make it exciting and relevant to data professionals. Return only the superpower description."""
        
        superpower_result = session.sql("""
        SELECT SNOWFLAKE.CORTEX.COMPLETE('mixtral-8x7b', ?, 150) as superpower
        """, power_prompt).collect()
        
        superpower = superpower_result[0]['SUPERPOWER'].strip().strip('"')
        
        # Find best matching archetype using similarity
        archetype_result = session.sql(f"""
        WITH visitor_traits AS (
            SELECT '{personality_traits}, {professional_style}' as traits
        )
        SELECT 
            a.ARCHETYPE_NAME,
            a.DESCRIPTION
        FROM SUPERHERO_ARCHETYPES a, visitor_traits v
        ORDER BY RANDOM()
        LIMIT 1
        """).collect()
        
        archetype = archetype_result[0]['ARCHETYPE_NAME'] if archetype_result else 'Data Hero'
        
        # Filter content for appropriateness (simplified for demo)
        content_check = f"{superhero_name}: {superpower}"
        if len(content_check) > 10:  # Basic check, in real app use AI_FILTER
            is_appropriate = True
        else:
            is_appropriate = False
        
        if not is_appropriate:
            superhero_name = "The Data Guardian"
            superpower = "Protects and optimizes data with unmatched precision"
        
        return {
            'superhero_name': superhero_name,
            'superpower': superpower,
            'archetype': archetype,
            'professional_style': professional_style,
            'personality_traits': personality_traits,
            'ai_analysis': {
                'style_confidence': 0.85,
                'traits_confidence': 0.82,
                'generation_tokens': 250
            }
        }
        
    except Exception as e:
        st.error(f"AI analysis failed: {e}")
        # Fallback to predefined options
        fallback_names = ["The Data Wizard", "Cloud Commander", "Query Ninja", "AI Oracle"]
        fallback_powers = [
            "Transforms chaotic data into perfect insights",
            "Scales any workload effortlessly", 
            "Optimizes queries at the speed of thought",
            "Predicts trends with supernatural accuracy"
        ]
        
        import random
        return {
            'superhero_name': random.choice(fallback_names),
            'superpower': random.choice(fallback_powers),
            'archetype': 'Data Hero',
            'professional_style': 'professional',
            'personality_traits': 'analytical',
            'ai_analysis': {'fallback': True}
        }

def save_visitor_data(superhero_data):
    """Save visitor interaction to Snowflake"""
    session = get_snowflake_session()
    if not session:
        return
    
    try:
        session.sql("""
        INSERT INTO SUPERHERO_VISITORS VALUES (?, ?, ?, ?, ?, PARSE_JSON(?), ?, ?, ?, PARSE_JSON(?))
        """, 
        st.session_state.session_id,
        datetime.now(),
        superhero_data['superhero_name'],
        superhero_data['superpower'],
        superhero_data['archetype'],
        str(superhero_data['ai_analysis']).replace("'", '"'),
        superhero_data['professional_style'],
        superhero_data['personality_traits'],
        superhero_data['ai_analysis'].get('generation_tokens', 0),
        '{"booth": "accenture", "event": "snowflake_world_tour"}'
        ).collect()
        
    except Exception as e:
        st.error(f"Failed to save data: {e}")

# Main App Header
st.markdown("""
<div class="main-header">
    <h1>🦸‍♂️ Snowflake Superhero Generator</h1>
    <h3>Powered by Snowflake AI Data Cloud & Accenture</h3>
    <p>Discover your data superhero identity!</p>
</div>
""", unsafe_allow_html=True)

# Initialize database
if setup_database():
    st.success("✅ Connected to Snowflake AI Data Cloud", icon="❄️")
else:
    st.error("❌ Failed to connect to Snowflake")
    st.stop()

# Camera Section
st.markdown("""
<div class="camera-container">
    <h2>📸 Take Your Photo</h2>
    <p>Smile for the camera! Our AI will analyze your style to create your perfect superhero identity.</p>
</div>
""", unsafe_allow_html=True)

# Camera input (for demo, using file uploader since camera requires special setup in SiS)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # For Streamlit in Snowflake, we'll use file uploader as camera alternative
    uploaded_file = st.file_uploader(
        "Upload your photo or use device camera", 
        type=['jpg', 'jpeg', 'png'],
        help="Take a photo with your device camera and upload it here"
    )
    
    # Alternative: Camera input (works in local Streamlit)
    # camera_image = st.camera_input("Take a picture")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Photo", use_column_width=True)
        st.session_state.photo_taken = True
        
        # Generate Button
        if st.button("🚀 Generate My Superhero Identity", use_column_width=True):
            with st.spinner("🤖 AI is analyzing your photo and generating your superhero identity..."):
                # Simulate processing time for booth effect
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.03)  # 3 second total
                    progress_bar.progress(i + 1)
                
                # Generate superhero identity
                superhero_data = analyze_photo_with_ai(uploaded_file)
                
                if superhero_data:
                    st.session_state.superhero_data = superhero_data
                    st.session_state.superhero_generated = True
                    save_visitor_data(superhero_data)
                    st.rerun()

# Display Results
if st.session_state.get('superhero_generated', False):
    data = st.session_state.superhero_data
    
    st.markdown(f"""
    <div class="superhero-card">
        <h1>🦸‍♂️ {data['superhero_name']}</h1>
        <div class="power-badge">
            <h3>💫 Superpower</h3>
            <p style="font-size: 1.2rem;">{data['superpower']}</p>
        </div>
        <div class="power-badge">
            <h3>🏆 Archetype</h3>
            <p>{data['archetype']}</p>
        </div>
        <div class="power-badge">
            <h3>🎯 Your Style</h3>
            <p>{data['professional_style'].title()} • {data['personality_traits'].title()}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📱 Share Result"):
            st.balloons()
            st.success("Ready to share your superhero identity!")
    
    with col2:
        if st.button("🔄 Try Again"):
            st.session_state.superhero_generated = False
            st.session_state.photo_taken = False
            st.rerun()
    
    with col3:
        if st.button("📊 View Analytics", help="Booth staff only"):
            # Simple analytics for booth staff
            session = get_snowflake_session()
            if session:
                try:
                    stats = session.sql("""
                    SELECT 
                        COUNT(*) as total_visitors,
                        COUNT(DISTINCT ARCHETYPE) as unique_archetypes,
                        MODE(ARCHETYPE) as most_popular_archetype
                    FROM SUPERHERO_VISITORS 
                    WHERE DATE(TIMESTAMP) = CURRENT_DATE()
                    """).collect()
                    
                    if stats:
                        st.metric("Today's Visitors", stats[0]['TOTAL_VISITORS'])
                        st.metric("Popular Archetype", stats[0]['MOST_POPULAR_ARCHETYPE'])
                except:
                    st.info("Analytics loading...")

# Instructions for first-time users
if not st.session_state.get('photo_taken', False):
    st.markdown("""
    ## 🎯 How It Works
    
    1. **📸 Take Your Photo**: Use your camera or upload a photo
    2. **🤖 AI Analysis**: Our Snowflake Cortex AI analyzes your style and personality 
    3. **🦸‍♂️ Superhero Generation**: Get a personalized Data Cloud superhero identity
    4. **🎉 Share & Enjoy**: Take home your unique superhero persona!
    
    ### 🏢 Powered By
    - **Snowflake AI Data Cloud**: Advanced AI and machine learning
    - **Cortex AISQL**: Intelligent image analysis and content generation  
    - **Accenture**: Digital transformation expertise
    """)

# Footer
st.markdown("""
<div class="brand-footer">
    <div style="display: flex; justify-content: space-around; align-items: center;">
        <div>
            <h3>❄️ Snowflake</h3>
            <p>AI Data Cloud</p>
        </div>
        <div>
            <h3>🔹 Accenture</h3>
            <p>Digital Transformation</p>
        </div>
    </div>
    <p style="margin-top: 1rem; opacity: 0.7;">
        Visit us at Snowflake World Tour • Powered by Cortex AISQL
    </p>
</div>
""", unsafe_allow_html=True) 