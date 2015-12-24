#Full Stack Interview Dry-Run
##Question 1 - What is the most influential book or blog post you’ve read regarding web development
To be honest, I don't have any specific book or blog post regarding web development 
come to my mind. However, "Clean Code" is the recent most influential book for me. This book 
summarizes how we should write clean code with Java very well. Many of them can also be applied
to other programming languages. 

Also, some of those remind me of the importance of revisiting the existing coding standards
at my work. For instance, we have been trained to name class/abstract/interface and structure
them in certain ways. (e.g. Interface starts with the capital letter, "I", followed by class
name that implements it.) But this is no longer needed with the sophisticated development
environment we have these days and such rules would rather block new comers from getting
used to the working environment. Likewise, we have been trained to have comments in codes
as much as possible for long years. But rather it suggests codes should not require comments
and they are concise and self-descriptive.

##Question 2 - Tell me about a web application you have built. Why did you choose to build it? What did you learn? What challenges did you face and how did you overcome them?
I built a web application that handles localization of software resources. This was done for the work.
This web application was made so users can check what we have in translation memory, which is the
database to store translated texts for multiple languages. We actually started it as 
client server application rather than web application. So, we did not build backend so it could support
both native client and web client. Having queries in client codes result in redoing the backend implementation.

The lessons we learned are:

* Decoupling the backend from client codes by using ORM at least even if it's started as the small project.
* RESTFul API should better be prepared from the beginning.

##Question 3 - Write a function that takes a list of strings and returns a single string that is an HTML unordered list of those strings. You should include a brief explanation of your code. Then, what would you have to consider if the original list was provided by user input?
First, the API checks if the given input is None or empty list. If it's, then it returns None.
Then, it goes through the list of strings to build unordered list. While it does so,
it sanitizes the given text to avoid javascript insertion. Here I use "sanitize", which is not 
implemented below. "sanitize" function can be some function from the library like bleach.

```
def get_unordered_list(texts):
    if texts == None or len(texts) == 0:
        return None
    html = "<ul>"
    for text in texts:
       html += "<li>%s</li>" % sanitize(text) 
    html += "</ul>"
    return html
```
    
##Question 4 - List 2-3 attacks that web applications are vulnerable to. How do these attacks work? How can we prevent those attacks?
SQL injection/Javascript insertion are common attacks against web applications.
###SQL Injection
The attackers try to inject SQL statement like "); delete from table_name" through
web application's input field. They try to update/delete/retrieve data with those
injected SQL statement. One way to prevent it is binding parameters to cursor 
instead of building a SQL statement as a String.

###Javascript insertion
The attackers try to insert Javascript through web application's input field.
They try to alter site contents and/or retrieve user information and send it to 
other sites by those inserted Javascript. We can prevent it by cleaning up the given
input texts before the application process them for any purpose. This can be done
by using the library like bleach.

##Question 5 - Here is some starter code for a Flask Web Application. Expand on that and include a route that simulates rolling two dice and returns the result in JSON. You should include a brief explanation of your code.
When users access /roll_dice_json, it calls roll_dice_json function and it returns
JSON like the following. Result of each die is given by random.randint(1, 6).
```
{"dice":[
    {"die":"1"},
    {"die":"6"}
]}
```

```
from flask import Flask
app = Flask(__name__)

import json
import random


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/roll_dice_json')
def roll_dice_json():
    result = [{"die": random.randint(1, 6)} for i in range(2)]
    return jsonify(dice=result)

if __name__ == '__main__':
    app.debug = True
    app.run()
```

##Question 6 - If you were to start your full-stack developer position today, what would be your goals a year from now?
I am taking [Full Stack Engineer, International](https://jobs.lever.co/udacity/2d73b304-013c-4ad8-9bfa-718cc64a7dd2) at Udacity as a sample position.

I am currently Java engineer and I have focused on Java enterprise application's 
internationalizatin/localization. I am willing to shift to cloud solution and learn
new things like python/javascript and GAE/AWS. While I am very comfortable in writing
codes and working in internationalization/localization, I will need to learn a lot
of new things. My goals for a year would be:

* Deepening the knowledge in Python programming and one or a few web frameworks such as Flask/Django.
* Understanding development in GAE/AWS environment.
* Being able to address internationalization issues in all tiers fairly independently with new tech stack.
* Establishing the fully automated localization process/framework.
