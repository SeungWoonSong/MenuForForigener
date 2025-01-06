const express = require('express');
const sqlite3 = require('sqlite3');
const { open } = require('sqlite');
const cors = require('cors');
const config = require('../../config');
const path = require('path');

const app = express();
const port = config.API_PORT;

app.use(cors({
  origin: config.FRONTEND_URL // Only allow frontend to access the API
}));

// Database connection
const dbPath = path.resolve(__dirname, '../../data/menu.db');

app.get('/api/menu/:date', async (req, res) => {
  const date = req.params.date;
  const lang = req.query.lang || 'ko';

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

    // Group menus by meal type
    const lunch = formattedMainMenu
      .filter(item => item.meal_type === '중식')
      .map(item => ({
        ...item,
        sub_menus: formattedSubMenu
          .filter(sub => sub.main_menu_id === item.id)
          .map(sub => sub.name)
      }));

    const dinner = formattedMainMenu
      .filter(item => item.meal_type === '석식')
      .map(item => ({
        ...item,
        sub_menus: formattedSubMenu
          .filter(sub => sub.main_menu_id === item.id)
          .map(sub => sub.name)
      }));

    // Get dessert and salad
    const dessert = formattedMainMenu.find(item => 
      item.corner_name?.includes('디저트') || item.corner_name?.includes('후식')
    );
    const salad = formattedMainMenu.find(item => 
      item.corner_name?.includes('샐러드')
    );

    if (dessert) {
      dessert.sub_menus = formattedSubMenu
        .filter(sub => sub.main_menu_id === dessert.id)
        .map(sub => sub.name);
    }

    if (salad) {
      salad.sub_menus = formattedSubMenu
        .filter(sub => sub.main_menu_id === salad.id)
        .map(sub => sub.name);
    }

    await db.close();
    res.json({
      date,
      language: lang,
      lunch,
      dinner,
      dessert: dessert || null,
      salad: salad || null
    });
  } catch (error) {
    console.error('Error fetching menu:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(port, () => {
  console.log(`API server running at ${config.API_URL}`);
});
