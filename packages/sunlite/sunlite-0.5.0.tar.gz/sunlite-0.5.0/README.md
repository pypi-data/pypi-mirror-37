#sunlite


# Sunlite Simple Database System

<a href='#server' >[**Jump to sunlite database server*]</a>

## simple, fast, local, userfriendly

## Speed Menu
#### for sunlite database
<a href='#dbconnect' >[**Jump to sunlite database connection*]</a> <br>
<a href='#dbinfo' >[**Jump to sunlite database tutorials*]</a> <br>
<a href='#dbexample' >[**Jump to sunlite database examples*]</a> <br>
#### for sunlite server database 
<a href='#svwhy' >[**Jump to sunlite database server Q/A*]</a> <br>
<a href='#svmake' >[**Jump to sunlite database server getting started*]</a> <br>
<a href='#svlinks' >[**Jump to sunlite database server how to links*]</a> <br>
 
### what is sunlite ?

#### Ans: Sunlite is a module for simple data management. 

* How to use
   * Connect to memory.
     >>
    * connect to a database.
     >>
     * Create a new header .
      >>
      * add data , or pull data
       >>
       * enjoy ^~^

## Connecting
<a name='dbconnect'></a>
Sunlite lets you connect as you want.

```python
from sunlite.db import connect

db = connect() #for memory
db = connect("my_db") #for connecting with "my_db" , it will be auto generated if doesnt exists.
db = connect("my_db",logs=False)  # for connecting to "my_db" but say no to logs

```
<a name='dbinfo'></a>
## Generating new header
headers are like boxes which contains your datas , don't forget to make one before pushing or pulling data

```python

db = connect("my_db")

db.new("websites")  #here , we made a header named websites.

```

## Pushing   data to headers

by pushing , we add data in headers to contain . you can push any data .

```python 

db = connect("my_db")

db.new("websites")

name = "google"
data = "http://google.com"

db.push(name,data) #here , we are pushing http://google.com with the name google in websites header
```

## Pullling data from headers

you can pull all data of header or an invidual data

```python

db = connect("my_db",logs=False)

db.new("websites")

name = "google"
data = "http://google.com"

db.push(name,data)

a = db.pull("websites")  #it will pull all data in website header as a dictionary.

a = db.pull("google")  #it will only pull the data of google no matter where it is in which header .
```
don't use same names for two datas as it will remove 2nd one .

## Get a header as you want. This time duplicate names are accepted.
### unlike pull function , this function doesn't update duplicate datas as sends as they are . 
### this is useful in maintaining a large set of same data.
<a name='dbexample'></a>
example

```python

db.connect("students",logs=False)

db.new("Allan")

db.push("maths",50)
db.push("english",70)
db.push("science",40)


#now for akmal
db.new("Akmal")

db.push("maths",45)
db.push("english",60)
db.push("science",70)

db.get("Akmal")  #for getting akmal marks
db.get("allan") #for getting allan's marks


```

## Beauty print .

You can beauty print all data's in all headers .

```python

db = connect("my_db",logs=False)

db.new("websites")

name = "google"
data = "http://google.com"

db.push(name,data)

db.beauty()  #this prints all data nicely

```
# Get all headers

```python

db = connect("my_db",logs=False)

db.headers()

```

# Example with a user info system with sunlite 

```python

db = connect("my_db",logs=False)

db.new("users")

name = "Axel"
data = ["age":13 , "nation": "USA"]

db.push(name,data)

name = "Jack"
data = ["age":15, "nation": "England"]
db.push(name,data)

db.beauty()
```

<a name='server'></a>
#  Sunlite Server
**Sunlite** server is a database server which can be generated in memory or in a physical database .

### Why and How ?
<a name='svwhy'></a>
>  Q.  Why **Sunlite** need database server ?
>  A.   Sunlite is a python system which can't be used from other languages but with sunlite server, users can use this simple database system from any programming language after invoking the server with python.
> Q. How to use sunlite server from different programming languages?
> A.  Using **http get** requests to server. **Wrappers from different languages coming soon.**
#### I think i am ready for my first server  :)
To start a server of your existing sunlite database (  tutorials above about using sunlite database system ) , simply login to your python console installed and execute from sunlite.server import Serve  
  
  
<a name='svmake'></a>
```
from sunlite.server import Serve
Serve(name="[DBNAME]" , logfolder="[LOGPATH]").invoke()
# [DBNAME] is the database name you created using sunlite or any name if you want to create a new. remember sunlite can connect to database #  you create with server and vice versa.
# [LOGPATH] is the path to log your server tasks. ex. 'E:/logs'
```
So to connect a sunlite database with the name 'test' and save it's logs in a folder named logs in the project directory , just do 

```python
from sunlite.server import Serve
Serve(name="test" , logfolder="logs").invoke()
```
and your server will start running in http://localhost:5000

to disable or unable logs , you can use `logs=True` or `logs=False` inside Serve.

Ex. for turning logs off
```python
from sunlite.server import Serve
Serve(name="test" , logs=False , logfolder="logs").invoke()
```

logs are on by default.

##### To open the server on your prefered ip address, 

```python
from sunlite.server import Serve
Serve(name="test" , logs=False , logfolder="logs").invoke(ip='your ip' , port = your_port)
#example Serve(name="test" , logs=False , logfolder="logs").invoke(ip='127.0.0.1' , port = 5000)
```
<a name='svlinks'></a>
### Links to send database requests.

###### to get all data in your database

http://[your-ip]:[your-port]/a/

###### to get header list 

http://[your-ip]:[your-port]/h/

###### to create a new header 

http://[your-ip]:[your-port]/new/[header-name]

###### to pull a data 

http://[your-ip]:[your-port]/p/[data-name]

###### to get total data of a header

http://[your-ip]:[your-port]/g/[header-name]

###### to add a data or modify in a header


http://[your-ip]:[your-port]/add/[data-name]/[data]/[header-name]

**do remember html link syntaxes.**

ex. 


**http://127.0.0.1:5000/p/hello**  will pull the data named hello
**http://127.0.0.1:5000/g/myheader** will pull data from the header myheader etc


### Important

format spaces with %20f 

ex. if your data name was **my data** 
make the link like **http://127.0.0.1:5000/p/my%f20data**
not **http://127.0.0.1:5000/p/my data**

