# home-conn

small web tool to allow multiple users to access spotify controls of one user.

### Setup:

* frontend:
  * needs node (tested with v12.14.1) & npm (tested with 6.13.4)
  * run `npm install` in `frontend` folder
* backend:
  * set PYTHONPATH to the main project folder (NOT the server folder)
  * create config as seen in the `config-template.ini` as `server/config.ini`
  * install dependencies using `pipenv install`

#### DEV
* prod_mode = false in `server/config.ini`
* `pipenv run python main.py`

#### PROD (plain)
* run `npm run build-prod` in `frontend` folder, creating `dist`
* setup ssl as seen in the `config-template.ini`
* prod_mode = true in `server/config.ini`
* `pipenv run python main.py`

#### PROD (using apache2 as proxy)
* disable ssl settings in `server/config.ini` (apache2 will handle ssl)
* needs modules: `proxy_http` and `proxy_wstunnel`
* add site config as seen in `apache2_vhost.conf`
* `pipenv run python main.py`
* for proper security, close the port the server is running on to the public...
