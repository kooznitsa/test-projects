CREATE_STATUSES = \
    """
    DROP TABLE IF EXISTS status CASCADE;
    CREATE TABLE status (
        id SERIAL PRIMARY KEY,
        status VARCHAR(100) UNIQUE NOT NULL
    );"""

CREATE_TIMEZONES = \
    """
    DROP TABLE IF EXISTS timezone CASCADE;
    CREATE TABLE timezone (
        id SERIAL PRIMARY KEY,
        timezone VARCHAR(100) UNIQUE NOT NULL
    );"""

CREATE_PHONE_CODES = \
    """
    DROP TABLE IF EXISTS phone_code CASCADE;
    CREATE TABLE phone_code (
        id SERIAL PRIMARY KEY,
        phone_code INTEGER UNIQUE NOT NULL
    );"""

CREATE_TAGS = \
    """
    DROP TABLE IF EXISTS tag CASCADE;
    CREATE TABLE tag (
        id SERIAL PRIMARY KEY,
        tag VARCHAR(100) UNIQUE NOT NULL
    );"""

CREATE_MAILOUTS = \
    """
    DROP TABLE IF EXISTS mailout CASCADE;
    CREATE TABLE mailout (
        id SERIAL PRIMARY KEY,
        start_time TIMESTAMPTZ NOT NULL,
        finish_time TIMESTAMPTZ NOT NULL,
        available_start TIME WITH TIME ZONE,
        available_finish TIME WITH TIME ZONE
    );"""

CREATE_CUSTOMERS = \
    """
    DROP TABLE IF EXISTS customer CASCADE;
    CREATE TABLE customer (
        id SERIAL PRIMARY KEY,
        phone CHAR(11) NOT NULL CHECK(phone ~ '^7[0-9]{10}$'),
        phone_code_id INTEGER NOT NULL REFERENCES phone_code(id) ON DELETE SET NULL,
        timezone_id INTEGER REFERENCES timezone(id) ON DELETE SET NULL
    );"""

CREATE_MESSAGES = \
    """
    DROP TABLE IF EXISTS message CASCADE;
    CREATE TABLE message (
        id SERIAL PRIMARY KEY,
        text_message TEXT NOT NULL,
        create_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
        status_id INTEGER NOT NULL REFERENCES status(id) ON DELETE SET NULL,
        mailout_id INTEGER NOT NULL REFERENCES mailout(id) ON DELETE SET NULL
    );"""

CREATE_MAILOUTS_CUSTOMERS = \
    """
    DROP TABLE IF EXISTS mailout_customer CASCADE;
    CREATE TABLE mailout_customer (
        id SERIAL PRIMARY KEY,
        mailout_id INTEGER NOT NULL REFERENCES mailout(id) ON DELETE SET NULL,
        customer_id INTEGER NOT NULL REFERENCES customer(id) ON DELETE SET NULL
    );"""

CREATE_MAILOUTS_PHONE_CODES = \
    """
    DROP TABLE IF EXISTS mailout_phone_code CASCADE;
    CREATE TABLE mailout_phone_code (
        id SERIAL PRIMARY KEY,
        mailout_id INTEGER NOT NULL REFERENCES mailout(id) ON DELETE SET NULL,
        phone_code_id INTEGER NOT NULL REFERENCES phone_code(id) ON DELETE SET NULL
    );"""

CREATE_MAILOUTS_TAGS = \
    """
    DROP TABLE IF EXISTS mailout_tag CASCADE;
    CREATE TABLE mailout_tag (
        id SERIAL PRIMARY KEY,
        mailout_id INTEGER NOT NULL REFERENCES mailout(id) ON DELETE SET NULL,
        tag_id INTEGER NOT NULL REFERENCES tag(id) ON DELETE SET NULL
    );"""

CREATE_CUSTOMERS_TAGS = \
    """
    DROP TABLE IF EXISTS customer_tag CASCADE;
    CREATE TABLE customer_tag (
        id SERIAL PRIMARY KEY,
        customer_id INTEGER NOT NULL REFERENCES customer(id) ON DELETE SET NULL,
        tag_id INTEGER NOT NULL REFERENCES tag(id) ON DELETE SET NULL
    );"""

INSERT_DATA = \
    """
    WITH a AS (
            INSERT INTO phone_code (phone_code) VALUES (925)
            ON CONFLICT (phone_code) DO UPDATE SET phone_code = EXCLUDED.phone_code
            RETURNING id AS id_1
        ),
        b AS (
            INSERT INTO status (status) VALUES ('Not sent') 
            ON CONFLICT (status) DO UPDATE SET status = EXCLUDED.status
            RETURNING id AS id_2
        ),
        c AS (
            INSERT INTO tag (tag) VALUES ('Female') 
            ON CONFLICT (tag) DO UPDATE SET tag = EXCLUDED.tag
            RETURNING id AS id_3
        ),
        d AS (
            INSERT INTO timezone (timezone) VALUES ('Europe/Moscow') 
            ON CONFLICT (timezone) DO UPDATE SET timezone = EXCLUDED.timezone
            RETURNING id AS id_4
        ),
        e AS (
            INSERT INTO mailout (
                start_time, finish_time, available_start, available_finish, 
                text_message, phone_code_id
            ) 
            VALUES (
                '2023-06-22 19:10:25-07', '2023-06-23 19:10:25-07', '09:00:00', '17:00:00', 
                'Test Hello', (SELECT id_1 FROM a)
            )
            RETURNING id AS id_5
        ),
        f AS (
            INSERT INTO customer (phone, phone_code_id, timezone_id) 
            VALUES ('79250636831', (SELECT id_1 FROM a), (SELECT id_4 FROM d))
            RETURNING id AS id_6
        )

    INSERT INTO message (status_id, mailout_id, customer_id) 
    VALUES ((SELECT id_2 FROM b), (SELECT id_5 FROM e), (SELECT id_6 FROM f));
    """