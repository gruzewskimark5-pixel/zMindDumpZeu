-- Hardened Competitive OS v0.1: Rivalry Engine SQL Schema

-- Players
CREATE TABLE IF NOT EXISTS players (
  id UUID PRIMARY KEY,
  external_ref TEXT UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Rivalry pairs (directional)
CREATE TABLE IF NOT EXISTS rivalry_pairs (
  playeraid UUID NOT NULL REFERENCES players(id),
  playerbid UUID NOT NULL REFERENCES players(id),
  rhi NUMERIC(4,3) NOT NULL DEFAULT 0.0,
  momentum NUMERIC(4,3) NOT NULL DEFAULT 0.0,
  volatility NUMERIC(4,3) NOT NULL DEFAULT 0.0,
  confidence NUMERIC(4,3) NOT NULL DEFAULT 0.0,
  interactioncount30d INT NOT NULL DEFAULT 0,
  lastinteractionts TIMESTAMP,
  -- Welford's streaming stats
  delta_mean NUMERIC(6,4) DEFAULT 0,
  delta_m2 NUMERIC(6,4) DEFAULT 0,
  delta_count INT DEFAULT 0,
  priority NUMERIC(5,3),
  PRIMARY KEY (playeraid, playerbid)
);

-- Rivalry events (append-only)
CREATE TABLE IF NOT EXISTS rivalry_events (
  id UUID PRIMARY KEY,
  playeraid UUID NOT NULL REFERENCES players(id),
  playerbid UUID NOT NULL REFERENCES players(id),
  round_id UUID,
  hole_number INT,
  di NUMERIC(4,3),
  event_type TEXT NOT NULL,
  raw_weight NUMERIC(4,3) NOT NULL,
  effective_weight NUMERIC(4,3) NOT NULL,
  source_event_id TEXT NOT NULL,
  version INT NOT NULL DEFAULT 1,
  event_ts TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Round context (for batch updates)
CREATE TABLE IF NOT EXISTS round_results (
  id UUID PRIMARY KEY,
  round_id UUID,
  player_id UUID NOT NULL REFERENCES players(id),
  total_score INT,
  diweightedscore NUMERIC(6,3),
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_rivalry_pairs_a ON rivalry_pairs (playeraid);
CREATE INDEX IF NOT EXISTS idx_rivalry_pairs_b ON rivalry_pairs (playerbid);
CREATE INDEX IF NOT EXISTS idx_rivalry_events_pair ON rivalry_events (playeraid, playerbid);
CREATE INDEX IF NOT EXISTS idx_rivalry_events_ts ON rivalry_events (event_ts);
CREATE INDEX IF NOT EXISTS idx_rivalry_events_source ON rivalry_events (source_event_id, version);
CREATE INDEX IF NOT EXISTS idx_round_results_round ON round_results (round_id);
