--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

-- Started on 2021-06-02 17:39:18

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
-- TOC entry 3013 (class 1262 OID 24701)
-- Name: mtg; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE mtg WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';


ALTER DATABASE mtg OWNER TO postgres;

\connect mtg

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
-- TOC entry 207 (class 1255 OID 24791)
-- Name: clearall(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.clearall() RETURNS void
    LANGUAGE sql
    AS $$ DELETE FROM "Sets"
WHERE True;
DELETE FROM "Cards"
WHERE True;
$$;


ALTER FUNCTION public.clearall() OWNER TO postgres;

--
-- TOC entry 205 (class 1255 OID 24785)
-- Name: countcolor(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.countcolor(colorname character varying) RETURNS integer
    LANGUAGE sql
    AS $$ SELECT count(*) FROM "Cards"
WHERE "Color"=colorName
$$;


ALTER FUNCTION public.countcolor(colorname character varying) OWNER TO postgres;

--
-- TOC entry 203 (class 1255 OID 24776)
-- Name: dec_cards_count(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.dec_cards_count() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN
UPDATE "Sets" SET "CountCards" = "CountCards" - 1 where OLD."Set" = "Sets"."Name";
RETURN NEW;
END;
$$;


ALTER FUNCTION public.dec_cards_count() OWNER TO postgres;

--
-- TOC entry 206 (class 1255 OID 24789)
-- Name: dropblock(text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.dropblock(blockname text) RETURNS void
    LANGUAGE sql
    AS $$ DELETE FROM "Sets"
WHERE "Block"=blockName
$$;


ALTER FUNCTION public.dropblock(blockname text) OWNER TO postgres;

--
-- TOC entry 202 (class 1255 OID 24772)
-- Name: inc_cards_count(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.inc_cards_count() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN
UPDATE "Sets" SET "CountCards" = "CountCards" + 1 where NEW."Set" = "Sets"."Name";
RETURN NEW;
END;
$$;


ALTER FUNCTION public.inc_cards_count() OWNER TO postgres;

--
-- TOC entry 208 (class 1255 OID 24797)
-- Name: insertrowincards(text, character varying, smallint, character varying, text, character varying, boolean); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.insertrowincards(nname text, ncolor character varying, nmanavalue smallint, ntype character varying, nset text, nrarity character varying, nislegendary boolean) RETURNS void
    LANGUAGE sql
    AS $$
INSERT INTO "Cards" ("Name","Color","ManaValue","Type","Set","Rarity","isLegendary")
VALUES(nName,nColor,nManaValue,nType,nSet,nRarity,nisLegendary)
$$;


ALTER FUNCTION public.insertrowincards(nname text, ncolor character varying, nmanavalue smallint, ntype character varying, nset text, nrarity character varying, nislegendary boolean) OWNER TO postgres;

--
-- TOC entry 204 (class 1255 OID 24788)
-- Name: printcardstable(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.printcardstable() RETURNS TABLE("Name" text, "Color" character varying, "ManaValue" smallint, "Type" character varying, "Set" text, "Rarity" character varying, "isLegendary" boolean)
    LANGUAGE sql
    AS $$ SELECT * FROM "Cards"
$$;


ALTER FUNCTION public.printcardstable() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 201 (class 1259 OID 24741)
-- Name: Cards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Cards" (
    "Name" text NOT NULL,
    "Color" character varying(9) NOT NULL,
    "ManaValue" smallint NOT NULL,
    "Type" character varying(12) NOT NULL,
    "Set" text NOT NULL,
    "Rarity" character varying(8) NOT NULL,
    "isLegendary" boolean DEFAULT false NOT NULL,
    CONSTRAINT "Cards_ManaValue_check" CHECK (("ManaValue" >= 0))
);


ALTER TABLE public."Cards" OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 24715)
-- Name: Sets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Sets" (
    "Name" text NOT NULL,
    "SetCode" character varying(3) NOT NULL,
    "ReleaseDate" date NOT NULL,
    "Size" smallint NOT NULL,
    "Block" text NOT NULL,
    "CountCards" smallint DEFAULT 0,
    CONSTRAINT "Sets_SetCode_check" CHECK ((("SetCode")::text = upper(("SetCode")::text))),
    CONSTRAINT "Sets_Size_check" CHECK (("Size" > 0))
);


ALTER TABLE public."Sets" OWNER TO postgres;

--
-- TOC entry 3007 (class 0 OID 24741)
-- Dependencies: 201
-- Data for Name: Cards; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Captain Lanely Storm', 'Red', 3, 'Creature', 'Ixalan', 'Rare', true);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Axis of Mortality', 'White', 6, 'Enchantment', 'Ixalan', 'Mythic', false);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Cancel', 'Blue', 3, 'Instant', 'Ixalan', 'Common', false);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Primal Amulet', 'Colorless', 4, 'Artifact', 'Ixalan', 'Rare', false);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Star of Extinction', 'Red', 7, 'Sorcery', 'Ixalan', 'Mythic', false);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Engulf the Shore', 'Blue', 4, 'Instant', 'Shadows over Innistrad', 'Rare', false);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Tireless Tracker', 'Green', 3, 'Creature', 'Shadows over Innistrad', 'Rare', false);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Autumnal Gloom', 'Green', 3, 'Enchantment', 'Shadows over Innistrad', 'Uncommon', false);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('The Gitrog Monster', 'Multi', 5, 'Creature', 'Shadows over Innistrad', 'Mythic', true);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Loam Dryad', 'Green', 1, 'Creature', 'Shadows over Innistrad', 'Common', false);
INSERT INTO public."Cards" ("Name", "Color", "ManaValue", "Type", "Set", "Rarity", "isLegendary") VALUES ('Skyblade of the Legion', 'White', 2, 'Creature', 'Ixalan', 'Common', false);


--
-- TOC entry 3006 (class 0 OID 24715)
-- Dependencies: 200
-- Data for Name: Sets; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('New Phyrexia', 'NPH', '2011-05-07', 175, 'Scars of Mirrodin', 0);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Theros', 'THS', '2013-09-27', 249, 'Theros', 0);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Journey into Nyx', 'JOU', '2014-05-02', 165, 'Theros', 0);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Khans of Tarkir', 'KTK', '2014-09-26', 269, 'Khans of Tarkir', 0);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Fate Reforged', 'FRF', '2015-01-23', 185, 'Khans of Tarkir', 0);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Dragons of Tarkir', 'DTK', '2015-03-27', 264, 'Khans of Tarkir', 0);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Oath of the Gatewatch', 'OGW', '2016-01-22', 184, 'Battle for Zendikar', 0);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Eldritch Moon', 'EMN', '2016-07-22', 205, 'Shadows over Innistrad', 0);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Aether Revolt', 'AER', '2017-01-20', 165, 'Kaladesh', 0);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Shadows over Innistrad', 'SOI', '2016-04-08', 297, 'Shadows over Innistrad', 5);
INSERT INTO public."Sets" ("Name", "SetCode", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Ixalan', 'XLN', '2017-09-29', 279, 'Ixalan', 6);


--
-- TOC entry 2871 (class 2606 OID 24748)
-- Name: Cards Cards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Cards"
    ADD CONSTRAINT "Cards_pkey" PRIMARY KEY ("Name");


--
-- TOC entry 2867 (class 2606 OID 24740)
-- Name: Sets Sets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Sets"
    ADD CONSTRAINT "Sets_pkey" PRIMARY KEY ("Name");


--
-- TOC entry 2869 (class 2606 OID 24755)
-- Name: Sets UniqueSetCode; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Sets"
    ADD CONSTRAINT "UniqueSetCode" UNIQUE ("SetCode");


--
-- TOC entry 2872 (class 1259 OID 24778)
-- Name: cardsrarityindex; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX cardsrarityindex ON public."Cards" USING btree ("Rarity");


--
-- TOC entry 2874 (class 2620 OID 24777)
-- Name: Cards dec_cards_count; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER dec_cards_count AFTER DELETE ON public."Cards" FOR EACH ROW EXECUTE FUNCTION public.dec_cards_count();


--
-- TOC entry 2875 (class 2620 OID 24773)
-- Name: Cards inc_cards_count; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER inc_cards_count AFTER INSERT ON public."Cards" FOR EACH ROW EXECUTE FUNCTION public.inc_cards_count();


--
-- TOC entry 2873 (class 2606 OID 24749)
-- Name: Cards SetKey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Cards"
    ADD CONSTRAINT "SetKey" FOREIGN KEY ("Set") REFERENCES public."Sets"("Name") NOT VALID;


-- Completed on 2021-06-02 17:39:18

--
-- PostgreSQL database dump complete
--

