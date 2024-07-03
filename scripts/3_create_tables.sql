CREATE TABLE IF NOT EXISTS holders.holders
(
    holder_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    name character varying(255) COLLATE pg_catalog."default",
    document character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT holders_pkey PRIMARY KEY (holder_id)
);

CREATE TABLE IF NOT EXISTS accounts.accounts
(
    account_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    holder_id integer,
    balance numeric,
    status integer,
    CONSTRAINT accounts_pkey PRIMARY KEY (account_id),
    CONSTRAINT accounts_holder_id_fkey FOREIGN KEY (holder_id)
        REFERENCES holders.holders (holder_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS accounts.transactions
(
    transaction_id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    transaction_type character varying(255) COLLATE pg_catalog."default",
    transaction_value numeric,
    transaction_date timestamp without time zone,
    origin_account integer,
    destination_account integer,
    CONSTRAINT transactions_pkey PRIMARY KEY (transaction_id)
);