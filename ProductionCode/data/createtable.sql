CREATE TABLE observations (
    id INTEGER PRIMARY KEY,
    observed_on DATE,
    quality_grade TEXT,
    latitude REAL,
    longitude REAL,
    taxon_id INTEGER,
    taxon_name TEXT,
    common_name TEXT,
    iconic_taxon TEXT,
    rank TEXT,
    place_guess TEXT,
    observer TEXT,
    num_id_agreements INTEGER,
    url TEXT
);