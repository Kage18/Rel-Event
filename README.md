# SocialCircleEvents
All required packages are in the requirements.txt file

To install the packages,please do the following:(The below steps are for Ubuntu)

    Create a virtualenv by using the command: python3 -m virtualenv . If virtualenv is not present, install it by using the command, sudo pip3 install virtualenv
    Activate it by the command: source <path_to_environment>/bin/activate
    pip install -r requirements.txt

For Windows, use the equivalent windows commands

To run the project do the following:

1. Configure your MySQL database NAME, USER, PASSWORD inside eventManagement > settings.py

            DATABASES = {   
                'default': {
                    'ENGINE': 'django.db.backends.mysql',
                    'NAME': '---',
                    'USER': '---',
                    'PASSWORD': '----',
                    'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
                    'PORT': '3306',
                    }
                }

2. Activate the virtualenv and open the project directly in the terminal and write the following commands

        python manage.py makemigrations
        python manage.py migrate

3. Run the project by the command

        python manage.py runserver
