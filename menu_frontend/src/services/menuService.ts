import { WeekMenu, DayMenu } from '@/types/menu';
import { format, addDays, isSunday, isWeekend } from 'date-fns';

// Dynamically determine API URL based on the current hostname
const API_URL = typeof window !== 'undefined' && window.location.hostname === 'localhost'
  ? 'http://localhost:8888'
  : 'https://menu.api.sungwoonsong.com';

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
  let currentDate = startDate;
  
  // Continue fetching until we have 5 weekday menus
  while (days.length < 5) {
    // Skip weekends
    if (!isWeekend(currentDate)) {
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
    currentDate = addDays(currentDate, 1);
  }
  
  return { days };
}
