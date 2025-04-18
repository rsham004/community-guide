import { useState, useEffect } from 'react';
import { expenseService } from '../../services/expenseService';
import { useToast } from '../../context/ToastContext';

// Category presets with colors
const categories = [
  { name: 'Groceries', color: 'bg-primary' },
  { name: 'Dining', color: 'bg-secondary' },
  { name: 'Transportation', color: 'bg-accent-1' },
  { name: 'Rent', color: 'bg-accent-2' },
  { name: 'Utilities', color: 'bg-yellow-500' },
  { name: 'Entertainment', color: 'bg-pink-500' },
  { name: 'Shopping', color: 'bg-teal-500' },
  { name: 'Other', color: 'bg-gray-500' },
];

const initialFormData = {
  amount: '',
  category: '',
  date: new Date().toISOString().split('T')[0],
  note: '',
};

function ExpenseModal({ isOpen, onClose, onSaved, initialData = null, isEditing = false }) {
  const [formData, setFormData] = useState(initialData || initialFormData);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [customCategory, setCustomCategory] = useState('');
  const { showToast } = useToast();

  // Reset form or set initial data when modal is opened
  useEffect(() => {
    if (isOpen) {
      if (initialData) {
        setFormData(initialData);
      } else {
        setFormData(initialFormData);
      }
      setErrors({});
      setCustomCategory('');
    }
  }, [isOpen, initialData]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    
    // Clear any error for this field when it's changed
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  const selectCategory = (category) => {
    setFormData({
      ...formData,
      category,
    });
    
    if (errors.category) {
      setErrors(prev => ({ ...prev, category: null }));
    }
  };

  const handleCustomCategory = () => {
    if (customCategory.trim()) {
      selectCategory(customCategory.trim());
      setCustomCategory('');
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.amount || isNaN(Number(formData.amount)) || Number(formData.amount) <= 0) {
      newErrors.amount = 'Please enter a valid amount greater than zero';
    }
    if (!formData.category) {
      newErrors.category = 'Please select or enter a category';
    }
    if (!formData.date) {
      newErrors.date = 'Please select a date';
    }
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validate();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      // Format expense data
      const expenseData = {
        ...formData,
        amount: Number(formData.amount),
        date: formData.date,
      };
      
      // Save expense through service
      if (isEditing) {
        await expenseService.updateExpense(formData.id, expenseData);
      } else {
        await expenseService.addExpense(expenseData);
      }
      
      // Close modal and notify parent
      onSaved();
      onClose();
    } catch (error) {
      console.error('Error saving expense:', error);
      setErrors({ submit: 'Failed to save expense. Please try again.' });
      showToast('Failed to save expense', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle escape key press to close modal
  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  return (
    <div 
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      onKeyDown={handleKeyDown}
      tabIndex="-1"
    >
      <div 
        className="bg-surface rounded-lg shadow-lg w-full max-w-md mx-4 p-6 animate-fade-in"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-text-primary">
            {isEditing ? 'Edit Expense' : 'Add New Expense'}
          </h2>
          <button 
            onClick={onClose}
            className="text-text-secondary hover:text-text-primary transition-colors"
            aria-label="Close modal"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form onSubmit={handleSubmit}>
          {/* Amount Field */}
          <div className="mb-4">
            <label htmlFor="amount" className="block text-sm font-medium text-text-secondary mb-1">
              Amount ($)
            </label>
            <input
              type="number"
              id="amount"
              name="amount"
              step="0.01"
              className={`w-full p-2 bg-background border ${errors.amount ? 'border-red-500' : 'border-gray-700'} rounded-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors`}
              placeholder="0.00"
              value={formData.amount}
              onChange={handleChange}
              autoFocus
            />
            {errors.amount && (
              <p className="text-red-500 text-sm mt-1 animate-fade-in">{errors.amount}</p>
            )}
          </div>
          
          {/* Category Selection */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-text-secondary mb-1">
              Category
            </label>
            <div className="grid grid-cols-4 gap-2 mb-2">
              {categories.map((category) => (
                <button
                  type="button"
                  key={category.name}
                  className={`p-2 rounded-md text-center text-sm transition-colors ${
                    formData.category === category.name 
                      ? `${category.color} text-background` 
                      : 'bg-background text-text-primary hover:bg-gray-800'
                  }`}
                  onClick={() => selectCategory(category.name)}
                >
                  {category.name}
                </button>
              ))}
            </div>
            
            {/* Custom Category */}
            <div className="flex mt-2">
              <input
                type="text"
                className="flex-1 p-2 bg-background border border-gray-700 rounded-l-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary"
                placeholder="Custom category..."
                value={customCategory}
                onChange={(e) => setCustomCategory(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleCustomCategory())}
              />
              <button
                type="button"
                className="bg-primary text-background px-3 rounded-r-md hover:bg-primary/90 transition-colors"
                onClick={handleCustomCategory}
              >
                Add
              </button>
            </div>
            
            {errors.category && (
              <p className="text-red-500 text-sm mt-1 animate-fade-in">{errors.category}</p>
            )}
            
            {formData.category && (
              <div className="mt-2 animate-fade-in">
                <span className="text-text-secondary text-sm">Selected: </span>
                <span className="text-primary font-medium">{formData.category}</span>
              </div>
            )}
          </div>
          
          {/* Date Field */}
          <div className="mb-4">
            <label htmlFor="date" className="block text-sm font-medium text-text-secondary mb-1">
              Date
            </label>
            <input
              type="date"
              id="date"
              name="date"
              className={`w-full p-2 bg-background border ${errors.date ? 'border-red-500' : 'border-gray-700'} rounded-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary transition-colors`}
              value={formData.date}
              onChange={handleChange}
            />
            {errors.date && (
              <p className="text-red-500 text-sm mt-1 animate-fade-in">{errors.date}</p>
            )}
          </div>
          
          {/* Note Field */}
          <div className="mb-6">
            <label htmlFor="note" className="block text-sm font-medium text-text-secondary mb-1">
              Note (Optional)
            </label>
            <textarea
              id="note"
              name="note"
              rows="2"
              className="w-full p-2 bg-background border border-gray-700 rounded-md text-text-primary focus:outline-none focus:ring-1 focus:ring-primary resize-none transition-colors"
              placeholder="Add a note..."
              value={formData.note}
              onChange={handleChange}
            ></textarea>
          </div>
          
          {/* Submit Button */}
          <div className="flex justify-end">
            <button
              type="button"
              className="px-4 py-2 mr-2 border border-gray-700 text-text-primary rounded-md hover:bg-gray-700 focus:outline-none focus:ring-1 focus:ring-gray-500 transition-colors"
              onClick={onClose}
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-primary text-background rounded-md hover:bg-primary/90 disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-background inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Saving...
                </>
              ) : isEditing ? 'Update Expense' : 'Save Expense'}
            </button>
          </div>
          
          {errors.submit && (
            <p className="text-red-500 text-sm mt-4 text-center animate-fade-in">{errors.submit}</p>
          )}
        </form>
      </div>
    </div>
  );
}

export default ExpenseModal;
