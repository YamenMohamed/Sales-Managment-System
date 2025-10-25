from sqlalchemy.orm import Session
from backend import models, schema



# ------------------ OrderItems CRUD ------------------

# get all ordered Items
def get_orderItems(db:Session):
    return db.query(models.OrderItem).all()

# get all the products in a specific Order
def get_orderItems(db:Session,order_id:int):
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()

# get a specific Order Item
def get_orderItem(db:Session,orderItem_id:int):
    return db.query(models.OrderItem).filter(models.OrderItem.id == orderItem_id).first()

# create a new order Item
def create_orderItem(db:Session,orderItem :schema.OrderItemCreate):
    from backend.crud.product_crud import get_product
    from backend.crud.order_crud import get_order
    product = get_product(db, orderItem.product_id)
    if not product:
        raise Exception("Product not found")

    if product.stock_quantity < orderItem.quantity:
        raise Exception("Not enough stock for this product")

    item_price = orderItem.quantity * product.price
    new_orderItem = models.OrderItem(
        order_id = orderItem.order_id,
        product_id = orderItem.product_id,
        quantity = orderItem.quantity,
        price = item_price
    )
    db.add(new_orderItem)

    # Update the total_price of the order
    order = get_order(db,orderItem.order_id)
    if not order:
        raise Exception("Order not found")

    order.total_price += item_price


    db.commit()
    db.refresh(new_orderItem)
    db.refresh(order)
    return new_orderItem



def delete_orderItem(db:Session,orderItem_id):
    from backend.crud.product_crud import get_product
    orderItem = get_orderItem(db,orderItem)

    if orderItem:
        product = get_product(db,orderItem.product_id)
        product.stock_quantity += orderItem.quantity

        # update total_price in Order after decreasing an item
        order = db.query(models.Order).filter(models.Order.id == orderItem.order_id).first()
        if order:
            order.total_price -= orderItem.price

        db.delete(orderItem)
        db.commit()
        print("OrderItem is deleted successfully !!")
        return True
    
    print("OrderItem not Found !!")
    return False