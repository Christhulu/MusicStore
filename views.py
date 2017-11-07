from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response
from flask import session as login_session
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from models import *
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import os, random, string, datetime, json, httplib2, requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item-Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login Routing
#===================
# Login - Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# GConnect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        # response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('showCategories'))
        flash("You are now logged out.")
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response







# Show all categories
# Homepage
# Show all categories
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).filter_by(category_id=Category.id)
    # Display the newest item on the page
    newestItem = session.query(Item).order_by(Item.id.desc()).filter_by(category_id=Category.id).first()
    return render_template('catalog.html',
                            categories=categories, 
                            items=items,
                            newestItem=newestItem)

# Category CRUD operations
@app.route('/catalog/new', methods=['POST','GET'])
def newCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    if request.method == 'POST' and 'username' in login_session:
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        flash('New Category \"%s\" Successfully Created' % newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        flash('Log In if you want to edit this category')
        return render_template('newCategory.html',categories=categories)

@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategories(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    editCategories = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST' and 'username' in login_session:
        if request.form['name']:
            editCategories.name = request.form['name']
            session.add(editCategories)
            session.commit()
            flash('Category Successfully Edited \"%s\"' % editCategories.name)
            return redirect(url_for('showCategories'))
    else:
        flash('Log In if you want to edit this category')
        return render_template('editCategory.html', 
                                categories=categories, 
                                category=editCategories)

@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategories(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    deleteCategory = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST' and 'username' in login_session:
        session.delete(deleteCategory)
        flash('\"%s\" Successfully Deleted' % deleteCategory.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        flash('Log In if you want to delete this item')
        return render_template('deleteCategory.html', 
                                category=deleteCategory,
                                categories=categories)

@app.route('/catalog/<int:category_id>/')
def showItems(category_id):
    categories = session.query(Category).order_by(Category.name.asc()).all()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).order_by(Item.name.desc()).filter_by(category_id=category_id).all()
    return render_template('items.html', 
                            categories=categories, 
                            items=items, 
                            category=category)

# Item CRUD operations
@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def itemPage(category_id,item_id):
    categories = session.query(Category).order_by(asc(Category.name))
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template('item.html',
                            item=item,
                            category_id=category_id,
                            item_id=item_id,
                            categories=categories)
@app.route('/catalog/<int:category_id>/new', methods=['POST','GET'])
def newItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()    
    if request.method == 'POST' and 'username' in login_session:
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       price = request.form['price'],
                       image=request.form['image'],
                       category_id=category_id)
        session.add(newItem)
        flash('New item \"%s\" successfuly added' % newItem.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        flash('Log In if you want to add an item')
        return render_template('newItem.html', 
                                category_id=category_id,
                                category=category)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit', methods=['POST','GET'])
def editItem(category_id,item_id):
    categories = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(id=category_id).one()
    editItem = session.query(Item).filter_by(id=item_id).one()

    if request.method == 'POST' and 'username' in login_session:
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['price']:
            editItem.price = request.form['price']
        if request.form['image']:
            editItem.image = request.form['image']
        session.add(editItem)
        flash('\"%s\" Item Successfully Edited' %editItem.name)
        session.commit()
        return redirect(url_for('showCategories', item_id=item_id))
    else:
        flash('Log In if you want to edit this item')
        return render_template('editItem.html',
                                category_id=category_id, 
                                item_id=item_id, 
                                item=editItem, 
                                categories=categories)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete', methods=['POST','GET'])
def deleteItem(category_id,item_id):
    deleteItem = session.query(Item).filter_by(id=item_id).one()

    if request.method == 'POST' and 'username' in login_session:
        session.delete(deleteItem)
        flash('\"%s\" Successfully Deleted' % deleteItem.name)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('deleteItem.html', 
                                item=deleteItem,
                                category_id=category_id)


#===================
# JSON
#===================
@app.route('/catalog/JSON')
def allItemsJSON():
    categories = session.query(Category).all()
    category_dict = [c.serialize for c in categories]
    for c in range(len(category_dict)):
        items = [i.serialize for i in session.query(Item)\
                    .filter_by(category_id=category_dict[c]["id"]).all()]
        if items:
            category_dict[c]["Item"] = items
    return jsonify(Category=category_dict)

@app.route('/catalog/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/catalog/items/JSON')
def itemsJSON():
    items = session.query(Item).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<string:category_name>/items/JSON')
def categoryItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category=category).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def ItemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(name=item_name,\
                                        category=category).one()
    return jsonify(item=[item.serialize])

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    app.secret_key = 'super_secret_key'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)