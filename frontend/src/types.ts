export type ShiftType = 'morning' | 'night' | 'none';

export interface Shift {
  date: Date;
  type: ShiftType;
  userId: string;
}

export interface User {
  id: string;
  name: string;
}

export interface UserData {
  id: string;
  email: string;
  specialization: Specialization;
  departmentId: string;
}

export interface Specialization {
  id: string;
  name?: string;
  description?: string;
  shifts?: Record<string, { start: string; end: string }>;
}

export interface Department {
  id: string;
  name: string;
  users: string[];
}