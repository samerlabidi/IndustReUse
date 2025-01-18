import pandas as pd
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import MaterialDB, SessionLocal  # Assuming your database models and session setup are in `main.py`

# Define industries
industries = [
    "Automotive", "Electronics", "Textile", "Pharmaceuticals", "Food Processing",
    "Metalworks", "Plastics", "Renewable Energy", "Construction Materials",
    "Aerospace", "Defense", "Furniture", "Chemicals", "Packaging", "Agriculture Machinery"
]

# Define Tunisian-style prefixes, names, and locations in Ben Arous
tunisian_prefixes = [
    "Société", "Groupe", "Industrie", "Entreprise", "Usine", "Manufacture", "Fédération"
]
ben_arous_locations = [
    "Ben Arous", "Bir El Kassâa", "Mégrine", "Rades", "Fouchana", "El Mourouj", "Ezzahra", "Mohamedia"
]

# Generate 100 Ben Arous-specific enterprise names
ben_arous_enterprise_names = [
    f"{random.choice(tunisian_prefixes)} {random.choice(['Ben Arous', 'Cité', 'El Fath', 'Hannibal'])} "
    f"{random.choice(['Industries', 'Technologies', 'Solutions', 'Productions', 'Transformations'])} de {random.choice(ben_arous_locations)}"
    for _ in range(100)
]

# Generate data
data = {
    "name": ben_arous_enterprise_names,
    "industry": [random.choice(industries) for _ in range(100)],
    "quantity": [round(random.uniform(10, 1000), 2) for _ in range(100)],
    "unit": [random.choice(["kg", "tons", "liters"]) for _ in range(100)],
    "location": [random.choice(ben_arous_locations) for _ in range(100)],
    "condition": [random.choice(["new", "used", "scrap"]) for _ in range(100)],
    "description": [f"Material in {random.choice(['excellent', 'good', 'fair', 'poor'])} condition." for _ in range(100)]
}

# Create DataFrame
df = pd.DataFrame(data)

# Insert into the database
def populate_database():
    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            material = MaterialDB(
                name=row["name"],
                industry=row["industry"],
                quantity=row["quantity"],
                unit=row["unit"],
                location=row["location"],
                condition=row["condition"],
                description=row["description"]
            )
            db.add(material)
        db.commit()
        print("Data added successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()
