# Information systems application

**GoyoBurger** is a web application where users can customize their burgers by choosing up to 4 toppings from a variety of options. Users can register, log in, place orders and view their order history.

## Index
- [Requeriments](#Requirements)
- [Installation](#Installation)
- [Screenshots](#Screenshots)
- [Creators](#Creators)  

## Requirements

- [python or python3](https://www.python.org/)
- [MailHog](https://github.com/mailhog/MailHog)
- pip

## Screenshots

![image](https://github.com/user-attachments/assets/046c70e6-054e-4ef5-a9ae-f0b6ac7332bc)

## Installation

### linux/Mac OS
Create a folder called for example: test 
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
## Notes
This webpage currently uses MailHog for recieving emails when updating a forgotten password.

## Creators

- [Vicente Tapia](https://github.com/Mistakensito)
- [Manuel Dios](https://github.com/NeoManD10)
- [Ignacio Ahumada](https://github.com/xedohcan)
