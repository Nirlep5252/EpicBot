-- Migration 001: Initial database schema
-- Creates the foundation tables for EpicBot

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Guilds table - stores Discord guild information
CREATE TABLE IF NOT EXISTS guilds (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Guild prefixes table - stores custom prefixes for each guild
CREATE TABLE IF NOT EXISTS guild_prefixes (
    guild_id BIGINT REFERENCES guilds(id) ON DELETE CASCADE,
    prefix TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (guild_id, prefix)
);

-- Guild plugins table - stores which plugins are enabled for each guild
CREATE TABLE IF NOT EXISTS guild_plugins (
    guild_id BIGINT REFERENCES guilds(id) ON DELETE CASCADE,
    plugin_name TEXT NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    config JSONB DEFAULT '{}',
    installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (guild_id, plugin_name)
);

-- Users table - stores Discord user information
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Migration tracking table - keeps track of applied migrations
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert this migration record
INSERT INTO schema_migrations (version, name) 
VALUES (1, 'initial_schema') 
ON CONFLICT (version) DO NOTHING;