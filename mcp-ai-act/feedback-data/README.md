# MCP AI Act Compliance - Feedback Data

This directory contains comprehensive feedback data collected by the MCP AI Act Compliance server to monitor performance, quality, and user interactions.

## 📁 Directory Structure

```
feedback-data/
├── README.md                    # This file - explains the feedback system
├── feedback_<session_id>.json   # Individual session feedback logs
└── feedback_summary.json        # Aggregated statistics and trends
```

## 🔍 What Data Is Collected

### Session-Level Data (`feedback_<session_id>.json`)

Each time you use the MCP server, a detailed feedback log is created with:

#### 📝 Input Data
- **System Description**: Your original input (e.g., "AI chatbot for customer service")
- **Input Length**: Character count of your input
- **Input Hash**: Unique identifier for your input
- **Input Type**: Type of input (text_description)

#### 📤 Output Data
- **User-Facing Output**: The complete response you received
- **Output Length**: Character count of the response
- **Output Type**: Type of output (text_summary)

#### 🎯 Analysis Results
- **Risk Level**: AI Act risk classification (prohibited, high_risk, limited_risk, minimal_risk)
- **Confidence Score**: How confident the analysis is (0-100%)
- **Applicable Articles**: Number of AI Act articles that apply
- **Requirements Count**: Number of compliance requirements identified
- **Recommendations Count**: Number of recommendations provided
- **Compliance Score**: Overall compliance score (0-1.0)

#### 🧠 Intelligent Resolution
- **Resolved Parameters**: Automatically determined parameters from your input
- **Confidence Score**: How confident the parameter resolution is
- **Resolution Method**: How parameters were determined

#### ⚡ Performance Metrics
- **Analysis Duration**: Time taken for analysis (milliseconds)
- **Data Loaded**: Count of articles, chapters, and compliance categories loaded

#### 🏆 Quality Indicators (7 Different Scores)
1. **Input Completeness**: How detailed your input was
2. **Analysis Confidence**: How confident the analysis is
3. **Result Completeness**: How complete the results are
4. **Risk Assessment Quality**: How accurate the risk assessment is
5. **Recommendation Quality**: How actionable the recommendations are
6. **Output Quality**: How well-structured the output is
7. **Input-Output Coherence**: How well the output addresses your input

#### 📊 Input-Output Analysis
- **Length Ratio**: How much the output expands on your input
- **Word Overlap**: How many words from your input appear in the output
- **Risk Level Appropriateness**: Whether the risk level makes sense for your input
- **Output Completeness**: Whether the output covers all necessary components
- **User Satisfaction Indicators**: Positive/negative/neutral sentiment analysis

#### 👤 User Context
- **Working Directory**: Where the MCP was used
- **MCP Version**: Version of the MCP server
- **Data Version**: Version of the AI Act data used

### Summary Data (`feedback_summary.json`)

Aggregated statistics including:
- **Total Analyses**: Number of analyses performed
- **Risk Level Distribution**: Breakdown by risk level
- **Average Confidence Scores**: Mean confidence across all analyses
- **Average Quality Scores**: Mean quality scores across all analyses
- **Tool Usage Patterns**: Which tools are used most
- **Last Updated**: Timestamp of last summary update

## 🎯 Quality Indicators Explained

### Input Completeness (0-1.0)
- **0.9-1.0**: Very detailed input with specific use case, data types, deployment context
- **0.7-0.8**: Good input with clear purpose and some technical details
- **0.5-0.6**: Basic input with general description
- **0.0-0.4**: Minimal input, very brief description

### Analysis Confidence (0-1.0)
- **0.9-1.0**: Very confident analysis with clear AI Act mapping
- **0.7-0.8**: Confident analysis with good parameter resolution
- **0.5-0.6**: Moderate confidence, some uncertainty
- **0.0-0.4**: Low confidence, significant uncertainty

### Output Quality (0-1.0)
- **0.9-1.0**: Well-structured output with clear sections, actionable recommendations
- **0.7-0.8**: Good structure with most key components
- **0.5-0.6**: Basic structure, some components missing
- **0.0-0.4**: Poor structure, many components missing

### Input-Output Coherence (0-1.0)
- **0.9-1.0**: Output perfectly addresses the input, high word overlap, appropriate risk level
- **0.7-0.8**: Good coherence, output relevant to input
- **0.5-0.6**: Moderate coherence, some relevance
- **0.0-0.4**: Poor coherence, output doesn't well address input

## 📈 User Satisfaction Indicators

The system tracks sentiment indicators in outputs:

### Positive Indicators (+1 each)
- ✅, success, completed, saved, ready, working, available

### Negative Indicators (-1 each)
- ❌, error, failed, unable, cannot, missing, invalid

### Neutral Indicators (0)
- 📁, 📋, 💡, 🎯, report, analysis, assessment

**Satisfaction Score** = (Positive - Negative) / (Positive + Negative + Neutral)

## 🔒 Privacy & Data Usage

### What's Collected
- Your system descriptions and the MCP's responses
- Performance metrics and quality assessments
- Usage patterns and tool preferences

### What's NOT Collected
- Personal information beyond your working directory
- Sensitive business data from your system descriptions
- Any data outside the MCP interaction

### Data Retention
- Feedback data is stored locally in your project directory
- No data is sent to external servers
- You can delete feedback data at any time

## 🛠️ How to Use This Data

### For Monitoring MCP Performance
1. Check `feedback_summary.json` for overall trends
2. Look at quality scores over time
3. Monitor confidence scores and risk level accuracy

### For Improving Your Inputs
1. Review inputs with low completeness scores
2. See which inputs result in higher confidence analyses
3. Learn from high-quality input patterns

### For Understanding Results
1. Check input-output coherence scores
2. Review user satisfaction indicators
3. Analyze which types of systems get better results

### For Troubleshooting
1. Look for sessions with low quality scores
2. Check for patterns in failed analyses
3. Review performance metrics for bottlenecks

## 📊 Example Feedback Log

```json
{
  "session_id": "20250929_135842_a1b2c3d4",
  "timestamp": "2025-09-29T13:58:42.663Z",
  "tool_name": "check_compliance",
  "input_data": {
    "system_description": "AI chatbot for customer service",
    "input_length": 35,
    "input_hash": "a1b2c3d4",
    "input_type": "text_description"
  },
  "output_data": {
    "user_facing_output": "🟡 **LIMITED RISK - Requires transparency obligations**...",
    "output_length": 487,
    "output_type": "text_summary"
  },
  "analysis_result": {
    "risk_level": "limited_risk",
    "confidence_score": 0.7,
    "applicable_articles_count": 2,
    "requirements_count": 3,
    "recommendations_count": 4,
    "compliance_score": 0.8
  },
  "quality_indicators": {
    "input_completeness": 0.6,
    "analysis_confidence": 0.7,
    "result_completeness": 0.9,
    "risk_assessment_quality": 0.8,
    "recommendation_quality": 0.7,
    "output_quality": 0.8,
    "input_output_coherence": 0.9,
    "overall_quality_score": 0.8
  }
}
```

## 🚀 Benefits

This feedback system helps you:
- **Monitor MCP Performance**: Track how well the system is working
- **Improve Input Quality**: Learn what makes for better analyses
- **Understand Results**: See how outputs relate to inputs
- **Track Trends**: Monitor quality and performance over time
- **Troubleshoot Issues**: Identify patterns in problems
- **Optimize Usage**: Understand which tools work best for your needs

## 📞 Support

If you have questions about the feedback system or want to understand specific metrics, the feedback data provides comprehensive insights into every interaction with the MCP AI Act Compliance server.

---
*Generated by MCP AI Act Compliance Server v1.0.0*
