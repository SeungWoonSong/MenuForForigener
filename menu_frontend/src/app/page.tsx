import WeeklyMenu from '@/components/WeeklyMenu';
import TodayMenu from '@/components/TodayMenu';
import { getWeeklyMenu, Language } from '@/services/menuService';
import { WeekMenu } from '@/types/menu';
import { format } from 'date-fns';
import LanguageSelector from '@/components/LanguageSelector';
import { cookies } from 'next/headers';

export default async function Home() {
  // Get language from cookie or default to 'ko'
  const cookieStore = cookies();
  const language = (cookieStore.get('language')?.value as Language) || 'ko';
  
  let weeklyMenu: WeekMenu | null = null;
  let error: string | null = null;

  try {
    weeklyMenu = await getWeeklyMenu(new Date(), language);
  } catch (err) {
    error = err instanceof Error ? err.message : 'Failed to fetch menu';
    console.error('Error fetching menu:', err);
  }

  const today = format(new Date(), 'yyyyMMdd');
  const todayMenu = weeklyMenu?.days.find(day => day.date === today);

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
          <h1 className="text-2xl font-bold text-center mb-8">Loading...</h1>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <div className="flex justify-center mb-8">
          <LanguageSelector currentLanguage={language} />
        </div>

        {todayMenu && <TodayMenu menu={todayMenu} />}
        <WeeklyMenu weeklyMenu={weeklyMenu} />
      </div>
    </main>
  );
}
