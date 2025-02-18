import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Briefcase, Building2, Calendar, BarChart as ChartBar, Menu } from 'lucide-react';

export default function Sidebar() {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  const menuItems = [
    { path: '/specializations', icon: Briefcase, label: 'Specializations' },
    { path: '/departments', icon: Building2, label: 'Departments' },
    { path: '/calendar', icon: Calendar, label: 'Calendar' },
    { path: '/stats', icon: ChartBar, label: 'Stats' },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <>
      <button
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        className="lg:hidden fixed top-4 left-4 z-20 p-2 bg-white rounded-md shadow-md"
      >
        <Menu className="h-6 w-6" />
      </button>

      <div className={`
        fixed lg:static inset-y-0 left-0 z-10
        transform ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        transition-transform duration-300 ease-in-out
        w-64 bg-white shadow-lg
      `}>
        <div className="h-full flex flex-col">
          <div className="p-4">
            <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
          </div>

          <nav className="flex-1 p-4 space-y-2">
            {menuItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`
                  flex items-center px-4 py-3 rounded-lg
                  transition-colors duration-200
                  ${isActive(item.path)
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-600 hover:bg-gray-100'}
                `}
              >
                <item.icon className="h-5 w-5 mr-3" />
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </>
  );
}