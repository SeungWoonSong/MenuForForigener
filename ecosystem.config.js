module.exports = {
  apps: [
    {
      name: 'menu-api',
      script: './menu_crawler/src/api_server.js',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
      },
    },
    {
      name: 'menu-frontend',
      script: 'npm',
      args: 'start',
      cwd: './menu_frontend',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 8081
      },
    }
  ]
};
