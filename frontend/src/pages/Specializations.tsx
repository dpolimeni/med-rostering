import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { Plus } from 'lucide-react';

interface Specialization {
  id: string;
  name: string;
  description?: string;
}

export default function Specializations() {
  const { token, userData } = useAuth();
  const [specializations, setSpecializations] = useState<Specialization[]>([]);
  const [newSpecialization, setNewSpecialization] = useState({ name: '', description: '' });
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    const fetchSpecializations = async () => {
      if (userData?.specializations) {
        try {
          const detailedSpecializations = await Promise.all(
            userData.specializations.map(async (spec) => {
              const response = await axios.get(`/api/specializations/${spec.id}`, {
                headers: { Authorization: `Bearer ${token}` }
              });
              return response.data;
            })
          );
          setSpecializations(detailedSpecializations);
        } catch (error) {
          console.error('Failed to fetch specializations:', error);
        }
      }
    };

    fetchSpecializations();
  }, [userData, token]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/specializations', newSpecialization, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSpecializations([...specializations, response.data]);
      setNewSpecialization({ name: '', description: '' });
      setIsCreating(false);
    } catch (error) {
      console.error('Failed to create specialization:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-900">Specializations</h1>
        <button
          onClick={() => setIsCreating(true)}
          className="flex items-center px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
        >
          <Plus className="h-5 w-5 mr-2" />
          New Specialization
        </button>
      </div>

      {isCreating && (
        <form onSubmit={handleCreate} className="bg-white p-6 rounded-lg shadow-md">
          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Name
              </label>
              <input
                type="text"
                id="name"
                value={newSpecialization.name}
                onChange={(e) => setNewSpecialization({ ...newSpecialization, name: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Description
              </label>
              <textarea
                id="description"
                value={newSpecialization.description}
                onChange={(e) => setNewSpecialization({ ...newSpecialization, description: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                rows={3}
              />
            </div>
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => setIsCreating(false)}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
              >
                Create
              </button>
            </div>
          </div>
        </form>
      )}

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {specializations.map((spec) => (
          <div key={spec.id} className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-900">{spec.name}</h3>
            {spec.description && (
              <p className="mt-2 text-gray-600">{spec.description}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}