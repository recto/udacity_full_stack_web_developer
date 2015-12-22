# P5 Linux Server Configuration
## Linux Server information
* IP Address : 52.35.141.132
* URL : http://ec2-52-35-141-132.us-west-2.compute.amazonaws.com
## Summary of software installed and configuration changes made
* Installed apache2, mod_wsgi, postgresql, ntp, git, pip, setuptools, sqlalchemy, Flask, python-psycopg2.
* Modified configuration: Timezone is set to UTC. NTP is enabled, Created a new user grader and added "grader" to sudoers, Enabled outgoing ports and disabled incoming ports except ssh/www/ntp/2200.
* Modified apache2 configuration so mod_wsgi is enabled.
* Cloned git repository, https://github.com/recto/udacity_full_stack_web_developer.git.
* Copied Item Catalog App, which was modified to work with PostgreSQL instead of SQLite, to /var/www/catalog.
* Modified apache2 configuration so WSGIAlias "/" points to /var/www/catalog.
* Created item_catalog database on PostgreSQL server. Created a user, catalog, who can access only item_catalog database. Password for catalog user is 'udacity'.
* Executed database_setup.py and populate_catalog.py to create table/some seed database for Item Catalog App.
* Made Item Catalog App work with Apache2 + mod_wsgi.
## Item Catalog App (/var/www/catalog)
* application.py - Web Application.
* database_setup.py - a script to define database schema.
* populate_catalog.py - a script to populate catalog data.
* client_secrets.json - client secrets JSON file for OAuth2.
* settings.py - database connection setting.
## List of Third-Party Resources
* [Time Synchronisation with NTP](https://help.ubuntu.com/lts/serverguide/NTP.html)
* [Create a user, who can access only the specific database.](http://dba.stackexchange.com/questions/17790/created-user-can-access-all-databases-in-postgresql-without-any-grants)
* [PIP installation](https://pip.pypa.io/en/stable/installing/)
* [sqlalchemy installation](http://docs.sqlalchemy.org/en/latest/intro.html#installation-guide)
* [Deploying mod_wsgi](http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/)
* [mod_wsgi configuration directives](https://code.google.com/p/modwsgi/wiki/ConfigurationDirectives)
* [mod_wsgi debugging techniques](https://code.google.com/p/modwsgi/wiki/DebuggingTechniques)
* [Flask debug mode](http://flask.pocoo.org/docs/0.10/quickstart/#debug-mode)
* [Flask API](http://flask.pocoo.org/docs/0.10/api/) : This is used to address the issue with global functions used by templates.
## ~/.ssh/udacity_key.rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEAxU23ANPIW0n9EgMbHdkFCYXKP7X3l6I8cPlmuVEtmnZpJIXz
ePeKiCnkMOBAeh7hjFiMRS3k+pP7Nr4yIFoX4YirRLmHlnC4yx0QXmrEACBqFWIC
3G8TLuIGtahVWVzjk88kcrP3cAygw7+MujHaDJakRIkp/mh4HTVrCvAgE4SWUhDh
F8ptw5GjPY3k5yKdL5VUU/cR4wiy2G3SC/UWwHcNkAXgpasQPBYD6PG4+KuCnbvk
t3NSZxwUEYSvhvXmcNgyFxY6BjScjwKXvE6klJFf1UwdtnZEg0VoHT5GczZNo8oj
8QMyxqBwWlPel9Mui9kGZSGiRWO+3VgagmGjEwIDAQABAoIBAQCxLxdXENlu0cUI
te1WIpxZbuKv0FQmwjURJ4fOiE4x1oCZogmB6ptnqGcaVWjRwoW+qY5eWda2CMqi
4K7XStEDYt6bexl+SoBJNzKJ98tIadOanEgBeWZ6xdRMsnzjIX3mMTGEKIXfBBgj
chOI6lfs0iN2wM8LfvnPETetvPKxUt5ypmOg5ysLfbac2vn6aPyQuQ03twB+m/3S
fbZi8ZCXJywk00Hz2WpBFAUirAkwQ28+8iiWToKxRs2OEBpfw/n5w4dWq/5r0zAk
LkyKQqgFgsty6sn0+ao5H2oKd70+y27NgH+VNPOi8vl6Vnuf9h8WNM/QYnx6dUHA
TkMOeu5BAoGBAOcgG0jLsDy/SiRpU0FixlQg7cIYsz4GsnRIHedOo78edqwwaQ/0
sQU9mdjl46i2Qc5v7nJ/F9X7B2je25BqGdLBHVf1zaITXR1DDjmybygeoGgawPQJ
S2D/1W3PyjumfHC/DZDmbpqN0P1xZy4743UQ0poyuxHb3lIJlENt0c4xAoGBANqJ
wnvy3j5VMKH49cmNy5UcBwFCgruSygzYEU/DjjS8bEHUQgqSq6JLJM6IhrMzG5fc
Q8dZ8zWk34vHvs62a+7Pd8G8Wt3OazBO27fyBcEHhhTfjNr7Wf3D29Zz0+T7DnwO
LOOJ/awQ3knRAoQeye3rcL0zjDP8EvKTO2rfbyCDAoGBAMc4S4xh1lVmZVghWVwg
8ecOQyJs/ANY7nWAvBXnGQniDlS5nbXdKsDjqjrlXWjNQMfaf2Q93KPbLzXb8tH2
QrABOXPaMhekLTzN0fM1tM6WJ5nUhcFUSZ8gpi1zUFQ+W0ErzVu65FdgKmZrW47k
nFkJ2R6E3+6y4F1CWIQOoyvhAoGBAJuPsnQ+xrrCM3Mo3/UQTVmf8NCRwrO44sDP
0UrhHkol0j3t1PDnxOsq6FFoV9IZ0EuCTHEMc5a8/S/oCMfmjOAaqNmstVXsiNqD
V94Rlsz4CRa0pvR+NWnxUHzQSIZXu9DM2mFCKeOgwkrzUAIyVHVawg68MdITXn10
FriVwen3AoGACNe5H4kLm6pOTlrZ3D2PDDPd7izdhH8hM+Hsui7VYeeLWhWC+GIa
jWgX7+JucqVSfDakzXRPKAKowRcwVC9m+xHLBooxXvH+oZOA0nlxOw8C6ze6XSJD
w7LaCU0rhr9fQ3zxLvHBfXaAJk2e7eCefHPQ6rkEP3FZuRNgMyxq7qQ=
-----END RSA PRIVATE KEY-----
