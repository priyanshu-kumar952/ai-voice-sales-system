```markdown
# AI Voice Sales System

A backend-driven Voice AI sales and lead qualification system designed to handle property inquiries, qualify leads, query inventory, persist call data, and automate post-call lead processing.

## Overview

The system connects a voice agent with a controlled backend API, PostgreSQL/Supabase, Redis, and n8n automation.

Instead of allowing the AI agent to directly access the database, the agent interacts with controlled FastAPI tools for inventory lookup and call actions.

### Core Flow

```text
Voice Agent
     │
     ▼
FastAPI Backend
     │
     ├── Agent Tools
     │     ├── Check Inventory
     │     └── Transfer Call
     │
     ├── Call Management
     │
     ├── Webhook Validation
     │
     └── Rate Limiting
     │
     ▼
Supabase / PostgreSQL
     │
     ├── Inventory
     ├── Leads
     └── Calls
     
Call End
     │
     ▼
FastAPI Webhook
     │
     ▼
n8n
     │
     ├── Lead Extraction
     ├── Data Normalization
     ├── Existing Lead Matching
     ├── Lead Creation / Update
     └── Call → Lead Linking
     │
     ▼
Supabase
```

## Features

- FastAPI backend
- Controlled AI agent tools
- Property inventory search
- Lead creation and management
- Call lifecycle management
- Retell-compatible webhook endpoint
- HMAC webhook verification
- Redis-based token-bucket rate limiting
- PostgreSQL/Supabase persistence
- Structured lead extraction through n8n
- Existing lead detection
- Empty-field-only lead updates
- Automatic call-to-lead linking
- Pydantic request validation
- Environment-based configuration
- End-to-end tested FastAPI → n8n → Supabase pipeline

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Pydantic Settings
- Uvicorn
- HTTPX

### Database

- PostgreSQL
- Supabase
- Psycopg

### Infrastructure

- Redis / Valkey
- Git
- GitHub

### Automation

- n8n
- Structured LLM extraction

### Planned Integrations

- Retell AI
- WhatsApp Cloud API
- Exotel

## Project Structure

```text
ai-voice-sales-system/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── rate_limit.py
│   │   │   ├── redis.py
│   │   │   └── security.py
│   │   │
│   │   ├── models/
│   │   │   ├── call.py
│   │   │   ├── inventory.py
│   │   │   ├── lead.py
│   │   │   └── tools.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── call_repository.py
│   │   │   ├── inventory_repository.py
│   │   │   └── lead_repository.py
│   │   │
│   │   ├── routers/
│   │   │   ├── calls.py
│   │   │   ├── health.py
│   │   │   ├── inventory.py
│   │   │   ├── leads.py
│   │   │   ├── tools.py
│   │   │   └── webhooks.py
│   │   │
│   │   ├── services/
│   │   │   ├── call_service.py
│   │   │   ├── inventory_service.py
│   │   │   └── lead_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
│
├── database/
│   └── schema.sql
│
├── n8n/
│   └── workflows/
│       └── Voice AI - Post-Call Lead Processing (1).json
│
├── prompts/
│   └── 📁voice-agent/
│       ├── extraction_prompt.md
│       ├── qualification_prompt.md
│       └── system_prompt.md
│
└── .gitignore
```

## Backend Architecture

The backend follows a layered architecture:

```text
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

### Routers

Handle HTTP requests and expose the API.

### Services

Contain application/business logic.

### Repositories

Handle database operations.

### Models

Define validated request and response structures.

### Core

Contains shared infrastructure such as:

- Configuration
- Database connection pool
- Redis client
- Rate limiting
- Security utilities

## Agent Tools

The AI agent does not directly access the database.

Instead, it uses controlled API tools.

### Check Inventory

```http
POST /tools/check_inventory
```

Example:

```json
{
  "location": "Indore",
  "property_type": "Apartment",
  "max_budget": 6500000
}
```

The backend queries available inventory and returns matching properties.

### Transfer Call

```http
POST /tools/transfer_call
```

Example:

```json
{
  "reason": "Customer requested a sales representative",
  "phone_number": "+919811111111"
}
```

The current implementation records the transfer request. Actual telephony transfer integration is planned for the Exotel phase.

## Database

The system currently uses three primary tables.

### Inventory

Stores available property inventory.

```text
inventory
├── id
├── project_name
├── location
├── property_type
├── price
├── bedrooms
├── available_units
└── created_at
```

### Leads

Stores qualified customer information.

```text
leads
├── id
├── name
├── phone
├── budget
├── preferred_location
├── property_type
└── created_at
```

### Calls

Stores call lifecycle and transcript information.

```text
calls
├── id
├── call_id
├── lead_id
├── phone_number
├── status
├── started_at
├── ended_at
├── duration_seconds
├── transcript
└── created_at
```

## Security

The backend includes several security mechanisms:

- Environment-based secrets
- HMAC webhook verification
- Redis-backed rate limiting
- Pydantic request validation
- Controlled database access
- Secrets excluded from Git
- `.env` excluded through `.gitignore`

Sensitive configuration should be provided through environment variables and should never be committed to the repository.

## Post-Call Automation

After a call ends, the backend forwards structured call information to n8n.

The workflow performs:

```text
Call Ended
    ↓
Validate Call Data
    ↓
Extract Lead Information
    ↓
Normalize Phone / Budget
    ↓
Match Existing Lead
    ↓
      ┌───────────────┐
      │               │
Existing Lead     New Lead
      │               │
      ▼               ▼
Fill Empty Fields   Create Lead
      │               │
      └───────┬───────┘
              ▼
       Resolve Lead ID
              ↓
       Link Lead to Call
```

The workflow avoids overwriting existing non-empty lead information.

## End-to-End Testing

The complete post-call pipeline has been tested locally.

Test flow:

```text
Call Event
    ↓
FastAPI Webhook
    ↓
HMAC Verification
    ↓
Call Stored in Supabase
    ↓
n8n Webhook
    ↓
Structured Lead Extraction
    ↓
Lead Creation
    ↓
Call → Lead Linking
```

A test conversation containing:

```text
Name: Rahul
Location: Indore
Property: 2 BHK apartment
Budget: ₹60 lakh
```

was successfully transformed into structured lead data and linked to the corresponding call record.

Test records were removed after verification.

## Local Development

### Clone

```bash
git clone https://github.com/priyanshu-kumar952/ai-voice-sales-system.git
cd ai-voice-sales-system
```

### Create virtual environment

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment

```bash
cp .env.example .env
```

Set the required environment variables in `.env`.

### Run the backend

```bash
python -m uvicorn app.main:app --reload
```

The API will be available locally at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Current Status

### Completed

- Backend middleware
- Database layer
- Inventory API
- Lead API
- Call management
- Agent tools
- Webhook handling
- HMAC validation
- Redis rate limiting
- n8n post-call automation
- Structured lead extraction
- Lead matching and persistence
- End-to-end integration testing
- GitHub repository

### Planned

- WhatsApp follow-up automation
- Retell production integration
- Exotel telephony integration
- Real call transfer
- Production deployment
- Production monitoring and observability
- Additional automated tests

## Design Principles

### Controlled AI Access

The AI agent interacts with explicit backend tools rather than directly accessing the database.

### Separation of Concerns

API routing, business logic, persistence, and infrastructure are separated into independent layers.

### Structured Data

Lead information is converted from conversational text into validated structured data before database persistence.

### Safe Updates

Existing lead information is preserved unless a field is empty and can safely be filled.

### Event-Driven Processing

Call completion triggers asynchronous post-call processing through n8n.

## Future Architecture

```text
                 ┌──────────────┐
                 │ Voice Agent  │
                 └──────┬───────┘
                        │
                        ▼
                 ┌──────────────┐
                 │   FastAPI    │
                 └──────┬───────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      Inventory       Calls         Tools
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                  PostgreSQL
                   / Supabase
                        │
                  Call Completed
                        │
                        ▼
                       n8n
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
    Lead Processing              WhatsApp
                                      │
                                      ▼
                              Customer Follow-up

                  Telephony Layer
                        │
                      Exotel
                        │
                        ▼
                  Real Phone Calls
```

## License

This project is currently intended as a personal engineering project and portfolio project.
```
