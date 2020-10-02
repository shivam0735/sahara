import database
from flask import Flask, url_for, redirect, render_template, request

cart = {}

app = Flask(__name__,
    static_folder="static",
    template_folder="static/templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sahara_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database.db.init_app(app)

@app.route('/login')
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        return login_user(request.data)

@app.route('/signup')
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        pass
        # Create new user
        
        # Login user
        # Return to homepage


@app.route('/')
def index():
    return redirect(url_for('home_page'))

@app.route('/home')
def home_page():
    return render_template("home.html", items=database.Item.query.all())

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