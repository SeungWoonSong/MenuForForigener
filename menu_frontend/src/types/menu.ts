export interface MenuItem {
  id: number;
  name: string;
  meal_type: string;
  corner_name: string;
  description: string;
  sub_menus: string[];
}

export interface DayMenu {
  date: string;
  language: string;
  lunch: MenuItem[];
  dinner: MenuItem[];
  dessert: MenuItem | null;
  salad: MenuItem | null;
}

export interface WeekMenu {
  days: DayMenu[];
}
