"""
Database configuration and connection management
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from typing import Generator
import logging

logger = logging.getLogger(__name__)

# Database configuration - Use SQLite for demo
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./risk_monitor.db"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool if "sqlite" in DATABASE_URL else None,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """
    Initialize database tables
    """
    try:
        # Import all models to ensure they're registered
        from models import Customer, Transaction, RiskScore, OSINTSignal, RiskAlert
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # Initialize with sample data if empty
        try:
            await seed_sample_data()
        except Exception as e:
            logger.warning(f"Could not seed sample data: {e}")
            # Continue without sample data
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

async def seed_sample_data():
    """
    Seed database with sample data for demo purposes
    """
    from models import Customer, Transaction, RiskScore
    from datetime import datetime, timedelta
    import random
    
    db = SessionLocal()
    try:
        # Check if we already have data
        if db.query(Customer).count() > 0:
            return
        
        logger.info("Seeding database with sample data...")
        
        # Create sample customers
        customers = [
            Customer(
                id="cust_001",
                name="John Smith",
                email="john.smith@email.com",
                phone="+1-555-0101",
                address="123 Main St, New York, NY",
                credit_score=0.3,
                aml_score=0.2,
                combined_risk_score=0.25,
                risk_level="LOW"
            ),
            Customer(
                id="cust_002", 
                name="Maria Garcia",
                email="maria.garcia@email.com",
                phone="+1-555-0102",
                address="456 Oak Ave, Los Angeles, CA",
                credit_score=0.7,
                aml_score=0.8,
                combined_risk_score=0.75,
                risk_level="HIGH"
            ),
            Customer(
                id="cust_003",
                name="Robert Johnson",
                email="robert.johnson@email.com", 
                phone="+1-555-0103",
                address="789 Pine St, Miami, FL",
                credit_score=0.9,
                aml_score=0.6,
                combined_risk_score=0.75,
                risk_level="HIGH"
            ),
            Customer(
                id="cust_004",
                name="Sarah Wilson",
                email="sarah.wilson@email.com",
                phone="+1-555-0104", 
                address="321 Elm St, Chicago, IL",
                credit_score=0.4,
                aml_score=0.3,
                combined_risk_score=0.35,
                risk_level="LOW"
            ),
            Customer(
                id="cust_005",
                name="Ahmed Hassan",
                email="ahmed.hassan@email.com",
                phone="+1-555-0105",
                address="654 Maple Dr, Houston, TX", 
                credit_score=0.8,
                aml_score=0.9,
                combined_risk_score=0.85,
                risk_level="CRITICAL"
            )
        ]
        
        for customer in customers:
            db.add(customer)
        
        # Create sample transactions
        merchants = [
            "Amazon", "Walmart", "Target", "Best Buy", "Home Depot",
            "Starbucks", "McDonald's", "Shell", "Exxon", "BP",
            "Offshore Trading Co", "Crypto Exchange", "Casino Royale"
        ]
        
        categories = [
            "Retail", "Groceries", "Gas", "Restaurants", "Entertainment",
            "Electronics", "Home Improvement", "Financial Services"
        ]
        
        for i in range(100):
            customer_id = random.choice([c.id for c in customers])
            amount = round(random.uniform(10, 5000), 2)
            merchant = random.choice(merchants)
            category = random.choice(categories)
            timestamp = datetime.utcnow() - timedelta(days=random.randint(0, 30))
            
            # Mark suspicious transactions
            is_high_risk = (
                merchant in ["Offshore Trading Co", "Crypto Exchange", "Casino Royale"] or
                amount > 3000 or
                (amount > 1000 and category == "Financial Services")
            )
            
            transaction = Transaction(
                customer_id=customer_id,
                amount=amount,
                merchant=merchant,
                category=category,
                timestamp=timestamp,
                is_high_risk=is_high_risk,
                is_structured=amount > 2000 and amount % 1000 == 0,
                is_offshore=merchant == "Offshore Trading Co",
                is_cash_equivalent=merchant in ["Crypto Exchange", "Casino Royale"]
            )
            db.add(transaction)
        
        # Create sample risk scores
        for customer in customers:
            credit_score = RiskScore(
                customer_id=customer.id,
                score_type="CREDIT",
                score_value=customer.credit_score,
                confidence=0.85,
                factors=["payment_history", "credit_utilization", "account_age"],
                explanation=f"Credit risk based on payment history and utilization for {customer.name}"
            )
            
            aml_score = RiskScore(
                customer_id=customer.id,
                score_type="AML", 
                score_value=customer.aml_score,
                confidence=0.90,
                factors=["transaction_patterns", "merchant_risk", "amount_frequency"],
                explanation=f"AML risk based on transaction patterns and merchant analysis for {customer.name}"
            )
            
            combined_score = RiskScore(
                customer_id=customer.id,
                score_type="COMBINED",
                score_value=customer.combined_risk_score,
                confidence=0.88,
                factors=["credit_risk", "aml_risk", "osint_signals"],
                explanation=f"Combined risk assessment integrating credit, AML, and external intelligence for {customer.name}"
            )
            
            db.add(credit_score)
            db.add(aml_score) 
            db.add(combined_score)
        
        db.commit()
        logger.info("Sample data seeded successfully")
        
    except Exception as e:
        logger.error(f"Error seeding sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()
