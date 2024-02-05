# Sales App

## Packages used:
+ kivy.app
+ kivy.lang
+ kivy.config
+ kivy.graphics
+ kivy.uix
+ requests
+ certifi
+ functools
+ datetime
+ os

## Project Description
<p>This is a Mobile Application Project developed using Kivy framework
and Firebase database. This application aims to control a company's sales
by keeping track of each individual sale by each salesman.</p>

## Project Structure
<ul>
    <li>The "main.py" script is responsible for running the mobile application
and defines functionalities such as: loading user data; change screen;
change profile picture; add other salesman to the contact list;
add sale's information and store that data into the database; load other user's sales;
load all company's sale;</li>
    <li>The "myFirebase.py" script is responsible for defining functionalities that
requires the REST API authentication such as: create account, login and
creating refresh token;</li>
    <li>The "kv" files creates the structure of every browsable page, 
delegating functions to each button, label and scrollview object;</li>
    <li>The "main.kv" file is responsible for managing all the other kv files,
in other words, for the screen management;</li>
    <li>"telas.py" defines an object for every page, which enables Python to
interact with kv files;</li>
    <li>"botoes.py" creates 2 hybrid objects the first one inheriting both
Image and Button features and the second one inheriting both Label
and Button features;</li>
    <li>Both "bannervendedor.py" and "bannervenda.py" creates objects that
are going to be used as widgets for specific pages of the App.</li>
</ul>

## Login/Create Account Page

<p align="center">
    <img src = "imgs/img.png" />
</p>

## Login/Create Account error messages

| ![img_1.png](imgs/img_1.png) | ![img_2.png](imgs/img_2.png) |
|------------------------------|------------------------------|
| ![img_3.png](imgs/img_3.png) | ![img_4.png](imgs/img_4.png) |

## Salesman Profile

<p align="center">
    <img src = "imgs/img_5.png" />
</p>

## Add Sale

<p align="center">
    <img src = "imgs/img_6.png" />
</p>

## Configuration Page

<p align="center">
    <img src = "imgs/img_7.png" />
</p>

## Change Profile Picture Page

<p align="center">
    <img src = "imgs/img_8.png" />
</p>

## Add other user to the Contact List

<p align="center">
    <img src = "imgs/img_10.png" />
</p>

## Contact List

<p align="center">
    <img src = "imgs/img_11.png" />
</p>

## All Company's Sales Page

<p align="center">
    <img src = "imgs/img_12.png" />
</p>

## Deployment
<p>This project was deployed by using a Linux Virtual Machine to 
compile the project to an apk file and at last converting it into
an aab file which is the release version that is accepted by Google Play.</p>
