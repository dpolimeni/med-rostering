import React from 'react';
import { BarChart, Activity, Users, Calendar as CalendarIcon } from 'lucide-react';

export default function Stats() {
  const stats = [
    {
      title: 'Total Specializations',
      value: '12',
      icon: BarChart,
      change: '+2.5%',
      changeType: 'increase'
    },
    {
      title: 'Active Departments',
      value: '24',
      icon: Activity,
      change: '+3.2%',
      changeType: 'increase'
    },
    {
      title: 'Team Members',
      value: '48',
      icon: Users,
      change: '+12%',
      changeType: 'increase'
    },
    {
      title: 'Scheduled Events',
      value: '156',
      icon: CalendarIcon,
      change: '+8.1%',
      changeType: 'increase'
    }
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold text-gray-900">Statistics</h1>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div key={stat.title} className="bg-white p-6 rounded-lg shadow-md">
            <div className="flex items-center justify-between">
              <stat.icon className="h-8 w-8 text-blue-500" />
              <span className={`text-sm font-medium ${
                stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
              }`}>
                {stat.change}
              </span>
            </div>
            <h3 className="mt-4 text-2xl font-bold text-gray-900">{stat.value}</h3>
            <p className="mt-1 text-sm text-gray-500">{stat.title}</p>
          </div>
        ))}
      </div>

      <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Activity Overview</h2>
        <div className="h-64 flex items-center justify-center border-2 border-dashed border-gray-200 rounded-lg">
          <p className="text-gray-500">Chart will be implemented here</p>
        </div>
      </div>
    </div>
  );
}