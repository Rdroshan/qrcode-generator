
## QR CODE FILES GENERATOR

### Overview

Strictly adhere to the following versions of the stack:

- Python 3.6	
- Django 2.2

---


### Setup your development environment

Below instructions are tailored for the MacOs. Update the **Homebrew** before setting up your environment.


#### Python 3.6

- If you have a different version of python running, unhook it:

    `brew unlink python`

- Install Python 3.6 using the following brew formula:

    `
    brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
    `

- Switch to the installed version:

    `brew switch python 3.6.5_1`

- Install pip:

    `sudo easy_install pip`


#### Django 2.2

- Install *virtualenv* using pip3:

    `pip3 install virtualenv`

- Test if the setup works:

   `virtualenv --version`

- Create a virtualenv using the following cmd:

  `python3 -m venv venv`

- Activate the virtualenv:

    `source venv/bin/activate`

    #### Setting up the project

    - After cloning the project, move into the project dir:

        `cd qrcode-generator`

    - Install the specified *django* version and other packages through the requirements.txt:

        `pip install -r requirements.txt`

    - Use *sudo* incase you bump into the permission issue during *pip install*.

    - Run the migration:

        `python manage.py migrate`

    - Start the development server using

        `python manage.py runserver`

