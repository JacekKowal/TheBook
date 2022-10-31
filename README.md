# Social Network site using Django framework

## Screenshots

| Log In | Sign up | Main page |
| -------|--------------|-----------------|
| <img src="./screenshots/log_in.png" width="200"> | <img src="./screenshots/sign_up.png" width="200"> | <img src="./screenshots/main_page.png" width="200"> |

| Other user profile | Logged in user profile| Simple messages |
| ---------------|------------------|-----------------|
| <img src="./screenshots/other_user_profile.png" width="200"> | <img src="./screenshots/logged_in_user_profile.png" width="200"> | <img src="./screenshots/simple_messages.png" width="200"> |

## Functionality

- Posts: Add, update, delete
- CustomUser(AbstractUser): Add, update, delete
- Log in, log out
- Posts likes, comments
- Follow users(contents of the main page filtered on that basis)
- Pagination
- Simple messages
- Tests for every view(pytest-django)

## Installing

### Clone the project

```
git clone https://github.com/JacekKowal/TheBook.git
```

### Install dependencies & activate virtualenv

```
pip install pipenv

pipenv install
pipenv shell
```

### Configure the settings (connection to the databasee)

1. Edit `TheBook/settings.py` for database settings.

### Apply migrations

```
python TheBook/manage.py migrate
```

### Running a development server

```
python TheBook/manage.py runserver
```
