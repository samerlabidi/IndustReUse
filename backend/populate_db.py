import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.models.models import User, Material, Transaction, UserRole, TransactionStatus
from app.core.security import get_password_hash
import random
from datetime import datetime, timedelta

def populate_db():
    db = SessionLocal()
    try:
        # Create some regular users
        users = []
        companies = ["EcoTech", "GreenCycle", "ReuseHub", "CircularInc", "WasteNot"]
        for i in range(5):
            user = User(
                email=f"user{i+1}@example.com",
                username=f"user{i+1}",
                hashed_password=get_password_hash("password123"),
                company_name=companies[i],
                role=UserRole.USER.value
            )
            db.add(user)
            users.append(user)
        db.commit()

        # Create materials
        materials = []
        material_types = [
            ("Recycled Steel", "Metalworks", "kg", "Ben Arous", "Used"),
            ("Plastic Granules", "Plastics", "kg", "Megrine", "New"),
            ("Wood Scraps", "Furniture", "kg", "Rades", "Scrap"),
            ("Glass Cullet", "Glass", "tons", "Tunis", "Recycled"),
            ("Textile Waste", "Textiles", "kg", "Sfax", "Used"),
            ("Paper Pulp", "Paper", "tons", "Sousse", "Recycled"),
            ("Metal Shavings", "Manufacturing", "kg", "Bizerte", "Scrap"),
            ("Rubber Waste", "Automotive", "kg", "Gabes", "Used")
        ]

        for mat_type in material_types:
            for user in users:
                material = Material(
                    name=mat_type[0],
                    industry=mat_type[1],
                    quantity=random.randint(100, 1000),
                    unit=mat_type[2],
                    location=mat_type[3],
                    condition=mat_type[4],
                    description=f"High quality {mat_type[0].lower()} available for recycling",
                    status="available",
                    owner_id=user.id,
                    provider=user.company_name
                )
                db.add(material)
                materials.append(material)
        db.commit()

        # Create transactions
        statuses = [status.value for status in TransactionStatus]
        for _ in range(20):  # Create 20 transactions
            from_user = random.choice(users)
            to_user = random.choice([u for u in users if u != from_user])
            material = random.choice(materials)
            
            transaction = Transaction(
                material_id=material.id,
                from_owner_id=from_user.id,
                to_owner_id=to_user.id,
                quantity=random.randint(10, 100),
                status=random.choice(statuses),
                message=f"Request for {material.name}",
                delivery_method=random.choice(["Pickup", "Delivery", "Shipping"]),
                delivery_date=(datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                created_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            db.add(transaction)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_db()