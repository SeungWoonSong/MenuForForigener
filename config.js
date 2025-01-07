const path = require('path');

module.exports = {
  // Frontend configuration
  FRONTEND_PORT: 8081,
  FRONTEND_URL: 'http://localhost:8081',

  // Backend API configuration
  API_PORT: 8888,
  API_URL: 'http://localhost:8888',

  // Database configuration
  DB_PATH: path.resolve(__dirname, 'data/menu.db'),
};
