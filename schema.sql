CREATE TABLE videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    thumbnail TEXT,
    click_count INTEGER DEFAULT 0
);