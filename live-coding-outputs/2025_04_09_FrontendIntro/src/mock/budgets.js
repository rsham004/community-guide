// Mock budget data with realistic category limits

// Helper function to generate a budget ID
const generateBudgetId = (category) => {
  return `budget-${category.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`;
};

// Function to generate budgets with appropriate limits for each category
const generateBudgets = () => {
  return [
    { 
      id: generateBudgetId('Groceries'),
      category: 'Groceries',
      limit: 500.00,
      description: 'Monthly grocery shopping budget'
    },
    { 
      id: generateBudgetId('Dining'),
      category: 'Dining',
      limit: 300.00,
      description: 'Eating out, restaurants, cafes'
    },
    { 
      id: generateBudgetId('Transportation'),
      category: 'Transportation',
      limit: 250.00,
      description: 'Gas, public transport, ride sharing'
    },
    { 
      id: generateBudgetId('Rent'),
      category: 'Rent',
      limit: 1500.00,
      description: 'Monthly apartment rent'
    },
    { 
      id: generateBudgetId('Utilities'),
      category: 'Utilities',
      limit: 350.00,
      description: 'Electricity, water, internet, phone'
    },
    { 
      id: generateBudgetId('Entertainment'),
      category: 'Entertainment',
      limit: 200.00,
      description: 'Movies, concerts, streaming services'
    },
    { 
      id: generateBudgetId('Shopping'),
      category: 'Shopping',
      limit: 300.00,
      description: 'Clothes, electronics, home goods'
    },
    { 
      id: generateBudgetId('Healthcare'),
      category: 'Healthcare',
      limit: 400.00,
      description: 'Medical costs, prescriptions, insurance co-pays'
    },
    { 
      id: generateBudgetId('Travel'),
      category: 'Travel',
      limit: 600.00,
      description: 'Vacations, weekend trips, flights'
    },
    { 
      id: generateBudgetId('Education'),
      category: 'Education',
      limit: 300.00,
      description: 'Books, courses, subscriptions'
    }
  ];
};

export const budgets = generateBudgets();
