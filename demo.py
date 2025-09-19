#!/usr/bin/env python3
"""
Demo script for Unified Risk Monitor
This script demonstrates the key features of the risk monitoring system
"""

import asyncio
import requests
import json
from datetime import datetime, timedelta
import random

API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the backend is running on port 8000")
        return False

def test_risky_customers():
    """Test getting risky customers"""
    try:
        response = requests.get(f"{API_BASE_URL}/customers/risky?limit=10&min_risk_score=0.5")
        if response.status_code == 200:
            customers = response.json()
            print(f"✅ Retrieved {len(customers)} risky customers")
            
            # Display top 3 customers
            for i, customer in enumerate(customers[:3]):
                print(f"  {i+1}. {customer['name']} - Risk: {customer['risk_level']} ({customer['combined_risk_score']:.1%})")
            
            return customers
        else:
            print(f"❌ Failed to get risky customers: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting risky customers: {e}")
        return []

def test_customer_explanation(customer_id):
    """Test getting customer risk explanation"""
    try:
        response = requests.get(f"{API_BASE_URL}/customers/{customer_id}/explain")
        if response.status_code == 200:
            explanation = response.json()
            print(f"✅ Retrieved explanation for customer {customer_id}")
            print(f"  Credit: {explanation['credit_explanation'][:100]}...")
            print(f"  AML: {explanation['aml_explanation'][:100]}...")
            print(f"  Confidence: {explanation['confidence_score']:.1%}")
            return explanation
        else:
            print(f"❌ Failed to get explanation for customer {customer_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting explanation: {e}")
        return None

def test_dashboard_stats():
    """Test getting dashboard statistics"""
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Retrieved dashboard statistics")
            print(f"  Total customers: {stats['total_customers']}")
            print(f"  High risk: {stats['high_risk_customers']}")
            print(f"  Critical risk: {stats['critical_risk_customers']}")
            print(f"  OSINT signals today: {stats['osint_signals_today']}")
            return stats
        else:
            print(f"❌ Failed to get dashboard stats: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting dashboard stats: {e}")
        return None

def test_create_transaction():
    """Test creating a new transaction"""
    try:
        transaction = {
            "customer_id": "cust_001",
            "amount": 1500.00,
            "merchant": "Test Merchant",
            "category": "Retail",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        response = requests.post(f"{API_BASE_URL}/transactions", json=transaction)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Created transaction: {result['transaction_id']}")
            return result
        else:
            print(f"❌ Failed to create transaction: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error creating transaction: {e}")
        return None

def test_osint_enrichment(customer_id):
    """Test OSINT enrichment"""
    try:
        response = requests.post(f"{API_BASE_URL}/osint/enrich/{customer_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ OSINT enrichment completed for customer {customer_id}")
            print(f"  Signals found: {len(result['signals'])}")
            return result
        else:
            print(f"❌ Failed to enrich customer {customer_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error enriching customer: {e}")
        return None

def main():
    """Run the demo"""
    print("🚀 Unified Risk Monitor Demo")
    print("=" * 50)
    
    # Test API health
    if not test_api_health():
        return
    
    print("\n📊 Testing Dashboard Statistics...")
    stats = test_dashboard_stats()
    
    print("\n👥 Testing Risky Customers...")
    customers = test_risky_customers()
    
    if customers:
        # Test explanation for first customer
        print(f"\n🔍 Testing Risk Explanation for {customers[0]['name']}...")
        explanation = test_customer_explanation(customers[0]['customer_id'])
        
        # Test OSINT enrichment
        print(f"\n🌐 Testing OSINT Enrichment for {customers[0]['name']}...")
        osint_result = test_osint_enrichment(customers[0]['customer_id'])
    
    print("\n💳 Testing Transaction Creation...")
    test_create_transaction()
    
    print("\n✅ Demo completed!")
    print("\n🌐 You can now visit the frontend at: http://localhost:3000")
    print("📚 API documentation at: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
