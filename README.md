# Unified Credit + AML Risk Monitor with OSINT Enrichment

A TigerData-powered, agentic risk monitoring system that unifies credit risk and anti-money laundering (AML) detection, enriched with external OSINT signals, and explained transparently by AI agents.

## 🎯 Problem Statement

Financial institutions struggle with two critical gaps:
1. **Credit Risk** systems are mostly numeric scores → opaque, not real-time
2. **AML** systems generate massive false positives → compliance fatigue

Both run in silos, leaving blind spots, poor explainability, and missed risks.

## 💡 Solution

A real-time monitoring platform that unifies Credit + AML risk:
- Built on TigerData for time-series transactions + vector search patterns
- Enriched by OSINT layer (Bright Data/public web sources)
- Powered by MCP agents for data processing, explainability, and actions
- Dashboard shows top risky customers with transparent explanations

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │    │   FastAPI       │    │   TigerData     │
│   Dashboard     │◄──►│   Backend       │◄──►│   Hypertables   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   MCP Agents    │
                       │   - Data        │
                       │   - Explain     │
                       │   - Action      │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OSINT Layer   │
                       │   - Bright Data │
                       │   - Web Sources │
                       └─────────────────┘
```

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Clone and start the application
git clone <your-repo-url>
cd unified-risk-monitor
./start.sh
```

### Option 2: Manual Setup

1. **Backend Setup:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   REACT_APP_API_URL=http://localhost:8000 npm start
   ```

3. **Test the Application:**
   ```bash
   python3 demo.py
   ```

### Access Points
- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, TigerData
- **Frontend:** React, TypeScript, Tailwind CSS, Recharts
- **Agents:** MCP (Model Context Protocol)
- **OSINT:** Bright Data API, Web Scraping
- **Database:** TigerData Hypertables

## 📊 Key Features

### 🎯 Core Functionality
- **Unified Risk Scoring:** Combines credit and AML risk in a single workflow
- **Real-time Monitoring:** Live transaction processing and risk updates
- **OSINT Enrichment:** External intelligence from Bright Data and web sources
- **AI Agent Explainability:** Human-readable explanations of risk decisions
- **Interactive Dashboard:** Modern React UI with risk visualization

### 🤖 MCP Agents
- **Data Agent:** Retrieves and aggregates risk data
- **Explainability Agent:** Provides transparent risk explanations
- **Action Agent:** Recommends next steps based on risk assessment

### 📈 Risk Assessment
- **Credit Risk:** Payment history, utilization, account age analysis
- **AML Risk:** Structuring patterns, high-risk merchants, offshore activity
- **OSINT Signals:** Adverse media, sanctions lists, PEP status, domain risk
- **Combined Scoring:** Weighted integration of all risk factors

### 🎨 Dashboard Features
- Risk distribution charts and metrics
- Top risky customers table with detailed views
- Real-time OSINT signal monitoring
- Customer risk explanations and recommended actions
- Responsive design with modern UI components

## 🏆 Hackathon Innovation

### 🎯 Novel Approach
This project addresses a critical gap in financial risk management by:
1. **Unifying Credit + AML Risk:** First system to combine both risk types in a single workflow
2. **OSINT Integration:** Leverages external intelligence sources rarely used in traditional risk systems
3. **AI Agent Explainability:** Transparent, human-readable explanations of risk decisions
4. **MCP Agent Architecture:** Composable, extensible agent system for risk management

### 🚀 Technical Innovation
- **Real-time Risk Scoring:** SQL-based rules with vector search capabilities
- **Multi-source OSINT:** Bright Data API + web scraping for comprehensive intelligence
- **Agent Orchestration:** Multiple MCP agents working together seamlessly
- **Modern UI/UX:** React dashboard with real-time updates and interactive visualizations

### 💡 Business Impact
- **Reduced False Positives:** Better AML detection with OSINT context
- **Improved Compliance:** Transparent, auditable risk decisions
- **Operational Efficiency:** Unified workflow instead of siloed systems
- **Scalable Architecture:** Agent-based system grows with business needs

## 🔧 Development

This project uses a modular architecture with clear separation of concerns:
- `backend/` - FastAPI server with risk scoring and MCP agents
- `frontend/` - React dashboard for risk monitoring
- `agents/` - MCP server implementation
- `data/` - Synthetic data generation and migration scripts
- `osint/` - External data enrichment layer

## 🎮 Demo Instructions

1. **Start the application:** `./start.sh`
2. **View the dashboard:** http://localhost:3000
3. **Explore risky customers:** Click "View Details" on any customer
4. **Test the API:** Run `python3 demo.py`
5. **Check API docs:** http://localhost:8000/docs

## 🔮 Future Enhancements

- **TigerData Integration:** Full hypertable implementation for time-series data
- **Machine Learning:** Advanced ML models for risk prediction
- **Real-time Alerts:** WebSocket-based live risk notifications
- **Mobile App:** React Native mobile dashboard
- **Advanced OSINT:** Integration with more intelligence sources
