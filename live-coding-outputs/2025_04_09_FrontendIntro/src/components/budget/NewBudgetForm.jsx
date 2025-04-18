import { useState } from 'react';

function NewBudgetForm({ existingCategories = [], onSave, onCancel }) {
  const [category, setCategory] = useState('');
  const [limit, setLimit] = useState('');
  const [description, setDescription] = useState('');
  const [errors, setErrors] = useState({});

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const newErrors = {};
    if (!category.trim()) {
      newErrors.category = 'Please enter a category name';
    } else if (existingCategories.includes(category)) {
      newErrors.category = 'This category already has a budget';
    }
    
    const limitValue = parseFloat(limit);
    if (!limit.trim() || isNaN(limitValue) || limitValue <= 0) {
      newErrors.limit = 'Please enter a valid amount greater than zero';
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    onSave({
      category,
      limit: limitValue,
      description: description.trim() || `Budget for ${category}`,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="category-name" className="block text-sm font-medium text-text-secondary mb-1">
          Category Name
        </label>
        <input
          id="category-name"
          type="text"
          value={category}
          onChange={(e) => {
            setCategory(e.target.value);
            setErrors((prev) => ({ ...prev, category: null }));
          }}
          className={`w-full p-2 bg-background border ${
            errors.category ? 'border-red-500' : 'border-gray-700'
          } rounded-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary`}
          placeholder="e.g., Groceries, Entertainment"
        />
        {errors.category && <p className="mt-1 text-sm text-red-500">{errors.category}</p>}
      </div>
      
      <div>
        <label htmlFor="budget-limit" className="block text-sm font-medium text-text-secondary mb-1">
          Monthly Budget Limit ($)
        </label>
        <input
          id="budget-limit"
          type="number"
          min="0"
          step="0.01"
          value={limit}
          onChange={(e) => {
            setLimit(e.target.value);
            setErrors((prev) => ({ ...prev, limit: null }));
          }}
          className={`w-full p-2 bg-background border ${
            errors.limit ? 'border-red-500' : 'border-gray-700'
          } rounded-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary`}
          placeholder="0.00"
        />
        {errors.limit && <p className="mt-1 text-sm text-red-500">{errors.limit}</p>}
      </div>
      
      <div>
        <label htmlFor="budget-description" className="block text-sm font-medium text-text-secondary mb-1">
          Description (Optional)
        </label>
        <textarea
          id="budget-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows="2"
          className="w-full p-2 bg-background border border-gray-700 rounded-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary"
          placeholder="Add a description for this budget category"
        />
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
          Create Budget
        </button>
      </div>
    </form>
  );
}

export default NewBudgetForm;
