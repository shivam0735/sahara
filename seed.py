from database import db, User, Item, SellerItem, initialize_db

if __name__ == '__main__':
    initialize_db()

    user1 = User(name="Rounaq Jhunjhunu Wala", username="rjalfa", password="rounaq", email="rounaqwl66@gmail.com")
    user2 = User(name="Shivam Jhunjhunu Wala", username="shivam", password="shivam", email="shivamj2005@gmail.com")
    user3 = User(name="Anand Stationers", username="ast", password="vkj", email="anandstationers73@gmail.com")
    
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    db.session.commit()

    item1 = Item(title="Pencil", description="writing tool", img_url='https://cdn5.vectorstock.com/i/1000x1000/22/49/yellow-pencil-symbol-icon-design-beautiful-vector-21872249.jpg')
    item2 = Item(title="Eraser", description="erasing tool", img_url="https://5.imimg.com/data5/SR/PX/MY-50438317/non-dust-eraser-500x500.jpg")
    item3 = Item(title="Pen", description="writing tool")

    db.session.add(item1)
    db.session.add(item2)
    db.session.add(item3)
    db.session.commit()

    selleritem1 = SellerItem(item_id=item1.id, seller_id=user3.id, price=2.0, quantity=4)

    db.session.add(selleritem1)
    db.session.commit()

    db.session.commit()
    