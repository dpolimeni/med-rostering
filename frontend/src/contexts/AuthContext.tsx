import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import axios from 'axios';
import api from '../api';

api.defaults.baseURL = 'http://localhost:8000';

interface UserData {
  specializations: Specialization[];
  departments: Department[];
}

interface Specialization {
  id: string;
  name: string;
}

interface Department {
  id: string;
  name: string;
}

interface AuthContextType {
  token: string | null;
  userData: UserData | null;
  login: (accessToken: string, refreshToken: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [token, setToken] = useState<string | null>(localStorage.getItem('access_token'));
    const [refreshToken, setRefreshToken] = useState<string | null>(localStorage.getItem('refresh_token'));
    const [userData, setUserData] = useState<UserData | null>(null);
  
  useEffect(() => {
    const fetchUserData = async () => {
      if (token) {
        try {
          const response = await api.get('/users/me', {
            headers: { Authorization: `Bearer ${token}` }
          });
          setUserData(response.data);
        } catch (error) {
          console.error('Failed to fetch user data:', error);
          logout();
        }
      }
    };

    fetchUserData();
  }, [token]);

  const login = (accessToken: string, refreshToken: string) => {
    setToken(accessToken);
    setRefreshToken(refreshToken);
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  };

  const logout = () => {
    setToken(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  return (
    <AuthContext.Provider value={{ token, userData, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}