CREATE TABLE records (
    id UUID PRIMARY KEY,
    schema_version VARCHAR(20) NOT NULL,
    data JSONB NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT false,
    CONSTRAINT fk_schema
      FOREIGN KEY(schema_version)
      REFERENCES schema_versions(version)
);
