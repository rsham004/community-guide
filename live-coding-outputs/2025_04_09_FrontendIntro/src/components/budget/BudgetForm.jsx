import { useState } from 'react';

function BudgetForm({ budget, onSave, onCancel }) {
  const [limit, setLimit] = useState(budget ? budget.limit.toString() : '');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const limitValue = parseFloat(limit);
    
    // Validate input
    if (!limit.trim() || isNaN(limitValue) || limitValue <= 0) {
      setError('Please enter a valid budget amount greater than zero');
      return;
    }
    
    onSave({
      ...budget,
      limit: limitValue
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="budget-limit" className="block text-sm font-medium text-text-secondary mb-1">
          Budget Limit ($)
        </label>
        <input
          id="budget-limit"
          type="number"
          min="0"
          step="0.01"
          value={limit}
          onChange={(e) => {
            setLimit(e.target.value);
            setError('');
          }}
          className="w-full p-2 bg-background border border-gray-700 rounded-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary"
          placeholder="0.00"
          autoFocus
        />
        {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
      </div>
      
      <div className="flex justify-end space-x-2">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-gray-700 text-text-primary rounded-md hover:bg-gray-700 transition-colors"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-primary text-background rounded-md hover:bg-primary/90 transition-colors"
        >
          Save Budget
        </button>
      </div>
    </form>
  );
}

export default BudgetForm;
