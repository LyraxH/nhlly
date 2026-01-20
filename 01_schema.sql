CREATE TABLE colors (
    code CHAR(3) PRIMARY KEY NOT NULL,
    team_name CHAR(100) NOT NULL,
    light CHAR(7) NOT NULL,
    dark CHAR(7) NOT NULL,
    accent CHAR(7) NOT NULL,
    CHECK (light LIKE '#%'),
    CHECK (dark LIKE '#%'),
    CHECK (accent LIKE '#%')
);