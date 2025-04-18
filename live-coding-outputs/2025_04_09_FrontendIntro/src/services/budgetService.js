import { budgets as mockBudgets } from '../mock/budgets';
import { expenseService } from './expenseService';

// Mock in-memory storage
let budgets = [...mockBudgets];

// Simulate API call delay - reduced for better performance with larger datasets
const delay = (ms = 100) => new Promise(resolve => setTimeout(resolve, ms));

export const budgetService = {
  // Get all budgets
  async getBudgets() {
    await delay();
    return [...budgets];
  },

  // Get a specific budget by category
  async getBudgetByCategory(category) {
    await delay();
    const budget = budgets.find(b => b.category === category);
    return budget || null;
  },

  // Set a budget for a category
  async setBudget(category, limit, description = '') {
    await delay(200);
    const existingIndex = budgets.findIndex(b => b.category === category);
    
    if (existingIndex >= 0) {
      // Update existing budget
      budgets[existingIndex] = {
        ...budgets[existingIndex],
        limit,
        description: description || budgets[existingIndex].description
      };
      return budgets[existingIndex];
    } else {
      // Create new budget
      const newBudget = {
        id: `budget-${category.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}`,
        category,
        limit,
        description: description || `Budget for ${category}`
      };
      budgets = [...budgets, newBudget];
      return newBudget;
    }
  },

  // Delete a budget
  async deleteBudget(category) {
    await delay(200);
    budgets = budgets.filter(b => b.category !== category);
    return { success: true };
  },

  // Get budget usage (compare expenses to budget limits) for a specific date range
  async getBudgetUsage(startDate = null, endDate = null) {
    await delay(200);
    
    // Get category summary from expense service for the specified date range
    const categorySummary = await expenseService.getCategorySummary(startDate, endDate);
    
    // Map budgets with their usage
    return await Promise.all(budgets.map(async budget => {
      const categoryData = categorySummary.find(item => item.category === budget.category);
      const spent = categoryData ? categoryData.amount : 0;
      
      return {
        category: budget.category,
        limit: budget.limit,
        spent,
        remaining: budget.limit - spent,
        percentage: Math.min(100, (spent / budget.limit * 100)),
        description: budget.description
      };
    }));
  },
  
  // Get total budget amount and spending
  async getBudgetSummary(startDate = null, endDate = null) {
    await delay();
    
    const usage = await this.getBudgetUsage(startDate, endDate);
    
    const totalBudget = budgets.reduce((total, budget) => total + budget.limit, 0);
    const totalSpent = usage.reduce((total, item) => total + item.spent, 0);
    
    return {
      totalBudget,
      totalSpent,
      remaining: totalBudget - totalSpent,
      percentage: Math.min(100, (totalSpent / totalBudget * 100))
    };
  }
};
