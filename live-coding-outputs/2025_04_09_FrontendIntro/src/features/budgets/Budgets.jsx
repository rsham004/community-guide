import { useState, useEffect } from 'react';
import { budgetService } from '../../services/budgetService';
import { expenseService } from '../../services/expenseService';
import { useToast } from '../../context/ToastContext';
import BudgetItem from '../../components/budget/BudgetItem';
import NewBudgetForm from '../../components/budget/NewBudgetForm';

function Budgets() {
  const [budgetUsage, setBudgetUsage] = useState([]);
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [isAddingNew, setIsAddingNew] = useState(false);
  const [categories, setCategories] = useState([]);
  const [dateRange, setDateRange] = useState({
    start: null,
    end: null
  });
  const { showToast } = useToast();

  // Initialize date range to current month
  useEffect(() => {
    const now = new Date();
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
    
    setDateRange({
      start: firstDay.toISOString().split('T')[0],
      end: now.toISOString().split('T')[0]
    });
  }, []);

  // Fetch budget data when date range changes
  useEffect(() => {
    async function fetchBudgetData() {
      if (!dateRange.start || !dateRange.end) return;
      
      setLoading(true);
      try {
        // Fetch budget usage for the selected period
        const usage = await budgetService.getBudgetUsage(dateRange.start, dateRange.end);
        setBudgetUsage(usage);
        
        // Fetch budget summary totals
        const summaryData = await budgetService.getBudgetSummary(dateRange.start, dateRange.end);
        setSummary(summaryData);
        
        // Get categories for new budget form
        const expenseCategories = await expenseService.getCategorySummary();
        setCategories(expenseCategories.map(cat => cat.category));
      } catch (error) {
        console.error('Failed to fetch budget data:', error);
        showToast('Failed to load budget data', 'error');
      } finally {
        setLoading(false);
      }
    }
    
    fetchBudgetData();
  }, [dateRange, showToast]);

  // Handle budget update
  const handleBudgetUpdate = async (updatedBudget) => {
    try {
      // Update the budget via service
      await budgetService.setBudget(
        updatedBudget.category, 
        updatedBudget.limit, 
        updatedBudget.description
      );
      
      // Refresh budget data
      const usage = await budgetService.getBudgetUsage(dateRange.start, dateRange.end);
      setBudgetUsage(usage);
      
      // Refresh budget summary
      const summaryData = await budgetService.getBudgetSummary(dateRange.start, dateRange.end);
      setSummary(summaryData);
      
      showToast(`Budget for ${updatedBudget.category} updated successfully`, 'success');
    } catch (error) {
      console.error('Failed to update budget:', error);
      showToast('Failed to update budget', 'error');
      throw error;
    }
  };

  // Handle new budget creation
  const handleNewBudget = async (newBudget) => {
    try {
      // Create the new budget via service
      await budgetService.setBudget(
        newBudget.category, 
        newBudget.limit, 
        newBudget.description
      );
      
      // Refresh budget data
      const usage = await budgetService.getBudgetUsage(dateRange.start, dateRange.end);
      setBudgetUsage(usage);
      
      // Refresh budget summary
      const summaryData = await budgetService.getBudgetSummary(dateRange.start, dateRange.end);
      setSummary(summaryData);
      
      // Hide the form
      setIsAddingNew(false);
      
      showToast(`Budget for ${newBudget.category} created`, 'success');
    } catch (error) {
      console.error('Failed to create budget:', error);
      showToast('Failed to create budget', 'error');
    }
  };

  // Handle date range change
  const handleMonthChange = (e) => {
    const value = e.target.value; // Format: YYYY-MM
    
    if (value) {
      const [year, month] = value.split('-');
      const firstDay = new Date(parseInt(year), parseInt(month) - 1, 1);
      const lastDay = new Date(parseInt(year), parseInt(month), 0);
      
      setDateRange({
        start: firstDay.toISOString().split('T')[0],
        end: lastDay.toISOString().split('T')[0]
      });
    }
  };

  // Get current month value for the month picker
  const getCurrentMonthValue = () => {
    if (!dateRange.start) return '';
    
    const date = new Date(dateRange.start);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    
    return `${year}-${month}`;
  };

  if (loading && !budgetUsage.length) {
    return (
      <div className="min-h-[400px] flex items-center justify-center">
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-6 py-1">
            <div className="h-10 bg-surface rounded"></div>
            <div className="space-y-3">
              <div className="h-20 bg-surface rounded"></div>
              <div className="h-20 bg-surface rounded"></div>
              <div className="h-20 bg-surface rounded"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Budget Settings</h1>
      
      {/* Month Selector */}
      <div className="mb-6">
        <label htmlFor="month-selector" className="block text-sm font-medium text-text-secondary mb-1">
          Select Month
        </label>
        <input
          id="month-selector"
          type="month"
          value={getCurrentMonthValue()}
          onChange={handleMonthChange}
          className="p-2 bg-background border border-gray-700 rounded-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary"
        />
      </div>
      
      {/* Budget Summary */}
      {summary && (
        <div className="card mb-6">
          <h2 className="text-xl font-bold mb-2">Budget Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <p className="text-text-secondary">Total Budget</p>
              <p className="text-2xl font-bold text-primary">${summary.totalBudget.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-text-secondary">Total Spent</p>
              <p className="text-2xl font-bold">${summary.totalSpent.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-text-secondary">Remaining</p>
              <p className={`text-2xl font-bold ${summary.remaining < 0 ? 'text-red-500' : 'text-secondary'}`}>
                ${Math.abs(summary.remaining).toFixed(2)}
                <span className="text-sm font-normal ml-1">
                  {summary.remaining < 0 ? 'over budget' : 'remaining'}
                </span>
              </p>
            </div>
          </div>
          
          {/* Overall budget progress */}
          <div className="mt-4">
            <div className="flex justify-between items-center mb-1">
              <span className="text-text-secondary">Overall Budget Usage</span>
              <span className="text-text-secondary">{summary.percentage.toFixed(0)}%</span>
            </div>
            <div className="h-2.5 bg-background rounded-full">
              <div 
                className={`h-2.5 rounded-full ${
                  summary.percentage >= 100 
                    ? 'bg-red-500' 
                    : summary.percentage >= 85 
                      ? 'bg-yellow-500' 
                      : 'bg-primary'
                }`} 
                style={{ width: `${Math.min(100, summary.percentage)}%` }}
              ></div>
            </div>
          </div>
        </div>
      )}
      
      {/* Budget List */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Category Budgets</h2>
          {!isAddingNew && (
            <button
              onClick={() => setIsAddingNew(true)}
              className="px-4 py-2 bg-primary text-background rounded-md hover:bg-primary/90 transition-colors"
            >
              Add New Budget
            </button>
          )}
        </div>
        
        {isAddingNew && (
          <div className="card mb-4">
            <h3 className="text-lg font-medium mb-3">Create New Budget</h3>
            <NewBudgetForm 
              existingCategories={budgetUsage.map(b => b.category)}
              onSave={handleNewBudget}
              onCancel={() => setIsAddingNew(false)}
            />
          </div>
        )}
        
        {budgetUsage.length > 0 ? (
          budgetUsage.map((budget) => (
            <BudgetItem 
              key={budget.category} 
              budget={budget} 
              onUpdate={handleBudgetUpdate} 
            />
          ))
        ) : (
          <div className="card text-center py-8 text-text-secondary">
            <p>No budgets found.</p>
            <p className="text-sm mt-2">Click "Add New Budget" to create your first budget category.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Budgets;
