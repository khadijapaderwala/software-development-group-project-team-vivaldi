##  Software Development Project
##  Team Vivaldi

## Description

## Dependencies

## Environment setup

1. Install [virtualenv](https://pypi.org/project/virtualenv/) in global Python:

```shell
pip install virtualenv
```

2. Create virtual environment:

```shell
python -m venv venv
```

3. Source the environment:

```shell
source venv/bin/activate
```

4. Install project dependencies:

```shell
pip install -r requirements.txt
```

5. Please freeze your environment if adding new packages:

```shell
pip freeze > requirements.txt
```

## Contributing

1. Please add GitHub username and email to global git:

```shell
git config --global user.name <username>
git config --global user.email <email>
```

2. Clone repository:

```shell
git clone https://github.com/khadijapaderwala/team-vivaldi.git && cd team-vivaldi
```

Since we're using a private repo, we need to generate a personal access token ([PAT](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)) and use it to authenticate the clone, i.e., enter the PAT when prompted to enter your password.

3. Create a feature branch from main to start your work:

```shell
git checkout -b <feature>
```

## Data Wrangling
## GWAS data
## Population Data

All the population data that we used was obtained from the international genome sample resource (IGSR) available at: https://www.internationalgenome.org/data-portal/sample . The data collection was filtered to 1000 genomes on GRCh38 data. We have selected three populations to calculate the population allele frequencies and linkage disequilibriums (LD) however, you can choose any suitable populations and however many populations based off your preferences. The three populations we have selected are: 
- British in England and Scotland (GBR)
- Esan in Nigeria (ESN) 
- Japanese in Tokyo, Japan (JPT) 
