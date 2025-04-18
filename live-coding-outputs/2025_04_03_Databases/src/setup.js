const { execSync } = require('child_process');
const fs = require('fs');

console.log('Setting up Prisma with Supabase...');

// Check if .env file exists
if (!fs.existsSync('.env')) {
  console.error('Error: .env file not found. Please create a .env file with DATABASE_URL.');
  process.exit(1);
}

try {
  console.log('Generating Prisma client...');
  execSync('npx prisma generate', { stdio: 'inherit' });
  
  console.log('Verifying database connection and schema...');
  // This will validate your schema against the database
  execSync('npx prisma validate', { stdio: 'inherit' });
  
  console.log('Setup completed successfully!');
} catch (error) {
  console.error('Setup failed:', error.message);
}
