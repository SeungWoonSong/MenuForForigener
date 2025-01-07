'use client';

import { Language, LANGUAGES } from '@/services/menuService';
import { useTransition } from 'react';
import { changeLanguage } from '@/app/actions';

interface LanguageSelectorProps {
  currentLanguage: Language;
}

export default function LanguageSelector({ currentLanguage }: LanguageSelectorProps) {
  const [isPending, startTransition] = useTransition();

  return (
    <form action={changeLanguage}>
      <select
        name="language"
        className={`px-4 py-2 border rounded-lg shadow-sm ${
          isPending ? 'opacity-50' : ''
        }`}
        defaultValue={currentLanguage}
        disabled={isPending}
        onChange={(e) => {
          const form = e.target.form;
          if (form) {
            startTransition(() => {
              form.requestSubmit();
            });
          }
        }}
      >
        {LANGUAGES.map((lang) => (
          <option key={lang} value={lang}>
            {lang.toUpperCase()}
          </option>
        ))}
      </select>
      {isPending && (
        <span className="ml-2 text-sm text-gray-500">Changing language...</span>
      )}
    </form>
  );
}
