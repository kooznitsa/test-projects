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
    currency_id INTEGER NULL,
    request_time TIMESTAMP NOT NULL,

    CONSTRAINT fk_currency
        FOREIGN KEY(currency_id)
        REFERENCES currencies(id)
        ON DELETE SET NULL
);

CREATE TABLE itineraries (
    id SERIAL PRIMARY KEY,
    itinerary_count INTEGER UNIQUE NOT NULL,
    container_count_id INTEGER NOT NULL,
    total_flight_time INTEGER NOT NULL,
    priced_itinerary_id INTEGER NOT NULL,

    CONSTRAINT fk_container_count
        FOREIGN KEY(container_count_id)
        REFERENCES containers(container_count)
        ON DELETE SET NULL,

    CONSTRAINT fk_priced_itinerary
        FOREIGN KEY(priced_itinerary_id)
            REFERENCES priced_itineraries(id)
            ON DELETE SET NULL
);

CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    itinerary_count_id INTEGER NOT NULL,
    flight_part INTEGER NOT NULL,
    direct_flight BOOLEAN NOT NULL,
    carrier_id INTEGER NULL,
    flight_num INTEGER NULL,
    source_id INTEGER NULL,
    destination_id INTEGER NULL,
    departure_time TIMESTAMP NULL,
    arrival_time TIMESTAMP NULL,
    flight_time INTEGER NULL,
    class_field_id INTEGER NULL,
    num_stops INTEGER NULL,
    ticket_type_id INTEGER NULL,
    created TIMESTAMP NOT NULL,

    CONSTRAINT fk_itinerary_count
        FOREIGN KEY(itinerary_count_id)
            REFERENCES itineraries(itinerary_count)
            ON DELETE SET NULL,

    CONSTRAINT fk_carrier
        FOREIGN KEY(carrier_id)
            REFERENCES carriers(id)
            ON DELETE SET NULL,

    CONSTRAINT fk_source
        FOREIGN KEY(source_id)
            REFERENCES cities(id)
            ON DELETE SET NULL,

    CONSTRAINT fk_destination
        FOREIGN KEY(destination_id)
            REFERENCES cities(id)
            ON DELETE SET NULL,

    CONSTRAINT fk_class_field
        FOREIGN KEY(class_field_id)
            REFERENCES classes(id)
            ON DELETE SET NULL,

    CONSTRAINT fk_ticket_type
        FOREIGN KEY(ticket_type_id)
            REFERENCES ticket_types(id)
            ON DELETE SET NULL
);