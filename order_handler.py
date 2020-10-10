import database


def display_cart(user):
    return database.Order.query.filter_by(user_id=user.id, in_cart=True).all()

def create_order(user, selleritem, in_cart):
    order = database.Order(user_id=user.id,
                           item_id=selleritem.item_id,
                           seller_id=selleritem.seller_id,
                           quantity=selleritem.quantity,
                           price=selleritem.price,
                           is_complete=False,
                           in_cart=in_cart)

    database.save_object(order)
    return order


def add_to_cart(user, selleritem):
    cart_orders = display_cart(user)
    found = False
    found_order = None
    for cart_order in cart_orders:
        if cart_order.user == user and cart_order.item == selleritem.item and cart_order.seller == selleritem.seller:
            found = True
            found_order = cart_order
            break
    if found:
        found_order.quantity += 1
        return database.save_object(found_order)
    else:
        return create_order(user, selleritem, True)


def buy_now(user, selleritem):
    return create_order(user, selleritem, False)


def checkout_cart(user):
    cart_orders = display_cart(user)
    for order in cart_orders:
        order.in_cart = False
    database.save_objects(cart_orders)


def remove_from_cart(user, order_id):
    cart_orders = display_cart(user)
    found = False
    found_order = None
    for cart_order in cart_orders:
        if cart_order.id == order_id:
            found = True
            found_order = cart_order
            break
    if not found:
        return False
    database.remove_object(found_order)
    return True


def display_active_orders_user(user):
    return database.Order.query.filter_by(user_id=user.id, in_cart=False, is_complete=False).all()


def display_active_orders_seller(seller):
    return database.Order.query.filter_by(seller_id=seller.id, in_cart=False, is_complete=False).all()


def display_past_orders_user(user):
    return database.Order.query.filter_by(user_id=user.id, in_cart=False, is_complete=True).all()


def display_past_orders_seller(seller):
    return database.Order.query.filter_by(seller_id=seller.id, in_cart=False, is_complete=True).all()


def deliver_order(order):
    order.is_complete = True
    database.save_object(order)
    return order
