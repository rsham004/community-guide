import { expenses as mockExpenses } from '../mock/expenses';

// Mock in-memory storage
let expenses = [...mockExpenses];

// Simulate API call delay - reduced for better performance with larger datasets
const delay = (ms = 100) => new Promise(resolve => setTimeout(resolve, ms));

// Helper function to paginate results
const paginateResults = (data, page = 1, pageSize = 20) => {
  const startIndex = (page - 1) * pageSize;
  const paginatedData = data.slice(startIndex, startIndex + pageSize);
  return {
    data: paginatedData,
    pagination: {
      page,
      pageSize,
      totalItems: data.length,
      totalPages: Math.ceil(data.length / pageSize)
    }
  };
};

export const expenseService = {
  // Get all expenses with optional pagination
  async getExpenses(page, pageSize) {
    await delay(); 
    if (page && pageSize) {
      return paginateResults(expenses, page, pageSize);
    }
    return [...expenses]; // Return the array directly, not an object
  },

  // Get expenses by date range with optional pagination
  async getExpensesByDateRange(startDate, endDate, page = 1, pageSize = 20) {
    await delay();
    const start = new Date(startDate);
    const end = new Date(endDate);
    
    // Set hours for accurate comparison
    start.setHours(0, 0, 0, 0);
    end.setHours(23, 59, 59, 999);
    
    const filtered = expenses.filter(expense => {
      const expenseDate = new Date(expense.date);
      return expenseDate >= start && expenseDate <= end;
    });
    
    if (page && pageSize) {
      return paginateResults(filtered, page, pageSize);
    }
    return filtered;
  },

  // Get expenses by category with optional pagination
  async getExpensesByCategory(category, page = 1, pageSize = 20) {
    await delay();
    const filtered = expenses.filter(expense => expense.category === category);
    
    if (page && pageSize) {
      return paginateResults(filtered, page, pageSize);
    }
    return filtered;
  },

  // Add a new expense
  async addExpense(expense) {
    await delay(200);
    const newExpense = {
      ...expense,
      id: `exp-${Date.now()}`, // Simple ID generation
    };
    expenses = [newExpense, ...expenses];
    return newExpense;
  },

  // Update an expense
  async updateExpense(id, updates) {
    await delay(200);
    const index = expenses.findIndex(expense => expense.id === id);
    if (index === -1) throw new Error("Expense not found");
    
    expenses[index] = { ...expenses[index], ...updates };
    return expenses[index];
  },

  // Delete an expense
  async deleteExpense(id) {
    await delay(200);
    const index = expenses.findIndex(expense => expense.id === id);
    if (index === -1) throw new Error("Expense not found");
    
    expenses = expenses.filter(expense => expense.id !== id);
    return { success: true };
  },

  // Get total expenses for a date range
  async getTotalExpenses(startDate = null, endDate = null) {
    await delay();
    
    let filtered = [...expenses];
    
    if (startDate && endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      start.setHours(0, 0, 0, 0);
      end.setHours(23, 59, 59, 999);
      
      filtered = expenses.filter(expense => {
        const expenseDate = new Date(expense.date);
        return expenseDate >= start && expenseDate <= end;
      });
    }
    
    return filtered.reduce((total, expense) => total + expense.amount, 0);
  },

  // Get summary by category for a date range
  async getCategorySummary(startDate = null, endDate = null) {
    await delay();
    
    let filtered = [...expenses];
    
    if (startDate && endDate) {
      const start = new Date(startDate);
      const end = new Date(endDate);
      start.setHours(0, 0, 0, 0);
      end.setHours(23, 59, 59, 999);
      
      filtered = expenses.filter(expense => {
        const expenseDate = new Date(expense.date);
        return expenseDate >= start && expenseDate <= end;
      });
    }
    
    const summary = {};
    
    filtered.forEach(expense => {
      if (!summary[expense.category]) {
        summary[expense.category] = 0;
      }
      summary[expense.category] += expense.amount;
    });
    
    return Object.entries(summary).map(([category, amount]) => ({
      category,
      amount,
    }));
  },
  
  // Get expenses by month for trend analysis
  async getMonthlyExpenses(year = new Date().getFullYear()) {
    await delay();
    
    const monthlyData = Array(12).fill(0).map((_, i) => ({
      month: i + 1, 
      total: 0
    }));
    
    expenses.forEach(expense => {
      const expenseDate = new Date(expense.date);
      const expenseYear = expenseDate.getFullYear();
      const expenseMonth = expenseDate.getMonth();
      
      if (expenseYear === year) {
        monthlyData[expenseMonth].total += expense.amount;
      }
    });
    
    return monthlyData.map(item => ({
      month: new Date(year, item.month - 1).toLocaleString('default', { month: 'short' }),
      total: item.total
    }));
  }
};
