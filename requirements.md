# Snowflake World Tour - Superhero AI App Requirements

## Project Overview
Interactive Streamlit in Snowflake app for Accenture's booth activation at Snowflake World Tour. The app will capture photos of visitors and generate Snowflake AI Data Cloud-themed superhero identities with relevant superpowers.

## Business Requirements

### Primary Objectives
- **Booth Engagement**: Create an interactive, fun experience to draw visitors to Accenture's booth
- **Brand Alignment**: Showcase Snowflake AI Data Cloud capabilities in a creative way
- **Lead Generation**: Collect visitor engagement data and potentially contact information
- **Memorable Experience**: Provide shareable content that visitors will remember

### Target Audience
- Snowflake World Tour attendees
- Data professionals, engineers, analysts
- Decision makers in data and AI
- Technical and business stakeholders

## Functional Requirements

### Core Features
1. **Camera Integration**
   - Live camera feed display
   - Photo capture functionality
   - Image preview and retake option
   - Support for mobile and desktop cameras

2. **AI-Powered Predictions (using Snowflake Cortex AISQL)**
   - Generate Snowflake-themed superhero names using AI_COMPLETE
   - Classify visitor photos to determine superhero archetype using AI_CLASSIFY
   - Predict relevant superpowers based on image analysis using AI_COMPLETE
   - Filter superhero options based on data professional traits using AI_FILTER
   - Fast processing (< 5 seconds for booth environment)

3. **Result Display**
   - Professional-looking superhero identity card
   - Include captured photo
   - Display generated name and superpower
   - Accenture and Snowflake branding

4. **User Experience**
   - Simple, intuitive interface
   - Clear instructions
   - One-click photo capture
   - Option to restart/try again

### Superhero Themes (Snowflake AI Data Cloud Focused)

#### Superhero Names/Titles
- **Data Architects**: "The Schema Sage", "Pipeline Prophet", "The Data Whisperer"
- **AI Specialists**: "Cortex Commander", "ML Maverick", "The Algorithm Alchemist"
- **Analytics Heroes**: "Query Quantum", "Insight Oracle", "The Warehouse Wizard"
- **Cloud Champions**: "Elastico", "The Scale Master", "Cloud Conductor"
- **Performance Heroes**: "Zero-Copy Captain", "Compute Optimizer", "The Concurrency Guardian"

#### Superpowers
- **Data Powers**: "Can process petabytes in a single query", "Transforms messy data with a glance"
- **AI Powers**: "Predicts future trends with 99.9% accuracy", "Builds ML models at the speed of thought"
- **Scale Powers**: "Scales infinitely without breaking a sweat", "Handles any workload surge effortlessly"
- **Security Powers**: "Protects data with unbreakable encryption", "Detects anomalies before they happen"
- **Collaboration Powers**: "Shares insights across any cloud instantly", "Connects teams through data magic"

## Technical Requirements

### Snowflake Integration
- **Deployment**: Streamlit in Snowflake (SiS)
- **Data Storage**: Store visitor interactions, generated names, and analytics
- **AI Services**: Leverage Snowflake Cortex AISQL functions:
  - `AI_CLASSIFY()` for photo categorization (age group, professional style, mood)
  - `AI_COMPLETE()` for superhero name and power generation
  - `AI_FILTER()` for content filtering and appropriateness
  - `AI_SIMILARITY()` for matching similar superhero archetypes
- **Security**: Implement proper data governance and privacy controls

### App Architecture
```
├── streamlit_app.py          # Main application file
├── pages/
│   ├── camera_capture.py     # Camera functionality
│   ├── result_display.py     # Show superhero identity
│   └── admin_dashboard.py    # Analytics (optional)
├── utils/
│   ├── superhero_generator.py # Name and power logic
│   ├── image_processor.py     # Image handling
│   └── database_handler.py    # Snowflake operations
├── assets/
│   ├── logo_accenture.png
│   ├── logo_snowflake.png
│   └── superhero_template.png
├── environment.yml           # Dependencies
└── README.md                # Setup instructions
```

### Required Dependencies
```yaml
# environment.yml
name: superhero-app
dependencies:
  - streamlit
  - streamlit-webrtc  # Camera integration
  - opencv-python     # Image processing
  - pillow           # Image manipulation
  - pandas           # Data handling
  - snowflake-snowpark-python  # Snowflake integration
  - requests         # API calls if needed
```

### Cortex AISQL Implementation

#### Photo Analysis Pipeline
```sql
-- 1. Classify visitor photo characteristics
SELECT AI_CLASSIFY(
  image_data,
  ['professional', 'casual', 'creative', 'technical'],
  'style'
) as professional_style,
AI_CLASSIFY(
  image_data,
  ['confident', 'analytical', 'innovative', 'collaborative'],
  'personality_traits'
) as traits;

-- 2. Generate superhero identity based on classification
SELECT AI_COMPLETE(
  'Generate a Snowflake Data Cloud superhero name for someone with ' || 
  professional_style || ' style and ' || traits || ' traits. ' ||
  'The name should relate to data, AI, cloud computing, or analytics.',
  500
) as superhero_name;

-- 3. Generate matching superpower
SELECT AI_COMPLETE(
  'Create a data/AI-related superpower for ' || superhero_name || 
  ' that matches their ' || traits || ' personality. ' ||
  'Focus on Snowflake capabilities like scaling, performance, AI, or data governance.',
  300
) as superpower;

-- 4. Filter for appropriateness
SELECT AI_FILTER(
  superhero_name || ': ' || superpower,
  'inappropriate_content'
) as is_appropriate;
```

#### Superhero Archetype Matching
```sql
-- Use AI_SIMILARITY to match against predefined archetypes
WITH superhero_archetypes AS (
  SELECT * FROM VALUES
    ('Data Wizard', 'analytical, precise, transformative'),
    ('Cloud Commander', 'leadership, scalable, reliable'),
    ('AI Oracle', 'predictive, insightful, forward-thinking'),
    ('Query Ninja', 'fast, efficient, problem-solving')
  AS t(archetype, traits)
)
SELECT 
  archetype,
  AI_SIMILARITY(visitor_traits, traits) as similarity_score
FROM superhero_archetypes
ORDER BY similarity_score DESC
LIMIT 1;
```

### Performance Requirements
- **Response Time**: < 5 seconds from photo to result (including AI processing)
- **Concurrent Users**: Support 10-20 simultaneous booth visitors
- **Reliability**: 99%+ uptime during event hours
- **Mobile Responsive**: Work on phones, tablets, laptops
- **AI Token Limits**: Optimize prompt length for cost-effective Cortex usage

## Implementation Plan

### Phase 1: Core Application (Week 1)
1. **Setup Snowflake Environment**
   - Create database, schema, and tables
   - Set up Streamlit app framework
   - Configure development environment

2. **Basic UI Development**
   - Create main app structure
   - Implement camera capture interface
   - Design result display layout

3. **Cortex AISQL Integration**
   - Implement AI_CLASSIFY for photo analysis
   - Develop AI_COMPLETE prompts for name/power generation
   - Create superhero archetype database
   - Test AI response quality and performance

### Phase 2: Enhancement & Integration (Week 2)
1. **Advanced Features**
   - Integrate Snowflake Cortex for AI predictions
   - Add image processing capabilities
   - Implement data storage and analytics

2. **UI/UX Polish**
   - Apply Accenture and Snowflake branding
   - Optimize for booth environment
   - Add animations and visual effects

3. **Testing & Optimization**
   - Performance testing
   - Mobile compatibility testing
   - Load testing for concurrent users

### Phase 3: Deployment & Booth Prep (Week 3)
1. **Production Deployment**
   - Deploy to Snowflake production environment
   - Configure monitoring and logging
   - Set up backup plans

2. **Booth Integration**
   - Hardware setup guidelines
   - Staff training materials
   - Troubleshooting procedures

## Data Requirements

### Database Schema
```sql
-- Visitor interactions with AI analysis
CREATE TABLE superhero_visitors (
    visit_id STRING,
    timestamp TIMESTAMP,
    superhero_name STRING,
    superpower STRING,
    archetype STRING,
    image_path STRING,
    ai_analysis VARIANT,  -- Store AI_CLASSIFY results
    professional_style STRING,
    personality_traits STRING,
    similarity_scores VARIANT,
    ai_tokens_used NUMBER,
    session_data VARIANT
);

-- Analytics tracking
CREATE TABLE booth_analytics (
    event_time TIMESTAMP,
    action_type STRING,
    session_id STRING,
    ai_function_used STRING,
    processing_time_ms NUMBER,
    metadata VARIANT
);

-- Superhero archetypes for AI_SIMILARITY matching
CREATE TABLE superhero_archetypes (
    archetype_id STRING,
    archetype_name STRING,
    description STRING,
    traits_vector STRING,
    sample_names ARRAY,
    sample_powers ARRAY
);
```

### Privacy Considerations
- **Image Storage**: Store images temporarily, delete after session
- **Data Collection**: Minimal PII collection, focus on engagement metrics
- **Consent**: Clear privacy notice and opt-in mechanism
- **Compliance**: Follow GDPR/CCPA guidelines for data handling

## Success Metrics

### Primary KPIs
- **Engagement**: Number of photos taken per hour
- **Completion Rate**: % of visitors who complete the full experience
- **Sharing**: Social media mentions and shares
- **Lead Quality**: Booth conversation starter effectiveness

### Technical Metrics
- **Response Time**: Average time from photo to result
- **Error Rate**: % of failed photo captures or generations
- **Uptime**: App availability during event hours
- **Performance**: Page load times and user experience scores

## Risk Mitigation

### Technical Risks
- **Camera Compatibility**: Test across multiple devices and browsers
- **Network Dependency**: Offline mode for basic functionality
- **Performance Issues**: Load balancing and optimization strategies
- **Security**: Secure image handling and data protection

### Event Risks
- **Hardware Failure**: Backup devices and quick recovery procedures
- **High Traffic**: Queue management and user flow optimization
- **Staff Training**: Comprehensive booth staff onboarding
- **Connectivity**: Backup internet solutions

## Budget Considerations

### Development Costs
- Development time: 2-3 weeks
- Snowflake compute costs: Estimated $200-500 for event period
- **Cortex AISQL costs**: Estimated $300-800 for event period
  - AI_CLASSIFY: ~$0.02 per image analysis
  - AI_COMPLETE: ~$0.05 per superhero generation
  - Expected 500-1000 visitors during event
- Additional tools/services: $100-300

### Event Costs
- Hardware (tablets/cameras): $500-1000
- Booth setup support: Variable
- Staff training time: 2-4 hours

## Next Steps

1. **Approval**: Review and approve this requirements document
2. **Environment Setup**: Create Snowflake workspace and development environment
3. **Prototype Development**: Build MVP with basic camera and generation features
4. **Iterative Enhancement**: Add features based on testing and feedback
5. **Pre-Event Testing**: Full end-to-end testing in booth-like environment

---

**Timeline**: 3 weeks from approval to deployment
**Primary Contact**: Development team lead
**Review Date**: Weekly progress reviews
**Go-Live**: Snowflake World Tour event dates 