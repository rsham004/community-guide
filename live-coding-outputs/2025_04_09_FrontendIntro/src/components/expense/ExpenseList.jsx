import { useState } from 'react';
import { useToast } from '../../context/ToastContext';

function ExpenseList({ expenses, onEdit, onDelete, loading }) {
  const { showToast } = useToast();
  const [expandedId, setExpandedId] = useState(null);

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const handleDelete = async (expense) => {
    if (window.confirm(`Delete expense "${expense.category}: $${expense.amount}"?`)) {
      try {
        await onDelete(expense.id);
        showToast('Expense deleted successfully', 'success');
      } catch (error) {
        showToast('Failed to delete expense', 'error');
      }
    }
  };

  const getCategoryColor = (category) => {
    const categories = {
      'Groceries': 'bg-primary',
      'Dining': 'bg-secondary',
      'Transportation': 'bg-accent-1',
      'Rent': 'bg-accent-2',
      'Utilities': 'bg-yellow-500',
      'Entertainment': 'bg-pink-500',
      'Shopping': 'bg-teal-500',
    };
    
    return categories[category] || 'bg-gray-500';
  };

  if (loading) {
    return (
      <div className="flex justify-center p-8">
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-6 py-1">
            <div className="h-10 bg-surface rounded"></div>
            <div className="h-10 bg-surface rounded"></div>
            <div className="h-10 bg-surface rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (expenses.length === 0) {
    return (
      <div className="text-center py-8 text-text-secondary">
        <p>No expenses found.</p>
        <p className="text-sm mt-2">Try adjusting your filters or add a new expense.</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {expenses.map((expense) => (
        <div 
          key={expense.id} 
          className="card hover:bg-surface/80 transition-colors cursor-pointer"
          onClick={() => toggleExpand(expense.id)}
        >
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <div className={`w-4 h-4 rounded-full ${getCategoryColor(expense.category)}`}></div>
              <div>
                <div className="font-medium">{expense.category}</div>
                <div className="text-sm text-text-secondary">
                  {new Date(expense.date).toLocaleDateString()}
                </div>
              </div>
            </div>
            <div className="text-lg font-semibold">${expense.amount.toFixed(2)}</div>
          </div>
          
          {expandedId === expense.id && (
            <div className="mt-4 pt-3 border-t border-gray-700 animate-fade-in">
              {expense.note && (
                <div className="mb-2">
                  <span className="text-text-secondary">Note: </span>
                  <span>{expense.note}</span>
                </div>
              )}
              <div className="flex justify-end space-x-2 mt-2">
                <button 
                  className="px-3 py-1 text-sm bg-secondary text-background rounded hover:bg-secondary/90"
                  onClick={(e) => {
                    e.stopPropagation();
                    onEdit(expense);
                  }}
                >
                  Edit
                </button>
                <button 
                  className="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDelete(expense);
                  }}
                >
                  Delete
                </button>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default ExpenseList;
