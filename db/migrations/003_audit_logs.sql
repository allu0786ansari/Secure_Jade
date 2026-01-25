CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    record_id UUID,
    action VARCHAR(50),
    performed_by VARCHAR(100),
    timestamp TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);
