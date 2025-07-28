-- Snowflake Superhero Generator - Complete CI/CD Setup Script
-- This script creates all infrastructure and deploys from Git repository
--
-- PREREQUISITES (must be created by Snowflake admin):
-- 1. Git API Integration: CREATE API INTEGRATION git_api_integration (TYPE=GIT_HTTPS_API, ENABLED=TRUE)
-- 2. Git Credentials: CREATE SECRET git_creds (TYPE=PASSWORD, USERNAME='github_user', PASSWORD='github_token')
-- 3. Permissions: GRANT USAGE ON INTEGRATION git_api_integration TO ROLE CURRENT_ROLE
--
-- This approach enables true CI/CD: any Git push triggers automatic redeployment

-- Create the main visitor tracking table
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
);

-- Create the superhero archetypes reference table
CREATE TABLE IF NOT EXISTS SUPERHERO_ARCHETYPES (
    ARCHETYPE_ID STRING,
    ARCHETYPE_NAME STRING,
    DESCRIPTION STRING,
    TRAITS_VECTOR STRING,
    SAMPLE_NAMES ARRAY,
    SAMPLE_POWERS ARRAY
);

-- Create booth analytics table for event tracking
CREATE TABLE IF NOT EXISTS BOOTH_ANALYTICS (
    EVENT_TIME TIMESTAMP,
    ACTION_TYPE STRING,
    SESSION_ID STRING,
    AI_FUNCTION_USED STRING,
    PROCESSING_TIME_MS NUMBER,
    METADATA VARIANT
);

-- Create stage for photo analysis with AI_CLASSIFY
CREATE STAGE IF NOT EXISTS photo_analysis_stage
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    COMMENT = 'Stage for superhero photo analysis using Cortex AI';

-- Create Git repository integration for CI/CD deployment
CREATE OR REPLACE GIT REPOSITORY superhero_git_repo
    API_INTEGRATION = SFC_GH_MAKUKREJA_INTEGRATION
    ORIGIN = 'https://github.com/sfc-gh-makukreja/cursor-training.git'
    COMMENT = 'Git repository for Snowflake Superhero Generator CI/CD';

-- Create stage for Git repository files  
CREATE STAGE IF NOT EXISTS superhero_stage
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
    COMMENT = 'Stage for Snowflake Superhero Generator from Git repository';

-- Clear existing archetype data (for clean setup)
DELETE FROM SUPERHERO_ARCHETYPES;

-- Insert superhero archetypes using INSERT ... SELECT with PARSE_JSON
INSERT INTO SUPERHERO_ARCHETYPES (ARCHETYPE_ID, ARCHETYPE_NAME, DESCRIPTION, TRAITS_VECTOR, SAMPLE_NAMES, SAMPLE_POWERS)
SELECT 
    'wizard', 'Data Wizard', 'Analytical and transformative', 'analytical, precise, transformative', 
    PARSE_JSON('["The Schema Sage", "Query Quantum", "The Data Whisperer"]'), 
    PARSE_JSON('["Transforms messy data with a glance", "Processes petabytes in milliseconds"]');

INSERT INTO SUPERHERO_ARCHETYPES (ARCHETYPE_ID, ARCHETYPE_NAME, DESCRIPTION, TRAITS_VECTOR, SAMPLE_NAMES, SAMPLE_POWERS)
SELECT 
    'commander', 'Cloud Commander', 'Leadership and scalable', 'leadership, scalable, reliable',
    PARSE_JSON('["Elastico", "The Scale Master", "Cloud Conductor"]'), 
    PARSE_JSON('["Scales infinitely without breaking a sweat", "Commands any cloud workload"]');

INSERT INTO SUPERHERO_ARCHETYPES (ARCHETYPE_ID, ARCHETYPE_NAME, DESCRIPTION, TRAITS_VECTOR, SAMPLE_NAMES, SAMPLE_POWERS)
SELECT 
    'oracle', 'AI Oracle', 'Predictive and insightful', 'predictive, insightful, forward-thinking',
    PARSE_JSON('["Cortex Commander", "ML Maverick", "The Algorithm Alchemist"]'), 
    PARSE_JSON('["Predicts future trends with 99.9% accuracy", "Builds ML models at the speed of thought"]');

INSERT INTO SUPERHERO_ARCHETYPES (ARCHETYPE_ID, ARCHETYPE_NAME, DESCRIPTION, TRAITS_VECTOR, SAMPLE_NAMES, SAMPLE_POWERS)
SELECT 
    'ninja', 'Query Ninja', 'Fast and efficient', 'fast, efficient, problem-solving',
    PARSE_JSON('["Zero-Copy Captain", "Compute Optimizer", "The Concurrency Guardian"]'), 
    PARSE_JSON('["Optimizes any query instantly", "Handles massive concurrency effortlessly"]');

INSERT INTO SUPERHERO_ARCHETYPES (ARCHETYPE_ID, ARCHETYPE_NAME, DESCRIPTION, TRAITS_VECTOR, SAMPLE_NAMES, SAMPLE_POWERS)
SELECT 
    'guardian', 'Security Guardian', 'Protective and governance-focused', 'security, governance, compliance, trust',
    PARSE_JSON('["The Encryption Emperor", "Privacy Protector", "Compliance Commander"]'), 
    PARSE_JSON('["Protects data with unbreakable encryption", "Detects threats before they materialize"]');

INSERT INTO SUPERHERO_ARCHETYPES (ARCHETYPE_ID, ARCHETYPE_NAME, DESCRIPTION, TRAITS_VECTOR, SAMPLE_NAMES, SAMPLE_POWERS)
SELECT 
    'architect', 'Data Architect', 'Design-focused and structural', 'architecture, design, planning, structure',
    PARSE_JSON('["Schema Sage", "Design Deity", "Structure Savant"]'), 
    PARSE_JSON('["Designs perfect data models instantaneously", "Creates architectures that scale to infinity"]');

-- Insert sample booth analytics entry for testing
INSERT INTO BOOTH_ANALYTICS (EVENT_TIME, ACTION_TYPE, SESSION_ID, AI_FUNCTION_USED, PROCESSING_TIME_MS, METADATA)
SELECT 
    CURRENT_TIMESTAMP(),
    'APP_INITIALIZED',
    'system',
    'NONE',
    0,
    PARSE_JSON('{"event": "snowflake_world_tour", "booth": "accenture", "status": "ready"}');

-- Create useful views for analytics
CREATE OR REPLACE VIEW VISITOR_SUMMARY AS
SELECT 
    DATE(TIMESTAMP) as visit_date,
    COUNT(*) as total_visitors,
    COUNT(DISTINCT ARCHETYPE) as unique_archetypes,
    AVG(AI_TOKENS_USED) as avg_tokens_used,
    MODE(ARCHETYPE) as most_popular_archetype,
    MODE(PROFESSIONAL_STYLE) as most_common_style
FROM SUPERHERO_VISITORS
GROUP BY DATE(TIMESTAMP)
ORDER BY visit_date DESC;

CREATE OR REPLACE VIEW HOURLY_TRENDS AS
SELECT 
    DATE_TRUNC('hour', TIMESTAMP) as hour,
    COUNT(*) as visitor_count,
    COUNT(DISTINCT PROFESSIONAL_STYLE) as style_diversity,
    COUNT(DISTINCT ARCHETYPE) as archetype_diversity,
    AVG(AI_TOKENS_USED) as avg_tokens,
    MIN(TIMESTAMP) as first_visit,
    MAX(TIMESTAMP) as last_visit
FROM SUPERHERO_VISITORS
GROUP BY DATE_TRUNC('hour', TIMESTAMP)
ORDER BY hour DESC;

CREATE OR REPLACE VIEW ARCHETYPE_STATS AS
SELECT 
    a.ARCHETYPE_NAME,
    a.DESCRIPTION,
    COALESCE(v.visitor_count, 0) as total_visitors,
    COALESCE(ROUND(v.visitor_count * 100.0 / NULLIF(total.total_visitors, 0), 1), 0) as percentage,
    COALESCE(v.avg_tokens, 0) as avg_tokens_used
FROM SUPERHERO_ARCHETYPES a
LEFT JOIN (
    SELECT 
        ARCHETYPE,
        COUNT(*) as visitor_count,
        AVG(AI_TOKENS_USED) as avg_tokens
    FROM SUPERHERO_VISITORS 
    GROUP BY ARCHETYPE
) v ON a.ARCHETYPE_NAME = v.ARCHETYPE
CROSS JOIN (
    SELECT COUNT(*) as total_visitors FROM SUPERHERO_VISITORS
) total
ORDER BY visitor_count DESC NULLS LAST;

-- Create Streamlit application from Git repository
-- Note: Ensure all changes are merged to main branch before deployment
CREATE OR REPLACE STREAMLIT superhero_generator
  FROM @superhero_git_repo/branches/main/
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = COMPUTE_WH
  TITLE = 'Snowflake Superhero Generator - Git CI/CD'
  COMMENT = 'AI-powered superhero generator deployed from Git repository';

-- Grant permissions (adjust role names as needed)
-- GRANT SELECT ON SUPERHERO_VISITORS TO ROLE STREAMLIT_USER;
-- GRANT SELECT ON SUPERHERO_ARCHETYPES TO ROLE STREAMLIT_USER;
-- GRANT SELECT ON BOOTH_ANALYTICS TO ROLE STREAMLIT_USER;
-- GRANT SELECT ON VISITOR_SUMMARY TO ROLE STREAMLIT_USER;
-- GRANT SELECT ON HOURLY_TRENDS TO ROLE STREAMLIT_USER;
-- GRANT SELECT ON ARCHETYPE_STATS TO ROLE STREAMLIT_USER;

-- Verify setup
SELECT 'Database setup completed successfully!' as status;
SELECT COUNT(*) as archetype_count FROM SUPERHERO_ARCHETYPES;
SELECT COUNT(*) as visitor_count FROM SUPERHERO_VISITORS;
SELECT COUNT(*) as analytics_count FROM BOOTH_ANALYTICS; 