# URL Shortner

## Technologies used :
- Django
- Django Rest Framework
- PostgresQL


## Steps to run :

1. Clone the code from github
   ~~~
   git clone https://github.com/xan678/assignment.git
   
   cd assignment
   ~~~

2. Create a virtual environment and add dependencies 
    ~~~
    python3 -m venv <env_name>

    pip install requirements.txt
    ~~~

3. Create a .env file and set up Postgres credentials
    ~~~
    POSTGRES_DB=mydatabase
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    ~~~


4. Spin up container
    ~~~
    docker-compose up
    ~~~