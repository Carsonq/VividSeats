# Vivid Seats

### Installation (Ubuntu 18.04)

##### Install MySQL (5.7.24)  

```sh
$ sudo apt-get update
$ sudo apt-get install mysql-server
```

##### Setup MySQL  

```sh
$ sudo service mysql start
$ sudo mysql -u root
mysql: $ ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root'
```

##### Setup Env
```sh
$ sudo apt-get install python-mysqldb
$ sudo apt-get install python-pip
$ pip install Flask
$ pip install Flask-SQLAlchemy
$ pip install flask-jsonpify
$ pip install requests
```

##### Create Tables
```sh
$ mysql -u root -p < vivid.sql
```

##### Populate Tables
```sh
$ python populate_tables.py
```

##### Start Web Service
```sh
$ cd www
$ python web.py
```

##### Api Test
 - Recommend to use [Postman](https://www.getpostman.com/) to test the apis.
 - There are some test cases in api_test.py


### APIs

| API | method | Description | Example | Post Data Example |
| ------ | ------ | ------ | ------ | ------ |
| /events/<int:event_id>/tickets | GET | get available tickets for an event | 127.0.0.1:5000/v1/events/107/tickets |
| /sellers/<int:seller_id>/tickets | POST | post a new ticket from a seller | 127.0.0.1:5000/v1/sellers/1/tickets | {"event_id": 107, "ticket_section": 222, "ticket_row": "111", "ticket_quantity": 20, "ticket_price": 50}| 
| /ticket/<int:ticket_id> | PUT | update a ticekt to sold | 127.0.0.1:5000/v1/ticket/1533 | {"referal_id": 2, "customer_id": 3} |
| /events/<int:event_id>/tickets?search=best | GET | get best ticket from an event | 127.0.0.1:5000/v1/events/107/tickets?search=best |
