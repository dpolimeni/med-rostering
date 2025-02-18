import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Calendar from './pages/Calendar';
import Specializations from './pages/Specializations';
import Departments from './pages/Departments';
import Stats from './pages/Stats';
import DashboardLayout from './layouts/DashBoardLayout';

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuth();
  return token ? <>{children}</> : <Navigate to="/login" />;
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <DashboardLayout />
              </PrivateRoute>
            }
          >
            <Route path="specializations" element={<Specializations />} />
            <Route path="departments" element={<Departments />} />
            <Route path="calendar" element={<Calendar />} />
            <Route path="stats" element={<Stats />} />
            <Route path="" element={<Navigate to="/specializations" />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;