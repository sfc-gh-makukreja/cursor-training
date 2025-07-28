# 🦸‍♂️ Snowflake Superhero Generator

> **A complete Streamlit in Snowflake application built with Cursor AI for Snowflake World Tour booth activations**

## 🎯 For Snowflake Solution Engineers

This project demonstrates how to leverage **Cursor AI** to rapidly build compelling, production-ready demos for customer engagements. Learn AI-assisted development patterns that accelerate solution engineering workflows while showcasing advanced Snowflake capabilities.

## 🚀 Live Demo

**App URL**: [Snowflake Superhero Generator](https://app.snowflake.com/SFSEAPAC/makukreja_aws_us_west_2/#/streamlit-apps/CUBE_TESTING.PUBLIC.SUPERHERO_GENERATOR)

**Admin Dashboard**: Use password `snowflake2024` to access real-time analytics

## ✨ What This Demo Showcases

### 🎪 **Customer-Facing Features**
- **📷 Real Camera Input**: Native device camera capture with `st.camera_input()`
- **🤖 AI Image Analysis**: Uses Cortex `AI_CLASSIFY` to analyze professional style and personality
- **🧠 Personalized Generation**: `AI_COMPLETE` creates unique superhero identities 
- **📊 Real-Time Analytics**: Live visitor tracking and engagement metrics
- **🎨 Professional UI**: Accenture & Snowflake co-branded booth experience

### 🏗️ **Technical Architecture**
- **Streamlit in Snowflake (SiS)**: Native deployment with zero infrastructure
- **Cortex AISQL Functions**: `AI_CLASSIFY`, `AI_COMPLETE`, `AI_FILTER` integration
- **Secure File Processing**: Encrypted stages with automatic cleanup
- **Separation of Concerns**: Infrastructure (SQL) separated from application logic
- **Error Handling**: Robust fallback modes for reliable booth operation

## 🧠 Cursor AI Development Methodology

### **1. AI-Driven Requirements Gathering**
Started with natural language requirements and let Cursor AI help structure the technical approach:

```
User: "create a streamlit app for Snowflake World Tour booth that takes photos 
and generates superhero identities using AI"

Cursor AI: Generated comprehensive requirements.md with:
- Business objectives
- Technical architecture 
- Implementation roadmap
- Cost estimates
```

### **2. Iterative AI-Assisted Development**
Used Cursor AI's capabilities for rapid iteration:

- **Code Generation**: AI wrote initial Streamlit structure and Snowflake integration
- **Architecture Decisions**: AI suggested separation of concerns patterns
- **Error Resolution**: AI diagnosed and fixed deployment issues
- **Best Practices**: AI recommended modern Streamlit patterns and security measures

### **3. AI-Enhanced Documentation**
Generated comprehensive documentation including:
- **Cursor Rules**: Reusable patterns for future projects
- **Deployment Guides**: Step-by-step automation
- **Best Practices**: Captured in `.cursor/rules/` for team knowledge sharing

## 🛠️ Key Learning Outcomes for Solution Engineers

### **Prompt Engineering for Technical Projects**
Learn how to effectively communicate with AI for:
- Complex architecture decisions
- Multi-technology integration (Streamlit + Snowflake + Cortex)
- Production deployment requirements
- Error handling and edge cases

### **AI-Accelerated Demo Development**
- **Speed**: Built complete demo in hours, not days
- **Quality**: AI suggested enterprise-grade patterns and security
- **Maintenance**: Generated reusable components and documentation
- **Iteration**: Rapidly incorporated feedback and new requirements

### **Snowflake-Specific AI Assistance**
Cursor AI demonstrated deep knowledge of:
- Streamlit in Snowflake deployment patterns
- Cortex AISQL function integration
- Stage management and file processing
- Modern Snowflake CLI workflows

## 📁 Project Structure

```
├── streamlit_app.py          # Main application (camera input, AI analysis, UI)
├── setup.sql                 # Infrastructure layer (tables, stages, views)
├── deploy.sh                 # Automated deployment script
├── snowflake.yml            # Streamlit in Snowflake configuration
├── environment.yml          # Python dependencies (Snowflake channel only)
├── pages/
│   └── admin_dashboard.py   # Analytics dashboard for booth monitoring
├── .cursor/rules/           # Reusable AI development patterns
│   ├── streamlit-camera-input.mdc
│   ├── stage-separation-concerns.mdc
│   └── snowflake-ai-image-processing.mdc
└── DEPLOYMENT.md           # Comprehensive deployment guide
```

## 🚀 Quick Start for Solution Engineers

### **Prerequisites**
- Snowflake account with Cortex AI enabled
- Snowflake CLI installed and configured
- Cursor IDE with AI features enabled

### **1. Clone and Deploy**
```bash
git clone https://github.com/sfc-gh-makukreja/cursor-training.git
cd cursor-training
./deploy.sh  # Automated setup + deployment
```

### **2. Customize for Your Demo**
Use the established patterns to adapt for different use cases:
- Modify AI prompts in `streamlit_app.py`
- Update branding and styling 
- Add new Cortex AI functions
- Extend analytics dashboard

### **3. Learn from AI Development Process**
Study the git commit history to see:
- How requirements evolved through AI collaboration
- Problem-solving patterns with Cursor AI
- Architecture decisions and rationale
- Error resolution techniques

## 🎯 Use Cases for Solution Engineers

### **Customer Demos**
- **Retail**: Product recommendation engines
- **Healthcare**: Document AI for medical records
- **Finance**: Risk assessment with ML models
- **Manufacturing**: Predictive maintenance dashboards

### **Proof of Concepts**
- Rapid prototyping with Cortex AI functions
- Data pipeline visualization
- Real-time analytics dashboards
- Multi-modal AI applications

### **Internal Training**
- Hands-on Snowflake feature demonstrations
- AI/ML capability showcases
- Modern data app development patterns

## 🧰 Reusable Patterns (Cursor Rules)

This project generated three key **Cursor Rules** for future projects:

### 📷 **streamlit-camera-input.mdc**
- Camera integration best practices
- File upload alternatives
- PIL Image processing patterns
- Error handling for demos

### 🏗️ **stage-separation-concerns.mdc**
- Infrastructure vs application logic
- Stage management patterns
- Deployment architecture
- Security and cleanup practices

### 🤖 **snowflake-ai-image-processing.mdc**
- Cortex AISQL integration patterns
- AI_CLASSIFY implementation
- Fallback strategies
- Token usage optimization

## 📊 Technical Metrics

**Development Speed**: Complete demo built in ~4 hours with AI assistance
**Code Quality**: Enterprise-grade error handling and security patterns
**Maintainability**: Clear separation of concerns and documentation
**Scalability**: Designed for high-traffic booth environments

## 🎓 Learning Resources

### **Cursor AI Best Practices**
- Start with natural language requirements
- Iterate rapidly with AI feedback
- Use AI for architecture decisions
- Generate documentation alongside code

### **Snowflake Resources**
- [Streamlit in Snowflake Docs](https://docs.snowflake.com/en/developer-guide/streamlit)
- [Cortex AI Functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex)
- [Snowflake CLI Guide](https://docs.snowflake.com/en/developer-guide/snowflake-cli)

### **Demo Development Tips**
- Always include fallback modes for reliability
- Design for non-technical audiences
- Include real-time analytics for engagement
- Test thoroughly in target deployment environment

## 🤝 Contributing

Solution engineers are encouraged to:
- Adapt patterns for new use cases
- Contribute additional Cursor Rules
- Share AI prompt engineering techniques
- Extend the demo with new Snowflake features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using Cursor AI and Snowflake**

*Demonstrating the future of AI-assisted solution engineering* 