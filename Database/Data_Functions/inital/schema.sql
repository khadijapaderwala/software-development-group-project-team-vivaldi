CREATE TABLE IF NOT EXISTS SNP (
	SNP_ID text,
	Context_ID integer,
	Intergenic integer,
	P_value real,
	CADD real,
	PUBMEDID integer
);

CREATE TABLE IF NOT EXISTS Population (
	Sample_Size integer,
	Sample_Type text,
	Variant_ Frequency real
);

CREATE TABLE IF NOT EXISTS SNP_Gene (
	Gene_ID text,
	SNP_ID integer
);

CREATE TABLE IF NOT EXISTS Study (
	PUBMEDID integer,
	link text
);

CREATE TABLE IF NOT EXISTS Context (
	Context_ID text,
	Context text
);

CREATE TABLE IF NOT EXISTS Gene (
	Gene_ID text,
	functional term text,
	ontology term text
);

CREATE TABLE IF NOT EXISTS Region (
	Region text,
	SNP_ID integer,
	CHR_ID integer,
	CHR_pos integer
);

CREATE TABLE IF NOT EXISTS SNP_Population (
	SNP_ID integer,
	Sample_Type text
);

