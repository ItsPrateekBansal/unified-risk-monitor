"""
Database models for Unified Risk Monitor
"""

from sqlalchemy import Column, String, Float, DateTime, Integer, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    address = Column(Text)
    date_of_birth = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Risk-related fields
    credit_score = Column(Float, default=0.0)
    aml_score = Column(Float, default=0.0)
    combined_risk_score = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    
    # OSINT enrichment data
    osint_signals = Column(JSON, default=list)
    last_osint_check = Column(DateTime)
    
    # Flags
    is_flagged = Column(Boolean, default=False)
    is_monitored = Column(Boolean, default=False)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    merchant = Column(String, nullable=False)
    category = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Risk indicators
    is_high_risk = Column(Boolean, default=False)
    risk_factors = Column(JSON, default=list)
    
    # AML-specific fields
    is_structured = Column(Boolean, default=False)
    is_offshore = Column(Boolean, default=False)
    is_cash_equivalent = Column(Boolean, default=False)

class RiskScore(Base):
    __tablename__ = "risk_scores"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=False, index=True)
    score_type = Column(String, nullable=False)  # CREDIT, AML, COMBINED
    score_value = Column(Float, nullable=False)
    confidence = Column(Float, default=0.0)
    factors = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Explanation fields
    explanation = Column(Text)
    recommended_actions = Column(JSON, default=list)

class OSINTSignal(Base):
    __tablename__ = "osint_signals"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=False, index=True)
    signal_type = Column(String, nullable=False)  # ADVERSE_MEDIA, DOMAIN_RISK, MERCHANT_RISK
    signal_value = Column(Float, nullable=False)
    signal_data = Column(JSON, default=dict)
    source = Column(String, nullable=False)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Risk assessment
    risk_impact = Column(String, default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    is_verified = Column(Boolean, default=False)

class RiskAlert(Base):
    __tablename__ = "risk_alerts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, nullable=False, index=True)
    alert_type = Column(String, nullable=False)  # CREDIT, AML, OSINT, COMBINED
    severity = Column(String, nullable=False)  # LOW, MEDIUM, HIGH, CRITICAL
    message = Column(Text, nullable=False)
    data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Alert management
    is_acknowledged = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    acknowledged_by = Column(String)
    resolved_at = Column(DateTime)
