CREATE SCHEMA day10;
CREATE TABLE day10.users (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL
);

CREATE TABLE day10.events (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title text NOT NULL,
    seats_left integer NOT NULL,
    CONSTRAINT event_seats_check CHECK (seats_left >= 0)
);

CREATE TABLE day10.applications (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id bigint NOT NULL REFERENCES day10.users(id),
    event_id bigint NOT NULL REFERENCES day10.events(id),
    status text NOT NULL DEFAULT 'new',
    CONSTRAINT applications_status_check CHECK (status IN ('new', 'processing', 'done')),
    CONSTRAINT user_event_uniq UNIQUE (user_id, event_id)
);