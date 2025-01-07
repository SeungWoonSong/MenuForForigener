'use client';

import { DayMenu as DayMenuType } from '@/types/menu';
import { format, parse } from 'date-fns';
import { ko, enUS, zhCN, sv } from 'date-fns/locale';
import clsx from 'clsx';

interface DayMenuProps {
  menu: DayMenuType;
  isToday: boolean;
}

const locales = {
  ko,
  en: enUS,
  zh: zhCN,
  sv
};

export default function DayMenu({ menu, isToday }: DayMenuProps) {
  const date = parse(menu.date, 'yyyyMMdd', new Date());
  const locale = locales[menu.language as keyof typeof locales] || enUS;
  
  return (
    <div
      className={clsx(
        'rounded-lg shadow-lg p-4',
        isToday ? 'bg-blue-50 border-2 border-blue-500' : 'bg-white'
      )}
    >
      <div className="text-center mb-4">
        <h2 className="text-lg font-semibold">
          {format(date, 'M/d (EEE)', { locale })}
        </h2>
      </div>
      
      {/* Lunch Menu */}
      <div className="mb-4 border border-blue-200 p-2">
        <h3 className="text-md font-semibold text-blue-600 mb-2">Lunch</h3>
        {menu.lunch.length > 0 ? (
          menu.lunch.map((item, index) => (
            <div key={index} className="mb-2">
              <div className="flex justify-between items-start">
                <span className="font-medium">{item.name}</span>
              </div>
              {item.sub_menus && item.sub_menus.length > 0 && (
                <ul className="mt-1 text-sm text-gray-600">
                  {item.sub_menus.map((subItem, subIndex) => (
                    <li key={subIndex}>• {subItem}</li>
                  ))}
                </ul>
              )}
            </div>
          ))
        ) : (
          <p className="text-gray-500">No lunch menu available</p>
        )}
      </div>

      {/* Salad Menu */}
      {menu.salad && (
        <div className="mb-4 border border-green-200 p-2">
          <h3 className="text-md font-semibold text-green-600 mb-2">Salad</h3>
          <div className="mb-2">
            <div className="flex justify-between items-start">
              <span className="font-medium">{menu.salad.name}</span>
            </div>
            {menu.salad.sub_menus && menu.salad.sub_menus.length > 0 && (
              <ul className="mt-1 text-sm text-gray-600">
                {menu.salad.sub_menus.map((subItem, subIndex) => (
                  <li key={subIndex}>• {subItem}</li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}

      {/* Dessert Menu */}
      {menu.dessert && (
        <div className="mb-4 border border-gray-200 p-2">
          <h3 className="text-md font-semibold text-gray-600 mb-2">Dessert</h3>
          {menu.dessert.sub_menus && menu.dessert.sub_menus.length > 0 && (
            <ul className="mt-1 text-sm text-gray-600">
              <li>• {menu.dessert.name}</li>
              {menu.dessert.sub_menus.map((subItem, subIndex) => (
                <li key={subIndex}>• {subItem}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Dinner Menu */}
      <div className="mb-4 border border-purple-200 p-2">
        <h3 className="text-md font-semibold text-purple-600 mb-2">Dinner</h3>
        {menu.dinner.length > 0 ? (
          menu.dinner.map((item, index) => (
            <div key={index} className="mb-2">
              <div className="flex justify-between items-start">
                <span className="font-medium">{item.name}</span>
              </div>
              {item.sub_menus && item.sub_menus.length > 0 && (
                <ul className="mt-1 text-sm text-gray-600">
                  {item.sub_menus.map((subItem, subIndex) => (
                    <li key={subIndex}>• {subItem}</li>
                  ))}
                </ul>
              )}
            </div>
          ))
        ) : (
          <p className="text-gray-500">No dinner menu available</p>
        )}
      </div>
    </div>
  );
}
