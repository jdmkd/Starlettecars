###### Getting Started

## Open the project in VS Code Editor or your fevorite editor.

###### This is for python and Django setup ###########

## 1. python3 and pip should be installed in your system.

## 2. if you don't have the virtualenv installed in your system then run this command in you terminal:
	-> pip install virtualenv


## 3. if you already have the virtualenv installed in your system :
    - then you have to run this command to create a virtual env at your projects root location where the manage.py file must be visible.
    -> virtualenv venv

    - you can see the .venv folder created at your manage.py file level directory.

## 4. Activate the virtual environment run the command (this only work for Windows OS):
    -> venv/Scripts/activate

    - after that the virtual environment have been activated successfully
    - you also see the (.venv) at the starting of the terminals directory

    - now you have to install all the dependencies or libraries that required for this project to run at localhost.
    -> pip install -r requirements.txt

    - now have installe all the dependencies successfully that is written in the requirements.txt

## 5. Setup the the Database:
    - We are going to use Postgresql DB (Step-1) but if you want to use the SqliteDB that is default comes with django then and dont want to setup install the postgresBD than follows the (Step-2) and Skip the (Step-1) =>
        
        

        - (Step - 1). **Skip this step if you don't gona use the Postgresql_DB than go to the step-2
        Create a .env file at the manage.py directory level and copy these configrations and past into your .env file and make some changes where needed.

            # Database related configrations
                DATABASE_ENGINE=django.db.backends.postgresql
                DATABASE_NAME=Your_Postgres_DB_Name    //change this with your's
                DATABASE_USER=Your_Postgres_DB_User    //change this with your's
                DATABASE_PASSWORD=Your_Postgres_DB_Password    //change this with your's
                DATABASE_HOST=localhost
                DATABASE_PORT=5432
            ########

            # email configrations
                EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
                EMAIL_HOST=smtp.gmail.com
                EMAIL_USE_TLS=True
                EMAIL_PORT=587
                EMAIL_HOST_USER=EMAIL_HOST_USER_EMAIL               //change this with your's
                EMAIL_HOST_PASSWORD=EMAIL_HOST_USER_PASSWORD        //change this with your's
            ########

            -** you don't have to make changes for the DATABASE dict inside the settings.py file.
            


        - (Step-2) ***If you want to use the default SqliteDB that you have to uncomment the first section of code for sqlite3 and than comment all the others inside the DATABASES dict into the settings.py
            DATABASES = {
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": BASE_DIR / "db.sqlite3",
                },
            }
## 6. Till now you setup the Database successfull!


## 7. follow these migration commands to apply database migrations:
    1. Create Initial Migrations:

        -> python manage.py makemigrations

        - This generates migration files for any models defined in your app.

    2. Apply Migrations to the Database:

        -> python manage.py migrate

        - This applies all migrations to set up the database schema.

    3. Create a Superuser:
        - using Django's built-in authentication system:

            -> python manage.py createsuperuser

    4. Run the Development Server:
        -> python manage.py runserver

        - This starts the Django server, and your project is now ready.


    
###### This is for Tailwind setup  #############
- Open a seprate terminal that defferent from the activated virtual env (.env) must be a seprate terminal in you vs code.
- First you have to initialize the node setup for tailwind css that we are going to user inside the project.
    -> npm init -y

- after initializing node setup you have to install the tailwindcss 
    -> npm install -D tailwindcss
    -> npx tailwindcss init

- run the Deployment server and the development server:
    -> npm run tailwind-build
    -> npm run tailwind-watch

- find and go inside the /tailwindrun folder
    -> cd tailwindrun
    -> npm run dev

- after running the 'npm run dev' nodejs backend serves that tailwind-output.css file
- we access this tailwind css file into our templates for styling the html codes
- you have to write this line to the <head> tag in you html file. 
<!-- <link href="{% static 'css/tailwind-output.css' %}" rel="stylesheet" /> -->



#### Now I thing all done.

#### Thank you!!! ##########


