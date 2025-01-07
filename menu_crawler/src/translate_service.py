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
            menu_id INTEGER,
            language TEXT,
            translated_name TEXT,
            description TEXT,
            created_at TEXT,
            PRIMARY KEY (menu_id, language)
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
        # Special translations for specific menu items
        special_translations = {
            '두유': {
                'en': {'translated': 'Soy Milk', 'description': 'A plant-based milk made from soybeans'},
                'zh': {'translated': '豆浆', 'description': '用大豆制成的植物性饮料'},
                'sv': {'translated': 'Sojamjölk', 'description': 'En växtbaserad mjölk gjord på sojabönor'}
            },
            '코코넛쉬림프샐러드': {
                'en': {'translated': 'Coconut Shrimp Salad', 'description': 'A fresh salad featuring coconut-crusted shrimp'},
                'zh': {'translated': '椰子虾沙拉', 'description': '一道以椰丝裹虾为主的清新沙拉'},
                'sv': {'translated': 'Kokosräkor sallad', 'description': 'En fräsch sallad med kokospanerade räkor'}
            },
            '훈제오리단호박샐러드': {
                'en': {'translated': 'Smoked Duck and Pumpkin Salad', 'description': 'A fresh salad featuring smoked duck and sweet pumpkin'},
                'zh': {'translated': '烟熏鸭肉南瓜沙拉', 'description': '新鲜的沙拉，配有烟熏鸭肉和甜南瓜'},
                'sv': {'translated': 'Rökt anka- och pumpa sallad', 'description': 'En fräsch sallad med rökt anka och söt pumpa'}
            },
            '쥬스':{
                'en': {'translated': 'Juice', 'description': 'A refreshing and refreshing juice'},
                'zh': {'translated': '果汁', 'description': '一道清爽的果汁'},
                'sv': {'translated': 'Jus', 'description': 'En frisk och frisk jus'}
            },
            '팝콘치킨샐러드': {
                'en': {'translated': 'Popcorn Chicken Salad', 'description': 'A fresh salad topped with crispy bite-sized fried chicken pieces'},
                'zh': {'translated': '爆米花鸡肉沙拉', 'description': '一道清新的沙拉，配上香脆的小块炸鸡'},
                'sv': {'translated': 'Popcornkyckling sallad', 'description': 'En fräsch sallad toppad med krispiga små bitar av friterad kyckling'}
            }
        }

        # Check if any menu item has a special translation
        for menu_item in menu_items:
            if menu_item in special_translations:
                translation = special_translations[menu_item][target_lang]
                return json.dumps([{
                    'original': menu_item,
                    'translated': translation['translated'],
                    'description': translation['description']
                }], ensure_ascii=False)

        # If no special translations, proceed with normal translation
        lang_names = {
            'en': 'English',
            'zh': 'Chinese (Simplified)',
            'sv': 'Swedish'
        }
        
        lang_examples = {
            'en': '''[
  {
    "original": "김치찌개",
    "translated": "Kimchi Stew",
    "description": "A traditional Korean stew made with fermented kimchi, pork, and tofu"
  },
  {
    "original": "훈제오리단호박샐러드",
    "translated": "Smoked Duck and Pumpkin Salad",
    "description": "A fresh salad featuring smoked duck and sweet pumpkin"
  }
]''',
            'zh': '''[
  {
    "original": "김치찌개",
    "translated": "泡菜汤",
    "description": "一道传统的韩国汤，用发酵泡菜、猪肉和豆腐制成"
  },
  {
    "original": "훈제오리단호박샐러드",
    "translated": "烟熏鸭肉南瓜沙拉",
    "description": "新鲜的沙拉，配有烟熏鸭肉和甜南瓜"
  }
]''',
            'sv': '''[
  {
    "original": "김치찌개",
    "translated": "Kimchigryta",
    "description": "En traditionell koreansk gryta gjord på fermenterad kimchi, fläsk och tofu"
  },
  {
    "original": "훈제오리단호박샐러드",
    "translated": "Rökt anka- och pumpa sallad",
    "description": "En fräsch sallad med rökt anka och söt pumpa"
  }
]'''
        }
        
        return f"""Please translate the following Korean menu items to {lang_names[target_lang]}.
For Korean dishes that might be unfamiliar to foreigners, add a brief description in {lang_names[target_lang]}.
Pay special attention to menu items containing '샐러드' (salad) and ensure they are translated accurately.
Please maintain the original meaning and ingredients in the translation.
Please respond in this exact JSON format:

{lang_examples[target_lang]}

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
            print(f"\nTranslating to {target_lang}: {menu_items}")
            prompt = self._get_translation_prompt(menu_items, target_lang)
            print(f"\nPrompt:\n{prompt}")
            
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are a professional menu translator."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            
            content = response.choices[0].message.content
            print(f"\nAPI Response:\n{content}")
            
            # Remove markdown code block if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            translations = json.loads(content)
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
            WHERE menu_id = ? AND language = ?
            ''', (menu_id, lang))
            
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
                    INSERT INTO menu_translations (menu_id, language, translated_name, description, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        menu_id,
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
        SELECT DISTINCT m.menu_name as name, m.id, 'sub' as type 
        FROM sub_menu m
        UNION 
        SELECT DISTINCT m.main_menu as name, m.id, 'main' as type 
        FROM main_menu m
        ''')
        menu_items = cursor.fetchall()
        conn.close()
        
        # Translate each menu item
        languages = ['en', 'zh', 'sv']
        for menu_name, menu_id, item_type in menu_items:
            # Skip if the menu item is just a number or simple text
            if menu_name.replace('/', '').replace('.', '').isdigit():
                continue
                
            translations = service.get_or_create_translations(menu_id, menu_name, languages)
            
            # Insert translations into database
            conn = sqlite3.connect(service.db_path)
            cursor = conn.cursor()
            
            for lang, trans in translations.items():
                if trans.get('translated'):
                    try:
                        cursor.execute('''
                        INSERT OR REPLACE INTO menu_translations 
                        (menu_id, language, translated_name, description, created_at)
                        VALUES (?, ?, ?, ?, ?)
                        ''', (
                            menu_id,
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
