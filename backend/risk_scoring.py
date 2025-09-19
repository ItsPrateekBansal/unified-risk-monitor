"""
Risk Scoring Engine for Credit and AML Risk Assessment
"""

from sqlalchemy.orm import Session
from models import Customer, Transaction, RiskScore
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
import math

logger = logging.getLogger(__name__)

class RiskScoringEngine:
    """
    Unified risk scoring engine that calculates both credit and AML risk scores
    """
    
    def __init__(self):
        self.credit_weights = {
            "payment_history": 0.35,
            "credit_utilization": 0.30,
            "account_age": 0.15,
            "transaction_frequency": 0.10,
            "amount_consistency": 0.10
        }
        
        self.aml_weights = {
            "structuring_patterns": 0.25,
            "high_risk_merchants": 0.20,
            "offshore_transactions": 0.20,
            "cash_equivalents": 0.15,
            "amount_frequency": 0.10,
            "time_patterns": 0.10
        }
    
    async def calculate_risk_scores(self, customer_id: str, db: Session = None):
        """
        Calculate and update risk scores for a customer
        """
        try:
            # Get customer and recent transactions
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            if not customer:
                logger.error(f"Customer {customer_id} not found")
                return
            
            # Get transactions from last 90 days
            cutoff_date = datetime.utcnow() - timedelta(days=90)
            transactions = db.query(Transaction).filter(
                Transaction.customer_id == customer_id,
                Transaction.timestamp >= cutoff_date
            ).all()
            
            # Calculate credit risk score
            credit_score = await self._calculate_credit_risk(customer, transactions)
            
            # Calculate AML risk score
            aml_score = await self._calculate_aml_risk(customer, transactions)
            
            # Calculate combined risk score
            combined_score = self._calculate_combined_risk(credit_score, aml_score)
            
            # Update customer record
            customer.credit_score = credit_score["score"]
            customer.aml_score = aml_score["score"]
            customer.combined_risk_score = combined_score["score"]
            customer.risk_level = self._determine_risk_level(combined_score["score"])
            customer.updated_at = datetime.utcnow()
            
            # Store detailed risk scores
            await self._store_risk_scores(customer_id, credit_score, aml_score, combined_score, db)
            
            logger.info(f"Updated risk scores for customer {customer_id}: Credit={credit_score['score']:.3f}, AML={aml_score['score']:.3f}, Combined={combined_score['score']:.3f}")
            
        except Exception as e:
            logger.error(f"Error calculating risk scores for customer {customer_id}: {e}")
            raise
    
    async def _calculate_credit_risk(self, customer: Customer, transactions: List[Transaction]) -> Dict[str, Any]:
        """
        Calculate credit risk score based on payment patterns and utilization
        """
        factors = {}
        
        # Payment history (simulated - in real system would come from credit bureau)
        factors["payment_history"] = 0.2  # Good payment history
        
        # Credit utilization (simulated)
        total_amount = sum(t.amount for t in transactions)
        avg_monthly_amount = total_amount / 3  # 3 months of data
        credit_limit = 10000  # Simulated credit limit
        utilization = min(avg_monthly_amount / credit_limit, 1.0)
        factors["credit_utilization"] = utilization
        
        # Account age (simulated)
        account_age_days = (datetime.utcnow() - customer.created_at).days
        factors["account_age"] = max(0, 1 - (account_age_days / 365))  # Newer accounts are riskier
        
        # Transaction frequency
        transaction_count = len(transactions)
        factors["transaction_frequency"] = min(transaction_count / 30, 1.0)  # Normalize to daily average
        
        # Amount consistency
        if len(transactions) > 1:
            amounts = [t.amount for t in transactions]
            mean_amount = sum(amounts) / len(amounts)
            variance = sum((x - mean_amount) ** 2 for x in amounts) / len(amounts)
            std_dev = math.sqrt(variance)
            cv = std_dev / mean_amount if mean_amount > 0 else 1
            factors["amount_consistency"] = min(cv, 1.0)  # Higher variance = higher risk
        else:
            factors["amount_consistency"] = 0.5
        
        # Calculate weighted score
        score = sum(factors[factor] * self.credit_weights[factor] for factor in factors)
        
        return {
            "score": min(score, 1.0),
            "factors": factors,
            "confidence": 0.85,
            "explanation": f"Credit risk based on utilization ({utilization:.1%}), account age ({account_age_days} days), and transaction patterns"
        }
    
    async def _calculate_aml_risk(self, customer: Customer, transactions: List[Transaction]) -> Dict[str, Any]:
        """
        Calculate AML risk score based on transaction patterns and red flags
        """
        factors = {}
        
        # Structuring patterns (transactions just under reporting thresholds)
        structuring_count = sum(1 for t in transactions if 900 <= t.amount <= 999)
        factors["structuring_patterns"] = min(structuring_count / 10, 1.0)
        
        # High-risk merchants
        high_risk_merchants = ["Offshore Trading Co", "Crypto Exchange", "Casino Royale"]
        high_risk_count = sum(1 for t in transactions if t.merchant in high_risk_merchants)
        factors["high_risk_merchants"] = min(high_risk_count / 5, 1.0)
        
        # Offshore transactions
        offshore_count = sum(1 for t in transactions if t.is_offshore)
        factors["offshore_transactions"] = min(offshore_count / 3, 1.0)
        
        # Cash equivalents
        cash_equiv_count = sum(1 for t in transactions if t.is_cash_equivalent)
        factors["cash_equivalents"] = min(cash_equiv_count / 5, 1.0)
        
        # Amount frequency (unusual amounts)
        unusual_amounts = sum(1 for t in transactions if t.amount % 1000 == 0 and t.amount > 1000)
        factors["amount_frequency"] = min(unusual_amounts / 5, 1.0)
        
        # Time patterns (transactions at unusual hours)
        night_transactions = sum(1 for t in transactions if t.timestamp.hour < 6 or t.timestamp.hour > 22)
        factors["time_patterns"] = min(night_transactions / 10, 1.0)
        
        # Calculate weighted score
        score = sum(factors[factor] * self.aml_weights[factor] for factor in factors)
        
        return {
            "score": min(score, 1.0),
            "factors": factors,
            "confidence": 0.90,
            "explanation": f"AML risk based on structuring patterns ({structuring_count} transactions), high-risk merchants ({high_risk_count}), and offshore activity ({offshore_count})"
        }
    
    def _calculate_combined_risk(self, credit_risk: Dict, aml_risk: Dict) -> Dict[str, Any]:
        """
        Calculate combined risk score with weighted average
        """
        # Weight credit and AML equally, but can be adjusted
        credit_weight = 0.4
        aml_weight = 0.6  # AML typically weighted higher in financial institutions
        
        combined_score = (credit_risk["score"] * credit_weight + aml_risk["score"] * aml_weight)
        
        return {
            "score": min(combined_score, 1.0),
            "credit_contribution": credit_risk["score"] * credit_weight,
            "aml_contribution": aml_risk["score"] * aml_weight,
            "confidence": (credit_risk["confidence"] + aml_risk["confidence"]) / 2,
            "explanation": f"Combined risk score integrating credit risk ({credit_risk['score']:.3f}) and AML risk ({aml_risk['score']:.3f})"
        }
    
    def _determine_risk_level(self, score: float) -> str:
        """
        Determine risk level based on score
        """
        if score >= 0.8:
            return "CRITICAL"
        elif score >= 0.6:
            return "HIGH"
        elif score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    async def _store_risk_scores(self, customer_id: str, credit_risk: Dict, aml_risk: Dict, combined_risk: Dict, db: Session):
        """
        Store detailed risk scores in database
        """
        try:
            # Store credit risk score
            credit_score_record = RiskScore(
                customer_id=customer_id,
                score_type="CREDIT",
                score_value=credit_risk["score"],
                confidence=credit_risk["confidence"],
                factors=credit_risk["factors"],
                explanation=credit_risk["explanation"]
            )
            db.add(credit_score_record)
            
            # Store AML risk score
            aml_score_record = RiskScore(
                customer_id=customer_id,
                score_type="AML",
                score_value=aml_risk["score"],
                confidence=aml_risk["confidence"],
                factors=aml_risk["factors"],
                explanation=aml_risk["explanation"]
            )
            db.add(aml_score_record)
            
            # Store combined risk score
            combined_score_record = RiskScore(
                customer_id=customer_id,
                score_type="COMBINED",
                score_value=combined_risk["score"],
                confidence=combined_risk["confidence"],
                factors={
                    "credit_contribution": combined_risk["credit_contribution"],
                    "aml_contribution": combined_risk["aml_contribution"]
                },
                explanation=combined_risk["explanation"]
            )
            db.add(combined_score_record)
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Error storing risk scores: {e}")
            db.rollback()
            raise
