import React from 'react';
import { useAuth } from '../contexts/AuthContext';

export default function Departments() {
  const { userData } = useAuth();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Departments</h1>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {userData?.departments.map((dept) => (
          <div key={dept.id} className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold text-gray-900">{dept.name}</h3>
          </div>
        ))}
      </div>
    </div>
  );
}