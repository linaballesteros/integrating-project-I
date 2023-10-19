<h1 align="center">
    <tt>> SeekU: Lost Objects </tt> :mag_right:
</h1>

![image](https://github.com/linaballesteros/integrating-project-I/assets/140737132/88b9b215-cdd4-470c-96d6-70e24161da83)

Is a service for EAFIT users who have lost their objects in campus. It is called Seeku and it is a web page that will allow users to find their objects and reclaim them from a device connected to the internet. Unlike looking for the object in person at the lost objects place, our service saves time and effort for users to find their lost objects since they can use the web page to find out if their object was found.

Project for the fourth-semester course "Integrating Project I" (ST0251) taught at EAFIT University by prof Paola Vallejo.

## Motivation

Lost and found objects represent a significant issue in universities due to the dynamic and bustling nature of these institutions. With a large and diverse population of students, faculty, staff, and visitors constantly moving within the campus, the likelihood of misplacing or forgetting personal belongings increases substantially. The fast-paced academic environment, coupled with the myriad of activities and events taking place daily, makes it easy for individuals to unintentionally leave behind items in various locations, such as classrooms, libraries, cafeterias, or communal areas.

Given the significant volume of lost and found items, universities must allocate valuable resources to address this issue effectively. Staff members responsible for managing lost and found departments may find themselves overwhelmed by the sheer quantity of items, leading to potential errors and mishandling of possessions, making it even more challenging to reunite them with their owners.

The team proposes the creation of a platform where articles can be searched more easily and comfortably, for example, with a keyword, and in the same way to be able to make claim requests for these articles. In order to have a broader perspective of the impact that this application could have, a brief survey was carried out on students from the EAFIT university, where more than half of the people surveyed stated that they had lost an item at least once and where they also considered approximately 77% said that the implementation of a web page to search for lost objects was convenient, adding to this that 89% justified the idea of the project since they agreed that time could be saved by searching for a lost article from an electronic device.

## Install

Follow these instructions to run the program:

1. Clone the project on your machine.

    ```bash
    git clone git@github.com:linaballesteros/integrating-project-I.git
    ```
2. Go to the project directory (or wherever you stored it).

    ```bash
    cd seekuproject/seeku/
    ```
3. Install the dependencies/libraries required using `pip`

    ```bash
    pip install -r requirements.txt
    ```
    **Note:** You need to have Python installed in order to run the program

## Run the Program

1. Go to the project directory in your code editor:
   
    ```bash
    cd seekuproject/seeku/
    ```

2. Activate your virtual environment if you are using one. If you're not using a virtual environment, you can skip this step.

    ```bash
      source venv/bin/activate  # For Linux/macOS
      # or
      venv\Scripts\activate    # For Windows
    ```

3. Run the following in your command prompt:

    ```bash
    python manage.py makemigrations
    ```

    ```bash
    python manage.py migrate
    ```
    
4. Run the server with:

    ```bash
    python manage.py runserver
    ```
-  Or go to http://localhost:8000/ in your web browser.

## Navigation

You can navigate through the web application by indicating the specified path:

```bash
    http://localhost:8000/ -> Home
    http://localhost:8000/admin -> Manage Database
    http://localhost:8000/search
    http://localhost:8000/register
    http://localhost:8000/login
    http://localhost:8000/claim_request
    http://localhost:8000/profile
    http://localhost:8000/history

```
## Usage

- In order to use the application you need to create an account. Go to the Sign Up module or http://localhost:8000/register to do it.
- Note: Only EAFIT accounts are allowed, an email will be sent to the account in order to verify the user's identity.
- Log in to your account once verified.
- Complete a Claim Request to find the object you want to claim.
- 

## Contribute

This project can be used as a basis for developing new features.

## Authors

[Lina Ballesteros](https://github.com/linaballesteros) , [Juan Esteban García](https://github.com/Juanstevan1) and [David Grisales](https://github.com/Davidgp04) developed the entire program. 

<a href="https://github.com/linaballesteros/integrating-project-I/graphs/contributors">
  <img src="https://github.com/linaballesteros.png" width="60px" style="margin-right: 10px;">
  <img src="https://github.com/Juanstevan1.png" width="60px" style="margin-right: 10px;">
  <img src="https://github.com/Davidgp04.png" width="60px">
</a>


<!-- Made with [contrib.rocks](https://contrib.rocks).
-->

## License

Copyright (c) 2023, Lina Sofía Ballesteros Merchan, David Grisales Posada and Juan Esteban García Galvis. All rights reserved.
