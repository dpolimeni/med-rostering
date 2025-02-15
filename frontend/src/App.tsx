import React, { useState } from 'react';
import { addMonths, subMonths } from 'date-fns';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Calendar } from './components/Calendar';
import { ShiftForm } from './components/ShiftForm';
import { Shift, User, ShiftType } from './types';

const initialUsers: User[] = [
  { id: '1', name: 'John Doe' },
  { id: '2', name: 'Jane Smith' },
  { id: '3', name: 'Mike Johnson' },
];

function App() {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [shifts, setShifts] = useState<Shift[]>([]);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const handleAddShift = (userId: string, date: Date, type: ShiftType) => {
    setShifts([...shifts, { userId, date, type }]);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Shift Calendar</h1>
          <div className="flex gap-4">
            <select
              value={selectedUser?.id || ''}
              onChange={(e) => {
                const user = initialUsers.find(u => u.id === e.target.value);
                setSelectedUser(user || null);
              }}
              className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="">Select a user</option>
              {initialUsers.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.name}
                </option>
              ))}
            </select>
            
            <div className="flex items-center gap-4">
              <button
                onClick={() => setCurrentMonth(subMonths(currentMonth, 1))}
                className="p-2 rounded hover:bg-gray-200"
              >
                <ChevronLeft className="h-5 w-5" />
              </button>
              <span className="font-medium">
                {currentMonth.toLocaleString('default', { month: 'long', year: 'numeric' })}
              </span>
              <button
                onClick={() => setCurrentMonth(addMonths(currentMonth, 1))}
                className="p-2 rounded hover:bg-gray-200"
              >
                <ChevronRight className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-3">
            <Calendar
              shifts={shifts}
              selectedUser={selectedUser}
              currentMonth={currentMonth}
            />
          </div>
          <div>
            <ShiftForm users={initialUsers} onAddShift={handleAddShift} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;