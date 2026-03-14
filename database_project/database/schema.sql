-- vision data from camera
CREATE TABLE IF NOT EXISTS vision_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    face_detected BOOLEAN NOT NULL,
    emotion TEXT
);

-- nlp data from mic/transcription
CREATE TABLE IF NOT EXISTS nlp_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    sentiment TEXT,
    keywords TEXT
);

-- correlation between vision & nlp
CREATE TABLE IF NOT EXISTS insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vision_id INTEGER NOT NULL,
    nlp_id INTEGER NOT NULL,
    correlation_score REAL,

    FOREIGN KEY (vision_id) REFERENCES vision_data(id),
    FOREIGN KEY (nlp_id) REFERENCES nlp_data(id)
);

-- scoring system
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    insight_id INTEGER NOT NULL,
    engagement REAL,
    clarity REAL,
    interaction REAL,
    final_score REAL,

    FOREIGN KEY (insight_id) REFERENCES insights(id)
);


