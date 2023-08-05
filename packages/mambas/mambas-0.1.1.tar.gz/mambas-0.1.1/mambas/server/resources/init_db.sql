CREATE TABLE IF NOT EXISTS projects (
    id_project INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(40),
    session_counter INTEGER DEFAULT 0,
    token VARCHAR(32),
    CONSTRAINT name_unique UNIQUE (name),
    CONSTRAINT token_unique UNIQUE (token)
);

CREATE TABLE IF NOT EXISTS sessions (
    id_session INTEGER PRIMARY KEY AUTOINCREMENT,
    session_index INTEGER NOT NULL,
    dt_start TIMESTAMP,
    dt_end TIMESTAMP,
    is_active BIT DEFAULT 1,
    host VARCHAR(30),
    id_project VARCHAR(40) NOT NULL,
    FOREIGN KEY(id_project) REFERENCES projects(id_project)
);

CREATE TABLE IF NOT EXISTS epochs (
    id_epoch INTEGER PRIMARY KEY AUTOINCREMENT,
    epoch_index INTEGER NOT NULL,
    metrics VARCHAR(256) NOT NULL,
    time TIMESTAMP NOT NULL,
    id_session INTEGER NOT NULL,
    FOREIGN KEY(id_session) REFERENCES sessions(id_session)
);