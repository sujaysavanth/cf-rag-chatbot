CREATE TABLE IF NOT EXISTS documents (
    file_id TEXT NOT NULL,
    chunk_id TEXT PRIMARY KEY,
    chunk_index INTEGER NOT NULL,
    text_content TEXT NOT NULL,
    source TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
