# T1 Diabetes SNP Search Tool
##  Software Development Project - Team Vivaldi

## Description
'T1 Diabetes SNP search' is a tool we have created as part of our MSc Bioinformatics Software Development Group Project. 
Team members are Marta, Khadija, Thuvarahgan, Jiang and Tobi. 

The aim of this project was to produce a functioning web-based software tool that allows users to search and explore genetic variants that have been associated with high susceptibility of Type 1 Diabetes. The tool also retrieves genomic information and integrates it with population data and functional information.





## Environment setup and Dependencies

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
## Databases

### Genome Wide Association Study Data (GWAS)
The type 1 diabetes GWAS data was obtained from https://www.ebi.ac.uk/gwas/efotraits/MONDO_0005147.

### SNP Measures of Functional Impact
The CADD scores which highlight functional impact of the SNPS were obtained from SNPnexus https://www.snp-nexus.org/v4/.

### Gene Functional Terms
The functional terms were obtained from SNPnexus connected to reactome data to link mapped genes to their biological pathways.

### Population Data
All population data we have obtained is from the international genome sample resource website (IGSR) https://www.internationalgenome.org.

### Haplotype Data for Linkage Disequilibrium Calculations
The haplotype data was also obtained from the IGSR website https://www.internationalgenome.org.

## License

## Contact



