# T1 Diabetes SNP Search Tool
##  Software Development Project - Team Vivaldi

## Description
'T1 Diabetes SNP search' is a web browser tool we have created as part of our MSc Bioinformatics Software Development Group Project. 
Team members are Marta, Khadija, Thuvarahgan, Jiang and Tobi.

Type 1 diabetes (T1D) is a chronic autoimmune disorder in which the body’s immune system attacks and destroys pancreatic cells, specifically the β cells in the pancreas which produces insulin. The lack of insulin results in blood sugar levels not being regulated properly therefore blood glucose levels rise, which can cause further symptoms and serious complications over time. Type 1 diabetes usually develops in childhood or adolescence, but it can also occur in adulthood. While there is currently no cure for type 1 diabetes, it can be managed with insulin therapy and other treatments to help people with the condition live long and healthy lives.  

Genome wide association studies (GWAS) have been able to identify single nucleotide polymorphisms (SNPs) that are linked to type 1 diabetes. Databases such as SNPnexus can provide information about SNPs such as functional information, functional impact or clinical relevance. The aim of this project was to produce a functioning web-based software tool that allows users to search and explore genetic variants that have been associated with high susceptibility of Type 1 Diabetes. The tool also retrieves genomic information and integrates it with population data and functional information. We have called it ‘T1D SNP Search Tool.’  

The website allows users to search for genetic variants by single nucleotide polymorphism (SNP) name (rs ID), genomic position or gene name. For each query, the web page returns information on SNP name (rs ID), genomic position, p-value from association tests, mapped genes, allele frequency in three different human populations (British GBR, Nigerian ESN, Japanese JPT), one measure of functional impact and one functional term associated with each mapped gene. When users search the website for SNPs by genomic region range, the webpage returns a Manhattan plot of all the p-values returned from the search. The webpage has an option to select SNPs, calculate linkage disequilibrium (LD) of those SNPs, and return plots for those LD measures. We aim for this tool to be used to interpret the mapping of the genetic basis of T1D. 

## Environment Setup

1. Install [virtualenv](https://pypi.org/project/virtualenv/) in global Python:

```shell
pip install virtualenv
```

2. Create virtual environment:

```shell
python -m venv venv
```

3.1 Source the environment (on Mac):
```shell
source venv/bin/activate
```

3.1 Source the environment (on Windows):
```shell
venv\Scripts\activate
```

4. Install project dependencies:

```shell
pip install -r requirements.txt
```

5. Please freeze your environment if adding new packages:

```shell
pip freeze > requirements.txt
``` 

6. Run the main.py python script:
```shell
python main.py
```

[https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/]

## Usage
[Insert instructions for how to use your web browser, including any necessary input formats or parameters]
### Search by SNP name (rsID)

### Search by genomic region

### Search by genomic coordinates

### Search by mapped genes

## Technical Details
[Insert technical details about your web browser, including programming languages, frameworks, and databases used]
## Programming Language

## SQL Database
Made up of 4 tables: SNP, Gene, Gene_SNP and P_Value. SNP table contains id (text), CHR_N (integer), CHR_P (integer), REF_ALLELE (real), ALT_ALLELE (real), GBR_REF (real), GBR_ALT (real), JPT_REF (real), JPT_ALT (real), ESN_REF (real), ESN_ALT (real), CADD (real). Gene table contains id (text) and Function (text). Gene_SNP is a join table that joins Gene and SNP tables using their respective id. P_Value has Link (text), Date Published (integer), M_log (real), P_value (real) and RS_ID (text) which links to the SNP table's id column. 

## Data
The data we have used in our web browser was obtained from various sources. Below is a brief description of where to find the relevant data. For further information on how we used the data and how you can replicate this refer to the sofware documentation.

### Genome Wide Association Study Data (GWAS)
We obtained type 1 diabetes GWAS data from the NHGRI-EBI Catalog of human genome-wide association studies to investigate the genetic basis of T1D. The NHGRI-EBI Catalog is a database that includes information on published genome-wide association studies from various populations worldwide. The results of this search included information on the genetic variants, their frequencies, and effect sizes on the risk of type 1 diabetes from various populations. The type 1 diabetes GWAS data was obtained from https://www.ebi.ac.uk/gwas/efotraits/MONDO_0005147.

### SNP Measures of Functional Impact
As a measure of functional impact, we chose CADD scores for the SNPs. CADD scoring is a measure of deleteriousness of single nucleotide variants in the human genome. The CADD scores which highlight functional impact of the SNPS were obtained from SNPnexus https://www.snp-nexus.org/v4/.

### Gene Functional Terms
Gene functional terms are terms that describe the biological process, cellular component, or molecular function. A database that can be used to obtain gene and SNP functional data is SNPnexus, which integrates data from multiple sources, including the Reactome pathway database. The functional terms were obtained from SNPnexus connected to reactome data to link mapped genes to their biological pathways. https://www.snp-nexus.org/v4/.

### Population Data
The 1000 genomes project has successfully established detailed information regarding human genetic variation. This is possible as the individual haplotypes of many participants have been mapped to a reference human genome. The 1000 genomes project data is available at the international genome sample resource (IGSR) website. All population data we have obtained is from the international genome sample resource website (IGSR) https://www.internationalgenome.org.

### Haplotype Data for Linkage Disequilibrium Calculations
The haplotype data was also obtained from the IGSR website https://www.internationalgenome.org.

## License

## Contact
bt22061@qmul.ac.uk
@qmul.ac.uk
@qmul.ac.uk
@qmul.ac.uk
@qmul.ac.uk


