import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from snowflake.snowpark import Session

# Configure page
st.set_page_config(
    page_title="Booth Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

def get_snowflake_session():
    """Get Snowflake session using Streamlit connection"""
    try:
        session = st.connection("snowflake").session()
        return session
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {e}")
        return None

def get_visitor_stats(session, hours_back=24):
    """Get visitor statistics for the specified time period"""
    try:
        # Get visitor count and trends
        stats_query = f"""
        SELECT 
            COUNT(*) as total_visitors,
            COUNT(DISTINCT DATE_TRUNC('hour', TIMESTAMP)) as active_hours,
            AVG(AI_TOKENS_USED) as avg_tokens_used,
            MODE(ARCHETYPE) as most_popular_archetype,
            MODE(PROFESSIONAL_STYLE) as most_common_style,
            MODE(PERSONALITY_TRAITS) as most_common_trait
        FROM SUPERHERO_VISITORS 
        WHERE TIMESTAMP >= DATEADD('hour', -{hours_back}, CURRENT_TIMESTAMP())
        """
        
        result = session.sql(stats_query).collect()
        return result[0] if result else None
        
    except Exception as e:
        st.error(f"Error fetching visitor stats: {e}")
        return None

def get_hourly_trends(session, hours_back=24):
    """Get hourly visitor trends"""
    try:
        trends_query = f"""
        SELECT 
            DATE_TRUNC('hour', TIMESTAMP) as hour,
            COUNT(*) as visitor_count,
            COUNT(DISTINCT PROFESSIONAL_STYLE) as style_diversity,
            AVG(AI_TOKENS_USED) as avg_tokens
        FROM SUPERHERO_VISITORS 
        WHERE TIMESTAMP >= DATEADD('hour', -{hours_back}, CURRENT_TIMESTAMP())
        GROUP BY DATE_TRUNC('hour', TIMESTAMP)
        ORDER BY hour DESC
        """
        
        result = session.sql(trends_query).collect()
        return pd.DataFrame([row.asDict() for row in result]) if result else pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error fetching hourly trends: {e}")
        return pd.DataFrame()

def get_archetype_distribution(session, hours_back=24):
    """Get distribution of superhero archetypes"""
    try:
        archetype_query = f"""
        SELECT 
            ARCHETYPE,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
        FROM SUPERHERO_VISITORS 
        WHERE TIMESTAMP >= DATEADD('hour', -{hours_back}, CURRENT_TIMESTAMP())
        GROUP BY ARCHETYPE
        ORDER BY count DESC
        """
        
        result = session.sql(archetype_query).collect()
        return pd.DataFrame([row.asDict() for row in result]) if result else pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error fetching archetype distribution: {e}")
        return pd.DataFrame()

def get_recent_visitors(session, limit=10):
    """Get most recent visitors with their superhero identities"""
    try:
        recent_query = f"""
        SELECT 
            TIMESTAMP,
            SUPERHERO_NAME,
            SUPERPOWER,
            ARCHETYPE,
            PROFESSIONAL_STYLE,
            PERSONALITY_TRAITS
        FROM SUPERHERO_VISITORS 
        ORDER BY TIMESTAMP DESC
        LIMIT {limit}
        """
        
        result = session.sql(recent_query).collect()
        return pd.DataFrame([row.asDict() for row in result]) if result else pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error fetching recent visitors: {e}")
        return pd.DataFrame()

# Admin Authentication (simple password protection)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Booth Staff Access")
    password = st.text_input("Enter admin password:", type="password")
    
    if st.button("Login"):
        if password == "snowflake2024":  # Simple password for demo
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

# Main Dashboard
st.title("📊 Snowflake World Tour - Booth Analytics Dashboard")
st.markdown("**Real-time visitor engagement and superhero generation insights**")

# Get Snowflake session
session = get_snowflake_session()
if not session:
    st.error("Unable to connect to database")
    st.stop()

# Dashboard controls
col1, col2, col3 = st.columns(3)
with col1:
    hours_back = st.selectbox("Time Period", [1, 4, 8, 24, 48], index=3, help="Hours to look back")
with col2:
    if st.button("🔄 Refresh Data"):
        st.rerun()
with col3:
    st.metric("Status", "🟢 Live", help="Dashboard is connected and updating")

# Get data
visitor_stats = get_visitor_stats(session, hours_back)
hourly_trends = get_hourly_trends(session, hours_back)
archetype_dist = get_archetype_distribution(session, hours_back)
recent_visitors = get_recent_visitors(session)

# Key Metrics Row
if visitor_stats:
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Visitors", 
            visitor_stats['TOTAL_VISITORS'],
            help=f"Visitors in last {hours_back} hours"
        )
    
    with col2:
        st.metric(
            "Active Hours", 
            visitor_stats['ACTIVE_HOURS'],
            help="Hours with visitor activity"
        )
    
    with col3:
        avg_tokens = visitor_stats['AVG_TOKENS_USED'] or 0
        st.metric(
            "Avg AI Tokens", 
            f"{avg_tokens:.0f}",
            help="Average tokens used per generation"
        )
    
    with col4:
        st.metric(
            "Popular Archetype", 
            visitor_stats['MOST_POPULAR_ARCHETYPE'] or "N/A",
            help="Most generated superhero type"
        )
    
    with col5:
        st.metric(
            "Common Style", 
            visitor_stats['MOST_COMMON_STYLE'] or "N/A",
            help="Most detected professional style"
        )

st.divider()

# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Visitor Trends")
    if not hourly_trends.empty:
        fig = px.line(
            hourly_trends, 
            x='HOUR', 
            y='VISITOR_COUNT',
            title=f"Visitors per Hour (Last {hours_back}h)",
            labels={'VISITOR_COUNT': 'Visitors', 'HOUR': 'Time'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No visitor data available for the selected time period")

with col2:
    st.subheader("🦸‍♂️ Superhero Types")
    if not archetype_dist.empty:
        fig = px.pie(
            archetype_dist, 
            values='COUNT', 
            names='ARCHETYPE',
            title="Superhero Archetype Distribution"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No archetype data available")

st.divider()

# Recent Activity
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🕐 Recent Visitors")
    if not recent_visitors.empty:
        # Format the dataframe for display
        display_df = recent_visitors.copy()
        display_df['TIMESTAMP'] = pd.to_datetime(display_df['TIMESTAMP']).dt.strftime('%H:%M:%S')
        display_df = display_df.rename(columns={
            'TIMESTAMP': 'Time',
            'SUPERHERO_NAME': 'Hero Name',
            'SUPERPOWER': 'Superpower',
            'ARCHETYPE': 'Type',
            'PROFESSIONAL_STYLE': 'Style',
            'PERSONALITY_TRAITS': 'Traits'
        })
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=300
        )
    else:
        st.info("No recent visitors")

with col2:
    st.subheader("📋 Booth Actions")
    
    if st.button("📱 Share App URL", use_container_width=True):
        app_url = "https://app.snowflake.com/SFSEAPAC/makukreja_aws_us_west_2/#/streamlit-apps/CUBE_TESTING.PUBLIC.SUPERHERO_GENERATOR"
        st.code(app_url)
        st.success("URL ready to share!")
    
    if st.button("💾 Export Data", use_container_width=True):
        if not recent_visitors.empty:
            csv = recent_visitors.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "booth_visitors.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.warning("No data to export")
    
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# Auto-refresh footer
st.markdown("---")
st.markdown(
    "**💡 Tip:** This dashboard auto-refreshes when you click 'Refresh Data'. "
    "Monitor visitor engagement throughout the event!"
)

# Real-time status indicator
current_time = datetime.now().strftime("%H:%M:%S")
st.caption(f"Last updated: {current_time} | Snowflake World Tour Booth Analytics") 