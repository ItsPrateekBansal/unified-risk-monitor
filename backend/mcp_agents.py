"""
MCP (Model Context Protocol) Agents for Risk Monitoring
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import asyncio

from models import Customer, Transaction, RiskScore, OSINTSignal
from risk_scoring import RiskScoringEngine
from osint_enrichment import OSINTEnrichmentService

logger = logging.getLogger(__name__)

class MCPAgentOrchestrator:
    """
    Orchestrates multiple MCP agents for risk monitoring
    """
    
    def __init__(self):
        self.risk_engine = RiskScoringEngine()
        self.osint_service = OSINTEnrichmentService()
        self.data_agent = DataAgent()
        self.explainability_agent = ExplainabilityAgent()
        self.action_agent = ActionAgent()
    
    async def get_all_customers(self, limit: int = 100, offset: int = 0, search: Optional[str] = None, risk_level: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all customers using Data Agent
        """
        try:
            return await self.data_agent.get_all_customers(limit, offset, search, risk_level)
        except Exception as e:
            logger.error(f"Error getting all customers: {e}")
            return []

    async def get_risky_customers(self, limit: int = 50, min_risk_score: float = 0.7) -> List[Dict[str, Any]]:
        """
        Get top risky customers using Data Agent
        """
        try:
            return await self.data_agent.get_risky_customers(limit, min_risk_score)
        except Exception as e:
            logger.error(f"Error getting risky customers: {e}")
            return []
    
    async def explain_customer_risk(self, customer_id: str) -> Dict[str, Any]:
        """
        Get detailed explanation of customer risk using Explainability Agent
        """
        try:
            return await self.explainability_agent.explain_customer_risk(customer_id)
        except Exception as e:
            logger.error(f"Error explaining customer risk: {e}")
            return {"error": str(e)}
    
    async def get_recommended_actions(self, customer_id: str) -> List[str]:
        """
        Get recommended actions using Action Agent
        """
        try:
            return await self.action_agent.get_recommended_actions(customer_id)
        except Exception as e:
            logger.error(f"Error getting recommended actions: {e}")
            return []
    
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get dashboard statistics using Data Agent
        """
        try:
            return await self.data_agent.get_dashboard_stats()
        except Exception as e:
            logger.error(f"Error getting dashboard stats: {e}")
            return {}

    async def generate_customer_data(self, num_customers: int = 100, include_risky: bool = True, risk_distribution: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        Generate AI-powered synthetic customer data
        """
        try:
            return await self.data_agent.generate_customer_data(num_customers, include_risky, risk_distribution)
        except Exception as e:
            logger.error(f"Error generating customer data: {e}")
            return {"error": str(e)}

    async def clear_all_data(self) -> Dict[str, Any]:
        """
        Clear all customer data
        """
        try:
            return await self.data_agent.clear_all_data()
        except Exception as e:
            logger.error(f"Error clearing data: {e}")
            return {"error": str(e)}

class DataAgent:
    """
    MCP Data Agent - Handles data retrieval and aggregation
    """
    
    def __init__(self):
        self.generated_customers = []
    
    async def get_all_customers(self, limit: int = 100, offset: int = 0, search: Optional[str] = None, risk_level: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all customers with optional filtering
        """
        try:
            # Use generated customers if available, otherwise fall back to mock data
            if self.generated_customers:
                all_customers = self.generated_customers
            else:
                # Fallback mock data
                all_customers = [
                    {
                        "customer_id": "cust_001",
                        "name": "John Smith",
                        "credit_score": 0.3,
                        "aml_score": 0.2,
                        "combined_risk_score": 0.25,
                        "risk_level": "LOW",
                        "last_updated": datetime.utcnow().isoformat(),
                        "osint_signals": [],
                        "explanation": "Low risk customer with good credit history"
                    },
                    {
                        "customer_id": "cust_002",
                        "name": "Maria Garcia",
                        "credit_score": 0.7,
                        "aml_score": 0.8,
                        "combined_risk_score": 0.75,
                        "risk_level": "HIGH",
                        "last_updated": datetime.utcnow().isoformat(),
                        "osint_signals": [
                            {"type": "PEP_STATUS", "value": 0.6, "impact": "MEDIUM"},
                            {"type": "MERCHANT_RISK", "value": 0.6, "impact": "HIGH"}
                        ],
                        "explanation": "High risk due to PEP status and high-risk merchant transactions"
                    },
                    {
                        "customer_id": "cust_003",
                        "name": "Robert Johnson",
                        "credit_score": 0.9,
                        "aml_score": 0.6,
                        "combined_risk_score": 0.75,
                        "risk_level": "HIGH",
                        "last_updated": datetime.utcnow().isoformat(),
                        "osint_signals": [
                            {"type": "DOMAIN_RISK", "value": 0.7, "impact": "HIGH"}
                        ],
                        "explanation": "High risk due to suspicious domain activity"
                    },
                    {
                        "customer_id": "cust_004",
                        "name": "Sarah Wilson",
                        "credit_score": 0.4,
                        "aml_score": 0.3,
                        "combined_risk_score": 0.35,
                        "risk_level": "LOW",
                        "last_updated": datetime.utcnow().isoformat(),
                        "osint_signals": [],
                        "explanation": "Low risk customer with stable financial profile"
                    },
                    {
                        "customer_id": "cust_005",
                        "name": "Ahmed Hassan",
                        "credit_score": 0.8,
                        "aml_score": 0.9,
                        "combined_risk_score": 0.85,
                        "risk_level": "CRITICAL",
                        "last_updated": datetime.utcnow().isoformat(),
                        "osint_signals": [
                            {"type": "SANCTIONS_CHECK", "value": 0.9, "impact": "CRITICAL"},
                            {"type": "ADVERSE_MEDIA", "value": 0.7, "impact": "HIGH"}
                        ],
                        "explanation": "High risk due to sanctions list match and adverse media coverage"
                    }
                ]
            
            # Apply filtering
            filtered_customers = all_customers
            
            if search:
                filtered_customers = [c for c in filtered_customers if search.lower() in c["name"].lower()]
            
            if risk_level:
                filtered_customers = [c for c in filtered_customers if c["risk_level"] == risk_level]
            
            # Apply pagination
            start_idx = offset
            end_idx = offset + limit
            paginated_customers = filtered_customers[start_idx:end_idx]
            
            return paginated_customers
            
        except Exception as e:
            logger.error(f"Error getting all customers: {e}")
            return []
    
    async def get_risky_customers(self, limit: int = 50, min_risk_score: float = 0.7) -> List[Dict[str, Any]]:
        """
        Retrieve top risky customers with enriched data
        """
        try:
            # Use generated customers if available, otherwise fall back to mock data
            if self.generated_customers:
                # Filter generated customers by risk score
                risky_customers = [
                    c for c in self.generated_customers 
                    if c["combined_risk_score"] >= min_risk_score
                ]
                # Sort by risk score descending and limit
                risky_customers = sorted(risky_customers, key=lambda x: x["combined_risk_score"], reverse=True)[:limit]
                return risky_customers
            
            # Fallback mock data
            risky_customers = [
                {
                    "customer_id": "cust_005",
                    "name": "Ahmed Hassan",
                    "credit_score": 0.8,
                    "aml_score": 0.9,
                    "combined_risk_score": 0.85,
                    "risk_level": "CRITICAL",
                    "last_updated": datetime.utcnow().isoformat(),
                    "osint_signals": [
                        {"type": "SANCTIONS_CHECK", "value": 0.9, "impact": "CRITICAL"},
                        {"type": "ADVERSE_MEDIA", "value": 0.7, "impact": "HIGH"}
                    ],
                    "explanation": "High risk due to sanctions list match and adverse media coverage"
                },
                {
                    "customer_id": "cust_002",
                    "name": "Maria Garcia",
                    "credit_score": 0.7,
                    "aml_score": 0.8,
                    "combined_risk_score": 0.75,
                    "risk_level": "HIGH",
                    "last_updated": datetime.utcnow().isoformat(),
                    "osint_signals": [
                        {"type": "PEP_STATUS", "value": 0.6, "impact": "MEDIUM"},
                        {"type": "MERCHANT_RISK", "value": 0.6, "impact": "HIGH"}
                    ],
                    "explanation": "High risk due to PEP status and high-risk merchant transactions"
                },
                {
                    "customer_id": "cust_003",
                    "name": "Robert Johnson",
                    "credit_score": 0.9,
                    "aml_score": 0.6,
                    "combined_risk_score": 0.75,
                    "risk_level": "HIGH",
                    "last_updated": datetime.utcnow().isoformat(),
                    "osint_signals": [
                        {"type": "DOMAIN_RISK", "value": 0.3, "impact": "LOW"},
                        {"type": "MERCHANT_RISK", "value": 0.4, "impact": "MEDIUM"}
                    ],
                    "explanation": "High risk due to poor credit score and moderate AML indicators"
                }
            ]
            
            # Filter by minimum risk score
            filtered_customers = [c for c in risky_customers if c["combined_risk_score"] >= min_risk_score]
            
            # Sort by combined risk score (descending)
            filtered_customers.sort(key=lambda x: x["combined_risk_score"], reverse=True)
            
            return filtered_customers[:limit]
            
        except Exception as e:
            logger.error(f"Error in DataAgent.get_risky_customers: {e}")
            return []
    
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get dashboard statistics and metrics
        """
        try:
            # Use generated customers if available, otherwise fall back to mock data
            if self.generated_customers:
                total_customers = len(self.generated_customers)
                high_risk_customers = len([c for c in self.generated_customers if c["risk_level"] == "HIGH"])
                critical_risk_customers = len([c for c in self.generated_customers if c["risk_level"] == "CRITICAL"])
                
                # Calculate risk distribution
                risk_distribution = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
                for customer in self.generated_customers:
                    risk_level = customer["risk_level"]
                    if risk_level in risk_distribution:
                        risk_distribution[risk_level] += 1
                
                # Count OSINT signals
                osint_signals_today = sum(len(customer.get("osint_signals", [])) for customer in self.generated_customers)
                
                return {
                    "total_customers": total_customers,
                    "high_risk_customers": high_risk_customers,
                    "critical_risk_customers": critical_risk_customers,
                    "total_transactions_today": 1250,
                    "flagged_transactions_today": 23,
                    "osint_signals_today": osint_signals_today,
                    "risk_score_distribution": risk_distribution,
                    "top_risk_factors": [
                        "High credit utilization",
                        "Offshore transactions",
                        "Structuring patterns",
                        "Adverse media coverage"
                    ],
                    "last_updated": datetime.utcnow().isoformat()
                }
            
            # Fallback mock data
            return {
                "total_customers": 1000,
                "high_risk_customers": 45,
                "critical_risk_customers": 8,
                "total_transactions_today": 1250,
                "flagged_transactions_today": 23,
                "osint_signals_today": 12,
                "risk_score_distribution": {
                    "LOW": 750,
                    "MEDIUM": 187,
                    "HIGH": 45,
                    "CRITICAL": 8
                },
                "top_risk_factors": [
                    "High credit utilization",
                    "Offshore transactions",
                    "Structuring patterns",
                    "Adverse media coverage"
                ],
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in DataAgent.get_dashboard_stats: {e}")
            return {}

    async def generate_customer_data(self, num_customers: int = 100, include_risky: bool = True, risk_distribution: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        Generate AI-powered synthetic customer data
        """
        try:
            import random
            import uuid
            from datetime import datetime, timedelta
            
            # Default risk distribution if not provided
            if not risk_distribution:
                risk_distribution = {
                    "LOW": int(num_customers * 0.4),
                    "MEDIUM": int(num_customers * 0.3),
                    "HIGH": int(num_customers * 0.2),
                    "CRITICAL": int(num_customers * 0.1)
                }
            
            # Sample data for generation
            first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Maria", "Ahmed", "Jennifer", 
                          "James", "Emily", "William", "Jessica", "Richard", "Ashley", "Charles", "Amanda", "Thomas", "Stephanie"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                         "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
            
            osint_signal_types = ["SANCTIONS_CHECK", "ADVERSE_MEDIA", "PEP_STATUS", "MERCHANT_RISK", "DOMAIN_RISK", "GEOGRAPHIC_RISK"]
            risk_impacts = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
            
            generated_customers = []
            
            for i in range(num_customers):
                # Determine risk level based on distribution
                risk_level = random.choices(
                    list(risk_distribution.keys()),
                    weights=list(risk_distribution.values()),
                    k=1
                )[0]
                
                # Generate scores based on risk level
                if risk_level == "LOW":
                    credit_score = random.uniform(0.1, 0.4)
                    aml_score = random.uniform(0.1, 0.3)
                elif risk_level == "MEDIUM":
                    credit_score = random.uniform(0.3, 0.6)
                    aml_score = random.uniform(0.3, 0.5)
                elif risk_level == "HIGH":
                    credit_score = random.uniform(0.6, 0.8)
                    aml_score = random.uniform(0.6, 0.8)
                else:  # CRITICAL
                    credit_score = random.uniform(0.8, 0.95)
                    aml_score = random.uniform(0.8, 0.95)
                
                combined_risk_score = (credit_score + aml_score) / 2
                
                # Generate OSINT signals for higher risk customers
                osint_signals = []
                if risk_level in ["HIGH", "CRITICAL"]:
                    num_signals = random.randint(1, 4)
                    for _ in range(num_signals):
                        signal_type = random.choice(osint_signal_types)
                        signal_value = random.uniform(0.3, 0.9)
                        signal_impact = random.choice(risk_impacts)
                        osint_signals.append({
                            "type": signal_type,
                            "value": signal_value,
                            "impact": signal_impact
                        })
                
                # Generate customer data
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                customer = {
                    "customer_id": f"cust_{str(uuid.uuid4())[:8]}",
                    "name": f"{first_name} {last_name}",
                    "credit_score": round(credit_score, 2),
                    "aml_score": round(aml_score, 2),
                    "combined_risk_score": round(combined_risk_score, 2),
                    "risk_level": risk_level,
                    "last_updated": datetime.utcnow().isoformat(),
                    "osint_signals": osint_signals,
                    "explanation": f"AI-generated {risk_level.lower()} risk customer with {len(osint_signals)} OSINT signals"
                }
                
                generated_customers.append(customer)
            
            # Store the generated customers
            self.generated_customers = generated_customers
            
            return {
                "customers": generated_customers,
                "total_generated": len(generated_customers),
                "risk_distribution": risk_distribution,
                "generated_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating customer data: {e}")
            return {"error": str(e)}

    async def clear_all_data(self) -> Dict[str, Any]:
        """
        Clear all customer data
        """
        try:
            # Clear the stored generated customers
            self.generated_customers = []
            
            return {
                "message": "All customer data cleared successfully",
                "cleared_at": datetime.utcnow().isoformat(),
                "note": "Generated data has been cleared"
            }
        except Exception as e:
            logger.error(f"Error clearing data: {e}")
            return {"error": str(e)}

class ExplainabilityAgent:
    """
    MCP Explainability Agent - Provides human-readable explanations
    """
    
    async def explain_customer_risk(self, customer_id: str) -> Dict[str, Any]:
        """
        Provide detailed explanation of customer risk factors
        """
        try:
            # In real implementation, this would analyze actual customer data
            # For demo, return mock explanations based on customer ID
            
            explanations = {
                "cust_005": {
                    "customer_id": "cust_005",
                    "credit_explanation": "Ahmed Hassan has a credit score of 0.8 due to high credit utilization (85%) and recent missed payments. His account shows signs of financial stress with increasing debt levels over the past 3 months.",
                    "aml_explanation": "AML risk score of 0.9 is driven by multiple high-risk factors: 3 offshore transactions totaling $15,000, 2 structuring patterns (transactions of $9,500 and $9,800), and frequent transactions with crypto exchanges. The pattern suggests potential money laundering activity.",
                    "osint_explanation": "OSINT analysis reveals critical findings: Customer appears on OFAC sanctions list with 95% confidence match. Additional adverse media coverage from 2024 regarding financial fraud investigation. Email domain shows signs of temporary/disposable nature.",
                    "recommended_actions": [
                        "Immediate account freeze pending investigation",
                        "Enhanced due diligence review",
                        "Report to compliance team within 24 hours",
                        "Consider SAR filing if investigation confirms suspicious activity"
                    ],
                    "confidence_score": 0.92
                },
                "cust_002": {
                    "customer_id": "cust_002",
                    "credit_explanation": "Maria Garcia has a credit score of 0.7 due to moderate credit utilization (65%) but shows concerning payment patterns with 2 late payments in the last 6 months. Account age is relatively new (8 months).",
                    "aml_explanation": "AML risk score of 0.8 is primarily driven by PEP (Politically Exposed Person) status as family member of government official, combined with 4 transactions with high-risk merchants including offshore trading companies. Transaction amounts show unusual patterns.",
                    "osint_explanation": "OSINT analysis confirms PEP status with 88% confidence. No adverse media found, but family connections to government officials increase corruption risk. Merchant analysis shows 60% of transactions with offshore entities.",
                    "recommended_actions": [
                        "Enhanced monitoring for 90 days",
                        "PEP-specific due diligence review",
                        "Transaction pattern analysis",
                        "Regular risk reassessment"
                    ],
                    "confidence_score": 0.85
                },
                "cust_003": {
                    "customer_id": "cust_003",
                    "credit_explanation": "Robert Johnson has a very high credit score of 0.9 due to extremely high credit utilization (95%) and multiple recent credit applications. Account shows signs of potential credit abuse or fraud.",
                    "aml_explanation": "AML risk score of 0.6 is moderate, driven by some high-risk merchant transactions (casino and crypto exchanges) but no clear structuring patterns. Transaction frequency is unusually high for the account type.",
                    "osint_explanation": "OSINT analysis shows low domain risk but moderate merchant risk. No adverse media or sanctions hits. Some transactions with crypto exchanges raise questions about source of funds.",
                    "recommended_actions": [
                        "Credit limit review and potential reduction",
                        "Enhanced transaction monitoring",
                        "Source of funds verification",
                        "Regular account review"
                    ],
                    "confidence_score": 0.78
                }
            }
            
            return explanations.get(customer_id, {
                "customer_id": customer_id,
                "credit_explanation": "No detailed explanation available for this customer.",
                "aml_explanation": "No detailed explanation available for this customer.",
                "osint_explanation": "No detailed explanation available for this customer.",
                "recommended_actions": ["Standard monitoring"],
                "confidence_score": 0.5
            })
            
        except Exception as e:
            logger.error(f"Error in ExplainabilityAgent.explain_customer_risk: {e}")
            return {"error": str(e)}

class ActionAgent:
    """
    MCP Action Agent - Recommends actions based on risk assessment
    """
    
    async def get_recommended_actions(self, customer_id: str) -> List[str]:
        """
        Get recommended actions for a customer based on risk profile
        """
        try:
            # In real implementation, this would analyze actual risk data
            # For demo, return actions based on customer ID
            
            action_sets = {
                "cust_005": [
                    "IMMEDIATE: Freeze account and halt all transactions",
                    "URGENT: Notify compliance team within 2 hours",
                    "REQUIRED: Enhanced due diligence review",
                    "CONSIDER: SAR filing if investigation confirms suspicious activity",
                    "FOLLOW-UP: Regular risk reassessment every 30 days"
                ],
                "cust_002": [
                    "MONITOR: Enhanced transaction monitoring for 90 days",
                    "REVIEW: PEP-specific due diligence documentation",
                    "ANALYZE: Transaction pattern analysis and source of funds",
                    "SCHEDULE: Regular risk reassessment every 60 days",
                    "DOCUMENT: All findings in customer risk profile"
                ],
                "cust_003": [
                    "REVIEW: Credit limit and account terms",
                    "MONITOR: Enhanced transaction monitoring",
                    "VERIFY: Source of funds for large transactions",
                    "SCHEDULE: Account review in 30 days",
                    "CONSIDER: Additional identity verification"
                ]
            }
            
            return action_sets.get(customer_id, [
                "MONITOR: Standard account monitoring",
                "REVIEW: Regular risk assessment",
                "DOCUMENT: All findings in customer profile"
            ])
            
        except Exception as e:
            logger.error(f"Error in ActionAgent.get_recommended_actions: {e}")
            return ["Error retrieving recommended actions"]
