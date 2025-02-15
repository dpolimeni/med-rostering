import React from 'react';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameDay } from 'date-fns';
import { Shift, User } from '../types';

interface CalendarProps {
  shifts: Shift[];
  selectedUser: User | null;
  currentMonth: Date;
}

export function Calendar({ shifts, selectedUser, currentMonth }: CalendarProps) {
  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(currentMonth);
  const days = eachDayOfInterval({ start: monthStart, end: monthEnd });

  const getShiftForDay = (day: Date) => {
    return shifts.find(
      (shift) => 
        isSameDay(new Date(shift.date), day) && 
        shift.userId === selectedUser?.id
    );
  };

  const getShiftColor = (shift?: Shift) => {
    if (!shift) return 'bg-gray-100';
    switch (shift.type) {
      case 'morning':
        return 'bg-green-100';
      case 'night':
        return 'bg-blue-100';
      case 'none':
        return 'bg-red-100';
      default:
        return 'bg-gray-100';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-4">
      <div className="grid grid-cols-7 gap-2 mb-2">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
          <div key={day} className="text-center font-semibold text-gray-600">
            {day}
          </div>
        ))}
      </div>
      <div className="grid grid-cols-7 gap-2">
        {days.map((day) => {
          const shift = getShiftForDay(day);
          return (
            <div
              key={day.toISOString()}
              className={`p-2 min-h-[80px] rounded ${getShiftColor(shift)} transition-colors`}
            >
              <div className="font-medium">{format(day, 'd')}</div>
              {shift && (
                <div className="text-xs mt-1">
                  {shift.type === 'morning' && 'Morning Shift'}
                  {shift.type === 'night' && 'Night Shift'}
                  {shift.type === 'none' && 'Off Duty'}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}