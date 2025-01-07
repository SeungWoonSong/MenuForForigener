const express = require('express');
const sqlite3 = require('sqlite3');
const { open } = require('sqlite');
const cors = require('cors');
const config = require('../../config');
const path = require('path');

const app = express();
const port = config.API_PORT;

// CORS configuration
const corsOptions = {
  origin: [
    'http://localhost:8081',
    'http://localhost:8888',
    'http://3.37.156.53:8081',
    'http://3.37.156.53:8888',
    'http://3.37.156.53'  // 도메인만 있는 경우도 허용
  ],
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: false,
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));

// Add request logging middleware
app.use((req, res, next) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
  console.log('Origin:', req.headers.origin);
  next();
});

// Database connection
const dbPath = path.resolve(__dirname, '/home/ubuntu/susong/ForeignMenu/data/menu.db');

app.get('/api/menu/:date', async (req, res) => {
  const date = req.params.date;
  const lang = req.query.lang || 'ko';

  console.log(`Fetching menu for date: ${date}, language: ${lang}`);

  try {
    const db = await open({
      filename: dbPath,
      driver: sqlite3.Database
    });
    
    // Get main menu items with translations
    const mainMenuQuery = `
      SELECT m.id, m.main_menu as name, m.meal_type, m.corner_name,
             t.translated_name, t.description
      FROM main_menu m
      LEFT JOIN menu_translations t ON m.id = t.menu_id AND t.language = ?
      WHERE m.date = ?
    `;
    
    const mainMenu = await db.all(mainMenuQuery, [lang, date.replace(/-/g, '')]);
    
    // Get sub menu items with translations
    const subMenuQuery = `
      SELECT s.id, s.menu_name as name, s.main_menu_id,
             t.translated_name, t.description
      FROM sub_menu s
      LEFT JOIN menu_translations t ON s.id = t.menu_id AND t.language = ?
      WHERE s.main_menu_id IN (
        SELECT id FROM main_menu WHERE date = ?
      )
    `;
    
    const subMenu = await db.all(subMenuQuery, [lang, date.replace(/-/g, '')]);

    // Process and format the response
    const formattedMainMenu = mainMenu.map(item => ({
      id: item.id,
      name: lang === 'ko' ? item.name : (item.translated_name || item.name),
      meal_type: item.meal_type,
      corner_name: item.corner_name,
      description: item.description || ''
    }));

    const formattedSubMenu = subMenu.map(item => ({
      id: item.id,
      name: lang === 'ko' ? item.name : (item.translated_name || item.name),
      main_menu_id: item.main_menu_id,
      description: item.description || ''
    }));

    // Helper function to add sub-menus to an item
    const addSubMenus = (item) => ({
      ...item,
      sub_menus: formattedSubMenu
        .filter(sub => sub.main_menu_id === item.id)
        .map(sub => sub.name)
    });

    // Categorize menu items
    const categories = formattedMainMenu.reduce((acc, item) => {
      const lowerCornerName = (item.corner_name || '').toLowerCase();
      const lowerName = (item.name || '').toLowerCase();
      const lowerMealType = (item.meal_type || '').toLowerCase();
      
      if (lowerCornerName.includes('후식') || lowerCornerName.includes('디저트') || lowerCornerName.includes('dessert')) {
        if (!acc.dessert) acc.dessert = item;
        else {
          // Merge sub-menus if there are multiple dessert items
          const existingSubMenus = formattedSubMenu
            .filter(sub => sub.main_menu_id === acc.dessert.id)
            .map(sub => sub.name);
          const newSubMenus = formattedSubMenu
            .filter(sub => sub.main_menu_id === item.id)
            .map(sub => sub.name);
          acc.dessert.sub_menus = [...new Set([...existingSubMenus, ...newSubMenus])];
        }
      } else if (
        lowerCornerName.includes('샐러드') || 
        lowerCornerName.includes('salad') ||
        lowerName.includes('샐러드') ||
        lowerName.includes('salad')
      ) {
        if (!acc.salad) acc.salad = item;
        else {
          // Merge sub-menus if there are multiple salad items
          const existingSubMenus = formattedSubMenu
            .filter(sub => sub.main_menu_id === acc.salad.id)
            .map(sub => sub.name);
          const newSubMenus = formattedSubMenu
            .filter(sub => sub.main_menu_id === item.id)
            .map(sub => sub.name);
          acc.salad.sub_menus = [...new Set([...existingSubMenus, ...newSubMenus])];
        }
      } else if (lowerMealType.includes('중식') || lowerMealType.includes('lunch')) {
        acc.lunch.push(item);
      } else if (lowerMealType.includes('석식') || lowerMealType.includes('dinner')) {
        acc.dinner.push(item);
      }
      return acc;
    }, { lunch: [], dinner: [], dessert: null, salad: null });

    // Add sub-menus to each category
    const lunch = categories.lunch.map(addSubMenus);
    const dinner = categories.dinner.map(addSubMenus);
    const dessert = categories.dessert ? addSubMenus(categories.dessert) : null;
    const salad = categories.salad ? addSubMenus(categories.salad) : null;

    await db.close();
    res.json({
      date,
      language: lang,
      lunch,
      dinner,
      dessert,
      salad
    });
  } catch (error) {
    console.error('Error fetching menu:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Start server
app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on port ${port}`);
  console.log(`Database path: ${dbPath}`);
});
