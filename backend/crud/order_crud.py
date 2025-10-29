from sqlalchemy.orm import Session , joinedload
from backend import models, schema
from .orderItem_crud import *
# ------------------ Order CRUD ------------------

# all orders made 
def get_orders(db: Session):
    orders = db.query(models.Order).options(
        joinedload(models.Order.items).joinedload(models.OrderItem.product)
    ).all()

    result = []
    for order in orders:
        result.append({
            "id": order.id,
            "user_id": order.user_id,
            "order_date": str(order.order_date),
            "total_price": order.total_price,
            "items": [
                {
                    "product_name": item.product.name if item.product else "Unknown Product",
                    "quantity": item.quantity,
                    "item_price": item.price
                }
                for item in order.items
            ]
        })
    return result

# a specific Order
def get_order(db:Session,order_id:int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


# all orders by a specific user
def get_user_orders(db:Session,user_id:int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()

def get_orders_by_user(db: Session, user_id: int):
    orders = get_user_orders(db,user_id)

    result = []
    for order in orders:
        order_data = {
            "id": order.id,
            "user_id": order.user_id,
            "order_date": order.order_date,
            "total_price": order.total_price,
            "items": []
        }
        for item in order.items:
            order_data["items"].append({
                "product_name": item.product.name if item.product else "Unknown Product",
                "quantity": item.quantity,
                "item_price": item.price
            })
        result.append(order_data)
    return result




# Create new order
def create_order(db: Session, order: schema.OrderCreate):
    total_price = 0.0

    # Calculate total price and validate stock
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product or product.stock_quantity < item.quantity:
            raise Exception(f"Product {item.product_id} not available in stock.")
        total_price += item.quantity * product.price

    # Create order
    new_order = models.Order(
        user_id=order.user_id,
        order_date=order.order_date,
        total_price=total_price
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Add order items
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        product.stock_quantity -= item.quantity
        order_item = models.OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.quantity * product.price
        )
        db.add(order_item)

    db.commit()
    db.refresh(new_order)

    return {
        "id": new_order.id,
        "user_id": new_order.user_id,
        "order_date": str(new_order.order_date),
        "total_price": new_order.total_price,
        "items": [
            {
                "product_id": item.product_id,
                "product_name": item.product.name if item.product else "Unknown Product",
                "quantity": item.quantity,
                "item_price": item.price
            }
            for item in new_order.items
        ]
    }


def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)

    if order:
        # Return each product's stock before deleting the order
        orderItems = get_orderItems(db, order.id)
        for orderItem in orderItems:
            delete_orderItem(db, orderItem.id)

        db.delete(order)
        db.commit()
        print("Order deleted successfully !!")
        return True
    
    print("Order not Found !!")
    return False
