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