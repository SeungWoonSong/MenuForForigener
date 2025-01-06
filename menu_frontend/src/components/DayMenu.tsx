'use client';

import { DayMenu as DayMenuType } from '@/types/menu';
import { format } from 'date-fns';
import clsx from 'clsx';

interface DayMenuProps {
  menu: DayMenuType;
  isToday: boolean;
}

export default function DayMenu({ menu, isToday }: DayMenuProps) {
  const date = new Date(menu.date);
  
  return (
    <div
      className={clsx(
        'rounded-lg shadow-lg p-4',
        isToday ? 'bg-blue-50 border-2 border-blue-500' : 'bg-white'
      )}
    >
      <div className="text-center mb-4">
        <h2 className="text-lg font-semibold">
          {format(date, 'M/d (EEE)')}
        </h2>
      </div>
      
      {/* Lunch Menu */}
      <div className="mb-6">
        <h3 className="text-md font-semibold text-blue-600 mb-2">Lunch</h3>
        {menu.lunch.map((item, index) => (
          <div key={index} className="mb-2">
            <p className="font-medium">{item.corner_name}</p>
            <p className="text-gray-800">{item.main_menu}</p>
            {item.sub_menus.map((sub, subIndex) => (
              <p key={subIndex} className="text-sm text-gray-600">
                {sub}
              </p>
            ))}
          </div>
        ))}
      </div>
      
      {/* Dinner Menu */}
      <div className="mb-6">
        <h3 className="text-md font-semibold text-purple-600 mb-2">Dinner</h3>
        {menu.dinner.map((item, index) => (
          <div key={index} className="mb-2">
            <p className="font-medium">{item.corner_name}</p>
            <p className="text-gray-800">{item.main_menu}</p>
            {item.sub_menus.map((sub, subIndex) => (
              <p key={subIndex} className="text-sm text-gray-600">
                {sub}
              </p>
            ))}
          </div>
        ))}
      </div>
      
      {/* Dessert & Salad */}
      {menu.dessert && (
        <div className="mb-2">
          <h3 className="text-md font-semibold text-pink-600 mb-1">Dessert</h3>
          <p className="text-gray-800">{menu.dessert.main_menu}</p>
        </div>
      )}
      
      {menu.salad && (
        <div>
          <h3 className="text-md font-semibold text-green-600 mb-1">Salad</h3>
          <p className="text-gray-800">{menu.salad.main_menu}</p>
        </div>
      )}
    </div>
  );
}
