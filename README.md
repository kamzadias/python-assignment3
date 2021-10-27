# Flask web server
Flask web server, where user can to login a user from PostgreSQL database and check unique token.

## Installation

- Install libraries:

```shell
$ pip install Flask
$ pip install flask_sqlalchemy
$ pip install SQLAlchemy
$ pip install pyjwt
$ pip install jwt
```

- Create tables in your database:

```PostgreSQL
CREATE TABLE users(
  user_id SERIAL PRIMARY KEY,
  login VARCHAR(256),
  password VARCHAR(256),
  token TEXT
);
```
## Usage

- /login
```shell
@app.route('/login') - After successful login(if login and password matches with a record in users table), 
as response route return html text: token: <token value> and store that token in the users Table
```
- /protected 
```shell
@app.route('/protected') - This route receive as a parameter token value.
- This route return html text: <h1>Hello, token which is provided is correct </h1>, if as a parameter RIGHT token value is passed
- This route return html text: <h1>Hello, Could not verify the token </h1>, if as a parameter WRONG token value is passed
```
## Examples

Example of usage:
- Insert some values(login,password) to users table

- Go to the link
```shell
http://127.0.0.1:5000/
```
- Click to "login link" button and receive token
```shell
http://127.0.0.1:5000/login
```
- Paste token to form and check user
```shell
http://127.0.0.1:5000/protected?token=...
```
