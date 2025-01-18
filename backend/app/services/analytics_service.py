from datetime import datetime, timedelta
from sqlalchemy import func
from app.models.models import Transaction
from app.models.models import Material
from app.models.models import User
from typing import Dict, Any, List
from fastapi import Depends
from app.db.database import get_db

class AnalyticsService:
    def __init__(self, db=Depends(get_db)):
        self.db = db

    async def get_stats(self) -> Dict[str, Any]:
        # Get basic stats for all time
        total_transactions = self.db.query(Transaction).count()
        active_materials = self.db.query(Material).filter(Material.quantity > 0).count()
        total_users = self.db.query(User).count()
        
        # Calculate success rate
        completed_transactions = self.db.query(Transaction).filter(
            Transaction.status == 'COMPLETED'
        ).count()
        success_rate = (completed_transactions / total_transactions * 100) if total_transactions > 0 else 0

        # Get status distribution
        status_distribution = self.db.query(
            Transaction.status,
            func.count(Transaction.id).label('count')
        ).group_by(Transaction.status).all()

        # Get top materials
        top_materials = self.db.query(
            Material.name,
            func.count(Transaction.id).label('transactions')
        ).join(Transaction).group_by(Material.name).order_by(
            func.count(Transaction.id).desc()
        ).limit(10).all()

        # Get transaction locations
        transaction_locations = self.db.query(
            Material.location,
            func.count(Transaction.id).label('count')
        ).join(Transaction).group_by(Material.location).all()

        return {
            "totalTransactions": total_transactions,
            "activeMaterials": active_materials,
            "totalUsers": total_users,
            "successRate": round(success_rate, 2),
            "materialsTrend": "+12",
            "transactionsTrend": "+5",
            "successRateTrend": "+18",
            "usersTrend": "+2",
            "statusDistribution": [
                {"status": s.status, "value": s.count}
                for s in status_distribution
            ],
            "topMaterials": [
                {"name": m.name, "transactions": m.transactions}
                for m in top_materials
            ],
            "transactionLocations": [
                {"location": loc.location, "count": loc.count}
                for loc in transaction_locations
                if loc.location in [
                    'Tunis', 'Sfax', 'Sousse', 'Bizerte', 
                    'Gabes', 'Ben Arous', 'Megrine', 'Rades'
                ]
            ]
        } 