import React from 'react';

function BudgetProgressBar({ category, limit, spent, percentage }) {
  // Determine color based on percentage of budget used
  const getBarColor = () => {
    if (percentage >= 100) return 'bg-red-500'; // Over budget
    if (percentage >= 85) return 'bg-yellow-500'; // Close to limit
    return 'bg-primary'; // Healthy usage
  };

  return (
    <div className="mb-4">
      <div className="flex justify-between items-center mb-1">
        <div className="flex items-center">
          <span className="font-medium">{category}</span>
          {percentage >= 100 && (
            <span className="ml-2 text-xs bg-red-500 text-white px-2 py-0.5 rounded-full">
              Over Budget
            </span>
          )}
        </div>
        <div className="text-text-secondary text-sm">
          <span className={percentage >= 100 ? 'text-red-500 font-medium' : ''}>
            ${spent.toFixed(2)}
          </span>
          <span> / </span>
          <span>${limit.toFixed(2)}</span>
        </div>
      </div>
      
      <div className="h-2.5 bg-background rounded-full overflow-hidden">
        <div 
          className={`h-full rounded-full ${getBarColor()}`} 
          style={{ width: `${Math.min(100, percentage)}%` }} 
        ></div>
      </div>
    </div>
  );
}

export default BudgetProgressBar;
