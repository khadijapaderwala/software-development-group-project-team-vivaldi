# Software development project

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

## Updating the requirements.txt file 

[https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/]