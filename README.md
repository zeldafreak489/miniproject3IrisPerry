### INF601 - Advanced Programming in Python
### Iris Perry
### Mini Project 3
 
 
# Video Game Inventory
 
A simple Flask app to manage a personal video game inventory. Users can register an account, log in, add/edit/delete items from their inventory, view item details, and change their password. The UI uses Bootstrapp and includes a confirmation modal for deletes.
 
## Description
 
A small web app built with Flask and SQLite. Each user has a separate inventory (inventory items are linked to users via a foreign key). Templates use a shared base with Bootstrap styles. The project follows the Flask application factory and blueprint pattern.
 
## Getting Started
 
### Dependencies
 
* Python 3.11+
* pip
* The Python packages listed in requirements.txt:

#### Install Python packages:

Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install Python packages:
```bash
pip install -r requirements.txt
```
 
### Installing
 
1. Ensure the repo is cloned.
2. If templates are moved, ensure auth and inventory templates live under:
    - app/templates/auth/
    - app/templates/inventory/
 
### Executing program
 
* First, you must initialize the data base:
```bash
flask init-db
```

* Next, start the dev server:
```bash
flask --app app run
```

* The server will automatically run at http://127.0.0.1:5000 on port 5000. Open this to view and use the application.

* Register a new user with a username and password. After registering, you will be automatically redirected to the Log In page. Log in to view your inventory and profile.
 
## Authors

Iris Perry
[GitHub](https://github.com/zeldafreak489)
 
## Version History
 
* 0.1
    * Initial Release
 
## Acknowledgments
 
* [Flask tutorial structure and patterns] (https://flask.palletsprojects.com/en/stable/tutorial/)
* [Bootstrap documentation] (https://getbootstrap.com/docs/5.3/getting-started/introduction/)