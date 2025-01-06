'use client';

import { WeekMenu } from '@/types/menu';
import DayMenu from './DayMenu';
import { format } from 'date-fns';

interface WeeklyMenuProps {
  menu: WeekMenu;
}

export default function WeeklyMenu({ menu }: WeeklyMenuProps) {
  const today = format(new Date(), 'yyyy-MM-dd');

  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
      {menu.days.map((day) => (
        <DayMenu
          key={day.date}
          menu={day}
          isToday={day.date === today}
        />
      ))}
    </div>
  );
}
