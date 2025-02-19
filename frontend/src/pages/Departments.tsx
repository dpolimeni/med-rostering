import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Plus, Edit } from 'lucide-react';
import api from '../api';
import { Department, NewDepartment, UpdateDepartment } from '../types';

api.defaults.baseURL = 'http://localhost:8000';

interface DepartmentData {
  departments: Department[];
}

export default function Departments() {
  const { token, userData } = useAuth();
  const [stateData, setStateData] = useState<DepartmentData>({
    departments: []
  });
  const [newDepartment, setNewDepartment] = useState<NewDepartment>({
    name: '',
    description: '',
    type: 'low',
    users: [],
    constraints: [],
    specialization: ''
  });
  const [editDepartment, setEditDepartment] = useState<UpdateDepartment & { id: string } | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [constraintDay, setConstraintDay] = useState('');
  const [constraintShift, setConstraintShift] = useState('');

  useEffect(() => {
    const fetchDepartments = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        if (!userData?.specialization?.id) {
          throw new Error('No specialization ID found');
        }

        // Fetch departments associated with user's specialization
        const departmentsResponse = await Promise.all(
          userData.specialization.departments?.map((deptId: string) => 
            api.get(`/departments/${deptId}`, {
              params: { specialization_id: userData.specialization.id },
              headers: { Authorization: `Bearer ${token}` }
            })
          ) || []
        );
        
        const departmentsData = departmentsResponse.map(response => response.data);
        
        setStateData({
          departments: departmentsData
        });
        
      } catch (error) {
        console.error('Failed to fetch departments:', error);
        setError('Failed to load departments. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    if (token && userData && userData.specialization) {
      // Initialize the new department form with the current specialization ID
      setNewDepartment(prev => ({
        ...prev,
        specialization: userData.specialization.id
      }));
      
      fetchDepartments();
    } else {
      setIsLoading(false);
    }
  }, [token, userData]);

  const handleAddConstraint = () => {
    if (constraintDay && constraintShift) {
      if (isEditing && editDepartment) {
        setEditDepartment({
          ...editDepartment,
          constraints: [...editDepartment.constraints, [constraintDay, constraintShift]]
        });
      } else {
        setNewDepartment({
          ...newDepartment,
          constraints: [...newDepartment.constraints, [constraintDay, constraintShift]]
        });
      }
      setConstraintDay('');
      setConstraintShift('');
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await api.post('/departments/create', newDepartment, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setStateData(prevState => ({
        ...prevState,
        departments: [
          ...(prevState.departments || []),
          response.data
        ]
      }));
    
      setNewDepartment({
        name: '',
        description: '',
        type: 'low',
        users: [],
        constraints: [],
        specialization: userData?.specialization?.id || ''
      });
      setIsCreating(false);
    } catch (error) {
      console.error('Failed to create department:', error);
      setError('Failed to create department. Please try again.');
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editDepartment) return;
    
    try {
      const { id, ...updateData } = editDepartment;
      const response = await api.put(`/departments/${id}`, updateData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setStateData(prevState => ({
        ...prevState,
        departments: prevState.departments.map(dept => 
          dept.id === id ? response.data : dept
        )
      }));
    
      setEditDepartment(null);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update department:', error);
      setError('Failed to update department. Please try again.');
    }
  };

  const startEditing = (department: Department) => {
    setEditDepartment({
      id: department.id,
      name: department.name,
      description: department.description,
      type: department.type,
      users: department.users || [],
      constraints: department.constraints || []
    });
    setIsEditing(true);
    setIsCreating(false);
  };

  const getDayName = (day: string) => {
    const days: Record<string, string> = {
      'monday': 'Monday',
      'tuesday': 'Tuesday',
      'wednesday': 'Wednesday',
      'thursday': 'Thursday',
      'friday': 'Friday',
      'saturday': 'Saturday',
      'sunday': 'Sunday'
    };
    return days[day.toLowerCase()] || day;
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
        <h1 className="text-2xl font-semibold text-gray-900">Departments</h1>
        <button
          onClick={() => {
            setIsCreating(true);
            setIsEditing(false);
            setEditDepartment(null);
          }}
          className="flex items-center px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
        >
          <Plus className="h-5 w-5 mr-2" />
          New Department
        </button>
      </div>

      {/* Form for creating new department */}
      {isCreating && (
        <form onSubmit={handleCreate} className="bg-white p-6 rounded-lg shadow-md">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <input
                type="text"
                value={newDepartment.name}
                onChange={(e) => setNewDepartment({ ...newDepartment, name: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                value={newDepartment.description}
                onChange={(e) => setNewDepartment({ ...newDepartment, description: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                rows={3}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Type</label>
              <select
                value={newDepartment.type}
                onChange={(e) => setNewDepartment({ ...newDepartment, type: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Constraints</label>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                <select
                  value={constraintDay}
                  onChange={(e) => setConstraintDay(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="">Select day...</option>
                  <option value="monday">Monday</option>
                  <option value="tuesday">Tuesday</option>
                  <option value="wednesday">Wednesday</option>
                  <option value="thursday">Thursday</option>
                  <option value="friday">Friday</option>
                  <option value="saturday">Saturday</option>
                  <option value="sunday">Sunday</option>
                </select>
                <input
                  type="text"
                  placeholder="Shift ID"
                  value={constraintShift}
                  onChange={(e) => setConstraintShift(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
                <button 
                  type="button" 
                  onClick={handleAddConstraint} 
                  className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
                >
                  Add
                </button>
              </div>
              <ul className="mt-2">
                {newDepartment.constraints.map((constraint, index) => (
                  <li key={index} className="text-gray-600">
                    {getDayName(constraint[0])}: {constraint[1]}
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

      {/* Form for editing department */}
      {isEditing && editDepartment && (
        <form onSubmit={handleUpdate} className="bg-white p-6 rounded-lg shadow-md">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <input
                type="text"
                value={editDepartment.name}
                onChange={(e) => setEditDepartment({ ...editDepartment, name: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                value={editDepartment.description}
                onChange={(e) => setEditDepartment({ ...editDepartment, description: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                rows={3}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Type</label>
              <select
                value={editDepartment.type}
                onChange={(e) => setEditDepartment({ ...editDepartment, type: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Constraints</label>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                <select
                  value={constraintDay}
                  onChange={(e) => setConstraintDay(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  <option value="">Select day...</option>
                  <option value="monday">Monday</option>
                  <option value="tuesday">Tuesday</option>
                  <option value="wednesday">Wednesday</option>
                  <option value="thursday">Thursday</option>
                  <option value="friday">Friday</option>
                  <option value="saturday">Saturday</option>
                  <option value="sunday">Sunday</option>
                </select>
                <input
                  type="text"
                  placeholder="Shift ID"
                  value={constraintShift}
                  onChange={(e) => setConstraintShift(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
                <button 
                  type="button" 
                  onClick={handleAddConstraint} 
                  className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
                >
                  Add
                </button>
              </div>
              <ul className="mt-2">
                {editDepartment.constraints.map((constraint, index) => (
                  <li key={index} className="text-gray-600">
                    {getDayName(constraint[0])}: {constraint[1]}
                  </li>
                ))}
              </ul>
            </div>
            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => {
                  setIsEditing(false);
                  setEditDepartment(null);
                }}
                className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
              >
                Update
              </button>
            </div>
          </div>
        </form>
      )}

      {/* Display departments */}
      {stateData.departments.length === 0 ? (
        <div className="bg-gray-50 p-8 rounded-lg text-center">
          <p className="text-gray-600">No departments found. Create your first one!</p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {stateData.departments.map((dept) => (
            <div key={dept.id} className="bg-white p-6 rounded-lg shadow-md relative">
              <button
                onClick={() => startEditing(dept)}
                className="absolute top-4 right-4 p-1 text-gray-400 hover:text-blue-500"
                aria-label="Edit department"
              >
                <Edit className="h-5 w-5" />
              </button>
              
              <dl className="space-y-4">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Name:</dt>
                  <dd className="text-lg font-semibold text-gray-900">{dept.name}</dd>
                </div>
                
                <div>
                  <dt className="text-sm font-medium text-gray-500">Description:</dt>
                  <dd className="text-gray-600">{dept.description || "No description provided"}</dd>
                </div>
                
                <div>
                  <dt className="text-sm font-medium text-gray-500">Type:</dt>
                  <dd className="text-gray-600 capitalize">{dept.type}</dd>
                </div>
                
                <div>
                  <dt className="text-sm font-medium text-gray-500">Constraints:</dt>
                  <dd>
                    {dept.constraints && dept.constraints.length > 0 ? (
                      <ul className="mt-1 space-y-1">
                        {dept.constraints.map((constraint, index) => (
                          <li key={index} className="text-gray-600">
                            <span className="font-medium">{getDayName(constraint[0])}:</span> {constraint[1]}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <span className="text-gray-500 italic">No constraints defined</span>
                    )}
                  </dd>
                </div>
                
                <div>
                  <dt className="text-sm font-medium text-gray-500">Users:</dt>
                  <dd>
                    {dept.users && dept.users.length > 0 ? (
                      <div className="flex flex-wrap gap-1 mt-1">
                        {dept.users.map((userId, index) => (
                          <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                            {userId}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <span className="text-gray-500 italic">No users assigned</span>
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