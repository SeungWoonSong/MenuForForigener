import json
import os
from openai import OpenAI
from typing import Dict, List
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class TranslationService:
    """
    Service for translating menu items to multiple languages and managing translations in the database.
    Supports English, Chinese, and Swedish translations with descriptions for unfamiliar Korean dishes.
    """
    
    def __init__(self):
        """Initialize the translation service with API client and database connection."""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")
            
        print(f"Initializing with API key: {api_key[:8]}...")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

        self.db_path = os.getenv('DB_PATH')
        if not self.db_path:
            raise ValueError("DB_PATH not found in environment variables")
        
        self._setup_database()

    def _setup_database(self):
        """Create the translations table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create translations table if not exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu_translations (
            menu_name TEXT,
            language TEXT,
            translated_name TEXT,
            description TEXT,
            created_at TEXT,
            PRIMARY KEY (menu_name, language)
        )
        ''')
        
        conn.commit()
        conn.close()

    def _get_translation_prompt(self, menu_items: List[str], target_lang: str) -> str:
        """
        Generate a prompt for the translation API.
        
        Args:
            menu_items: List of Korean menu items to translate
            target_lang: Target language code ('en', 'zh', or 'sv')
            
        Returns:
            Formatted prompt string for the API
        """
        language_map = {
            'en': 'English',
            'zh': 'Chinese (Simplified)',
            'sv': 'Swedish'
        }
        
        examples = {
            'en': [
                {
                    "original": "김치찌개",
                    "translated": "Kimchi Stew",
                    "description": "A traditional Korean stew made with fermented kimchi, pork, and tofu"
                },
                {
                    "original": "팝콘치킨샐러드",
                    "translated": "Popcorn Chicken Salad",
                    "description": "A fresh salad topped with crispy bite-sized fried chicken pieces"
                }
            ],
            'zh': [
                {
                    "original": "김치찌개",
                    "translated": "泡菜汤",
                    "description": "一道传统的韩国汤，用发酵泡菜、猪肉和豆腐制成"
                },
                {
                    "original": "팝콘치킨샐러드",
                    "translated": "爆米花鸡肉沙拉",
                    "description": "一道清新的沙拉，配上香脆的小块炸鸡"
                }
            ],
            'sv': [
                {
                    "original": "김치찌개",
                    "translated": "Kimchigryta",
                    "description": "En traditionell koreansk gryta gjord på fermenterad kimchi, fläsk och tofu"
                },
                {
                    "original": "팝콘치킨샐러드",
                    "translated": "Popcornkycklingssallad",
                    "description": "En fräsch sallad toppad med krispiga små bitar av friterad kyckling"
                }
            ]
        }
        
        return f"""You are a professional menu translator. Please translate the following Korean menu items to {language_map[target_lang]}.
For Korean dishes that might be unfamiliar to foreigners, add a brief description.
Please maintain the original meaning and ingredients in the translation.
Please respond ONLY in this exact JSON format and nothing else.
Make sure to translate both the name and description to {language_map[target_lang]}.

Here are some examples in {language_map[target_lang]}:
{json.dumps(examples[target_lang], ensure_ascii=False, indent=2)}

Korean menu items to translate:
{json.dumps(menu_items, ensure_ascii=False)}"""

    def _translate_batch(self, menu_items: List[str], target_lang: str) -> List[Dict]:
        """
        Translate a batch of menu items using the DeepSeek API.
        
        Args:
            menu_items: List of menu items to translate
            target_lang: Target language code
            
        Returns:
            List of translation results with descriptions
        """
        try:
            prompt = self._get_translation_prompt(menu_items, target_lang)
            
            completion = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a professional menu translator. Always respond in the exact JSON format requested, with no additional text or explanations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            response_text = completion.choices[0].message.content
            
            # Extract JSON from response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                print(f"Invalid response format: {response_text}")
                return []
                
            json_str = response_text[start_idx:end_idx]
            translations = json.loads(json_str)
            
            return translations
            
        except Exception as e:
            print(f"Translation error: {str(e)}")
            print(f"Full error details: {e.__class__.__name__}")
            return []

    def get_or_create_translations(self, menu_id: int, menu_name: str, languages: List[str]) -> Dict[str, Dict]:
        """
        Get existing translations or create new ones for menu items.
        
        Args:
            menu_id: ID of the menu item
            menu_name: Name of the menu item in Korean
            languages: List of target language codes
            
        Returns:
            Dictionary of translations and descriptions by language
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        translations = {}
        to_translate = []
        
        for lang in languages:
            cursor.execute('''
            SELECT translated_name, description
            FROM menu_translations
            WHERE menu_name = ? AND language = ?
            ''', (menu_name, lang))
            
            result = cursor.fetchone()
            if result:
                translations[lang] = {
                    'translated': result[0],
                    'description': result[1]
                }
            else:
                to_translate.append(lang)
        
        if to_translate:
            for lang in to_translate:
                translated_batch = self._translate_batch([menu_name], lang)
                if translated_batch:
                    trans_item = translated_batch[0]
                    translations[lang] = {
                        'translated': trans_item['translated'],
                        'description': trans_item.get('description')
                    }
                    
                    cursor.execute('''
                    INSERT INTO menu_translations (menu_name, language, translated_name, description, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        menu_name,
                        lang,
                        trans_item['translated'],
                        trans_item.get('description'),
                        datetime.now().isoformat()
                    ))
        
        conn.commit()
        conn.close()
        return translations

def test_translation():
    """Test the translation service with a single menu item"""
    try:
        translator = TranslationService()
        
        # Test menu item
        test_menu = "순살감자탕"
        print(f"\nTesting translation for: {test_menu}")
        
        # Test English translation first
        result = translator._translate_batch([test_menu], "en")
        print(f"\nTranslation result:\n{json.dumps(result, ensure_ascii=False, indent=2)}")
        
    except Exception as e:
        print(f"Test failed: {e}")
        raise

def translate_menu():
    """
    Main function to translate all menu items in the database.
    Supports translation to English (en), Chinese (zh), and Swedish (sv).
    """
    service = TranslationService()
    
    try:
        # Get all menu items first
        conn = sqlite3.connect(service.db_path)
        cursor = conn.cursor()
        
        # Get all unique menu items from both main_menu and sub_menu tables
        cursor.execute('''
        SELECT DISTINCT menu_name as name
        FROM sub_menu
        UNION 
        SELECT DISTINCT main_menu as name
        FROM main_menu
        ''')
        menu_items = cursor.fetchall()
        conn.close()
        
        # Translate each menu item
        languages = ['en', 'zh', 'sv']
        for (menu_name,) in menu_items:
            # Skip if the menu item is just a number or simple text
            if menu_name.replace('/', '').replace('.', '').isdigit():
                continue
                
            translations = service.get_or_create_translations(None, menu_name, languages)
            
            # Insert translations into database
            conn = sqlite3.connect(service.db_path)
            cursor = conn.cursor()
            
            for lang, trans in translations.items():
                if trans.get('translated'):
                    try:
                        cursor.execute('''
                        INSERT OR REPLACE INTO menu_translations 
                        (menu_name, language, translated_name, description, created_at)
                        VALUES (?, ?, ?, ?, ?)
                        ''', (
                            menu_name,
                            lang,
                            trans['translated'],
                            trans.get('description'),
                            datetime.now().isoformat()
                        ))
                    except Exception as e:
                        print(f"Error inserting translation for {menu_name}: {e}")
            
            conn.commit()
            conn.close()
            
        print("Translation completed successfully!")
        
    except Exception as e:
        print(f"Error during translation: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    translate_menu()  # Run full translation
