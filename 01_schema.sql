CREATE TABLE colors (
    tricode CHAR(3) PRIMARY KEY NOT NULL,
    team_name CHAR(100) NOT NULL,
    color_primary CHAR(7) NOT NULL,
    color_secondary CHAR(7) NOT NULL,
    color_accent CHAR(7) NOT NULL,
    neutral_dark CHAR(7) NOT NULL,
    neutral_light CHAR(7) NOT NULL,
    CHECK (color_primary LIKE '#%'),
    CHECK (color_secondary LIKE '#%'),
    CHECK (color_accent LIKE '#%'),
    CHECK (neutral_dark LIKE '#%'),
    CHECK (neutral_light LIKE '#%')
);