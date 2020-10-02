
users = []
items = []
sellers = []

class User:
    def __init__(self, _id, name, address, password):
        self.id = _id 
        self.name = name
        self.address = address
        self.password = password

class Item:
    def __init__(self, _id, title, description, price, qty, img_url='/static/img/placeholder_item.jpg'):
        self.id = _id
        self.title = title
        self.description = description
        self.price = price
        self.qty = qty
        self.img_url = img_url

# class Seller:
#     def __init__(self, name):
#         self.name = name

def seed_db():
    users.append(User(1, "Rounaq", "C-369, Ground Floor, Yojana Vihar", "rounaq"))
    users.append(User(2, "Shivam", "C-369, Ground Floor, Yojana Vihar", "rounaq"))
    items.append(Item(1, "Pencil", "writing tool", 2.0, 4, img_url='https://cdn5.vectorstock.com/i/1000x1000/22/49/yellow-pencil-symbol-icon-design-beautiful-vector-21872249.jpg'))
    items.append(Item(2, "Eraser", "erasing tool", 1.5, 10, img_url="https://5.imimg.com/data5/SR/PX/MY-50438317/non-dust-eraser-500x500.jpg"))
    items.append(Item(3, "Pen", "writing tool", 2.5, 10, img_url='https://cdn-media.williampenn.net/media/catalog/product/cache/image/360x310/e9c3970ab036de70892d86c6d221abfe/w/p/wp01709-a.jpg'))

def get_item_by_id(search_id):
    for item in items:
        if item.id == search_id:
            return item
    return None

def get_user_by_id(search_id):
    for user in users:
        if user.id == search_id:
            return user
    return None
