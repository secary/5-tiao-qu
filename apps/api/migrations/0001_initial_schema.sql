CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'import_status') THEN
    CREATE TYPE import_status AS ENUM (
      'uploaded',
      'extracting',
      'chunking',
      'embedding',
      'ready',
      'failed'
    );
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'answer_type') THEN
    CREATE TYPE answer_type AS ENUM (
      'direct_rule',
      'related_inference',
      'not_found',
      'conflict'
    );
  END IF;

  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'source_type') THEN
    CREATE TYPE source_type AS ENUM (
      'base_rulebook',
      'expansion_rulebook',
      'faq',
      'errata',
      'player_note'
    );
  END IF;
END
$$;

CREATE TABLE IF NOT EXISTS board_games (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  canonical_name text,
  description text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rulebooks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  board_game_id uuid REFERENCES board_games(id) ON DELETE SET NULL,
  title text NOT NULL,
  version text,
  language text,
  source_file text NOT NULL,
  storage_path text NOT NULL,
  import_status import_status NOT NULL DEFAULT 'uploaded',
  error_message text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS rule_pages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rulebook_id uuid NOT NULL REFERENCES rulebooks(id) ON DELETE CASCADE,
  page_number integer NOT NULL CHECK (page_number > 0),
  page_image_path text,
  extracted_text text,
  ocr_status text NOT NULL DEFAULT 'pending',
  ocr_metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (rulebook_id, page_number)
);

CREATE TABLE IF NOT EXISTS rule_chunks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rulebook_id uuid NOT NULL REFERENCES rulebooks(id) ON DELETE CASCADE,
  page_id uuid REFERENCES rule_pages(id) ON DELETE SET NULL,
  page_number integer NOT NULL CHECK (page_number > 0),
  chapter_title text,
  chunk_text text NOT NULL,
  chunk_index integer NOT NULL CHECK (chunk_index >= 0),
  source_file text NOT NULL,
  bounding_box jsonb,
  source_type source_type NOT NULL DEFAULT 'base_rulebook',
  source_priority integer NOT NULL DEFAULT 100,
  embedding vector(1536),
  embedding_model text,
  embedding_dimensions integer NOT NULL DEFAULT 1536,
  embedding_ref text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (rulebook_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS rule_chunks_rulebook_page_idx
  ON rule_chunks (rulebook_id, page_number);

CREATE INDEX IF NOT EXISTS rule_chunks_embedding_hnsw_idx
  ON rule_chunks USING hnsw (embedding vector_cosine_ops);

CREATE TABLE IF NOT EXISTS questions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rulebook_id uuid NOT NULL REFERENCES rulebooks(id) ON DELETE CASCADE,
  conversation_id uuid,
  question_text text NOT NULL,
  question_language text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS answers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  question_id uuid NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
  answer_type answer_type NOT NULL,
  conclusion text NOT NULL,
  explanation text,
  confidence numeric(4, 3) CHECK (confidence >= 0 AND confidence <= 1),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS citations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  answer_id uuid NOT NULL REFERENCES answers(id) ON DELETE CASCADE,
  rule_chunk_id uuid REFERENCES rule_chunks(id) ON DELETE SET NULL,
  citation_index integer NOT NULL CHECK (citation_index >= 0),
  page_number integer NOT NULL CHECK (page_number > 0),
  chapter_title text,
  chunk_text text NOT NULL,
  source_file text NOT NULL,
  source_type source_type NOT NULL DEFAULT 'base_rulebook',
  source_priority integer NOT NULL DEFAULT 100,
  similarity_score numeric(6, 5),
  bounding_box jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (answer_id, citation_index)
);
