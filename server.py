import database
from functools import wraps

import order_handler
from flask import Flask, url_for, redirect, render_template, request, make_response

cart = {}

app = Flask(__name__,
            static_folder="static",
            template_folder="static/templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sahara_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.db.init_app(app)


def ensure_loggedin(func):
    @wraps(func)
    def internal_func(*args, **kwargs):
        if get_current_user() is None:
            return redirect(url_for('home_page'))
        else:
            return func(*args, **kwargs)
    return internal_func


def get_current_user():
    user_id = request.cookies.get('id')
    return database.User.query.get(user_id)


def check_user_credentials(email, password):
    found_user = database.User.query.filter_by(email=email).first()
    if found_user is None:
        return False, "No user found with email:{}".format(email), -1

    if found_user.password != password:
        return False, "Incorrect password", -1
    return True, "User credentials correct", found_user.id


def make_login_response(resp, user_id):
    resp = make_response(resp)
    resp.set_cookie(b'id', str(user_id).encode())
    return resp


def make_logout_response(resp):
    resp = make_response(resp)
    resp.set_cookie(b'id', b'', expires=0)
    return resp


@app.route('/login', methods=['POST'])
def login():
    if get_current_user() is not None:
        return redirect(url_for('home_page'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        result, message, user_id = check_user_credentials(email, password)
        if not result:
            return "Login failed. Reason: {}".format(message), 401
        print("User logged in successfully for id:{}".format(user_id))
        return make_login_response(redirect(url_for('home_page')), user_id)


@app.route('/item/<id>')
def show_item(id):
    item = database.Item.query.get(id)
    if item is None:
        return "Item not found", 404

    seller_items = database.SellerItem.query.filter_by(item_id=item.id).all()
    return render_template('item.html', item=item, seller_items=seller_items)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if get_current_user() is not None:
        return redirect(url_for('home_page'))
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Create new user
        new_user = database.User(
            name=name, username=username, email=email, password=password)
        new_user = database.save_object(new_user)
        # Return to homepage
        return make_login_response(redirect(url_for('home_page')), new_user.id)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if get_current_user() is None:
        return redirect(url_for('home_page'))
    return make_logout_response(redirect(url_for('home_page')))


@app.route('/')
def index():
    return redirect(url_for('home_page'))


@app.route('/home')
def home_page():
    return render_template("home.html", items=database.Item.query.all(), current_user=get_current_user())


@app.route('/buy/<seller_id>/<item_id>')
@ensure_loggedin
def buy_item(seller_id, item_id):
    user = get_current_user()
    selleritem = database.SellerItem.query.filter_by(
        seller_id=seller_id, item_id=item_id).all()[0]
    placed_order = order_handler.buy_now(user, selleritem)
    return render_template('order.html', order=placed_order)


@app.route('/cart/add/<seller_id>/<item_id>')
@ensure_loggedin
def add_to_cart(seller_id, item_id):
    user = get_current_user()
    selleritem = database.SellerItem.query.filter_by(
        seller_id=seller_id, item_id=item_id).all()[0]
    order_handler.add_to_cart(user, selleritem)
    return redirect(url_for('view_cart'))


@app.route('/cart/remove/<order_id>')
@ensure_loggedin
def remove_from_cart(order_id):
    user = get_current_user()
    order_handler.remove_from_cart(user, order_id)
    return redirect(url_for('view_cart'))


@app.route('/cart/checkout')
@ensure_loggedin
def checkout_cart():
    user = get_current_user()
    order_handler.checkout_cart(user)
    return redirect(url_for('home_page'))


@app.route('/cart/view')
@ensure_loggedin
def view_cart():
    user = get_current_user()
    cart_orders = order_handler.display_cart(user)
    total = 0
    for cart_order in cart_orders:
        total += cart_order.total()
    return render_template('cart.html', orders=cart_orders, total=total)


if __name__ == "__main__":
    app.run(debug=True)
