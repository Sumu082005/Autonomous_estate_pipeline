# Autonomous Estate Operations Pipeline 🏰🤖

A live REST API mapping unstructured WhatsApp text messages into structured operational insights. This pipeline acts as a fully autonomous digital manager for homestays and boutique estates, processing raw guest data to generate premium menus, enforce pricing rules, and handle legal compliance.

## 🚀 Overview

Managing a boutique estate involves parsing messy, fragmented communications from staff or guests. This pipeline intercepts those raw messages via WhatsApp (Twilio) and processes them through a multi-agent AI system (CrewAI). 

The system automatically:
1. **Parses unstructured text** to separate dietary needs from guest compliance data.
2. **Generates premium menu descriptions** with dynamic pricing (strictly between ₹800 - ₹2500).
3. **Handles edge cases**, such as automatically appending safe, pureed options if an infant is mentioned.
4. **Determines legal documentation requirements** (Visas, Passports, Domestic IDs) based on guest origin.
5. **Returns a pristine Markdown response**, securely wrapped in XML for Twilio delivery.

## 🧠 Tech Stack

* **Framework:** FastAPI
* **AI Orchestration:** CrewAI
* **LLM Provider:** Groq (`llama-3.3-70b-versatile`) via LiteLLM
* **Integration:** Twilio WhatsApp Sandbox
* **Cloud Hosting:** Render

## ⚙️ Multi-Agent Architecture

The pipeline utilizes a sequential CrewAI process with three distinct agents:

1. **Communications Ingestion Agent:** Reads the raw message and strictly separates food/menu items from document/compliance requests.
2. **Business Operations Agent:** Enforces hospitality rules. It writes appetizing menu descriptions, assigns strict INR pricing, accommodates infant dietary needs, and determines the exact legal documents required for check-in.
3. **Digital Clerk Agent:** Takes the operational data and formats it into a flawless, customer-ready Markdown document.

## 🛠️ Local Setup

### 1. Prerequisites
Ensure you have Python 3.10 - 3.13 installed (CrewAI currently requires Python < 3.14).

### 2. Installation
Clone the repository and install the dependencies:
```bash
git clone [https://github.com/YOUR-USERNAME/autonomous_estate_pipeline.git](https://github.com/YOUR-USERNAME/autonomous_estate_pipeline.git)
cd autonomous_estate_pipeline
pip install -r requirements.txt
