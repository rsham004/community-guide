const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Installing required dependencies...');

try {
  // Install the Supabase client and any other missing packages
  console.log('Installing Supabase client library...');
  execSync('npm install @supabase/supabase-js', { stdio: 'inherit' });
  
  console.log('Checking Prisma setup...');
  if (!fs.existsSync(path.join(__dirname, 'node_modules', '.prisma'))) {
    console.log('Installing Prisma client...');
    execSync('npm install prisma --save-dev', { stdio: 'inherit' });
    execSync('npx prisma generate', { stdio: 'inherit' });
  }
  
  console.log('All dependencies installed successfully!');
  console.log('You can now run the development server with: npm run dev');
} catch (error) {
  console.error('Installation failed:', error.message);
}
