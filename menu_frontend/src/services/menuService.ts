import { WeekMenu, DayMenu } from '@/types/menu';
import { format, addDays, isSunday } from 'date-fns';

// Dynamically determine API URL based on the current hostname
const API_URL = typeof window !== 'undefined' && window.location.hostname === 'localhost'
  ? 'http://localhost:8888'
  : 'http://3.37.156.53:8888';

export type Language = 'ko' | 'en' | 'zh' | 'sv';

export const LANGUAGES = {
  ko: '한국어',
  en: 'English',
  zh: '中文',
  sv: 'Svenska'
};

export async function getWeeklyMenu(date: Date = new Date(), language: Language = 'en'): Promise<WeekMenu> {
  // If it's Sunday, start from the next day (Monday)
  const startDate = isSunday(date) ? addDays(date, 1) : date;
  const days: DayMenu[] = [];
  
  // Fetch menu for 5 days starting from startDate
  for (let i = 0; i < 5; i++) {
    const currentDate = addDays(startDate, i);
    const formattedDate = format(currentDate, 'yyyyMMdd');
    
    try {
      const response = await fetch(`${API_URL}/api/menu/${formattedDate}?lang=${language}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch menu for ${formattedDate}`);
      }
      
      const dayMenu = await response.json();
      days.push(dayMenu);
    } catch (error) {
      console.error(`Error fetching menu for ${formattedDate}:`, error);
      // Add empty menu for this day
      days.push({
        date: formattedDate,
        language,
        lunch: [],
        dinner: [],
        dessert: null,
        salad: null,
      });
    }
  }
  
  return { days };
}
