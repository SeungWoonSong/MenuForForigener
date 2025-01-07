'use client';

import { WeekMenu } from '@/types/menu';
import DayMenu from './DayMenu';
import { format } from 'date-fns';

interface WeeklyMenuProps {
  menu: WeekMenu;
}

export default function WeeklyMenu({ menu }: WeeklyMenuProps) {
  const today = format(new Date(), 'yyyyMMdd');
  
  // Debug logs
  console.log('Today:', today);
  console.log('Available dates:', menu.days.map(day => day.date));

  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
      {menu.days.map((day) => {
        const isToday = day.date === today;
        console.log(`Comparing date ${day.date} with today ${today}, isToday: ${isToday}`);
        return (
          <DayMenu
            key={day.date}
            menu={day}
            isToday={isToday}
          />
        );
      })}
    </div>
  );
}
