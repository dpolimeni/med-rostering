import React, { useState } from 'react';
import { Calendar as CalendarIcon } from 'lucide-react';
import { User, ShiftType } from '../types';

interface ShiftFormProps {
  users: User[];
  onAddShift: (userId: string, date: Date, type: ShiftType) => void;
}

export function ShiftForm({ users, onAddShift }: ShiftFormProps) {
  const [userId, setUserId] = useState('');
  const [date, setDate] = useState('');
  const [shiftType, setShiftType] = useState<ShiftType>('morning');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (userId && date) {
      onAddShift(userId, new Date(date), shiftType);
      setDate('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-4 rounded-lg shadow">
      <div>
        <label className="block text-sm font-medium text-gray-700">User</label>
        <select
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        >
          <option value="">Select a user</option>
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Date</label>
        <div className="mt-1 relative rounded-md shadow-sm">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <CalendarIcon className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 sm:text-sm border-gray-300 rounded-md"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Shift Type</label>
        <select
          value={shiftType}
          onChange={(e) => setShiftType(e.target.value as ShiftType)}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        >
          <option value="morning">Morning Shift</option>
          <option value="night">Night Shift</option>
          <option value="none">No Shift</option>
        </select>
      </div>

      <button
        type="submit"
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        Add Shift
      </button>
    </form>
  );
}