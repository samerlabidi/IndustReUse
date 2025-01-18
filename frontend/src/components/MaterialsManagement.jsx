import React, { useState, useEffect } from 'react';
import { materialsApi } from '../../services/materialsApi';
import { useAuth } from '../../hooks/useAuth';

const MaterialsManagement = () => {
  const [materials, setMaterials] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    loadMaterials();
  }, []);

  const loadMaterials = async () => {
    try {
      const response = await materialsApi.getAll();
      setMaterials(response.data);
    } catch (error) {
      console.error('Failed to load materials:', error);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this material?')) {
      try {
        await materialsApi.delete(id);
        await loadMaterials();
      } catch (error) {
        console.error('Failed to delete material:', error);
      }
    }
  };

  const handleEdit = async (id) => {
    // Navigate to edit page or open edit modal
    window.location.href = `/admin/materials/${id}/edit`;
  };

  if (user?.role !== 'ADMIN') {
    return <div>Access denied. Admin only area.</div>;
  }

  const getConditionStyle = (condition) => {
    switch (condition.toLowerCase()) {
      case 'new': return 'bg-green-500 text-white';
      case 'used': return 'bg-orange-500 text-white';
      case 'scrap': return 'bg-red-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Materials Management</h2>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white rounded-lg overflow-hidden">
          <thead className="bg-blue-500 text-white">
            <tr>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Industry</th>
              <th className="px-4 py-3">Quantity</th>
              <th className="px-4 py-3">Unit</th>
              <th className="px-4 py-3">Location</th>
              <th className="px-4 py-3">Condition</th>
              <th className="px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {materials.map(material => (
              <tr key={material.id} className="border-b hover:bg-gray-50">
                <td className="px-4 py-3">{material.name}</td>
                <td className="px-4 py-3">
                  <span className="px-2 py-1 rounded-full bg-blue-100 text-blue-800">
                    {material.industry}
                  </span>
                </td>
                <td className="px-4 py-3">{material.quantity}</td>
                <td className="px-4 py-3">{material.unit}</td>
                <td className="px-4 py-3">{material.location}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-1 rounded-full ${getConditionStyle(material.condition)}`}>
                    {material.condition}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex space-x-2">
                    <button 
                      onClick={() => handleEdit(material.id)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      Edit
                    </button>
                    <button 
                      onClick={() => handleDelete(material.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MaterialsManagement; 