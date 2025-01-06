import { WeekMenu, DayMenu } from '@/types/menu';
import { format, addDays } from 'date-fns';

// API URL should be configured in environment variables
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export type Language = 'ko' | 'en' | 'zh' | 'sv';

export const LANGUAGES = {
  ko: '한국어',
  en: 'English',
  zh: '中文',
  sv: 'Svenska'
};

export async function getWeeklyMenu(startDate: Date, language: Language = 'en'): Promise<WeekMenu> {
  const days: DayMenu[] = [];
  
  // Fetch menu for 5 days starting from startDate
  for (let i = 0; i < 5; i++) {
    const currentDate = addDays(startDate, i);
    const formattedDate = format(currentDate, 'yyyy-MM-dd');
    
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
      });
    }
  }
  
  return { days };
}
