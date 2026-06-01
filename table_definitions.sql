CREATE TABLE users_raw
(
  id serial PRIMARY KEY NOT NULL,
  user_full_name character varying(50),
  user_city character varying(255),
  user_gender character varying(10),
  user_age integer,
  user_email character varying(50),
  user_phone character varying(12),
  user_bookingTime text,
  user_bookingComplaint text,
  user_bookingRating integer,
  user_allergy text, 
  CONSTRAINT persons_pkey PRIMARY KEY (id)
);

COPY users_raw(user_full_name, user_city, user_gender, user_age, user_email, user_phone, user_bookingTime, user_bookingComplaint, user_bookingRating, user_allergy)
FROM '/datagen.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE booking_info
(
  id serial PRIMARY KEY NOT NULL,
  user_full_name character varying(50),
  user_city character varying(255),
  user_gender character varying(10),
  user_age integer,
  user_email character varying(50),
  user_phone character varying(12),
  user_allergy text
);

UPDATE booking_info
SET user_full_name = users_raw.user_full_name,
    user_city = users_raw.user_city,
    user_gender = users_raw.user_gender,
    user_age = users_raw.user_age,
    user_email = users_raw.user_email,
    user_phone = users_raw.user_phone,
    user_allergy = users_raw.user_allergy
FROM users_raw
WHERE booking_info.id = users_raw.id;

CREATE TABLE user_booking_history
(
  id serial PRIMARY KEY NOT NULL,
  user_bookingTime text,
  user_bookingComplaint text,
  user_bookingRating integer
);

UPDATE user_booking_history
SET user_bookingTime = users_raw.user_bookingTime, 
    user_bookingComplaint = users_raw.user_bookingComplaint, 
    user_bookingRating = users_raw.user_bookingRating
FROM users_raw
WHERE user_booking_history.id = users_raw.id;

CREATE TABLE user_demographics
(
  id serial PRIMARY KEY NOT NULL,
  user_geopolygon character varying(255),
  user_gender character varying(10),
  user_age_range text
);

UPDATE user_demographics
SET user_gender = users_raw.user_gender,
    user_age_range = CASE 
                    WHEN users_raw.user_age < 18 THEN 'under 18'
                    WHEN users_raw.user_age >= 18 AND users_raw.user_age < 25 THEN '18-24'
                    WHEN users_raw.user_age >= 25 AND users_raw.user_age < 41 THEN '25-40'
                    WHEN users_raw.user_age >= 41 AND users_raw.user_age < 66 THEN '41-65'
                    WHEN users_raw.user_age >= 66 AND users_raw.user_age < 80 THEN '66-79'
                    ELSE '80+'
                 END
FROM users_raw
WHERE user_demographics.id = users_raw.id;

CREATE TABLE user_health_info
(
  id serial PRIMARY KEY NOT NULL,
  user_allergy text
);

UPDATE user_health_info
SET user_allergy = users_raw.user_allergy
FROM users_raw
WHERE user_health_info.id = users_raw.id;