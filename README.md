# esp8266-temperature
## Esp8266 Temperature Project
In this project I am going to show you how to set up your own temperature sensor in a room using Esp8266, store values received from a sensor in a database and then display those values on a webpage.

### Requirements
#### Hardware
  [NodeMCU Esp8266](https://www.amazon.com/AZDelivery-Nodemcu-Module-ESP8266-Development/dp/B07F8759RC/ref=sr_1_1_sspacrid=15HB6XNPPS5QL&keywords=nodemcu+esp8266&qid=1560081331&s=electronics&sprefix=nodemcu%2Caps%2C698&sr=1-1-spons&psc=1)
  
  [Temperature sensor](https://www.amazon.com/Dallas-DS18S20-Temperature-Digital-Serial/dp/B01MZE6ZBB/ref=sr_1_6?keywords=temperature+sensor+dallas&qid=1560081447&s=gateway&sr=8-6)
  
  [Resistor](https://www.amazon.com/EDGELEC-Resistor-Tolerance-Resistance-Optional/dp/B07HDFHPP3/ref=sr_1_2_sspa?crid=1UBAW8QKHDFH2&keywords=4.7k+ohm+resistor&qid=1560081709&s=gateway&sprefix=4.7k%2Caps%2C274&sr=8-2-spons&psc=1)
  
  Usb cabel
  
  Jumper wires
#### Software
  [Arduino IDE](https://www.arduino.cc/en/Main/Software)
  
  [Brackets](http://brackets.io/) (or another text editor you prefer)
  
  [Flask](http://flask.pocoo.org/) (Installation using cmd)
  
  ```
  pip install Flask
  ```
    
  [Mysql](https://dev.mysql.com/)
  
  And you will also need mysql.connector, since we are using it in our source code
  
  ```
  pip install mysql.connector
  ```

### Getting started
  #### Esp8266 and temperature sensor setup
  Watch this video - https://www.youtube.com/watch?v=YP34KloQvxE
  
  Note: Be careful when playing with wires and check everything twice just to be sure, because when you connect wrong pins together your temperature sensor can become very hot as a result. (Talking from my own experience.)
  #### Arduino IDE setup
    ...
  #### MySQL database setup
  1. Open MySQL command line client.
  2. ```create database databaseName;``` (I used temperatureData)
  3. ```use databaseName;```
  4. To check if you are using the right one, write ```status``` and current database should be your databaseName.
  5. ```create table temp (id int auto_increment primary key, name varchar(255), temperature float, timestamp varchar(255));```
  6. ```create table stats (name varchar(255), value float);```
  7. I recommend that you always have one row in your ```temp``` table, so you will not get any errors when drawing graph on a webpage.
  ```
  insert into temp(name, temperature, timestamp) values('esp8266#2', 0, 'date and time')
  ```
  8. In your ```stats``` table will be stored statistical values. We have to create rows and default values for them, so later we can update those values.
  ```
  insert into stats(name, value) values('Lowest', null);
  ```
  ```
  insert into stats(name, value) values('Highest', null);
  ```
  
  ```
  insert into stats(name, value) values('Average', 0);
  ```
  
  ```
  insert into stats(name, value) values('Count', 0);
  ```
  9. Now you can ```quit``` MySQL command line.
  
  #### Python Flask server setup
  1. If you have changed the names of tables in your database, then you will have to rewrite some lines of code here in order for it to work without errors.
  2. Edit user, password and database to match your setup.
  
  ```
  mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='temperatureData')
  ```
  3. Edit ```host``` (it can be either your domain if you have one or a computer you will  be running server on)
  ```
  app.run(host='localhost', port=8888, debug=True)
  ```
  #### Webpage setup
  1. If you do not want to have my name there, then you can remove or change it.
  ```
  <meta name="author" content="Samuel Ivan">
  ```
  ```
  <footer>
    <p>Created by Samuel Ivan - Copyright &copy; 2019</p>
  </footer>
  ```
  2. Feel free to play with design of webpage.
