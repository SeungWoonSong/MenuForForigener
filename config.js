const path = require('path');

module.exports = {
  // Frontend configuration
  FRONTEND_PORT: 3000,
  FRONTEND_URL: 'http://localhost:3000',

  // Backend API configuration
  API_PORT: 8080,
  API_URL: 'http://localhost:8080',

  // Database configuration
  DB_PATH: path.resolve(__dirname, 'data/menu.db'),
};
