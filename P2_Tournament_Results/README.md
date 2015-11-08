# P2: Tournament Results
## Contents
* tournament.sql - SQL script to set up your database schema.
* tournament.py - Python script to provide access to your database via a library of functions.
* tournament_test.py - Python script to test functions written in the tournament.py module.

## How to run Tournament Results
* go to P2_Tournament_Results directory
* copy sql/py files under the above directory to vagrant/tournament.
* start the virtual machine.
* start vagrant ssh and go to /vagrant/tournament.
* start psql.
* create "tournament" database if it's not created yet.
* connect to tournament database by "\c tournament".
* perform "\i tournament.sql".
* exit psql by "\q".
* perform the following command.
    python tournament_test.py

## Changes on template
In addition to the original requirement, this implementation supports multiple 
tournaments scenario. So, the template .py files are modified. Please note the
following changes.

**tournament.py**

Tournament class is implemented to represent the data structure of tournament. 
It provides methods to perform operations like register player, count player, 
and etc. There is one-to-one method against method in the original template so
all test cases in tournament_test.py work fine.

Since the methods in the original template do not allow to specify the 
tournament information. With those methods, it creates Tournament object with
Tournament.default, which is `___DEFAULT___`. Those methods work with the 
default tournament.

**tournament_test.py**

Original test cases are kept as they are. Additional test cases are added for
multiple tournaments scenario. Those additional test cases perform test against
Tournament methods directly instead of calling methods defined in tournament.py
template such as deletePlayers etc.

Those additional test cases are called after the original test cases in main
method.

## Table Schema
**tournament.sql** creates the following tables in tournament database. Also,
when a new tournament is added, it creates a view called "standings_< *tournament id* >".
Please refer to tournament.sql for details of schema definition.

**tournaments**

 id | name 
 ---- | ----
 1 | `___DEFAULT___`
 2 | Full Stack Developer Cup
 

**players**

 id | name 
 ---- | ----
 markov.chaney@gmail.com | Markov Chaney 
 
 **participants**
 
 t_id | p_id | 
 ---- | ----
 1 | markov.chaney@gmail.com
 
 **matches**

 t_id | p_id | points
 ---- | ----
 1 | markov.chaney@gmail.com | 1
 1 | joe.malik@gmail.com | 0
 
**standings_1**

 t_id | p_id | sum
 ---- | ----
 1 | markov.chaney@gmail.com | 1
 1 | joe.malik@gmail.com | 0
