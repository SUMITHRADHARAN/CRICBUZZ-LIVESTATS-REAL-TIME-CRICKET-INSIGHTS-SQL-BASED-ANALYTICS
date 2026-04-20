-- 1. DATABASE SETUP
CREATE DATABASE IF NOT EXISTS cricbuzz_db;
USE cricbuzz_db;

-- 2. TABLE CREATION (Ordered for Foreign Key constraints)

-- Table: venues
CREATE TABLE IF NOT EXISTS venues (
    venue_id INT PRIMARY KEY AUTO_INCREMENT,
    venue_name VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT
);

-- Table: players
CREATE TABLE IF NOT EXISTS players (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(255),
    name VARCHAR(100),
    playing_role VARCHAR(50),
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    country VARCHAR(50),
    total_runs INT DEFAULT 0,
    total_wickets INT DEFAULT 0
);

-- Table: series_matches
CREATE TABLE IF NOT EXISTS series_matches (
    id INT PRIMARY KEY AUTO_INCREMENT,
    series_name VARCHAR(255),
    team1 VARCHAR(100),
    team2 VARCHAR(100),
    venue VARCHAR(255),
    match_format VARCHAR(50),
    start_date DATE,
    status VARCHAR(100)
);

-- Table: recent_matches
CREATE TABLE IF NOT EXISTS recent_matches (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    match_desc VARCHAR(255),
    team1 VARCHAR(100),
    team2 VARCHAR(100),
    venue VARCHAR(255),
    venue_city VARCHAR(100),
    start_date DATETIME,
    state VARCHAR(20),
    status VARCHAR(255)
);

-- Table: combined_matches
CREATE TABLE IF NOT EXISTS combined_matches (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    team1 VARCHAR(100),
    team2 VARCHAR(100),
    match_winner VARCHAR(100),
    toss_winner VARCHAR(100),
    toss_decision ENUM('Bat', 'Field'),
    venue_country VARCHAR(100),
    team_country VARCHAR(100),
    format ENUM('Test', 'ODI', 'T20'),
    win_margin_runs INT DEFAULT 0,
    win_margin_wickets INT DEFAULT 0,
    start_date DATE
);

-- Table: players_stats
CREATE TABLE IF NOT EXISTS players_stats (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(255),
    test_runs INT DEFAULT 0,
    odi_runs INT DEFAULT 0,
    t20_runs INT DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Table: batting_data
CREATE TABLE IF NOT EXISTS batting_data (
    stat_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT,
    player_name VARCHAR(255),
    match_id INT,
    runs INT,
    balls_faced INT,
    strike_rate DECIMAL(5,2),
    dismissal VARCHAR(50),
    format VARCHAR(20),
    match_date DATE,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Table: bowling_data
CREATE TABLE IF NOT EXISTS bowling_data (
    stat_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT,
    player_name VARCHAR(255),
    match_id INT,
    overs DECIMAL(4,1),
    wickets INT,
    runs_conceded INT,
    economy_rate DECIMAL(4,2),
    format VARCHAR(20),
    venue VARCHAR(100),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Table: fielding_data
CREATE TABLE IF NOT EXISTS fielding_data (
    fielding_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT,
    match_id INT,
    catches INT DEFAULT 0,
    stumpings INT DEFAULT 0,
    run_outs INT DEFAULT 0,
    format VARCHAR(20),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- Table: players_partnerships_data
CREATE TABLE IF NOT EXISTS players_partnerships_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    match_id INT,
    innings_no INT,
    wicket_fallen INT DEFAULT 0,
    batter1_name VARCHAR(255),
    batter2_name VARCHAR(255),
    runs_partnership INT
);

-- Table: top_odi_runs
CREATE TABLE IF NOT EXISTS top_odi_runs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    player_name VARCHAR(255),
    runs INT,
    average DECIMAL(5,2),
    centuries INT
);

-- 3. INSERT SAMPLE DATA
INSERT INTO venues (venue_name, city, country, capacity) VALUES 
('Narendra Modi Stadium', 'Ahmedabad', 'India', 132000),
('Lord''s', 'London', 'England', 30000),
('MCG', 'Melbourne', 'Australia', 100024);


-- 2. Insert 12 unique world-class players
INSERT INTO players (full_name, name, playing_role, batting_style, bowling_style, country, total_runs, total_wickets) VALUES 
('Virat Kohli', 'V Kohli', 'Batsman', 'Right-hand bat', 'Right-arm medium', 'India', 12898, 4),
('Rohit Sharma', 'R Sharma', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'India', 10709, 8),
('Jasprit Bumrah', 'J Bumrah', 'Bowler', 'Right-hand bat', 'Right-arm fast', 'India', 212, 155),
('Hardik Pandya', 'H Pandya', 'Allrounder', 'Right-hand bat', 'Right-arm fast-medium', 'India', 1500, 60),
('Steve Smith', 'S Smith', 'Batsman', 'Right-hand bat', 'Right-arm legbreak', 'Australia', 9665, 19),
('Kane Williamson', 'K Williamson', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'New Zealand', 8263, 30),
('Joe Root', 'J Root', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'England', 11416, 60),
('Babar Azam', 'B Azam', 'Batsman', 'Right-hand bat', 'Right-arm offbreak', 'Pakistan', 5729, 0),
('Rashid Khan', 'R Khan', 'Bowler', 'Right-hand bat', 'Right-arm legbreak', 'Afghanistan', 1200, 180),
('Quinton de Kock', 'Q de Kock', 'Wicketkeeper', 'Left-hand bat', 'None', 'South Africa', 6770, 0),
('Mitchell Starc', 'M Starc', 'Bowler', 'Left-hand bat', 'Left-arm fast', 'Australia', 500, 350),
('Glenn Maxwell', 'G Maxwell', 'Allrounder', 'Right-hand bat', 'Right-arm offbreak', 'Australia', 3800, 70);


INSERT INTO players_stats (player_id, player_name, test_runs, odi_runs, t20_runs)
VALUES (1, 'Virat Kohli', 8848, 13848, 4037), (2, 'Rohit Sharma', 4137, 10709, 3853);

INSERT INTO series_matches (series_name, team1, team2, venue, match_format, start_date, status)
VALUES ('IPL 2024', 'CSK', 'RCB', 'Wankhede', 'T20', '2024-03-22', 'CSK won by 20 runs');

INSERT INTO combined_matches (team1, team2, match_winner, toss_winner, toss_decision, venue_country, team_country, format, win_margin_runs, win_margin_wickets, start_date) 
VALUES ('India', 'Australia', 'India', 'India', 'Bat', 'India', 'India', 'ODI', 50, 0, '2024-03-10');

-- Insert a match with a 12-run win margin
INSERT INTO combined_matches (team1, team2, match_winner, toss_winner, toss_decision, venue_country, team_country, format, win_margin_runs, win_margin_wickets, start_date) 
VALUES ('India', 'England', 'India', 'India', 'Bat', 'India', 'India', 'T20', 12, 0, '2024-04-12');

-- Link a batting performance to this new match (Match ID 4 or the next available ID)
INSERT INTO batting_data (player_id, player_name, match_id, runs, balls_faced, strike_rate, dismissal, format, match_date) 
VALUES (1, 'Virat Kohli', LAST_INSERT_ID(), 45, 30, 150.00, 'out', 'T20', '2024-04-12');



INSERT INTO batting_data (player_id, player_name, match_id, runs, balls_faced, strike_rate, dismissal, format, match_date) 
VALUES (1, 'Virat Kohli', 1, 82, 53, 154.71, 'not out', 'T20', '2024-03-10');

INSERT INTO top_odi_runs (player_name, runs, average, centuries) VALUES ('Sachin Tendulkar', 18426, 44.83, 49), ('Virat Kohli', 13848, 58.67, 50);

-- Add the missing venue column to bowling_data
ALTER TABLE bowling_data ADD COLUMN venue VARCHAR(255);

-- Update the venue data from the recent_matches table
UPDATE bowling_data b
JOIN recent_matches r ON b.match_id = r.match_id
SET b.venue = r.venue;

-- 1. First, clear existing records to start fresh
TRUNCATE TABLE bowling_data;
TRUNCATE TABLE recent_matches;

-- 2. Insert a match and get its ID (likely ID 1)
INSERT INTO recent_matches (match_id, match_desc, team1, team2, venue, venue_city, start_date, state, status) 
VALUES (1, 'World Cup Final', 'India', 'Australia', 'Narendra Modi Stadium', 'Ahmedabad', '2026-04-01 14:00:00', 'Complete', 'Australia won');

-- 3. Insert bowling stats using the EXACT same match_id (1)
INSERT INTO bowling_data (player_id, player_name, match_id, overs, wickets, runs_conceded, economy_rate, format) 
VALUES (3, 'Jasprit Bumrah', 1, 4.0, 2, 18, 4.50, 'T20');

UPDATE bowling_data 
SET overs = 12.0 
WHERE player_name = 'Jasprit Bumrah';
