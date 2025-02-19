import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Plus } from 'lucide-react';
import api from '../api';

api.defaults.baseURL = 'http://localhost:8000';

interface Specialization {
  id: string;
  name: string;
  description?: string;
  shifts: Record<string, { start: string; end: string }>;
}

export default function Specializations() {
  const { token, userData } = useAuth();
  const [specializations, setSpecializations] = useState<Specialization[]>([]);
  const [newSpecialization, setNewSpecialization] = useState({ 
    name: '', 
    description: '', 
    shifts: {} as Record<string, { start: string; end: string }> 
  });
  const [isCreating, setIsCreating] = useState(false);
  const [shiftKey, setShiftKey] = useState('');
  const [shiftStartTime, setShiftStartTime] = useState('');
  const [shiftEndTime, setShiftEndTime] = useState('');

  useEffect(() => {
    const fetchSpecializations = async () => {
      if (userData?.specializations) {
        try {
          const detailedSpecializations = await Promise.all(
            userData.specializations.map(async (spec) => {
              const response = await api.get(`/specializations/${spec.id}`, {
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

  const handleAddShift = () => {
    if (shiftKey && shiftStartTime && shiftEndTime) {
      setNewSpecialization((prev) => ({
        ...prev,
        shifts: { 
          ...prev.shifts, 
          [shiftKey]: { 
            start: shiftStartTime, 
            end: shiftEndTime 
          } 
        }
      }));
      setShiftKey('');
      setShiftStartTime('');
      setShiftEndTime('');
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      console.log(token);
      const response = await api.post('/specializations/create', newSpecialization, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSpecializations([...specializations, response.data]);
      setNewSpecialization({ 
        name: '', 
        description: '', 
        shifts: {} 
      });
      setIsCreating(false);
    } catch (error) {
      console.error('Failed to create specialization:', error);
    }
  };

  const formatTimeDisplay = (shift: { start: string; end: string }) => {
    return `${shift.start} - ${shift.end}`;
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
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <input
                type="text"
                value={newSpecialization.name}
                onChange={(e) => setNewSpecialization({ ...newSpecialization, name: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                value={newSpecialization.description}
                onChange={(e) => setNewSpecialization({ ...newSpecialization, description: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                rows={3}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Shifts</label>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
                <input
                  type="text"
                  placeholder="Shift name (e.g. morning)"
                  value={shiftKey}
                  onChange={(e) => setShiftKey(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
                <div className="flex items-center">
                  <label className="block text-sm font-medium text-gray-700 mr-2">Start:</label>
                  <input
                    type="time"
                    value={shiftStartTime}
                    onChange={(e) => setShiftStartTime(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
                <div className="flex items-center">
                  <label className="block text-sm font-medium text-gray-700 mr-2">End:</label>
                  <input
                    type="time"
                    value={shiftEndTime}
                    onChange={(e) => setShiftEndTime(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  />
                </div>
                <button 
                  type="button" 
                  onClick={handleAddShift} 
                  className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
                >
                  Add
                </button>
              </div>
              <ul className="mt-2">
                {Object.entries(newSpecialization.shifts).map(([key, timeWindow]) => (
                  <li key={key} className="text-gray-600">
                    {key}: {formatTimeDisplay(timeWindow)}
                  </li>
                ))}
              </ul>
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
            {spec.description && <p className="mt-2 text-gray-600">{spec.description}</p>}
            {spec.shifts && (
              <div className="mt-4">
                <h4 className="font-medium text-gray-700">Shifts:</h4>
                <ul className="mt-2 text-gray-600">
                  {Object.entries(spec.shifts).map(([key, timeWindow]) => (
                    <li key={key} className="py-1">
                      <span className="font-medium">{key}:</span> {' '}
                      {typeof timeWindow === 'string' 
                        ? timeWindow // Handle old format
                        : formatTimeDisplay(timeWindow) // Handle new format
                      }
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}