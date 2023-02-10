CREATE TABLE priced_itineraries (
    id SERIAL PRIMARY KEY,
    priced_itinerary VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE carriers (
    id SERIAL PRIMARY KEY,
    carrier VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE cities (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE classes (
    id SERIAL PRIMARY KEY,
    class_field VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE ticket_types (
    id SERIAL PRIMARY KEY,
    ticket_type VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE currencies (
    id SERIAL PRIMARY KEY,
    currency VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE containers (
    id SERIAL PRIMARY KEY,
    container_count INTEGER UNIQUE NOT NULL,
    adult_price FLOAT NULL,
    child_price FLOAT NULL,
    infant_price FLOAT NULL,
    currency_id INTEGER NULL REFERENCES currencies(id) ON DELETE SET NULL,
    request_time TIMESTAMP NOT NULL
);

CREATE TABLE itineraries (
    id SERIAL PRIMARY KEY,
    itinerary_count INTEGER UNIQUE NOT NULL,
    container_count_id INTEGER NOT NULL REFERENCES containers(container_count) ON DELETE SET NULL,
    total_flight_time INTEGER NOT NULL,
    priced_itinerary_id INTEGER NOT NULL REFERENCES priced_itineraries(id) ON DELETE SET NULL
);

CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    itinerary_count_id INTEGER NOT NULL REFERENCES itineraries(itinerary_count) ON DELETE SET NULL,
    flight_part INTEGER NOT NULL,
    direct_flight BOOLEAN NOT NULL,
    carrier_id INTEGER NULL REFERENCES carriers(id) ON DELETE SET NULL,
    flight_num INTEGER NULL,
    source_id INTEGER NULL REFERENCES cities(id) ON DELETE SET NULL,
    destination_id INTEGER NULL REFERENCES cities(id) ON DELETE SET NULL,
    departure_time TIMESTAMP NULL,
    arrival_time TIMESTAMP NULL,
    flight_time INTEGER NULL,
    class_field_id INTEGER NULL REFERENCES classes(id) ON DELETE SET NULL,
    num_stops INTEGER NULL,
    ticket_type_id INTEGER NULL REFERENCES ticket_types(id) ON DELETE SET NULL,
    created TIMESTAMP NOT NULL
);