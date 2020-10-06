import database
from flask import Flask, url_for, redirect, render_template, request, make_response

cart = {}

app = Flask(__name__,
    static_folder="static",
    template_folder="static/templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sahara_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.db.init_app(app)

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
    
    seller_items = database.SellerItem.query.filter_by(item_id=item.id)
    seller_data = []
    for seller_item in seller_items:
        seller_data_row = {}
        seller_data_row['quantity'] = seller_item.quantity
        seller_data_row['price'] = seller_item.price
        seller_data_row['name'] = seller_item.seller.name
        seller_data.append(seller_data_row)

    return render_template('item.html', item=item, seller_data=seller_data)

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
        new_user = database.User(name=name, username=username, email=email, password=password)
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

@app.route('/buy/<item_id>')
def buy_item(item_id):
    item = database.get_item_by_id(int(item_id))
    if item is None:
        return "Item not found", 404
    
    if item.qty > 0:
        item.qty -= 1
    else:
        return "Item not available", 400
    return render_template('after_buy.html', item=item)

@app.route('/cart/add/<item_id>')
def add_to_cart(item_id):
    item_id = int(item_id)
    item = database.get_item_by_id(item_id)
    if item is None:
        return "Item not found", 404
    
    if item.qty > 0:
        item.qty -= 1
        if item_id in cart:
            cart[item_id] += 1
        else:
            cart[item_id] = 1
    else:
        return "Item not available", 400
    return redirect(url_for('home_page'))

@app.route('/cart/remove/<item_id>')
def remove_from_cart(item_id):
    item_id = int(item_id)
    item = database.get_item_by_id(item_id)
    if item is None:
        return "Item not found", 404
    
    if item_id not in cart:
        return "Item not added to cart", 400
    
    cart[item_id] -= 1
    if cart[item_id] == 0:
        cart.pop(item_id)
    
    item.qty += 1

    return redirect(url_for('view_cart'))
    

@app.route('/cart/checkout')
def checkout_cart():
    global cart
    for item_id in cart:
        item = database.get_item_by_id(item_id)
        if item is None:
            return "Invalid item present in cart", 400
        if item.qty < cart[item_id]:
            return "Invalid item quantity present in cart", 400
 
    for item_id in cart:
        item_qty = cart[item_id]
        item = database.get_item_by_id(item_id)
        item.qty -= item_qty
    
    cart = {}
    
    return redirect(url_for('home_page'))


@app.route('/cart/view')
def view_cart():
    for item_id in cart:
        item = database.get_item_by_id(item_id)
        if item is None:
            return "Invalid item present in cart", 400
        if item.qty < cart[item_id]:
            return "Invalid item quantity present in cart", 400
    
    item_data = {}
    total = 0
    for item_id in cart:
        item = database.get_item_by_id(item_id)
        item_data[item] = cart[item_id]
        total += item.price * cart[item_id]
    return render_template('cart.html', item_data=item_data, total=total)

if __name__ == "__main__":
    app.run(debug=True)