import { useState } from 'react';
import BudgetProgressBar from './BudgetProgressBar';
import BudgetForm from './BudgetForm';

function BudgetItem({ budget, onUpdate }) {
  const [isEditing, setIsEditing] = useState(false);

  const handleSave = async (updatedBudget) => {
    try {
      await onUpdate(updatedBudget);
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update budget:", error);
    }
  };

  if (isEditing) {
    return (
      <div className="card mb-4">
        <h3 className="text-lg font-medium mb-3">{budget.category}</h3>
        <BudgetForm 
          budget={budget} 
          onSave={handleSave}
          onCancel={() => setIsEditing(false)}
        />
      </div>
    );
  }

  return (
    <div className="card mb-4">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-medium">{budget.category}</h3>
          {budget.description && (
            <p className="text-sm text-text-secondary">{budget.description}</p>
          )}
        </div>
        <button
          onClick={() => setIsEditing(true)}
          className="text-sm bg-gray-800 hover:bg-gray-700 text-text-primary px-3 py-1 rounded-md transition-colors"
        >
          Edit
        </button>
      </div>
      
      <BudgetProgressBar 
        category={budget.category}
        limit={budget.limit}
        spent={budget.spent}
        percentage={budget.percentage}
      />
      
      <div className="mt-2 text-sm text-text-secondary">
        <span className={budget.remaining < 0 ? 'text-red-500' : 'text-secondary'}>
          ${Math.abs(budget.remaining).toFixed(2)} {budget.remaining < 0 ? 'over budget' : 'remaining'}
        </span>
      </div>
    </div>
  );
}

export default BudgetItem;
