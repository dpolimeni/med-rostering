import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Briefcase, Building2, Calendar, BarChart as ChartBar, Menu, Users, X } from 'lucide-react';
import { UserData } from '../types';

export default function Sidebar() {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  const menuItems = [
    { path: '/specializations', icon: Briefcase, label: 'Specializations' },
    { path: '/departments', icon: Building2, label: 'Departments' },
    { path: '/people', icon: Users, label: 'People' },
    { path: '/calendar', icon: Calendar, label: 'Calendar' },
    { path: '/stats', icon: ChartBar, label: 'Stats' },
  ];

  const isActive = (path: string) => location.pathname === path;

  // Close mobile menu when clicking outside
  React.useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (isMobileMenuOpen) {
        const sidebar = document.getElementById('sidebar');
        const menuButton = document.getElementById('menu-button');
        if (sidebar && !sidebar.contains(e.target as Node) && 
            menuButton && !menuButton.contains(e.target as Node)) {
          setIsMobileMenuOpen(false);
        }
      }
    };

    document.addEventListener('mousedown', handleOutsideClick);
    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, [isMobileMenuOpen]);

  // Close mobile menu when route changes
  React.useEffect(() => {
    setIsMobileMenuOpen(false);
  }, [location]);

  return (
    <>
      <button
        id="menu-button"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        className="lg:hidden fixed top-4 left-4 z-20 p-2 bg-white rounded-md shadow-md"
        aria-label="Toggle menu"
      >
        {isMobileMenuOpen ? (
          <X className="h-6 w-6" />
        ) : (
          <Menu className="h-6 w-6" />
        )}
      </button>

      {/* Overlay for mobile */}
      {isMobileMenuOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-10"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      <aside
        id="sidebar"
        className={`
          fixed lg:sticky top-0 h-screen
          transform ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          transition-transform duration-300 ease-in-out
          w-64 md:w-72 lg:w-56 xl:w-64 bg-white shadow-lg
          z-20 lg:z-auto
          overflow-y-auto
        `}
      >
        <div className="h-full flex flex-col">
          <div className="p-4 flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
            <button 
              className="lg:hidden p-1 text-gray-500 hover:text-gray-700"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          <nav className="flex-1 p-4 space-y-1">
            {menuItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`
                  flex items-center px-3 py-2 rounded-lg
                  transition-colors duration-200
                  ${isActive(item.path)
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-600 hover:bg-gray-100'}
                `}
              >
                <item.icon className="h-5 w-5 mr-3 flex-shrink-0" />
                <span className="truncate">{item.label}</span>
              </Link>
            ))}
          </nav>

          <div className="p-4 border-t border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                <span className="text-blue-700 font-medium">
                  {localStorage.getItem('user_email')?.charAt(0).toUpperCase() || 'U'}
                </span>
              </div>
              <div className="overflow-hidden">
                <p className="text-sm font-medium text-gray-700 truncate">
                  {localStorage.getItem('user_email') || 'User'}
                </p>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Spacer div for layout when sidebar is fixed */}
    </>
  );
}