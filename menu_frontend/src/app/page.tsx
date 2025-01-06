'use client';

import { useState, useEffect } from 'react';
import WeeklyMenu from '@/components/WeeklyMenu';
import TodayMenu from '@/components/TodayMenu';
import { getWeeklyMenu, Language, LANGUAGES } from '@/services/menuService';
import { WeekMenu, DayMenu } from '@/types/menu';
import { format } from 'date-fns';

export default function Home() {
  const [weeklyMenu, setWeeklyMenu] = useState<WeekMenu | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showWeekly, setShowWeekly] = useState(false);
  const [language, setLanguage] = useState<Language>('ko');

  useEffect(() => {
    const fetchMenu = async () => {
      try {
        const menu = await getWeeklyMenu(new Date(), language);
        setWeeklyMenu(menu);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch menu');
      }
    };

    fetchMenu();
  }, [language]);

  if (error) {
    return (
      <main className="min-h-screen bg-gray-100 py-8">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold text-center mb-8 text-red-600">
            Error: {error}
          </h1>
        </div>
      </main>
    );
  }

  if (!weeklyMenu) {
    return (
      <main className="min-h-screen bg-gray-100 py-8">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold text-center mb-8">
            Loading...
          </h1>
        </div>
      </main>
    );
  }

  // Find today's menu
  const today = format(new Date(), 'yyyy-MM-dd');
  const todayMenu = weeklyMenu.days.find(day => day.date === today);

  return (
    <main className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center mb-8">
          <button
            onClick={() => setShowWeekly(!showWeekly)}
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-full transition-colors duration-200"
          >
            {showWeekly ? '오늘의 메뉴 보기' : '주간 메뉴 보기'}
          </button>

          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value as Language)}
            className="bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5"
          >
            {Object.entries(LANGUAGES).map(([code, name]) => (
              <option key={code} value={code}>
                {name}
              </option>
            ))}
          </select>
        </div>

        {showWeekly ? (
          <WeeklyMenu menu={weeklyMenu} />
        ) : todayMenu ? (
          <TodayMenu menu={todayMenu} />
        ) : (
          <div className="text-center text-gray-600">
            오늘은 메뉴가 없습니다.
          </div>
        )}
      </div>
    </main>
  );
}
