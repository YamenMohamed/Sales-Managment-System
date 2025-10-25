from sqlalchemy.orm import Session
from backend import models, schema


# ------------------ Category CRUD ------------------

def get_categories(db:Session):
    return db.query(models.Category).all()

def get_category(db:Session,category_id):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def create_category(db:Session,category:schema. CategoryCreate):
    # Check if the new category already exists
    existing_category = db.query(models.Category).filter(
        models.Category.name == category.name
    ).first()

    if existing_category:
        return category
    
    # Otherwise create a new one
    new_category = models.Category(name = category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def delete_category(db:Session, category_id:int):
    category = get_category(db,category_id)
    if category:
        db.delete(category)
        db.commit()
        print("Category deleted successfuly !")
        return True
    print("Category not Found !!")
    return False
