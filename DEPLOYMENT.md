# Snowflake Superhero Generator - Deployment Guide

A professional booth activation app for Snowflake World Tour that generates AI-powered superhero identities using Snowflake Cortex AISQL.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Snowflake     │    │   Cortex AI     │
│      App        │◄──►│   Database      │◄──►│   Functions     │
│                 │    │                 │    │                 │
│ • Photo Upload  │    │ • Visitor Data  │    │ • AI_COMPLETE   │
│ • UI/UX         │    │ • Archetypes    │    │ • Name Gen      │
│ • Analytics     │    │ • Analytics     │    │ • Power Gen     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

- ✅ **Snowflake Account** with Cortex AI access
- ✅ **Snowflake CLI** v3.10.0+ installed
- ✅ **VPN Connection** (if required)
- ✅ **Role with CORTEX_USER** privileges

## Quick Start (Automated)

### Option 1: One-Command Deployment

```bash
# Make deployment script executable
chmod +x deploy.sh

# Run complete deployment
./deploy.sh
```

### Option 2: Manual Step-by-Step

```bash
# 1. Test connection
snow connection test --connection default

# 2. Setup database
snow sql -f setup.sql --connection default

# 3. Deploy app
snow streamlit deploy --connection default --replace
```

## Database Schema

The `setup.sql` script creates:

### Tables
- **`SUPERHERO_VISITORS`** - Visitor interactions and generated heroes
- **`SUPERHERO_ARCHETYPES`** - 6 predefined superhero types with Snowflake themes
- **`BOOTH_ANALYTICS`** - Event tracking and performance metrics

### Views
- **`VISITOR_SUMMARY`** - Daily visitor aggregations
- **`HOURLY_TRENDS`** - Hour-by-hour booth activity
- **`ARCHETYPE_STATS`** - Superhero type popularity rankings

### Sample Archetypes
1. **Data Wizard** - Analytical and transformative
2. **Cloud Commander** - Leadership and scalable  
3. **AI Oracle** - Predictive and insightful
4. **Query Ninja** - Fast and efficient
5. **Security Guardian** - Protective and governance-focused
6. **Data Architect** - Design-focused and structural

## App Features

### Main Application
- 📸 **Photo Upload** with AI analysis simulation
- 🤖 **Cortex AI Integration** for personalized superhero generation
- 🎨 **Professional UI** with Snowflake & Accenture branding
- 📊 **Real-time Analytics** embedded in app

### Admin Dashboard (Password: `snowflake2024`)
- 📈 **Visitor Trends** with interactive charts
- 🦸‍♂️ **Archetype Distribution** analytics
- 🕐 **Recent Activity** live feed
- 💾 **Data Export** functionality
- 📱 **Booth Management** tools

## Configuration Files

### `snowflake.yml`
```yaml
definition_version: 2
entities:
  superhero_generator:
    type: streamlit
    identifier: superhero_generator
    stage: superhero_stage
    query_warehouse: CUBE_TESTING
    title: "Snowflake Superhero Generator"
    main_file: streamlit_app.py
    artifacts:
      - streamlit_app.py
      - environment.yml
      - pages/
      - setup.sql
```

### `environment.yml`
```yaml
name: superhero-app
channels:
  - snowflake
dependencies:
  - streamlit
  - pandas
  - numpy
  - pillow
  - plotly
  - snowflake-snowpark-python
  - requests
```

## Troubleshooting

### Common Issues

**❌ Connection Failed**
```bash
# Check VPN connection
# Verify credentials: ~/.snowflake/config.toml
snow connection test --connection default
```

**❌ Database Setup Failed**
```bash
# Run setup manually
snow sql -f setup.sql --connection default

# Check table creation
snow sql -q "SHOW TABLES LIKE 'SUPERHERO_%'" --connection default
```

**❌ Import Errors**
```bash
# Check environment.yml uses only Snowflake channel packages
# No pip dependencies allowed in SiS
```

**❌ Cortex AI Errors**
```bash
# Verify role has CORTEX_USER privileges
# Check prompt escaping in SQL strings
```

### Reset Database
```sql
-- Clean slate reset (careful!)
DROP TABLE IF EXISTS SUPERHERO_VISITORS;
DROP TABLE IF EXISTS SUPERHERO_ARCHETYPES;
DROP TABLE IF EXISTS BOOTH_ANALYTICS;
DROP VIEW IF EXISTS VISITOR_SUMMARY;
DROP VIEW IF EXISTS HOURLY_TRENDS;
DROP VIEW IF EXISTS ARCHETYPE_STATS;

-- Then run setup.sql again
```

## Monitoring & Analytics

### Real-time Metrics
- **Visitor Count** - Total booth visitors
- **Popular Archetypes** - Most generated superhero types
- **AI Token Usage** - Cortex function costs
- **Engagement Time** - Session duration analytics

### Booth Staff Tools
- 📊 **Live Dashboard** - Real-time visitor stats
- 📱 **App URL Sharing** - Quick QR code generation
- 💾 **Data Export** - CSV download for analysis
- 🔄 **Session Reset** - Clean booth demo state

## Security & Privacy

- 🔒 **No PII Storage** - Only superhero data and engagement metrics
- 🛡️ **Admin Authentication** - Password-protected booth controls
- 📝 **GDPR Compliant** - Minimal data collection with clear consent
- 🔐 **Role-based Access** - Proper Snowflake privilege management

## Event Day Checklist

### Pre-Event Setup
- [ ] Run `./deploy.sh` and verify success
- [ ] Test app functionality end-to-end
- [ ] Verify admin dashboard access
- [ ] Prepare booth hardware (tablets/displays)
- [ ] Brief booth staff on app features

### During Event
- [ ] Monitor app performance via admin dashboard
- [ ] Export visitor data periodically
- [ ] Reset app state if needed
- [ ] Assist visitors with photo uploads

### Post-Event
- [ ] Export final analytics data
- [ ] Generate visitor engagement report
- [ ] Archive booth interaction data
- [ ] Clean up demo tables if needed

## Cost Optimization

### Cortex AI Usage
- **AI_COMPLETE calls**: ~$0.05 per superhero generation
- **Expected volume**: 500-1000 visitors per event
- **Estimated cost**: $300-800 per event

### Warehouse Usage
- **Query processing**: Minimal for app operations
- **Analytics queries**: Lightweight aggregations
- **Estimated cost**: $50-200 per event

## Support & Contact

For issues during the event:
1. Check this troubleshooting guide
2. Verify network connectivity and VPN
3. Contact technical support with specific error messages
4. Have backup booth activities ready

---

**Happy Snowflake World Tour! 🦸‍♂️❄️** 