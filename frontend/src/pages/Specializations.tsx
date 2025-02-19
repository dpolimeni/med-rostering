import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Plus } from 'lucide-react';
import api from '../api';
import { UserData, Specialization, Department} from '../types';

api.defaults.baseURL = 'http://localhost:8000';

interface SpecializationData {
    specializations: Specialization[];
  }

export default function Specializations() {
  const { token, userData } = useAuth();
  const [stateData, setStateData] = useState<SpecializationData>({
    specializations: []
  });
  const [newSpecialization, setNewSpecialization] = useState({ 
    name: '', 
    description: '', 
    shifts: {} as Record<string, { start: string; end: string }> 
  });
  const [isCreating, setIsCreating] = useState(false);
  const [shiftKey, setShiftKey] = useState('');
  const [shiftStartTime, setShiftStartTime] = useState('');
  const [shiftEndTime, setShiftEndTime] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSpecialization = async (specId: string) => {
      setIsLoading(true);
      setError(null);
      
      try {
        // First, fetch the list of user's specialization IDs
        console.log(specId);
        
        // Then fetch detailed information for the specialization
        const detailedSpecialization = await api.get(`/specializations/${specId}`, {
            headers: { Authorization: `Bearer ${token}` }
            });
        console.log("DETAILED SPECIALIZATION", detailedSpecialization);
        
        setStateData(prevState => ({
          ...prevState,
          specializations: [detailedSpecialization.data]
        }));
        
      } catch (error) {
        console.error('Failed to fetch specializations:', error);
        setError('Failed to load specializations. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    if (token && userData && userData.specialization) {
        console.log("USER DATA IN SPEC", userData);
        fetchSpecialization(userData.specialization.id);
    } else {
        setIsLoading(false);
    }
  }, [token, userData]);

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
      const response = await api.post('/specializations/create', newSpecialization, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Append stateData with the new specialization
      setStateData(prevState => ({
        ...prevState,
        specializations: [
          ...(prevState.specializations || []),
          response.data
        ]
      }));
    
      setNewSpecialization({ 
        name: '', 
        description: '', 
        shifts: {} 
      });
      setIsCreating(false);
    } catch (error) {
      console.error('Failed to create specialization:', error);
      setError('Failed to create specialization. Please try again.');
    }
  };

  const formatTimeDisplay = (shift: { start: string; end: string }) => {
    return `${shift.start} - ${shift.end}`;
  };

  if (isLoading) {
    return <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>;
  }

  if (error) {
    return <div className="p-4 bg-red-50 text-red-700 rounded-md">
      <p>{error}</p>
      <button 
        onClick={() => window.location.reload()} 
        className="mt-2 px-4 py-2 bg-red-100 text-red-800 rounded-md hover:bg-red-200"
      >
        Retry
      </button>
    </div>;
  }

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

      {stateData.specializations.length === 0 ? (
        <div className="bg-gray-50 p-8 rounded-lg text-center">
          <p className="text-gray-600">No specializations found. Create your first one!</p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {stateData.specializations.map((spec) => (
            <div key={spec.id} className="bg-white p-6 rounded-lg shadow-md">
              <dl className="space-y-4">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Name:</dt>
                  <dd className="text-lg font-semibold text-gray-900">{spec.name}</dd>
                </div>
                
                <div>
                  <dt className="text-sm font-medium text-gray-500">Description:</dt>
                  <dd className="text-gray-600">{spec.description || "No description provided"}</dd>
                </div>
                
                <div>
                  <dt className="text-sm font-medium text-gray-500">Shifts:</dt>
                  <dd>
                    {spec.shifts && Object.entries(spec.shifts).length > 0 ? (
                      <ul className="mt-1 space-y-1">
                        {Object.entries(spec.shifts).map(([key, timeWindow]) => (
                          <li key={key} className="text-gray-600">
                            <span className="font-medium">{key}:</span> {' '}
                            {typeof timeWindow === 'string' 
                              ? timeWindow 
                              : formatTimeDisplay(timeWindow)
                            }
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <span className="text-gray-500 italic">No shifts defined</span>
                    )}
                  </dd>
                </div>
              </dl>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}