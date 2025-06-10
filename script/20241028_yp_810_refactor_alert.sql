-- This script only contains the table creation statements and does not fully represent the table in the database. Do not use it as a backup.

-- Sequence and defined type
CREATE SEQUENCE IF NOT EXISTS ai_token_log_id_seq ;

-- Table Definition
CREATE TABLE "public"."ai_token_log" (
"id" int4 NOT NULL DEFAULT nextval('ai_token_log_id_seq'::regclass),
"token_in" int4,
"token_out" int4,
"created_at" timestamp,
"ref" text,
"ref_id" text,
"action" text,
"meta" json,
"provider" text,
PRIMARY KEY ("id")
)                                                                    ;
