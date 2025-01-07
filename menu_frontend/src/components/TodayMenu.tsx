'use client';

import { DayMenu } from '@/types/menu';
import { format, parse } from 'date-fns';
import { ko, enUS, zhCN, sv } from 'date-fns/locale';

interface TodayMenuProps {
  menu: DayMenu;
}

const locales = {
  ko,
  en: enUS,
  zh: zhCN,
  sv
};

const dateFormats = {
  ko: 'M월 d일 (EEEE)',
  en: 'MMMM d, EEEE',
  zh: 'M月d日 EEEE',
  sv: 'd MMMM, EEEE'
};

export default function TodayMenu({ menu }: TodayMenuProps) {
  const date = parse(menu.date, 'yyyyMMdd', new Date());
  const locale = locales[menu.language as keyof typeof locales] || enUS;
  const dateFormat = dateFormats[menu.language as keyof typeof dateFormats] || dateFormats.en;
  const formattedDate = format(date, dateFormat, { locale });

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-6 text-center">
        {formattedDate}
      </h2>

      {/* Lunch Section */}
      {menu.lunch.length > 0 && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4 text-blue-600">Lunch</h3>
          <div className="space-y-4">
            {menu.lunch.map((item, index) => (
              <div key={index} className="border-l-4 border-blue-400 pl-4">
                <div className="flex justify-between items-start">
                  <h4 className="font-medium text-lg">{item.name}</h4>
                </div>
                {item.description && (
                  <p className="text-sm text-gray-600 mt-1 italic">
                    {item.description}
                  </p>
                )}
                {item.sub_menus && item.sub_menus.length > 0 && (
                  <ul className="mt-2 space-y-1">
                    {item.sub_menus.map((subItem, subIndex) => (
                      <li key={subIndex} className="text-gray-700">
                        • {subItem}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Salad Section */}
      {menu.salad && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4 text-green-600">Salad</h3>
          <div className="border-l-4 border-green-400 pl-4">
            <div className="flex justify-between items-start">
              <h4 className="font-medium text-lg">{menu.salad.name}</h4>
            </div>
            {menu.salad.description && (
              <p className="text-sm text-gray-600 mt-1 italic">
                {menu.salad.description}
              </p>
            )}
            {menu.salad.sub_menus && menu.salad.sub_menus.length > 0 && (
              <ul className="mt-2 space-y-1">
                {menu.salad.sub_menus.map((subItem, subIndex) => (
                  <li key={subIndex} className="text-gray-700">
                    • {subItem}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}

      {/* Dessert Section */}
      {menu.dessert && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4 text-gray-600">Dessert</h3>
          <div className="border-l-4 border-gray-300 pl-4">
            {menu.dessert.sub_menus && menu.dessert.sub_menus.length > 0 && (
              <ul className="mt-2 space-y-1">
                <li className="text-gray-700">• {menu.dessert.name}</li>
                {menu.dessert.sub_menus.map((subItem, subIndex) => (
                  <li key={subIndex} className="text-gray-700">
                    • {subItem}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}

      {/* Dinner Section */}
      {menu.dinner.length > 0 && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-4 text-purple-600">Dinner</h3>
          <div className="space-y-4">
            {menu.dinner.map((item, index) => (
              <div key={index} className="border-l-4 border-purple-400 pl-4">
                <div className="flex justify-between items-start">
                  <h4 className="font-medium text-lg">{item.name}</h4>
                </div>
                {item.description && (
                  <p className="text-sm text-gray-600 mt-1 italic">
                    {item.description}
                  </p>
                )}
                {item.sub_menus && item.sub_menus.length > 0 && (
                  <ul className="mt-2 space-y-1">
                    {item.sub_menus.map((subItem, subIndex) => (
                      <li key={subIndex} className="text-gray-700">
                        • {subItem}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </div>
      )}


    </div>
  );
}
