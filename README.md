# Information systems application

**GoyoBurger** is a web application where users can customize their burgers by choosing up to 4 toppings from a variety of options. Users can register, log in, place orders and view their order history.

## Index
- [Requeriments](#Requirements)
- [Installation](#Installation)
- [Screenshots](#Screenshots)
- [Creators](#Creators)  

## Requirements

- [python or python3](https://www.python.org/)
- pip
- [MailHog](https://github.com/mailhog/MailHog)

## Screenshots

![image](https://github.com/user-attachments/assets/046c70e6-054e-4ef5-a9ae-f0b6ac7332bc)

![image](https://github.com/user-attachments/assets/9b983e68-f7fa-4c7f-afb4-f999abcce50b)

![image](https://github.com/user-attachments/assets/6a1fd725-89d5-4232-91ca-ae24b129669a)


## Installation

### linux/Mac OS
Create a folder called for example, `GoyoBurger`.
Once inside this folder open the terminal and write the command
```bash
$ git clone https://github.com/NeoManD10/GoBurger.git
$ cd GoBurger
```
Create a virtual environment using the command
```bash
$ python3 -m venv "name_environment"
```
Activate the virtual environment using the command
```bash
$ source name_environment/bin/activate
```
Install the requirements using the command
```bash
$ pip install -r requirements.txt
```
Finally, run the application with
 ```bash
$ python3 manage.py runserver
```

### Windows
   Create a folder where you want to clone the repository, for example, `GoyoBurger`. Then, open the command terminal (CMD or PowerShell) and run
```bash
$ git clone https://github.com/NeoManD10/GoBurger.git
$ cd GoBurger
```
Create a virtual environment using the command
```bash
$ python3 -m venv "name_environment"
```
Activate the virtual environment using the command
```bash
$ name_environment\Scripts\activate
```
Once the environment is activated, install the project requirements by running
```bash
$ pip install -r requirements.txt
```
To start the application, use
```bash
$ python3 manage.py runserver
```

## Notes

Remember to have MailHog running as it's currently used for mail usage.

## Creators

- [Vicente Tapia](https://github.com/Mistakensito)
- [Manuel Dios](https://github.com/NeoManD10)
- [Ignacio Ahumada](https://github.com/xedohcan)
