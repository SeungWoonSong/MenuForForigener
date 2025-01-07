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
        console.log('Fetched menu:', menu); // Debug log
        setWeeklyMenu(menu);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch menu');
      }
    };

    fetchMenu();
  }, [language]);

  const today = format(new Date(), 'yyyyMMdd');
  const todayMenu = weeklyMenu?.days.find(day => day.date === today);

  console.log('Today:', today); // Debug log
  console.log('Today menu:', todayMenu); // Debug log

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

  return (
    <main className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        {/* Language selector */}
        <div className="flex justify-center mb-8 space-x-4">
          {Object.entries(LANGUAGES).map(([code, name]) => (
            <button
              key={code}
              onClick={() => setLanguage(code as Language)}
              className={`px-4 py-2 rounded-lg ${
                language === code
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {name}
            </button>
          ))}
        </div>

        {/* View toggle */}
        <div className="flex justify-center mb-8">
          <button
            onClick={() => setShowWeekly(!showWeekly)}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            {showWeekly ? 'Today Menu' : 'Weekly Menu'}
          </button>
        </div>

        {showWeekly ? (
          <WeeklyMenu menu={weeklyMenu} />
        ) : todayMenu ? (
          <TodayMenu menu={todayMenu} />
        ) : (
          <div className="text-center text-xl text-gray-600">
            오늘은 메뉴가 없습니다.
          </div>
        )}
      </div>
    </main>
  );
}
