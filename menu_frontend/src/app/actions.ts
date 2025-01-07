'use server';

import { Language } from '@/services/menuService';
import { revalidatePath } from 'next/cache';

export async function changeLanguage(formData: FormData) {
  const language = formData.get('language') as Language;
  
  if (!language) {
    throw new Error('Language is required');
  }

  // 페이지 재검증
  revalidatePath('/');
  
  return { language };
}
