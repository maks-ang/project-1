CREATE SCHEMA day10;
CREATE TABLE day10.users (
id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
name text NOT NULL,
email text NOT NULL UNIQUE
);
CREATE TABLE day10.events (
id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 title text NOT NULL
);
CREATE TABLE day10.applications (
id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
user_id bigint NOT NULL REFERENCES day10.users(id),
event_id bigint NOT NULL REFERENCES day10.events(id),
status text NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'processing', 'done'))
);