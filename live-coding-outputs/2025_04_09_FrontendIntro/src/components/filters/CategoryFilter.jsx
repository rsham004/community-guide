import { useState } from 'react';

function CategoryFilter({ categories, selectedCategories, onChange }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const handleCategoryClick = (category) => {
    if (selectedCategories.includes(category)) {
      onChange(selectedCategories.filter(c => c !== category));
    } else {
      onChange([...selectedCategories, category]);
    }
  };

  const handleSelectAll = () => {
    if (selectedCategories.length === categories.length) {
      onChange([]);
    } else {
      onChange([...categories]);
    }
  };

  const getCategoryColor = (category) => {
    const colorMap = {
      'Groceries': 'bg-primary',
      'Dining': 'bg-secondary',
      'Transportation': 'bg-accent-1',
      'Rent': 'bg-accent-2',
      'Utilities': 'bg-yellow-500',
      'Entertainment': 'bg-pink-500',
      'Shopping': 'bg-teal-500',
    };
    
    return colorMap[category] || 'bg-gray-500';
  };

  return (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-lg font-medium">Categories</h3>
        <button 
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-sm text-text-secondary hover:text-text-primary"
        >
          {isExpanded ? 'Collapse' : 'Expand'}
        </button>
      </div>

      <div className={`flex flex-wrap gap-2 ${isExpanded ? '' : 'max-h-[40px] overflow-hidden'}`}>
        <button
          onClick={handleSelectAll}
          className={`px-3 py-1 text-sm rounded-full ${
            selectedCategories.length === categories.length 
              ? 'bg-primary text-background' 
              : 'bg-gray-700 text-text-primary'
          }`}
        >
          {selectedCategories.length === categories.length ? 'Deselect All' : 'Select All'}
        </button>
        
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => handleCategoryClick(category)}
            className={`px-3 py-1 rounded-full text-sm flex items-center ${
              selectedCategories.includes(category)
                ? `${getCategoryColor(category)} text-background`
                : 'bg-gray-700 text-text-primary'
            }`}
          >
            <span className={`w-2 h-2 mr-1 rounded-full ${getCategoryColor(category)}`}></span>
            {category}
          </button>
        ))}
      </div>
    </div>
  );
}

export default CategoryFilter;
