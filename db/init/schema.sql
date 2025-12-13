CREATE TABLE IF NOT EXISTS pictures (
    id VARCHAR(36) PRIMARY KEY,
    path VARCHAR(255) NOT NULL,
    date VARCHAR(19) NOT NULL
);

CREATE TABLE IF NOT EXISTS tags (
    tag VARCHAR(32),
    picture_id VARCHAR(36),
    confidence FLOAT NOT NULL,
    date VARCHAR(19) NOT NULL,
    PRIMARY KEY (tag, picture_id),
    FOREIGN KEY (picture_id) REFERENCES pictures(id)
);
