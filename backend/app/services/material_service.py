from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from app.db.database import get_db
from app.models.models import Material
from app.schemas.material import MaterialResponse, MaterialCreate, MaterialUpdate
from datetime import datetime

class MaterialService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def get_materials(self) -> List[MaterialResponse]:
        try:
            materials = self.db.query(Material).all()
            return [
                MaterialResponse(
                    id=material.id,
                    name=material.name,
                    industry=material.industry,
                    quantity=material.quantity,
                    unit=material.unit,
                    location=material.location,
                    condition=material.condition,
                    description=material.description,
                    status=material.status or "available",
                    created_at=material.created_at or datetime.utcnow(),
                    owner_id=material.owner_id
                )
                for material in materials
            ]
        except Exception as e:
            print(f"Error in get_materials service: {e}")
            raise e

    async def create_material(self, material_data: MaterialCreate, owner_id: int) -> MaterialResponse:
        try:
            new_material = Material(
                **material_data.model_dump(),
                owner_id=owner_id,
                created_at=datetime.utcnow()
            )
            self.db.add(new_material)
            self.db.commit()
            self.db.refresh(new_material)
            return MaterialResponse.model_validate(new_material)
        except Exception as e:
            self.db.rollback()
            print(f"Error creating material: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_material(self, material_id: int, user_id: int) -> None:
        try:
            material = self.db.query(Material).filter(Material.id == material_id).first()
            if not material:
                raise HTTPException(status_code=404, detail="Material not found")
            
            # Optional: Check if user has permission to delete
            if material.owner_id != user_id:
                raise HTTPException(status_code=403, detail="Not authorized to delete this material")

            self.db.delete(material)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting material: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def get_material(self, material_id: int) -> Material:
        material = self.db.query(Material).filter(Material.id == material_id).first()
        return material 

    async def update_material(self, material_id: int, material_update: MaterialUpdate) -> MaterialResponse:
        try:
            material = self.db.query(Material).filter(Material.id == material_id).first()
            if not material:
                raise HTTPException(status_code=404, detail="Material not found")

            # Update only provided fields
            update_data = material_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(material, field, value)

            self.db.commit()
            self.db.refresh(material)
            
            return MaterialResponse.model_validate(material)
        except Exception as e:
            self.db.rollback()
            print(f"Error updating material: {e}")
            raise HTTPException(status_code=500, detail=str(e)) 