DROP TABLE IF EXISTS runs;

CREATE TABLE runs (
    device_fingerprint TEXT UNIQUE
);