from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.services.material_service import MaterialService
from app.schemas.material import MaterialResponse, MaterialCreate, MaterialUpdate
from app.core.dependencies import get_current_user
from app.models.models import User, UserRole
from app.models.models import Material
from app.db.database import get_db

router = APIRouter(prefix="/materials")

@router.get("", response_model=List[MaterialResponse])
async def get_materials(
    current_user = Depends(get_current_user),
    service: MaterialService = Depends()
):
    try:
        materials = await service.get_materials()
        return materials
    except Exception as e:
        print(f"Error in get_materials route: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=MaterialResponse)
async def create_material(
    material: MaterialCreate,
    current_user: User = Depends(get_current_user),
    service: MaterialService = Depends()
):
    try:
        return await service.create_material(material, current_user.id)
    except Exception as e:
        print(f"Error creating material: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{material_id}")
async def delete_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    service: MaterialService = Depends()
):
    try:
        await service.delete_material(material_id, current_user.id)
        return {"message": "Material deleted successfully"}
    except Exception as e:
        print(f"Error deleting material: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{material_id:int}", response_model=MaterialResponse)
async def get_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material 

@router.put("/{material_id}", response_model=MaterialResponse)
async def update_material(
    material_id: int,
    material_update: MaterialUpdate,
    current_user: User = Depends(get_current_user),
    service: MaterialService = Depends()
):
    try:
        # Get the material first to check ownership
        material = await service.get_material(material_id)
        if not material:
            raise HTTPException(status_code=404, detail="Material not found")
        
        # Allow update if user is admin or the owner of the material
        if current_user.role != UserRole.ADMIN and material.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only update your own materials")
        
        return await service.update_material(material_id, material_update)
    except Exception as e:
        print(f"Error updating material: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 