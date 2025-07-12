-- Add default prefix setting to guilds table
-- This allows guild owners to disable the default "!" prefix

ALTER TABLE guilds 
ADD COLUMN IF NOT EXISTS default_prefix_enabled BOOLEAN NOT NULL DEFAULT TRUE;

-- Update existing guilds to have default prefix enabled (safe to run multiple times)
UPDATE guilds SET default_prefix_enabled = TRUE WHERE default_prefix_enabled IS NULL;