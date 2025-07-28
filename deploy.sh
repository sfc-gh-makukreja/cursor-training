#!/bin/bash

# Snowflake Superhero Generator Deployment Script
# This script sets up the database and deploys the Streamlit app

set -e  # Exit on any error

echo "🚀 Starting Snowflake Superhero Generator deployment..."
echo ""

# Check if Snowflake CLI is available
if ! command -v snow &> /dev/null; then
    echo "❌ Snowflake CLI not found. Please install it first:"
    echo "   https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation/installation"
    exit 1
fi

# Test Snowflake connection
echo "🔗 Testing Snowflake connection..."
if ! snow connection test --connection default &> /dev/null; then
    echo "❌ Failed to connect to Snowflake with default connection."
    echo "   Please check your connection configuration or VPN status."
    exit 1
fi
echo "✅ Snowflake connection successful"
echo ""

# Run database setup
echo "🗄️ Setting up database schema and initial data..."
if snow sql -f setup.sql --connection default; then
    echo "✅ Database setup completed successfully"
else
    echo "❌ Database setup failed"
    exit 1
fi
echo ""

# Deploy Streamlit app
echo "📱 Deploying Streamlit app..."
if snow streamlit deploy --connection default --replace; then
    echo "✅ Streamlit app deployed successfully"
else
    echo "❌ Streamlit deployment failed"
    exit 1
fi
echo ""

# Get app URL
echo "🌐 Retrieving app URL..."
APP_URL=$(snow streamlit get-url --connection default superhero_generator 2>/dev/null | grep -o 'https://[^[:space:]]*' || echo "")

echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Summary:"
echo "   • Database schema: ✅ Created"
echo "   • Initial data: ✅ Populated (6 superhero archetypes)"
echo "   • Streamlit app: ✅ Deployed"
echo "   • Analytics views: ✅ Ready"
echo ""
if [ -n "$APP_URL" ]; then
    echo "🔗 App URL: $APP_URL"
else
    echo "🔗 App URL: Check Snowflake console for app URL"
fi
echo ""
echo "🦸‍♂️ Your Snowflake World Tour superhero generator is ready!"
echo "💡 Admin dashboard password: snowflake2024" 