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


CREATE DATABASE mtgS WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Russia.1251' LC_CTYPE = 'Russian_Russia.1251';
ALTER DATABASE mtg OWNER TO "Pasha";


CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';
CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA public;
COMMENT ON EXTENSION dblink IS 'connect to other PostgreSQL databases from within a database';


CREATE FUNCTION public.all_databases() RETURNS SETOF name
    LANGUAGE sql
    AS $$SELECT datname FROM pg_database where datallowconn = true and datname not in ('postgres', 'template0', 'template1');$$;
ALTER FUNCTION public.all_databases() OWNER TO "Pasha";

CREATE FUNCTION public.all_tables(dbname text, my_passwd text, host text DEFAULT '127.0.0.1'::text, port text DEFAULT '5432'::text) RETURNS SETOF text
    LANGUAGE plpgsql
    AS $$BEGIN
   -- выполняем SQL запрос на создание БД. оператор || - конкатенация
   -- current_database() - возврашает название БД в которой сейчас выполняется транзакция
   -- принцип работы dblink_exec: подключается к указанной бд(в примере - текущая), и выполняет запрос, 
   -- переданный вторым аргументом.
   -- для доп.информации можно добавить hostaddr=127.0.0.1 port=5432 dbname=mydb user=postgres password=mypasswd
   return query SELECT * FROM dblink('hostaddr=' || host || ' port=' || port || ' dbname=' || dbname || ' user=' || current_user || ' password=' || my_passwd  -- current db
                     , 'SELECT ' || quote_ident('table_name') || ' FROM ' || 'information_schema.' || quote_ident('tables') || ' WHERE table_schema = ' || quote_literal('public')) alias(col text);
END
$$;
ALTER FUNCTION public.all_tables(dbname text, my_passwd text, host text, port text) OWNER TO "Pasha";

CREATE FUNCTION public.create_database(dbname text, my_passwd text, templ text DEFAULT 'template0'::text, encode text DEFAULT 'UTF8'::text, is_templ boolean DEFAULT false, host text DEFAULT '127.0.0.1'::text, port text DEFAULT '5432'::text) RETURNS integer
    LANGUAGE plpgsql
    AS $$BEGIN
-- проверка на существование БД с таким же именем
IF EXISTS (SELECT 1 FROM pg_database WHERE datname = dbname) THEN
   -- Возвращаем сообщение (не ошибку)
   RAISE NOTICE 'Database already exists'; 
   RETURN 1;
ELSE
   -- выполняем SQL запрос на создание БД. оператор || - конкатенация
   -- current_database() - возврашает название БД в которой сейчас выполняется транзакция
   -- принцип работы dblink_exec: подключается к указанной бд(в примере - текущая), и выполняет запрос, 
   -- переданный вторым аргументом.
   -- для доп.информации можно добавить hostaddr=127.0.0.1 port=5432 dbname=mydb user=postgres password=mypasswd
   PERFORM dblink_exec('hostaddr=' || host || ' port=' || port || ' dbname=' || current_database() || ' user=' || current_user || ' password=' || my_passwd  -- current db
                     , 'CREATE DATABASE ' || quote_ident(dbname)) || ' OWNER ' || current_user || ' TEMPLATE ' || templ || ' IS_TEMPLATE ' || is_templ;
   RETURN 0;
END IF;
END
$$;
ALTER FUNCTION public.create_database(dbname text, my_passwd text, templ text, encode text, is_templ boolean, host text, port text) OWNER TO "Pasha";

CREATE FUNCTION public.create_table(tablename text, column_names integer[], column_types text[]) RETURNS integer
    LANGUAGE plpgsql
    AS $_$
DECLARE 
	zz int;
	s text;
BEGIN
FOREACH zz, s IN ARRAY $2, $3 
LOOP
RAISE NOTICE 'row = %', zz;
--CREATE TABLE IF NOT EXISTS tablename(
--ARRAY(FOR i in array_length(schedule, 1) LOOP
--column_names[i], column_types[i]
END LOOP;
RETURN 0;
END
$_$;
ALTER FUNCTION public.create_table(tablename text, column_names integer[], column_types text[]) OWNER TO "Pasha";

CREATE FUNCTION public.dec_cards_count() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN
UPDATE "Sets" SET "CountCards" = "CountCards" - 1 where OLD."Set" = "Sets"."Name";
RETURN NEW;
END;
$$;
ALTER FUNCTION public.dec_cards_count() OWNER TO Pasha;

CREATE FUNCTION public.drop_database(dbname text, my_passwd text, host text DEFAULT '127.0.0.1'::text, port text DEFAULT '5432'::text) RETURNS integer
    LANGUAGE plpgsql
    AS $$BEGIN
   -- выполняем SQL запрос на создание БД. оператор || - конкатенация
   -- current_database() - возврашает название БД в которой сейчас выполняется транзакция
   -- принцип работы dblink_exec: подключается к указанной бд(в примере - текущая), и выполняет запрос, 
   -- переданный вторым аргументом.
   -- для доп.информации можно добавить hostaddr=127.0.0.1 port=5432 dbname=mydb user=postgres password=mypasswd
   PERFORM dblink_exec('hostaddr=' || host || ' port=' || port || ' dbname=' || current_database() || ' user=' || current_user || ' password=' || my_passwd  -- current db
                     , 'DROP DATABASE ' || quote_ident(dbname));
   RETURN 0;
END
$$;
ALTER FUNCTION public.drop_database(dbname text, my_passwd text, host text, port text) OWNER TO "Pasha";


CREATE FUNCTION public.inc_cards_count() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN
UPDATE "Sets" SET "CountCards" = "CountCards" + 1 where NEW."Set" = "Sets"."Name";
RETURN NEW;
END;
$$;
ALTER FUNCTION public.inc_cards_count() OWNER TO Pasha;

CREATE FUNCTION public.insertrowincards(nname text, ncolor character varying, nmanavalue smallint, ntype character varying, nset text, nrarity character varying, nislegendary boolean) RETURNS void
    LANGUAGE sql
    AS $$
INSERT INTO "Cards" ("Name","Color","ManaValue","Type","Set","Rarity","isLegendary")
VALUES(nName,nColor,nManaValue,nType,nSet,nRarity,nisLegendary)
$$;
ALTER FUNCTION public.insertrowincards(nname text, ncolor character varying, nmanavalue smallint, ntype character varying, nset text, nrarity character varying, nislegendary boolean) OWNER TO "Pasha";

SET default_tablespace = '';
SET default_with_oids = false;

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
ALTER TABLE public."Cards" OWNER TO "Pasha";


CREATE FUNCTION public.print_cards() RETURNS SETOF public."Cards"
    LANGUAGE sql
    AS $$SELECT * FROM "Cards";$$;
ALTER FUNCTION public.print_cards() OWNER TO "Pasha";

CREATE TABLE public."Sets" (
    "Name" text NOT NULL,
    "ReleaseDate" date NOT NULL,
    "Size" smallint NOT NULL,
    "Block" text NOT NULL,
    "CountCards" smallint DEFAULT 0,
    CONSTRAINT "Sets_Size_check" CHECK (("Size" > 0))
);
ALTER TABLE public."Sets" OWNER TO "Pasha";


CREATE FUNCTION public.print_sets() RETURNS SETOF public."Sets"
    LANGUAGE sql
    AS $$SELECT * FROM "Sets";$$;
ALTER FUNCTION public.print_sets() OWNER TO "Pasha";

CREATE FUNCTION public.smart_print(tablename text) RETURNS SETOF record
    LANGUAGE sql
    AS $$SELECT * FROM quote_ident(tablename);$$;
ALTER FUNCTION public.smart_print(tablename text) OWNER TO "Pasha";

CREATE FUNCTION public.clearalltables() RETURNS void
    LANGUAGE sql
    AS $$ TRUNCATE "Cards" CASCADE;
	TRUNCATE "Sets" CASCADE
$$;
ALTER FUNCTION public.clearalltables() OWNER TO Grisha;

CREATE FUNCTION public.clearcards() RETURNS void
    LANGUAGE sql
    AS $$
DELETE FROM "Cards"
WHERE True;
$$;
ALTER FUNCTION public.clearcards() OWNER TO Grisha;

CREATE FUNCTION public.clearsets() RETURNS void
    LANGUAGE sql
    AS $$ DELETE FROM "Sets"
WHERE True;
$$;
ALTER FUNCTION public.clearsets() OWNER TO Grisha;

CREATE FUNCTION public.get_card(input_name text) RETURNS SETOF public."Cards"
    LANGUAGE sql
    AS $$
SELECT * FROM "Cards"
WHERE "Name" = input_name;
$$;
ALTER FUNCTION public.get_card(input_name text) OWNER TO Grisha;


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

INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('New Phyrexia', '2011-05-07', 175, 'Scars of Mirrodin', 0);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Journey into Nyx', '2014-05-02', 165, 'Theros', 0);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Khans of Tarkir', '2014-09-26', 269, 'Khans of Tarkir', 0);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Fate Reforged', '2015-01-23', 185, 'Khans of Tarkir', 0);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Dragons of Tarkir', '2015-03-27', 264, 'Khans of Tarkir', 0);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Oath of the Gatewatch', '2016-01-22', 184, 'Battle for Zendikar', 0);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Eldritch Moon', '2016-07-22', 205, 'Shadows over Innistrad', 0);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Aether Revolt', '2017-01-20', 165, 'Kaladesh', 0);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Shadows over Innistrad', '2016-04-08', 297, 'Shadows over Innistrad', 5);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Theros', '2013-09-27', 249, 'Theros', 0);
INSERT INTO public."Sets" ("Name", "ReleaseDate", "Size", "Block", "CountCards") VALUES ('Ixalan', '2017-09-29', 279, 'Ixalan', 14);


ALTER TABLE ONLY public."Cards"
    ADD CONSTRAINT "Cards_pkey" PRIMARY KEY ("Name");
ALTER TABLE ONLY public."Sets"
    ADD CONSTRAINT "Sets_pkey" PRIMARY KEY ("Name");

CREATE INDEX cardsrarityindex ON public."Cards" USING btree ("Rarity");

CREATE TRIGGER dec_cards_count AFTER DELETE ON public."Cards" FOR EACH ROW EXECUTE PROCEDURE public.dec_cards_count();
CREATE TRIGGER inc_cards_count AFTER INSERT ON public."Cards" FOR EACH ROW EXECUTE PROCEDURE public.inc_cards_count();

ALTER TABLE ONLY public."Cards"
    ADD CONSTRAINT "SetKey" FOREIGN KEY ("Set") REFERENCES public."Sets"("Name") NOT VALID;
