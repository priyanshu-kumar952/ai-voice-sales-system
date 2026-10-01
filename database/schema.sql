-- ============================================
-- VOICE AI SALES SYSTEM DATABASE SCHEMA
-- ============================================


-- ============================================
-- LEADS
-- ============================================

CREATE TABLE leads (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    budget BIGINT,
    preferred_location TEXT,
    property_type TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================
-- INVENTORY
-- ============================================

CREATE TABLE inventory (
    id BIGSERIAL PRIMARY KEY,
    project_name TEXT NOT NULL,
    location TEXT NOT NULL,
    property_type TEXT NOT NULL,
    price BIGINT NOT NULL,
    bedrooms INT,
    available_units INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================
-- CALLS
-- ============================================

CREATE TABLE calls (
    id BIGSERIAL PRIMARY KEY,
    call_id TEXT UNIQUE NOT NULL,
    lead_id BIGINT REFERENCES leads(id) ON DELETE SET NULL,
    phone_number TEXT,
    status TEXT NOT NULL DEFAULT 'started',
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    duration_seconds INT,
    transcript TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ============================================
-- CALL INDEXES
-- ============================================

CREATE INDEX idx_calls_lead_id
ON calls(lead_id);

CREATE INDEX idx_calls_call_id
ON calls(call_id);

CREATE INDEX idx_calls_status
ON calls(status);

CREATE INDEX idx_calls_started_at
ON calls(started_at);