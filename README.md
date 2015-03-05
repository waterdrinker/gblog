Gblog -- A Simple Python Blog  
=======================

This is a simple blogging engine based on python 3 and uses MySQL to store posts. See [Demo](http://gongyusong.com)

Requirements
-------------

1. python 3 
3. MySQL(mariaDB)

And the required Python packages (using pip or easy_install to install):

* tornado
* MySQL-python
* Markdown
* Pygments
* Unidecode 

目前封装 mysql 接口的 python 官方包还不支持 python 3 的，可以使用第三方的项目 [MySQL-for-Python-3](https://github.com/davispuh/MySQL-for-Python-3) :

```
git clone https://github.com/davispuh/MySQL-for-Python-3.git
python3 setup.py install
```

Set Up MySQL
------------

Since it depends on MySQL, you need to set up the database schema. Connect to MySQL and create a database and user for the blog.

1. Create the database

```
# Connect to MySQL as a user that can create databases and users:
mysql -u root

# Create a database named "blog":
mysql> CREATE DATABASE blog;

# Allow the "blog" user to connect with the password "blog":
mysql> GRANT ALL PRIVILEGES ON blog.* TO 'blog'@'localhost' IDENTIFIED BY 'blog';
```

2. Create the tables in your new database (using gblog/data/schema.sql).

```
# use the provided /data/schema.sql file by running this command:
mysql --user=blog --password=blog --database=blog < schema.sql
```

Run the blog
------------

Install and run in test 

```
python3.4 setup.py develop
gblog --port=3000
```

or you can use `nginx` and `supervisor` in production. 


Configure
------------

The configure file `gblog.conf` contains main blog settings.

```
mkdir ~/.gblog
cp /path/to/gblog/data/gblog.conf ~/.gblog/gblog.conf
```

