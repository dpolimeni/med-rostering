import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import { LogOut, User } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function DashboardLayout() {
  const { logout, userData } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Mobile header - fixed at top */}
      <header className="lg:hidden bg-white shadow-md fixed top-0 left-0 right-0 z-10 h-16">
        <div className="flex justify-end items-center h-full px-4">
          <button
            onClick={handleLogout}
            className="flex items-center px-3 py-2 text-gray-600 hover:text-gray-900"
            aria-label="Logout"
          >
            <LogOut className="h-5 w-5" />
            <span className="sr-only">Logout</span>
          </button>
        </div>
      </header>

      <div className="flex flex-1 pt-16 lg:pt-0">
        <Sidebar />
        
        <div className="flex-1 flex flex-col w-full overflow-x-hidden">
          {/* Desktop header */}
          <header className="hidden lg:block bg-white shadow-md sticky top-0 z-10">
            <div className="mx-auto px-4 sm:px-6 lg:px-8 w-full">
              <div className="flex justify-between items-center h-16">
                <div>
                  {userData && (
                    <div className="flex items-center">
                      <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
                        <span className="text-blue-700 font-medium">
                          {userData.email?.charAt(0).toUpperCase() || 'U'}
                        </span>
                      </div>
                      <span className="ml-2 text-sm text-gray-700">
                        {userData.email}
                      </span>
                    </div>
                  )}
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-900 rounded-md hover:bg-gray-100 transition-colors"
                >
                  <LogOut className="h-5 w-5 mr-2" />
                  Logout
                </button>
              </div>
            </div>
          </header>

          <main className="flex-1 py-6 px-4 sm:px-6 lg:px-8 w-full">
            <div className="w-full max-w-7xl mx-auto">
              <Outlet />
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}