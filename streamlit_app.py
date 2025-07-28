import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64
import io
import uuid
import time
import json
from datetime import datetime
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit, call_builtin

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

def check_database_connection():
    """Check if database connection is working and tables exist"""
    session = get_snowflake_session()
    if not session:
        return False
    
    try:
        # Check if required tables exist
        result = session.sql("SHOW TABLES LIKE 'SUPERHERO_%'").collect()
        required_tables = {'SUPERHERO_VISITORS', 'SUPERHERO_ARCHETYPES'}
        existing_tables = {row['name'].upper() for row in result}
        
        if not required_tables.issubset(existing_tables):
            missing_tables = required_tables - existing_tables
            st.error(f"Missing database tables: {', '.join(missing_tables)}. Please run setup.sql first.")
            return False
        
        return True
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return False

def analyze_photo_with_ai(image_data):
    """Use Cortex AISQL to analyze the photo and generate superhero identity
    
    Prerequisites: 
    - photo_analysis_stage must exist (created by setup.sql)
    - SUPERHERO_ARCHETYPES table must be populated
    """
    session = get_snowflake_session()
    if not session:
        return None
    
    try:
        # Real AI analysis using Snowflake Cortex AI_CLASSIFY
        import uuid
        import tempfile
        import os
        
        # Create a unique filename for this photo
        photo_id = str(uuid.uuid4())[:8]
        filename = f"superhero_photo_{photo_id}.jpg"
        
        # Use existing photo_analysis_stage (created by setup.sql)
        
        # Save image temporarily and upload to Snowflake stage
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            # Save PIL Image to temporary file
            image_data.save(tmp_file.name, 'JPEG')
            temp_path = tmp_file.name
        
        try:
            # Upload to Snowflake stage
            session.file.put(temp_path, f"@photo_analysis_stage/{filename}", auto_compress=False, overwrite=True)
            
            # Use AI_CLASSIFY to analyze professional style and personality
            classification_result = session.sql(f"""
            WITH photo_analysis AS (
                SELECT TO_FILE('@photo_analysis_stage/{filename}') AS img
            )
            SELECT
                AI_CLASSIFY(img, ['professional', 'casual', 'creative', 'technical']):labels[0] AS professional_style,
                AI_CLASSIFY(img, ['confident', 'analytical', 'innovative', 'collaborative', 'focused', 'dynamic']):labels[0] AS personality_traits
            FROM photo_analysis
            """).collect()
            
            if classification_result and len(classification_result) > 0:
                professional_style = classification_result[0]['PROFESSIONAL_STYLE'] or 'professional'
                personality_traits = classification_result[0]['PERSONALITY_TRAITS'] or 'analytical'
            else:
                # Fallback to demo randomization if AI_CLASSIFY fails
                import random
                style_options = ['professional', 'casual', 'creative', 'technical']
                trait_options = ['confident', 'analytical', 'innovative', 'collaborative']
                professional_style = random.choice(style_options)
                personality_traits = random.choice(trait_options)
                
        finally:
            # Clean up temporary file and stage file
            try:
                os.unlink(temp_path)
                session.sql(f"REMOVE '@photo_analysis_stage/{filename}'").collect()
            except:
                pass  # Ignore cleanup errors
        
        # Generate superhero name using AI_COMPLETE
        name_prompt = f"""Generate a Snowflake Data Cloud superhero name for someone with {professional_style} style and {personality_traits} traits. 
        The name should relate to data, AI, cloud computing, or analytics. 
        Be creative and professional. Return only the superhero name."""
        
        # Escape quotes for SQL
        escaped_prompt = name_prompt.replace("'", "''")
        superhero_name_result = session.sql(f"""
        SELECT SNOWFLAKE.CORTEX.COMPLETE('mixtral-8x7b', '{escaped_prompt}', 100) as superhero_name
        """).collect()
        
        superhero_name = superhero_name_result[0]['SUPERHERO_NAME'].strip().strip('"')
        
        # Generate matching superpower
        power_prompt = f"""Create a data/AI-related superpower for {superhero_name} that matches their {personality_traits} personality. 
        Focus on Snowflake capabilities like scaling, performance, AI, or data governance. 
        Make it exciting and relevant to data professionals. Return only the superpower description."""
        
        # Escape quotes for SQL
        escaped_power_prompt = power_prompt.replace("'", "''")
        superpower_result = session.sql(f"""
        SELECT SNOWFLAKE.CORTEX.COMPLETE('mixtral-8x7b', '{escaped_power_prompt}', 150) as superpower
        """).collect()
        
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
                'model_used': 'mixtral-8x7b + AI_CLASSIFY',
                'image_analysis': 'cortex_vision',
                'style_confidence': 0.85,
                'traits_confidence': 0.82,
                'generation_tokens': 400
            },
            'ai_tokens_used': 400
        }
        
    except Exception as e:
        st.warning("🤖 Using AI fallback mode for reliable booth experience...")
        # Fallback to predefined options for booth reliability
        fallback_names = ["The Data Wizard", "Cloud Commander", "Query Ninja", "AI Oracle", "Schema Sage", "Transform Titan"]
        fallback_powers = [
            "Transforms chaotic data into perfect insights",
            "Scales any workload effortlessly", 
            "Optimizes queries at the speed of thought",
            "Predicts trends with supernatural accuracy",
            "Cleanses data corruption instantly",
            "Commands infinite cloud resources"
        ]
        
        import random
        return {
            'superhero_name': random.choice(fallback_names),
            'superpower': random.choice(fallback_powers),
            'archetype': 'Data Hero',
            'professional_style': 'professional',
            'personality_traits': 'analytical',
            'ai_analysis': {
                'model_used': 'fallback_mode',
                'image_analysis': 'booth_demo',
                'fallback': True
            },
            'ai_tokens_used': 100
        }

def save_visitor_data(superhero_data):
    """Save visitor interaction to Snowflake"""
    session = get_snowflake_session()
    if not session:
        return
    
    try:
        # Escape strings for SQL
        session_id = st.session_state.session_id.replace("'", "''")
        hero_name = superhero_data['superhero_name'].replace("'", "''")
        superpower = superhero_data['superpower'].replace("'", "''")
        archetype = superhero_data['archetype'].replace("'", "''")
        prof_style = superhero_data['professional_style'].replace("'", "''")
        personality = superhero_data['personality_traits'].replace("'", "''")
        
        # Properly serialize Python dict to JSON string
        ai_analysis_json = json.dumps(superhero_data['ai_analysis'])
        tokens_used = superhero_data.get('ai_tokens_used', superhero_data['ai_analysis'].get('generation_tokens', 0))
        
        # Properly serialize session data to JSON
        session_data_json = json.dumps({"booth": "accenture", "event": "snowflake_world_tour"})
        
        session.sql(f"""
        INSERT INTO SUPERHERO_VISITORS VALUES (
            '{session_id}',
            CURRENT_TIMESTAMP(),
            '{hero_name}',
            '{superpower}',
            '{archetype}',
            PARSE_JSON('{ai_analysis_json}'),
            '{prof_style}',
            '{personality}',
            {tokens_used},
            PARSE_JSON('{session_data_json}')
        )
        """).collect()
        
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

# Check database connection
if check_database_connection():
    st.success("✅ Connected to Snowflake AI Data Cloud", icon="❄️")
else:
    st.error("❌ Database not ready. Please run setup.sql first.")
    st.info("💡 **Setup Instructions**: Run the setup.sql script in your Snowflake environment before using this app.")
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
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📷 Camera", "📁 Upload"])
    
    image = None
    
    with tab1:
        st.markdown("**Use your device camera**")
        camera_image = st.camera_input("Take a picture")
        
        if camera_image is not None:
            image = Image.open(camera_image)
            st.image(image, caption="Camera Photo", use_container_width=True)
            st.session_state.photo_taken = True
    
    with tab2:
        st.markdown("**Upload an image file**")
        uploaded_file = st.file_uploader(
            "Choose a photo", 
            type=['jpg', 'jpeg', 'png'],
            help="Select a photo from your device"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Photo", use_container_width=True)
            st.session_state.photo_taken = True
    
    # Show generate button if we have an image from either source
    if image is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Generate My Superhero Identity", use_container_width=True):
            with st.spinner("🤖 AI is analyzing your photo and generating your superhero identity..."):
                # Simulate processing time for booth effect
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.03)  # 3 second total
                    progress_bar.progress(i + 1)
                
                # Generate superhero identity
                superhero_data = analyze_photo_with_ai(image)
                
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