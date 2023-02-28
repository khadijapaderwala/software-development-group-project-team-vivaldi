CREATE TABLE IF NOT EXISTS SNP (
	id text PRIMARY KEY,
    CHR_N integer,
    CHR_P integer,
	REF_ALLELE text,
	ALT_ALLELE text,
    GBR_REF_FREQ real,
    GBR_ALT_FREQ real,
    JPT_REF_FREQ real,
    JPT_ALT_FREQ real,
    ESN_REF_FREQ real,
    ESN_ALT_FREQ real,
	CADD real,
    UNIQUE(id)
);

CREATE TABLE IF NOT EXISTS P_Value (
	RS_ID text,
    DATE_PUBLISHED integer,
	LINK text,
	P_VALUE real,
    M_LOG real
);

CREATE TABLE IF NOT EXISTS Gene (
	id text PRIMARY KEY,
	FUNCTIONAL text
);

CREATE TABLE IF NOT EXISTS Gene_SNP (
	GENE_ID text,
	SNP_ID text,
    FOREIGN KEY (GENE_ID) REFERENCES Gene(id),
    FOREIGN KEY (SNP_ID) REFERENCES SNP(id)
);