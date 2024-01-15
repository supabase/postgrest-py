CREATE TABLE public.countries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    iso CHAR (2) NOT NULL,
    country_name VARCHAR (80) NOT NULL,
    nicename VARCHAR (80) NOT NULL,
    iso3 CHAR (3) DEFAULT NULL,
    numcode SMALLINT DEFAULT NULL,
    phonecode INT NOT NULL
);

INSERT INTO public.countries (iso, country_name, nicename, iso3, numcode, phonecode) VALUES
    ('AF', 'AFGHANISTAN', 'Afghanistan', 'AFG', 4, 93),
    ('AL', 'ALBANIA', 'Albania', 'ALB', 8, 355),
    ('DZ', 'ALGERIA', 'Algeria', 'DZA', 12, 213),
    ('AQ', 'ANTARCTICA', 'Antarctica', NULL, NULL, 0),
    ('CR', 'COSTA RICA', 'Costa Rica', 'CRI', 188, 506),
    ('ES', 'SPAIN', 'Spain', 'ESP', 724, 34),
    ('TH', 'THAILAND', 'Thailand', 'THA', 764, 66),
    ('TG', 'TOGO', 'Togo', 'TGO', 768, 228),
    ('TT', 'TRINIDAD AND TOBAGO', 'Trinidad and Tobago', 'TTO', 780, 1868),
    ('GB', 'UNITED KINGDOM', 'United Kingdom', 'GBR', 826, 44),
    ('US', 'UNITED STATES', 'United States', 'USA', 840, 1),
    ('ZW', 'ZIMBABWE', 'Zimbabwe', 'ZWE', 716, 263);

create table public.users (
    id int8 primary key,
    name text,
    address jsonb
);

insert into public.users (id, name, address) values
    (1, 'Michael', '{ "postcode": 90210, "street": "Melrose Place" }'),
    (2, 'Jane', '{}');

create table public.reservations (
    id int8 primary key,
    room_name text,
    during tsrange
);

insert into public.reservations (id, room_name, during) values
    (1, 'Emerald', '[2000-01-01 13:00, 2000-01-01 15:00)'),
    (2, 'Topaz', '[2000-01-02 09:00, 2000-01-02 10:00)');


create table public.issues (
    id int8 primary key,
    title text,
    tags text[]
);

insert into public.issues (id, title, tags) values
    (1, 'Cache invalidation is not working', array['is:open', 'severity:high', 'priority:low']),
    (2, 'Use better names', array['is:open', 'severity:low', 'priority:medium']);
