## How to setup the database locally

### Open mySQL

`sudo mysql -u root -p`

### Create the database

I run the schema file on workbench but theres a bunch of ways to do this

Schema can be found at: `database/schema.sql` 

### Update DB Credentials in Python 

Add your root user credentials to the db_config struct in app.py

We should definitely change this lol

### Load Mock data

Load the mock data into the database

Mock Data can be found at: `database/mockdata.sql`
