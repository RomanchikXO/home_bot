--
-- PostgreSQL database dump
--

-- Dumped from database version 14.12 (Homebrew)
-- Dumped by pg_dump version 14.13 (Homebrew)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: romandikarev
--

CREATE TABLE IF NOT EXISTS public.accounts (
    id integer NOT NULL,
    created_at integer DEFAULT (EXTRACT(epoch FROM now()))::integer,
    password character varying(512),
    permissions text,
    tg_id bigint,
    budget_id integer,
    states character varying(128)
);


ALTER TABLE public.accounts OWNER TO romandikarev;

--
-- Name: COLUMN accounts.budget_id; Type: COMMENT; Schema: public; Owner: romandikarev
--

COMMENT ON COLUMN public.accounts.budget_id IS 'id в таблице с бюджетами';


--
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: romandikarev
--

CREATE SEQUENCE public.accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.accounts_id_seq OWNER TO romandikarev;

--
-- Name: accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: romandikarev
--

ALTER SEQUENCE public.accounts_id_seq OWNED BY public.accounts.id;


--
-- Name: budgets; Type: TABLE; Schema: public; Owner: romandikarev
--

CREATE TABLE IF NOT EXISTS public.budgets (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    pass character varying(128)
);


ALTER TABLE public.budgets OWNER TO romandikarev;

--
-- Name: budgets_id_seq; Type: SEQUENCE; Schema: public; Owner: romandikarev
--

CREATE SEQUENCE public.budgets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.budgets_id_seq OWNER TO romandikarev;

--
-- Name: budgets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: romandikarev
--

ALTER SEQUENCE public.budgets_id_seq OWNED BY public.budgets.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: romandikarev
--

CREATE TABLE IF NOT EXISTS public.categories (
    id integer NOT NULL,
    id_budget integer NOT NULL,
    category character varying(512) NOT NULL,
    type character varying(255)
);


ALTER TABLE public.categories OWNER TO romandikarev;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: romandikarev
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO romandikarev;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: romandikarev
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: money_move; Type: TABLE; Schema: public; Owner: romandikarev
--

CREATE TABLE IF NOT EXISTS public.money_move (
    category character varying(255),
    income double precision DEFAULT 0,
    expenditure double precision DEFAULT 0,
    id_user integer,
    id_budgets integer,
    date_add integer DEFAULT (EXTRACT(epoch FROM now()))::integer,
    id integer NOT NULL
);


ALTER TABLE public.money_move OWNER TO romandikarev;

--
-- Name: money_move_id_seq; Type: SEQUENCE; Schema: public; Owner: romandikarev
--

CREATE SEQUENCE public.money_move_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.money_move_id_seq OWNER TO romandikarev;

--
-- Name: money_move_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: romandikarev
--

ALTER SEQUENCE public.money_move_id_seq OWNED BY public.money_move.id;


--
-- Name: task; Type: TABLE; Schema: public; Owner: romandikarev
--

CREATE TABLE IF NOT EXISTS public.task (
    id integer NOT NULL,
    id_user integer NOT NULL,
    task character varying(512) NOT NULL,
    date_add integer DEFAULT (EXTRACT(epoch FROM now()))::integer,
    status character varying(20) NOT NULL,
    plane_date bigint
);


ALTER TABLE public.task OWNER TO romandikarev;

--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: romandikarev
--

CREATE SEQUENCE public.task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_id_seq OWNER TO romandikarev;

--
-- Name: task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: romandikarev
--

ALTER SEQUENCE public.task_id_seq OWNED BY public.task.id;


--
-- Name: accounts id; Type: DEFAULT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.accounts ALTER COLUMN id SET DEFAULT nextval('public.accounts_id_seq'::regclass);


--
-- Name: budgets id; Type: DEFAULT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.budgets ALTER COLUMN id SET DEFAULT nextval('public.budgets_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: money_move id; Type: DEFAULT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.money_move ALTER COLUMN id SET DEFAULT nextval('public.money_move_id_seq'::regclass);


--
-- Name: task id; Type: DEFAULT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.task ALTER COLUMN id SET DEFAULT nextval('public.task_id_seq'::regclass);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: budgets budgets_pkey; Type: CONSTRAINT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.budgets
    ADD CONSTRAINT budgets_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: money_move money_move_pkey; Type: CONSTRAINT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.money_move
    ADD CONSTRAINT money_move_pkey PRIMARY KEY (id);


--
-- Name: task task_pkey; Type: CONSTRAINT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

--
-- Name: piggy; Type: TABLE; Schema: public; Owner: romandikarev
--

CREATE TABLE IF NOT EXISTS public.piggy (
    id SERIAL PRIMARY KEY,
    money INT,
    budget_id INT,
    time_add BIGINT DEFAULT EXTRACT(EPOCH FROM NOW()),
    status VARCHAR(255)
);

ALTER TABLE public.piggy OWNER TO romandikarev;

--
-- Name: piggy id; Type: DEFAULT; Schema: public; Owner: romandikarev
--

ALTER TABLE ONLY public.piggy ALTER COLUMN id SET DEFAULT nextval('public.piggy_id_seq'::regclass);

--
-- Name: piggy_id_seq; Type: SEQUENCE; Schema: public; Owner: romandikarev
--

CREATE SEQUENCE public.piggy_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.piggy_id_seq OWNER TO romandikarev;

--
-- Name: piggy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: romandikarev
--

ALTER SEQUENCE public.piggy_id_seq OWNED BY public.piggy.id;

--
-- Изменение типа поля money на FLOAT в таблице piggy
--

ALTER TABLE public.piggy
ALTER COLUMN money TYPE FLOAT USING money::FLOAT;
