--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.17
-- Dumped by pg_dump version 11.2

-- Started on 2019-05-22 11:10:52

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 201 (class 1255 OID 16517)
-- Name: idf(text); Type: FUNCTION; Schema: public; Owner: doc_org
--

CREATE FUNCTION public.idf(query text) RETURNS numeric
    LANGUAGE plpgsql
    AS $_$
	DECLARE
		total numeric;
		keyword_total numeric;
		idf numeric;
	BEGIN
		SELECT count(*) into total FROM document;
		SELECT COUNT(DISTINCT ki.file_id) into keyword_total
			FROM keyword_instance ki
			LEFT JOIN keyword keys on ki.keyword_id = keys.keyword_id
			WHERE keys.keyword = $1;
		idf = log(total/keyword_total);
		RETURN idf;
	END;
$_$;


ALTER FUNCTION public.idf(query text) OWNER TO doc_org;

--
-- TOC entry 204 (class 1255 OID 16527)
-- Name: idf_from_id(integer); Type: FUNCTION; Schema: public; Owner: doc_org
--

CREATE FUNCTION public.idf_from_id(keyword_id integer) RETURNS numeric
    LANGUAGE plpgsql
    AS $_$
	DECLARE
		total numeric;
		keyword_total numeric;
		idf numeric;
	BEGIN
		SELECT count(*) into total FROM document;
		SELECT COUNT(DISTINCT ki.file_id) into keyword_total
			FROM keyword_instance ki
			WHERE ki.keyword_id = $1;
		idf = log(total/keyword_total);
		RETURN idf;
	END;
$_$;


ALTER FUNCTION public.idf_from_id(keyword_id integer) OWNER TO doc_org;

--
-- TOC entry 205 (class 1255 OID 17251)
-- Name: query(text); Type: FUNCTION; Schema: public; Owner: doc_org
--

CREATE FUNCTION public.query(query text) RETURNS TABLE(file_id integer, rating numeric)
    LANGUAGE plpgsql
    AS $$
	DECLARE
		query_words text[];
		num_words int;
		doc_ids int[];
		bsqrt numeric;
	BEGIN
		SELECT DISTINCT string_to_array(lower(query), ' ') into query_words;
		SELECT count(query_words) into num_words;

		DROP TABLE IF EXISTS query_tfidf;
		CREATE TEMP TABLE query_tfidf(keyword_id int, keyword text, idf numeric, tfidf numeric);
		INSERT INTO query_tfidf
			SELECT keys.keyword_id, keys.keyword, idf(keys.keyword),  1::numeric/num_words * idf(keys.keyword)
				FROM keyword keys
				WHERE keys.keyword = ANY(query_words);

		SELECT sqrt(sum(power(q.tfidf,2))) into bsqrt
			FROM query_tfidf q;
		RETURN QUERY SELECT doc.file_id,
				sum((ki.count::numeric/doc.num_words)*q.idf * q.tfidf)
				/
				(sqrt(sum(power((ki.count::numeric/doc.num_words)*q.idf,2)))
				*bsqrt) as rating
			FROM query_tfidf q
			LEFT JOIN keyword_instance ki ON q.keyword_id = ki.keyword_id
			LEFT JOIN document doc ON doc.file_id = ki.file_id
			GROUP BY doc.file_id
			ORDER BY rating desc;
	END;
$$;


ALTER FUNCTION public.query(query text) OWNER TO doc_org;

--
-- TOC entry 202 (class 1255 OID 16522)
-- Name: tf(text, integer); Type: FUNCTION; Schema: public; Owner: doc_org
--

CREATE FUNCTION public.tf(query text, doc_id integer) RETURNS numeric
    LANGUAGE plpgsql
    AS $_$
	DECLARE
		tf numeric;
	BEGIN
		SELECT ki.count::double precision / doc.num_words into tf
		FROM document doc
		LEFT JOIN keyword_instance ki on doc.file_id = ki.file_id
		LEFT JOIN keyword keys on ki.keyword_id = keys.keyword_id
		WHERE keys.keyword = $1 AND doc.file_id = $2;
		return tf;
	END;
$_$;


ALTER FUNCTION public.tf(query text, doc_id integer) OWNER TO doc_org;

--
-- TOC entry 203 (class 1255 OID 16526)
-- Name: tf_from_id(integer, integer); Type: FUNCTION; Schema: public; Owner: doc_org
--

CREATE FUNCTION public.tf_from_id(keyword_id integer, doc_id integer) RETURNS numeric
    LANGUAGE plpgsql
    AS $_$
	DECLARE
		tf numeric;
	BEGIN
		SELECT ki.count::double precision / doc.num_words into tf
		FROM document doc
		LEFT JOIN keyword_instance ki on doc.file_id = ki.file_id
		WHERE ki.keyword_id = $1 AND doc.file_id = $2;
		return tf;
	END;
$_$;


ALTER FUNCTION public.tf_from_id(keyword_id integer, doc_id integer) OWNER TO doc_org;

--
-- TOC entry 200 (class 1255 OID 16529)
-- Name: tf_idf(text, integer); Type: FUNCTION; Schema: public; Owner: doc_org
--

CREATE FUNCTION public.tf_idf(query text, file_id integer) RETURNS numeric
    LANGUAGE plpgsql
    AS $$
	DECLARE
		key_id int;
		tfidf numeric;
	BEGIN
		SELECT keys.keyword_id into key_id from keyword keys where keys.keyword = query;
		tfidf = tf_from_id(key_id, file_id)/idf_from_id(key_id);
		return tfidf;
	END;
$$;


ALTER FUNCTION public.tf_idf(query text, file_id integer) OWNER TO doc_org;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 181 (class 1259 OID 16416)
-- Name: document; Type: TABLE; Schema: public; Owner: doc_org
--

CREATE TABLE public.document (
    date_parse timestamp without time zone NOT NULL,
    date_create timestamp without time zone NOT NULL,
    date_edit timestamp without time zone NOT NULL,
    path text NOT NULL,
    file_id integer NOT NULL,
    hash text NOT NULL,
    file_size integer NOT NULL,
    num_words integer NOT NULL
);


ALTER TABLE public.document OWNER TO doc_org;

--
-- TOC entry 182 (class 1259 OID 16422)
-- Name: document_file_id_seq; Type: SEQUENCE; Schema: public; Owner: doc_org
--

CREATE SEQUENCE public.document_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.document_file_id_seq OWNER TO doc_org;

--
-- TOC entry 2183 (class 0 OID 0)
-- Dependencies: 182
-- Name: document_file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doc_org
--

ALTER SEQUENCE public.document_file_id_seq OWNED BY public.document.file_id;


--
-- TOC entry 183 (class 1259 OID 16424)
-- Name: keyword; Type: TABLE; Schema: public; Owner: doc_org
--

CREATE TABLE public.keyword (
    keyword text NOT NULL,
    keyword_id integer NOT NULL
);


ALTER TABLE public.keyword OWNER TO doc_org;

--
-- TOC entry 184 (class 1259 OID 16430)
-- Name: keyword_instance; Type: TABLE; Schema: public; Owner: doc_org
--

CREATE TABLE public.keyword_instance (
    keyword_id integer NOT NULL,
    file_id integer NOT NULL,
    count integer NOT NULL,
    tag boolean DEFAULT false NOT NULL
);


ALTER TABLE public.keyword_instance OWNER TO doc_org;

--
-- TOC entry 185 (class 1259 OID 16433)
-- Name: keyword_keyword_id_seq; Type: SEQUENCE; Schema: public; Owner: doc_org
--

CREATE SEQUENCE public.keyword_keyword_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.keyword_keyword_id_seq OWNER TO doc_org;

--
-- TOC entry 2184 (class 0 OID 0)
-- Dependencies: 185
-- Name: keyword_keyword_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: doc_org
--

ALTER SEQUENCE public.keyword_keyword_id_seq OWNED BY public.keyword.keyword_id;


--
-- TOC entry 187 (class 1259 OID 16523)
-- Name: tf; Type: TABLE; Schema: public; Owner: doc_org
--

CREATE TABLE public.tf (
    "?column?" integer
);


ALTER TABLE public.tf OWNER TO doc_org;

--
-- TOC entry 186 (class 1259 OID 16518)
-- Name: total; Type: TABLE; Schema: public; Owner: doc_org
--

CREATE TABLE public.total (
    count bigint
);


ALTER TABLE public.total OWNER TO doc_org;

--
-- TOC entry 2043 (class 2604 OID 16435)
-- Name: document file_id; Type: DEFAULT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.document ALTER COLUMN file_id SET DEFAULT nextval('public.document_file_id_seq'::regclass);


--
-- TOC entry 2044 (class 2604 OID 16436)
-- Name: keyword keyword_id; Type: DEFAULT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.keyword ALTER COLUMN keyword_id SET DEFAULT nextval('public.keyword_keyword_id_seq'::regclass);


--
-- TOC entry 2047 (class 2606 OID 16438)
-- Name: document document_pkey; Type: CONSTRAINT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT document_pkey PRIMARY KEY (path);


--
-- TOC entry 2049 (class 2606 OID 16440)
-- Name: document file_id; Type: CONSTRAINT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT file_id UNIQUE (file_id);


--
-- TOC entry 2053 (class 2606 OID 16442)
-- Name: keyword keyword_id; Type: CONSTRAINT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.keyword
    ADD CONSTRAINT keyword_id UNIQUE (keyword_id);


--
-- TOC entry 2060 (class 2606 OID 16444)
-- Name: keyword_instance keyword_instance_pkey; Type: CONSTRAINT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.keyword_instance
    ADD CONSTRAINT keyword_instance_pkey PRIMARY KEY (keyword_id, file_id);


--
-- TOC entry 2055 (class 2606 OID 16446)
-- Name: keyword keyword_pkey; Type: CONSTRAINT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.keyword
    ADD CONSTRAINT keyword_pkey PRIMARY KEY (keyword);


--
-- TOC entry 2057 (class 2606 OID 16448)
-- Name: keyword keyword_unique; Type: CONSTRAINT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.keyword
    ADD CONSTRAINT keyword_unique UNIQUE (keyword);


--
-- TOC entry 2051 (class 2606 OID 16450)
-- Name: document path; Type: CONSTRAINT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT path UNIQUE (path);


--
-- TOC entry 2058 (class 1259 OID 18444)
-- Name: is_tag; Type: INDEX; Schema: public; Owner: doc_org
--

CREATE INDEX is_tag ON public.keyword_instance USING btree (tag);


--
-- TOC entry 2062 (class 2606 OID 16466)
-- Name: keyword_instance file_id; Type: FK CONSTRAINT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.keyword_instance
    ADD CONSTRAINT file_id FOREIGN KEY (file_id) REFERENCES public.document(file_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2061 (class 2606 OID 16461)
-- Name: keyword_instance keyword_id; Type: FK CONSTRAINT; Schema: public; Owner: doc_org
--

ALTER TABLE ONLY public.keyword_instance
    ADD CONSTRAINT keyword_id FOREIGN KEY (keyword_id) REFERENCES public.keyword(keyword_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 2182 (class 0 OID 0)
-- Dependencies: 7
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2019-05-22 11:11:09

--
-- PostgreSQL database dump complete
--

