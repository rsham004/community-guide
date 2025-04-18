import { useState, useEffect } from 'react';
import { expenseService } from '../../services/expenseService';
import ExpenseList from '../../components/expense/ExpenseList';
import CategoryFilter from '../../components/filters/CategoryFilter';
import DateRangeFilter from '../../components/filters/DateRangeFilter';
import ExpenseModal from '../../components/expense/ExpenseModal';
import { useToast } from '../../context/ToastContext';

function History() {
  const [expenses, setExpenses] = useState([]);
  const [filteredExpenses, setFilteredExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categories, setCategories] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [currentExpense, setCurrentExpense] = useState(null);
  const { showToast } = useToast();

  // Initialize dates to current month
  useEffect(() => {
    const now = new Date();
    const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
    
    setStartDate(firstDay.toISOString().split('T')[0]);
    setEndDate(now.toISOString().split('T')[0]);
  }, []);

  // Fetch expenses and extract unique categories
  useEffect(() => {
    async function fetchExpenses() {
      setLoading(true);
      try {
        const data = await expenseService.getExpenses();
        // Ensure data is an array before setting state
        if (Array.isArray(data)) {
          setExpenses(data);
          
          // Extract unique categories
          const uniqueCategories = [...new Set(data.map(expense => expense.category))];
          setCategories(uniqueCategories);
          setSelectedCategories(uniqueCategories); // Initially select all
        } else {
          console.error('Expected expenses to be an array but got:', typeof data);
          setExpenses([]);
          setCategories([]);
        }
      } catch (error) {
        console.error('Failed to fetch expenses:', error);
        showToast('Failed to load expenses', 'error');
        setExpenses([]);
      } finally {
        setLoading(false);
      }
    }
    
    fetchExpenses();
  }, [showToast]);

  // Apply filters when dependencies change
  useEffect(() => {
    if (!startDate || !endDate || !Array.isArray(expenses)) return;
    
    try {
      // Filter by date range and categories
      const filtered = expenses.filter(expense => {
        const expenseDate = new Date(expense.date);
        const start = new Date(startDate);
        const end = new Date(endDate);
        
        // Set time to midnight for proper comparison
        start.setHours(0, 0, 0, 0);
        end.setHours(23, 59, 59, 999);
        
        const isInDateRange = expenseDate >= start && expenseDate <= end;
        const isInSelectedCategory = selectedCategories.includes(expense.category);
        
        return isInDateRange && isInSelectedCategory;
      });
      
      // Sort by date (newest first)
      filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
      
      setFilteredExpenses(filtered);
    } catch (error) {
      console.error('Error filtering expenses:', error);
      setFilteredExpenses([]);
    }
  }, [expenses, startDate, endDate, selectedCategories]);

  // Handle date range change
  const handleDateRangeChange = (start, end) => {
    setStartDate(start);
    setEndDate(end);
  };

  // Handle editing an expense
  const handleEdit = (expense) => {
    setCurrentExpense(expense);
    setIsEditModalOpen(true);
  };

  // Handle deleting an expense
  const handleDelete = async (id) => {
    try {
      await expenseService.deleteExpense(id);
      setExpenses(prev => prev.filter(expense => expense.id !== id));
      return true;
    } catch (error) {
      console.error('Failed to delete expense:', error);
      throw error;
    }
  };

  // Handle saving edited expense
  const handleExpenseSaved = async () => {
    try {
      // Refresh expenses from service
      const data = await expenseService.getExpenses();
      if (Array.isArray(data)) {
        setExpenses(data);
      }
      showToast('Expense updated successfully', 'success');
    } catch (error) {
      console.error('Failed to refresh expenses:', error);
    }
  };

  // Calculate totals for the summary
  const totalAmount = Array.isArray(filteredExpenses) 
    ? filteredExpenses.reduce((sum, expense) => sum + expense.amount, 0)
    : 0;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Expense History</h1>
      
      {/* Filters Section */}
      <div className="card mb-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <DateRangeFilter 
            startDate={startDate} 
            endDate={endDate} 
            onChange={handleDateRangeChange} 
          />
          <CategoryFilter 
            categories={categories}
            selectedCategories={selectedCategories}
            onChange={setSelectedCategories}
          />
        </div>
      </div>
      
      {/* Summary Section */}
      <div className="card mb-6">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="text-lg font-medium">Summary</h3>
            <p className="text-text-secondary">
              Showing {filteredExpenses.length} of {expenses.length} expenses
            </p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-primary">${totalAmount.toFixed(2)}</div>
            <div className="text-text-secondary text-sm">Total amount</div>
          </div>
        </div>
      </div>
      
      {/* Expense List Section */}
      <ExpenseList 
        expenses={filteredExpenses} 
        onEdit={handleEdit}
        onDelete={handleDelete}
        loading={loading}
      />
      
      {/* Edit Expense Modal */}
      {isEditModalOpen && currentExpense && (
        <ExpenseModal 
          isOpen={isEditModalOpen}
          onClose={() => setIsEditModalOpen(false)}
          onSaved={handleExpenseSaved}
          initialData={currentExpense}
          isEditing={true}
        />
      )}
    </div>
  );
}

export default History;
