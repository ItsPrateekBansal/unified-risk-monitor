"""
OSINT Enrichment Service for External Intelligence Gathering
"""

import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging
import os
import json

logger = logging.getLogger(__name__)

class OSINTEnrichmentService:
    """
    Service for enriching customer data with OSINT (Open Source Intelligence)
    """
    
    def __init__(self):
        self.bright_data_api_key = os.getenv("BRIGHT_DATA_API_KEY", "")
        self.bright_data_endpoint = "https://api.brightdata.com/v1"
        self.timeout = 30.0
        
    async def enrich_customer(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Enrich customer with OSINT data from multiple sources
        """
        try:
            signals = []
            
            # Get customer data (in real implementation, this would come from database)
            customer_data = await self._get_customer_data(customer_id)
            if not customer_data:
                return signals
            
            # Run OSINT checks in parallel
            tasks = [
                self._check_adverse_media(customer_data),
                self._check_domain_risk(customer_data),
                self._check_merchant_risk(customer_data),
                self._check_sanctions_list(customer_data),
                self._check_pep_status(customer_data)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, dict) and result.get("signal_type"):
                    signals.append(result)
                elif isinstance(result, Exception):
                    logger.error(f"OSINT check failed: {result}")
            
            # Store signals in database
            await self._store_osint_signals(customer_id, signals)
            
            logger.info(f"Enriched customer {customer_id} with {len(signals)} OSINT signals")
            return signals
            
        except Exception as e:
            logger.error(f"Error enriching customer {customer_id}: {e}")
            return []
    
    async def _get_customer_data(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Get customer data for OSINT enrichment
        """
        # In real implementation, this would query the database
        # For demo purposes, return mock data
        return {
            "id": customer_id,
            "name": "John Smith",
            "email": "john.smith@email.com",
            "phone": "+1-555-0101",
            "address": "123 Main St, New York, NY"
        }
    
    async def _check_adverse_media(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check for adverse media mentions using Bright Data or web search
        """
        try:
            # Simulate API call to Bright Data or web search
            name = customer_data.get("name", "")
            
            # Mock adverse media check
            adverse_media_found = False
            risk_score = 0.0
            sources = []
            
            # Simulate finding adverse media for high-risk customers
            if "Garcia" in name or "Hassan" in name:
                adverse_media_found = True
                risk_score = 0.7
                sources = [
                    {
                        "title": "Financial Fraud Investigation",
                        "url": "https://example-news.com/fraud-investigation",
                        "date": "2024-01-15",
                        "relevance": 0.8
                    }
                ]
            
            return {
                "signal_type": "ADVERSE_MEDIA",
                "signal_value": risk_score,
                "signal_data": {
                    "found": adverse_media_found,
                    "sources": sources,
                    "search_terms": [name]
                },
                "source": "bright_data_news_api",
                "confidence": 0.85,
                "risk_impact": "HIGH" if risk_score > 0.5 else "LOW"
            }
            
        except Exception as e:
            logger.error(f"Error checking adverse media: {e}")
            return {"signal_type": "ADVERSE_MEDIA", "signal_value": 0.0, "error": str(e)}
    
    async def _check_domain_risk(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check domain risk for email addresses
        """
        try:
            email = customer_data.get("email", "")
            domain = email.split("@")[-1] if "@" in email else ""
            
            # Mock domain risk assessment
            risk_score = 0.0
            risk_factors = []
            
            # Check for suspicious domains
            suspicious_domains = ["tempmail.com", "10minutemail.com", "guerrillamail.com"]
            if domain in suspicious_domains:
                risk_score = 0.8
                risk_factors.append("temporary_email_domain")
            
            # Check domain age (simulated)
            if domain and len(domain) < 10:  # Short domains might be suspicious
                risk_score += 0.2
                risk_factors.append("short_domain")
            
            return {
                "signal_type": "DOMAIN_RISK",
                "signal_value": min(risk_score, 1.0),
                "signal_data": {
                    "domain": domain,
                    "risk_factors": risk_factors,
                    "domain_age_days": 365 if domain not in suspicious_domains else 30
                },
                "source": "domain_analysis",
                "confidence": 0.75,
                "risk_impact": "MEDIUM" if risk_score > 0.3 else "LOW"
            }
            
        except Exception as e:
            logger.error(f"Error checking domain risk: {e}")
            return {"signal_type": "DOMAIN_RISK", "signal_value": 0.0, "error": str(e)}
    
    async def _check_merchant_risk(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check risk associated with merchants in transaction history
        """
        try:
            # In real implementation, this would analyze transaction history
            # For demo, return mock merchant risk data
            
            high_risk_merchants = ["Offshore Trading Co", "Crypto Exchange", "Casino Royale"]
            merchant_risk_score = 0.0
            risky_merchants = []
            
            # Simulate finding high-risk merchant transactions
            if customer_data.get("id") in ["cust_002", "cust_005"]:  # High-risk customers
                merchant_risk_score = 0.6
                risky_merchants = ["Offshore Trading Co", "Crypto Exchange"]
            
            return {
                "signal_type": "MERCHANT_RISK",
                "signal_value": merchant_risk_score,
                "signal_data": {
                    "risky_merchants": risky_merchants,
                    "transaction_count": len(risky_merchants) * 3,
                    "total_merchants": 10
                },
                "source": "transaction_analysis",
                "confidence": 0.90,
                "risk_impact": "HIGH" if merchant_risk_score > 0.5 else "LOW"
            }
            
        except Exception as e:
            logger.error(f"Error checking merchant risk: {e}")
            return {"signal_type": "MERCHANT_RISK", "signal_value": 0.0, "error": str(e)}
    
    async def _check_sanctions_list(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check against sanctions lists and watchlists
        """
        try:
            name = customer_data.get("name", "")
            
            # Mock sanctions check
            sanctions_hit = False
            risk_score = 0.0
            matched_lists = []
            
            # Simulate sanctions hit for specific customers
            if "Hassan" in name:
                sanctions_hit = True
                risk_score = 0.9
                matched_lists = ["OFAC", "EU_SANCTIONS"]
            
            return {
                "signal_type": "SANCTIONS_CHECK",
                "signal_value": risk_score,
                "signal_data": {
                    "sanctions_hit": sanctions_hit,
                    "matched_lists": matched_lists,
                    "check_date": datetime.utcnow().isoformat()
                },
                "source": "sanctions_api",
                "confidence": 0.95,
                "risk_impact": "CRITICAL" if sanctions_hit else "LOW"
            }
            
        except Exception as e:
            logger.error(f"Error checking sanctions: {e}")
            return {"signal_type": "SANCTIONS_CHECK", "signal_value": 0.0, "error": str(e)}
    
    async def _check_pep_status(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if customer is a Politically Exposed Person (PEP)
        """
        try:
            name = customer_data.get("name", "")
            
            # Mock PEP check
            is_pep = False
            risk_score = 0.0
            pep_type = None
            
            # Simulate PEP status for specific customers
            if "Garcia" in name:
                is_pep = True
                risk_score = 0.6
                pep_type = "FAMILY_MEMBER"
            
            return {
                "signal_type": "PEP_STATUS",
                "signal_value": risk_score,
                "signal_data": {
                    "is_pep": is_pep,
                    "pep_type": pep_type,
                    "pep_lists_checked": ["UN_PEP", "US_PEP", "EU_PEP"]
                },
                "source": "pep_database",
                "confidence": 0.88,
                "risk_impact": "MEDIUM" if is_pep else "LOW"
            }
            
        except Exception as e:
            logger.error(f"Error checking PEP status: {e}")
            return {"signal_type": "PEP_STATUS", "signal_value": 0.0, "error": str(e)}
    
    async def _store_osint_signals(self, customer_id: str, signals: List[Dict[str, Any]]):
        """
        Store OSINT signals in database
        """
        try:
            # In real implementation, this would store in database
            # For demo, just log the signals
            logger.info(f"Storing {len(signals)} OSINT signals for customer {customer_id}")
            for signal in signals:
                logger.debug(f"OSINT Signal: {signal['signal_type']} - {signal['signal_value']}")
                
        except Exception as e:
            logger.error(f"Error storing OSINT signals: {e}")
    
    async def get_osint_summary(self, customer_id: str) -> Dict[str, Any]:
        """
        Get summary of OSINT signals for a customer
        """
        try:
            # In real implementation, this would query the database
            # For demo, return mock summary
            return {
                "customer_id": customer_id,
                "total_signals": 5,
                "high_risk_signals": 2,
                "last_updated": datetime.utcnow().isoformat(),
                "signal_types": ["ADVERSE_MEDIA", "DOMAIN_RISK", "MERCHANT_RISK", "SANCTIONS_CHECK", "PEP_STATUS"]
            }
            
        except Exception as e:
            logger.error(f"Error getting OSINT summary: {e}")
            return {"error": str(e)}
