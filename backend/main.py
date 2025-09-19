"""
Unified Credit + AML Risk Monitor
FastAPI backend with MCP agent integration
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
from datetime import datetime, timedelta
import logging

from models import Customer, Transaction, RiskScore
from database import get_db, init_db
from risk_scoring import RiskScoringEngine
from osint_enrichment import OSINTEnrichmentService
from mcp_agents import MCPAgentOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Unified Risk Monitor API",
    description="Credit + AML Risk Monitoring with OSINT Enrichment",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
risk_engine = RiskScoringEngine()
osint_service = OSINTEnrichmentService()
mcp_orchestrator = MCPAgentOrchestrator()

# Pydantic models for API
class CustomerRiskResponse(BaseModel):
    customer_id: str
    name: str
    credit_score: float
    aml_score: float
    combined_risk_score: float
    risk_level: str
    last_updated: datetime
    osint_signals: List[Dict[str, Any]]
    explanation: str

class RiskExplanationResponse(BaseModel):
    customer_id: str
    credit_explanation: str
    aml_explanation: str
    osint_explanation: str
    recommended_actions: List[str]
    confidence_score: float

class TransactionRequest(BaseModel):
    customer_id: str
    amount: float
    merchant: str
    category: str
    timestamp: datetime

@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    await init_db()
    logger.info("Unified Risk Monitor API started")

@app.get("/")
async def root():
    return {"message": "Unified Credit + AML Risk Monitor API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/customers", response_model=List[CustomerRiskResponse])
async def get_all_customers(
    limit: int = 100,
    offset: int = 0,
    search: Optional[str] = None,
    risk_level: Optional[str] = None,
    db=Depends(get_db)
):
    """
    Get all customers with optional filtering
    """
    try:
        # Use MCP Data Agent to fetch all customers
        customers = await mcp_orchestrator.get_all_customers(
            limit=limit,
            offset=offset,
            search=search,
            risk_level=risk_level
        )
        
        return customers
    except Exception as e:
        logger.error(f"Error fetching customers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers/risky", response_model=List[CustomerRiskResponse])
async def get_risky_customers(
    limit: int = 50,
    min_risk_score: float = 0.7,
    db=Depends(get_db)
):
    """
    Get top risky customers with combined credit + AML scores
    """
    try:
        # Use MCP Data Agent to fetch risky customers
        risky_customers = await mcp_orchestrator.get_risky_customers(
            limit=limit, 
            min_risk_score=min_risk_score
        )
        
        return risky_customers
    except Exception as e:
        logger.error(f"Error fetching risky customers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers/{customer_id}/explain", response_model=RiskExplanationResponse)
async def explain_customer_risk(customer_id: str, db=Depends(get_db)):
    """
    Get detailed explanation of customer risk using MCP Explainability Agent
    """
    try:
        explanation = await mcp_orchestrator.explain_customer_risk(customer_id)
        return explanation
    except Exception as e:
        logger.error(f"Error explaining customer risk: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transactions")
async def create_transaction(transaction: TransactionRequest, db=Depends(get_db)):
    """
    Process new transaction and update risk scores
    """
    try:
        # Store transaction
        db_transaction = Transaction(
            customer_id=transaction.customer_id,
            amount=transaction.amount,
            merchant=transaction.merchant,
            category=transaction.category,
            timestamp=transaction.timestamp
        )
        db.add(db_transaction)
        db.commit()
        
        # Trigger risk recalculation
        await risk_engine.calculate_risk_scores(transaction.customer_id)
        
        # Enrich with OSINT data
        await osint_service.enrich_customer(transaction.customer_id)
        
        return {"message": "Transaction processed", "transaction_id": db_transaction.id}
    except Exception as e:
        logger.error(f"Error processing transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers/{customer_id}/actions")
async def get_recommended_actions(customer_id: str, db=Depends(get_db)):
    """
    Get recommended actions for a customer using MCP Action Agent
    """
    try:
        actions = await mcp_orchestrator.get_recommended_actions(customer_id)
        return {"customer_id": customer_id, "recommended_actions": actions}
    except Exception as e:
        logger.error(f"Error getting recommended actions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard/stats")
async def get_dashboard_stats(db=Depends(get_db)):
    """
    Get dashboard statistics and metrics
    """
    try:
        stats = await mcp_orchestrator.get_dashboard_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting dashboard stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/osint/enrich/{customer_id}")
async def trigger_osint_enrichment(customer_id: str, db=Depends(get_db)):
    """
    Manually trigger OSINT enrichment for a customer
    """
    try:
        result = await osint_service.enrich_customer(customer_id)
        return {"message": "OSINT enrichment completed", "signals": result}
    except Exception as e:
        logger.error(f"Error enriching customer with OSINT: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class DataGenerationRequest(BaseModel):
    num_customers: int = 100
    include_risky: bool = True
    risk_distribution: Optional[Dict[str, int]] = None

@app.post("/data/generate")
async def generate_ai_data(request: DataGenerationRequest, db=Depends(get_db)):
    """
    Generate AI-powered synthetic customer data
    """
    try:
        result = await mcp_orchestrator.generate_customer_data(
            num_customers=request.num_customers,
            include_risky=request.include_risky,
            risk_distribution=request.risk_distribution
        )
        return {"message": f"Generated {request.num_customers} customers", "data": result}
    except Exception as e:
        logger.error(f"Error generating data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/data/clear")
async def clear_all_data(db=Depends(get_db)):
    """
    Clear all customer data
    """
    try:
        result = await mcp_orchestrator.clear_all_data()
        return {"message": "All data cleared successfully", "result": result}
    except Exception as e:
        logger.error(f"Error clearing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
