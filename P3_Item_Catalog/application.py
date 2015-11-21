from flask import Flask, render_template, request, redirect, jsonify, url_for,\
    flash
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
from datetime import date
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open("client_secrets.json", "r").read())["web"]["client_id"]
APPLICATION_NAME = "Item Catalog"

engine = create_engine("sqlite:///item_category.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

##
# Routing functions
##

@app.route("/category/<int:category_id>/items/json")
def category_item_json(category_id):
    """
    Category items JSON endpoint.
    :param category_id: category ID
    :return: Category items in JSON format.
    """
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return jsonify(items=[i.serialize for i in items])

@app.route("/category/<int:category_id>/items/<int:item_id>/json")
def item_json(category_id, item_id):
    """
    Item information JSON endpoint.
    :param category_id: Category ID
    :param item_id: Item ID
    :return: Item information in JSON format.
    """
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item=item.serialize)

@app.route("/category/json")
def category_json():
    """
    Categories JSON endpoint.
    :return: Categories in JSON format.
    """
    categories = get_categories()
    return jsonify(categories=[r.serialize for r in categories])

@app.route("/login")
def show_login():
    """
    Show login page.
    :return: login page.
    """
    state = "".join(random.choice(string.ascii_uppercase + string.digits)
            for x in xrange(32))
    login_session["state"] = state
    return render_template("login.html", STATE=state)


@app.route("/gconnect", methods=["POST"])
def gconnect():
    """
    Login with google account. Set login_session parameters.
    :return: login result.
    """
    # Validate state token
    if request.args.get("state") != login_session["state"]:
        response = make_response(json.dumps("Invalid state parameter."), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets("client_secrets.json", scope="")
        oauth_flow.redirect_uri = "postmessage"
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps("Failed to upgrade the authorization code."), 401)
        response.headers["Content-Type"] = "application/json"
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token

    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, "GET")[1])
    # If there was an error in the access token info, abort.
    if result.get("error") is not None:
        response = make_response(json.dumps(result.get("error")), 500)
        response.headers["Content-Type"] = "application/json"


    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token["sub"]
    if result["user_id"] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers["Content-Type"] = "application/json"
        return response

    # Verify that the access token is valid for this app.
    if result["issued_to"] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers["Content-Type"] = "application/json"
        return response

    stored_credentials = login_session.get("credentials")
    stored_gplus_id = login_session.get("gplus_id")
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already connected."),
                                 200)
        response.headers["Content-Type"] = "application/json"
        return response

    # Store the access token in the session for later use.
    login_session["credentials"] = credentials.access_token
    login_session["access_token"] = credentials.access_token
    credentials = AccessTokenCredentials(login_session["credentials"],
                                         "user-agent-value")
    # login_session["credentials"] = credentials
    login_session["gplus_id"] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {"access_token": credentials.access_token, "alt": "json"}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session["username"] = data["name"]
    login_session["picture"] = data["picture"]
    login_session["email"] = data["email"]

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session["user_id"] = user_id

    output = ""
    output += "<h1>Welcome, "
    output += login_session["username"]
    output += "!</h1>"
    output += "<img src='"
    output += login_session["picture"]
    output += " ' style = 'width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;'> "
    flash("you are now logged in as %s" % login_session["username"])
    print "done!"
    return output

@app.route("/gdisconnect")
def gdisconnect():
    """
    Disconnect from google account.
    :return: Redirect to show_catalog.
    """
    print(login_session)
    access_token = login_session["access_token"]
    print("In gdisconnect access token is %s" % access_token)
    print("User name is: ")
    print(login_session["username"])
    if access_token is None:
        print("Access Token is None")
        response = make_response(json.dumps("Current user not connected."), 401)
        response.headers["Content-Type"] = "application/json"
        return response

    url = "https://accounts.google.com/o/oauth2/revoke?token=%s" % login_session["access_token"]
    h = httplib2.Http()
    result = h.request(url, "GET")[0]
    if result["status"] == "200":
        flash("Successfully disconnected.")
    else:
        flash("Failed to revoke token for given user.")

    del login_session["access_token"]
    del login_session["gplus_id"]
    del login_session["username"]
    del login_session["email"]
    del login_session["picture"]
    return redirect(url_for("show_catalog"))

@app.route("/")
@app.route("/catalog/")
def show_catalog():
    """
    Show all categories and latest 20 items.
    :return: show all categories and latest 20 items.
    """
    return render_template("latest_item.html", categories=get_categories(),
                           items=get_latest_items(), login_session=login_session)


@app.route("/category/new/", methods=["GET", "POST"])
def new_category():
    """
    Create a new category and redirect to /catalog.
    :return: create a new category.
    """
    if "username" not in login_session:
        return redirect("/login")
    if request.method == "POST":
        if request.form["name"]:
            category = Category(name=request.form["name"],
                                    description=request.form["description"],
                                    user_id=login_session["user_id"])
            session.add(category)
            session.commit()
        else:
            flash("Name is required. Please specify category name.")
            return render_template("new_category.html", login_session=login_session)

        return redirect(url_for("show_catalog"))
    else:
        return render_template("new_category.html", login_session=login_session)

@app.route("/category/<int:category_id>/edit/", methods=["GET", "POST"])
def edit_category(category_id):
    """
    Edit the category.
    :param category_id: category ID
    :return: Redirect to edit category page.
    """
    if "username" not in login_session:
        return redirect("/login")
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id != login_session["user_id"]:
        user = get_user_info(category.user_id)
        flash("%s is created by other user, %s. You are not authorized \
              to edit this. " % (category.name, user.email))
        return redirect(url_for("show_catalog"))
    if request.method == "POST":
        if request.form["name"]:
            category.name = request.form["name"]
        if request.form["description"]:
            category.description = request.form["description"]
        session.add(category)
        session.commit()
        return redirect(url_for("show_catalog"))
    else:
        return render_template("edit_category.html", category=category,
                               login_session=login_session)

@app.route("/category/<int:category_id>/delete/", methods=["GET", "POST"])
def delete_category(category_id):
    """
    Delete the category.
    :param category_id: category ID.
    :return: Redirect to delete the category.
    """
    if "username" not in login_session:
        return redirect("/login")
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id != login_session["user_id"]:
        user = get_user_info(category.user_id)
        flash("%s is created by other user, %s. You are not authorized \
              to delete this. " % (category.name, user.email))
        return redirect(url_for("show_catalog"))
    if request.method == "POST":
        session.delete(category)
        session.commit()
        return redirect(url_for("show_catalog"))
    else:
        return render_template("delete_category.html", category=category,
                               login_session=login_session)

@app.route("/category/<int:category_id>/")
@app.route("/category/<int:category_id>/items/")
def show_items(category_id):
    """
    Show item list of the category.
    :param category_id: category ID.
    :return: Item list page.
    """
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template("item.html", categories=get_categories(),
                           items=items, category=category,
                           login_session=login_session)


@app.route(
    "/category/<int:category_id>/item/new/", methods=["GET", "POST"])
def new_item(category_id):
    """
    Create a new item under the category.
    :param category_id: category ID.
    :return: Redirect to add new item.
    """
    if "username" not in login_session:
        return redirect("/login")
    if request.method == "POST":
        if request.form["name"]:
            item = Item(name=request.form["name"],
                        description=request.form["description"],
                        category_id=request.form["category_id"],
                        user_id=login_session["user_id"],
                        date=date.today())
            session.add(item)
            session.commit()
        else:
            flash("Name is required. Please specify item name.")
            return render_template("new_item.html", categories=get_categories(),
                                   category_id=category_id,
                                   login_session=login_session)

        return redirect(url_for("show_items", categories=get_categories(),
                                category_id=category_id))
    else:
        return render_template("new_item.html", categories=get_categories(),
                               category_id=category_id,
                               login_session=login_session)

@app.route("/category/<int:category_id>/items/<int:item_id>/edit",
           methods=["GET", "POST"])
def edit_item(category_id, item_id):
    """
    Edit item page.
    :param category_id: category ID.
    :param item_id: item ID.
    :return: Redirect to edit item page.
    """
    if "username" not in login_session:
        return redirect("/login")
    item = session.query(Item).filter_by(id=item_id).one()
    if item.user_id != login_session["user_id"]:
        user = get_user_info(item.user_id)
        flash("%s is created by other user, %s. You are not authorized \
              to edit this. " % (item.name, user.email))
        return redirect(url_for("show_items", categories=get_categories(),
                                category_id=category_id))
    if request.method == "POST":
        if request.form["name"]:
            item.name = request.form["name"]
        if request.form["description"]:
            item.description = request.form["description"]
        if request.form["category_id"]:
            item.category_id = request.form["category_id"]
        item.user_id = login_session["user_id"]
        session.add(item)
        session.commit()
        return redirect(url_for("show_items", categories=get_categories(),
                                category_id=category_id))
    else:
        return render_template("edit_item.html", categories=get_categories(),
                               category_id=category_id,
                               item_id=item_id, item=item,
                               login_session=login_session)

@app.route("/category/<int:category_id>/items/<int:item_id>/delete",
           methods=["GET", "POST"])
def delete_item(category_id, item_id):
    """
    Delete the item.
    :param category_id: category ID.
    :param item_id: Item ID.
    :return: Redirect to delete item page.
    """
    if "username" not in login_session:
        return redirect("/login")
    item = session.query(Item).filter_by(id=item_id).one()
    if item.user_id != login_session["user_id"]:
        user = get_user_info(item.user_id)
        flash("%s is created by other user, %s. You are not authorized \
              to delete this. " % (item.name, user.email))
        return redirect(url_for("show_items", categories=get_categories(),
                                category_id=category_id))
    if request.method == "POST":
        session.delete(item)
        session.commit()
        return redirect(url_for("show_items", categories=get_categories(),
                                category_id=category_id))
    else:
        return render_template("delete_item.html", item=item,
                               login_session=login_session)


##
# global APIs to get various information from the database.
##

def create_user(login_session):
    """
    Create a user based on login session.
    :param login_session: login session.
    :return: user ID.
    """
    newUser = User(name=login_session["username"],
                   email=login_session["email"],
                   picture=login_session["picture"])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def get_user_info(user_id):
    """
    Get user information.
    :param user_id: user ID.
    :return: User for the given user ID.
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user

def get_user_id(email):
    """
    Get user ID for the given email.
    :param email: email address.
    :return: User.id for the email address.
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def get_categories():
    """
    Get all categories defined in the database.
    :return: All categories.
    """
    categories = session.query(Category).all()
    return categories

def get_latest_items():
    """
    Get latest items from the database.
    :return: latest items.
    """
    items = session.query(Item).order_by(desc(Item.date)).limit(20).all()
    return items

def get_category(categories, category_id):
    """
    Get Category for the given category ID.
    :param categories: all categories.
    :param category_id: category ID.
    :return: Category for the given category ID.
    """
    for category in categories:
        if category.id == category_id:
            return category
    return None

if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.jinja_env.globals.update(get_category=get_category)
    app.run(host="0.0.0.0", port=8000)
