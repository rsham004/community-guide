// Mock expense data generator

// Define categories with typical amount ranges
const expenseCategories = [
  { name: 'Groceries', minAmount: 5, maxAmount: 200 },
  { name: 'Dining', minAmount: 10, maxAmount: 150 },
  { name: 'Transportation', minAmount: 5, maxAmount: 100 },
  { name: 'Rent', minAmount: 800, maxAmount: 2500 },
  { name: 'Utilities', minAmount: 50, maxAmount: 300 },
  { name: 'Entertainment', minAmount: 10, maxAmount: 200 },
  { name: 'Shopping', minAmount: 15, maxAmount: 500 },
  { name: 'Healthcare', minAmount: 20, maxAmount: 400 },
  { name: 'Travel', minAmount: 100, maxAmount: 1500 },
  { name: 'Education', minAmount: 50, maxAmount: 500 },
];

// Common notes for each category
const categoryNotes = {
  'Groceries': ['Weekly shopping', 'Fresh produce', 'Snacks and drinks', 'Pantry restocking', 'Organic items'],
  'Dining': ['Lunch with coworkers', 'Dinner date', 'Coffee break', 'Fast food', 'Weekend brunch'],
  'Transportation': ['Gas refill', 'Bus pass', 'Uber ride', 'Train ticket', 'Car maintenance'],
  'Rent': ['Monthly rent', 'Apartment fee', 'Sublease payment'],
  'Utilities': ['Electricity bill', 'Water bill', 'Internet service', 'Gas bill', 'Phone bill'],
  'Entertainment': ['Movie tickets', 'Concert', 'Streaming subscription', 'Video games', 'Sports event'],
  'Shopping': ['New clothes', 'Electronics', 'Home decor', 'Gifts', 'Books'],
  'Healthcare': ['Doctor visit', 'Prescription', 'Gym membership', 'Dental check-up', 'Vitamins'],
  'Travel': ['Flight tickets', 'Hotel stay', 'Car rental', 'Travel insurance', 'Souvenirs'],
  'Education': ['Textbooks', 'Course fee', 'Online class', 'Tutoring', 'School supplies'],
};

// Helper function to generate a random number between min and max
const getRandomNumber = (min, max) => {
  return Math.random() * (max - min) + min;
};

// Helper function to get a random item from an array
const getRandomItem = (array) => {
  return array[Math.floor(Math.random() * array.length)];
};

// Helper function to generate a random date within the given range
const getRandomDate = (start, end) => {
  const startDate = new Date(start).getTime();
  const endDate = new Date(end).getTime();
  const randomTime = startDate + Math.random() * (endDate - startDate);
  const randomDate = new Date(randomTime);
  return randomDate.toISOString().split('T')[0]; // Format as YYYY-MM-DD
};

// Generate a set of mock expenses across a 2-year period
const generateMockExpenses = (count = 250) => {
  // Set date range for a 2-year period
  const endDate = new Date(); // Today
  const startDate = new Date();
  startDate.setFullYear(endDate.getFullYear() - 2); // 2 years ago
  
  const expenses = [];
  
  // Format dates as strings for use in the generator
  const startDateStr = startDate.toISOString().split('T')[0];
  const endDateStr = endDate.toISOString().split('T')[0];
  
  // Create regular monthly expenses like rent and utilities
  const regularExpenses = ['Rent', 'Utilities'];
  
  // Loop through each month in the 2-year period
  for (let d = new Date(startDate); d <= endDate; d.setMonth(d.getMonth() + 1)) {
    regularExpenses.forEach(category => {
      const categoryData = expenseCategories.find(c => c.name === category);
      if (categoryData) {
        // For rent, keep the amount consistent each month with small variations
        const baseAmount = category === 'Rent' 
          ? getRandomNumber(categoryData.minAmount, categoryData.maxAmount)
          : getRandomNumber(categoryData.minAmount, categoryData.maxAmount);
          
        // Small variations month to month (especially for utilities)
        const variation = category === 'Rent' ? 0.01 : 0.1;
        const amount = Math.round((baseAmount * (1 + getRandomNumber(-variation, variation))) * 100) / 100;
        
        const monthDate = new Date(d);
        monthDate.setDate(category === 'Rent' ? 1 : Math.floor(Math.random() * 5) + 1); // Rent on the 1st, utilities within first 5 days
        
        expenses.push({
          id: `reg-${category}-${monthDate.getTime()}`,
          amount,
          category,
          date: monthDate.toISOString().split('T')[0],
          note: getRandomItem(categoryNotes[category]),
        });
      }
    });
    
    // Add semi-regular expenses (e.g., groceries weekly) - FIX: Remove reference to undefined "category" variable
    // Generate weekly grocery expenses
    const month = d.getMonth();
    const year = d.getFullYear();
    // 4 weeks of groceries per month
    for (let week = 0; week < 4; week++) {
      const groceryDate = new Date(year, month, (week * 7) + 3 + Math.floor(Math.random() * 3)); // 3rd-5th, 10th-12th, etc.
      if (groceryDate <= endDate) {
        expenses.push({
          id: `grocery-${groceryDate.getTime()}`,
          amount: Math.round(getRandomNumber(40, 120) * 100) / 100,
          category: 'Groceries',
          date: groceryDate.toISOString().split('T')[0],
          note: getRandomItem(categoryNotes['Groceries']),
        });
      }
    }
  }
  
  // Generate remaining random expenses to reach the desired count
  const remainingCount = Math.max(0, count - expenses.length);
  
  for (let i = 0; i < remainingCount; i++) {
    // Pick a random category, excluding rent and utilities which are already generated monthly
    let category;
    do {
      category = getRandomItem(expenseCategories);
    } while (regularExpenses.includes(category.name));
    
    const amount = Math.round(getRandomNumber(category.minAmount, category.maxAmount) * 100) / 100;
    const date = getRandomDate(startDateStr, endDateStr);
    
    expenses.push({
      id: `exp-${Date.now()}-${i}`,
      amount,
      category: category.name,
      date,
      note: getRandomItem(categoryNotes[category.name] || ['Expense']),
    });
  }
  
  // Generate some grocery expenses as well (outside the monthly loop)
  for (let i = 0; i < count / 10; i++) {
    const date = getRandomDate(startDateStr, endDateStr);
    expenses.push({
      id: `grocery-rand-${Date.now()}-${i}`,
      amount: Math.round(getRandomNumber(20, 150) * 100) / 100,
      category: 'Groceries',
      date,
      note: getRandomItem(categoryNotes['Groceries']),
    });
  }
  
  // Sort by date, descending (newest first)
  return expenses.sort((a, b) => new Date(b.date) - new Date(a.date));
};

// Generate 250 expenses over a 2-year period
export const expenses = generateMockExpenses(250);
