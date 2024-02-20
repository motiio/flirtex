--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg120+2)
-- Dumped by pg_dump version 16.2 (Debian 16.2-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: core; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA core;


ALTER SCHEMA core OWNER TO postgres;

--
-- Name: tech; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tech;


ALTER SCHEMA tech OWNER TO postgres;

--
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger;


ALTER SCHEMA tiger OWNER TO postgres;

--
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tiger_data;


ALTER SCHEMA tiger_data OWNER TO postgres;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


--
-- Name: genderenum; Type: TYPE; Schema: core; Owner: api_user
--

CREATE TYPE core.genderenum AS ENUM (
    'male',
    'female'
);


ALTER TYPE core.genderenum OWNER TO api_user;

--
-- Name: lookinggenderenum; Type: TYPE; Schema: core; Owner: api_user
--

CREATE TYPE core.lookinggenderenum AS ENUM (
    'nevermind',
    'male',
    'female'
);


ALTER TYPE core.lookinggenderenum OWNER TO api_user;

--
-- Name: photoprocessstatusenum; Type: TYPE; Schema: core; Owner: api_user
--

CREATE TYPE core.photoprocessstatusenum AS ENUM (
    'approved',
    'processing',
    'rejected'
);


ALTER TYPE core.photoprocessstatusenum OWNER TO api_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: filter; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core.filter (
    id uuid NOT NULL,
    looking_gender core.lookinggenderenum NOT NULL,
    age_from integer NOT NULL,
    age_to integer NOT NULL,
    max_distance integer NOT NULL,
    profile_id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core.filter OWNER TO api_user;

--
-- Name: interest; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core.interest (
    id uuid NOT NULL,
    name character varying(32) NOT NULL,
    icon text NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core.interest OWNER TO api_user;

--
-- Name: like; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core."like" (
    id uuid NOT NULL,
    source_profile uuid NOT NULL,
    target_profile uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core."like" OWNER TO api_user;

--
-- Name: match; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core.match (
    id uuid NOT NULL,
    profile_1 uuid NOT NULL,
    profile_2 uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core.match OWNER TO api_user;

--
-- Name: photo; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core.photo (
    id uuid NOT NULL,
    profile_id uuid NOT NULL,
    displaying_order integer NOT NULL,
    status core.photoprocessstatusenum NOT NULL,
    status_description character varying(32),
    hash character varying(32) NOT NULL,
    url character varying(512),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core.photo OWNER TO api_user;

--
-- Name: profile; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core.profile (
    id uuid NOT NULL,
    owner_id uuid NOT NULL,
    name character varying(32) NOT NULL,
    bio character varying(600),
    birthdate date NOT NULL,
    gender core.genderenum NOT NULL,
    location public.geometry(Point,4326),
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core.profile OWNER TO api_user;

--
-- Name: profile_interests; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core.profile_interests (
    id uuid NOT NULL,
    profile_id uuid NOT NULL,
    interest_id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core.profile_interests OWNER TO api_user;

--
-- Name: refresh_token; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core.refresh_token (
    id uuid NOT NULL,
    "user" uuid NOT NULL,
    value character varying NOT NULL,
    user_agent character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core.refresh_token OWNER TO api_user;

--
-- Name: save; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core.save (
    id uuid NOT NULL,
    profile_id uuid NOT NULL,
    saved_profile_id uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core.save OWNER TO api_user;

--
-- Name: skip; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core.skip (
    id uuid NOT NULL,
    source_profile uuid NOT NULL,
    target_profile uuid NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core.skip OWNER TO api_user;

--
-- Name: user; Type: TABLE; Schema: core; Owner: api_user
--

CREATE TABLE core."user" (
    id uuid NOT NULL,
    tg_id integer,
    tg_username character varying(32),
    tg_first_name character varying(32),
    tg_last_name character varying,
    tg_is_premium boolean,
    tg_language_code character varying,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE core."user" OWNER TO api_user;

--
-- Name: alembic_version; Type: TABLE; Schema: tech; Owner: api_user
--

CREATE TABLE tech.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE tech.alembic_version OWNER TO api_user;

--
-- Data for Name: filter; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core.filter (id, looking_gender, age_from, age_to, max_distance, profile_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: interest; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core.interest (id, name, icon, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: like; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core."like" (id, source_profile, target_profile, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: match; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core.match (id, profile_1, profile_2, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: photo; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core.photo (id, profile_id, displaying_order, status, status_description, hash, url, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: profile; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core.profile (id, owner_id, name, bio, birthdate, gender, location, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: profile_interests; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core.profile_interests (id, profile_id, interest_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: refresh_token; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core.refresh_token (id, "user", value, user_agent, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: save; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core.save (id, profile_id, saved_profile_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: skip; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core.skip (id, source_profile, target_profile, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: core; Owner: api_user
--

COPY core."user" (id, tg_id, tg_username, tg_first_name, tg_last_name, tg_is_premium, tg_language_code, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: tech; Owner: api_user
--

COPY tech.alembic_version (version_num) FROM stdin;
204350c470ac
\.


--
-- Data for Name: geocode_settings; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.geocode_settings (name, setting, unit, category, short_desc) FROM stdin;
\.


--
-- Data for Name: pagc_gaz; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_gaz (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_lex; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_lex (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_rules; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_rules (id, rule, is_custom) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Name: topology_id_seq; Type: SEQUENCE SET; Schema: topology; Owner: postgres
--

SELECT pg_catalog.setval('topology.topology_id_seq', 1, false);


--
-- Name: filter filter_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.filter
    ADD CONSTRAINT filter_pkey PRIMARY KEY (id);


--
-- Name: interest interest_name_key; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.interest
    ADD CONSTRAINT interest_name_key UNIQUE (name);


--
-- Name: interest interest_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.interest
    ADD CONSTRAINT interest_pkey PRIMARY KEY (id);


--
-- Name: like like_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core."like"
    ADD CONSTRAINT like_pkey PRIMARY KEY (id);


--
-- Name: match match_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.match
    ADD CONSTRAINT match_pkey PRIMARY KEY (id);


--
-- Name: photo photo_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.photo
    ADD CONSTRAINT photo_pkey PRIMARY KEY (id);


--
-- Name: photo photo_url_key; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.photo
    ADD CONSTRAINT photo_url_key UNIQUE (url);


--
-- Name: profile_interests profile_interests_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.profile_interests
    ADD CONSTRAINT profile_interests_pkey PRIMARY KEY (id);


--
-- Name: profile profile_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.profile
    ADD CONSTRAINT profile_pkey PRIMARY KEY (id);


--
-- Name: refresh_token refresh_token_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.refresh_token
    ADD CONSTRAINT refresh_token_pkey PRIMARY KEY (id);


--
-- Name: save save_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.save
    ADD CONSTRAINT save_pkey PRIMARY KEY (id);


--
-- Name: skip skip_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.skip
    ADD CONSTRAINT skip_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_tg_id_key; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core."user"
    ADD CONSTRAINT user_tg_id_key UNIQUE (tg_id);


--
-- Name: user user_tg_username_key; Type: CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core."user"
    ADD CONSTRAINT user_tg_username_key UNIQUE (tg_username);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: tech; Owner: api_user
--

ALTER TABLE ONLY tech.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: idx_profile_location; Type: INDEX; Schema: core; Owner: api_user
--

CREATE INDEX idx_profile_location ON core.profile USING gist (location);


--
-- Name: filter filter_profile_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.filter
    ADD CONSTRAINT filter_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: like like_source_profile_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core."like"
    ADD CONSTRAINT like_source_profile_fkey FOREIGN KEY (source_profile) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: like like_target_profile_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core."like"
    ADD CONSTRAINT like_target_profile_fkey FOREIGN KEY (target_profile) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: match match_profile_1_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.match
    ADD CONSTRAINT match_profile_1_fkey FOREIGN KEY (profile_1) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: match match_profile_2_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.match
    ADD CONSTRAINT match_profile_2_fkey FOREIGN KEY (profile_2) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: photo photo_profile_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.photo
    ADD CONSTRAINT photo_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: profile_interests profile_interests_interest_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.profile_interests
    ADD CONSTRAINT profile_interests_interest_id_fkey FOREIGN KEY (interest_id) REFERENCES core.interest(id) ON DELETE CASCADE;


--
-- Name: profile_interests profile_interests_profile_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.profile_interests
    ADD CONSTRAINT profile_interests_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: profile profile_owner_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.profile
    ADD CONSTRAINT profile_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES core."user"(id);


--
-- Name: refresh_token refresh_token_user_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.refresh_token
    ADD CONSTRAINT refresh_token_user_fkey FOREIGN KEY ("user") REFERENCES core."user"(id);


--
-- Name: save save_profile_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.save
    ADD CONSTRAINT save_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: save save_saved_profile_id_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.save
    ADD CONSTRAINT save_saved_profile_id_fkey FOREIGN KEY (saved_profile_id) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: skip skip_source_profile_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.skip
    ADD CONSTRAINT skip_source_profile_fkey FOREIGN KEY (source_profile) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: skip skip_target_profile_fkey; Type: FK CONSTRAINT; Schema: core; Owner: api_user
--

ALTER TABLE ONLY core.skip
    ADD CONSTRAINT skip_target_profile_fkey FOREIGN KEY (target_profile) REFERENCES core.profile(id) ON DELETE CASCADE;


--
-- Name: SCHEMA core; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA core TO api_user;
GRANT USAGE ON SCHEMA core TO evgen;


--
-- Name: SCHEMA tech; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA tech TO api_user;


--
-- Name: TABLE filter; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core.filter TO evgen;


--
-- Name: TABLE interest; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core.interest TO evgen;


--
-- Name: TABLE "like"; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core."like" TO evgen;


--
-- Name: TABLE match; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core.match TO evgen;


--
-- Name: TABLE photo; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core.photo TO evgen;


--
-- Name: TABLE profile; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core.profile TO evgen;


--
-- Name: TABLE profile_interests; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core.profile_interests TO evgen;


--
-- Name: TABLE refresh_token; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core.refresh_token TO evgen;


--
-- Name: TABLE save; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core.save TO evgen;


--
-- Name: TABLE skip; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core.skip TO evgen;


--
-- Name: TABLE "user"; Type: ACL; Schema: core; Owner: api_user
--

GRANT SELECT ON TABLE core."user" TO evgen;


--
-- PostgreSQL database dump complete
--

