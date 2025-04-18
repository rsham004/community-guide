import { useState, useEffect } from 'react';

function DateRangeFilter({ startDate, endDate, onChange }) {
  const [localStartDate, setLocalStartDate] = useState(startDate);
  const [localEndDate, setLocalEndDate] = useState(endDate);

  useEffect(() => {
    setLocalStartDate(startDate);
    setLocalEndDate(endDate);
  }, [startDate, endDate]);

  const handleStartDateChange = (e) => {
    const newStartDate = e.target.value;
    setLocalStartDate(newStartDate);
    if (new Date(newStartDate) <= new Date(localEndDate)) {
      onChange(newStartDate, localEndDate);
    }
  };

  const handleEndDateChange = (e) => {
    const newEndDate = e.target.value;
    setLocalEndDate(newEndDate);
    if (new Date(localStartDate) <= new Date(newEndDate)) {
      onChange(localStartDate, newEndDate);
    }
  };

  // Preset date range buttons
  const presets = [
    { label: 'This Month', 
      action: () => {
        const now = new Date();
        const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
        onChange(
          firstDay.toISOString().split('T')[0], 
          now.toISOString().split('T')[0]
        );
      } 
    },
    { label: 'Last Month', 
      action: () => {
        const now = new Date();
        const firstDay = new Date(now.getFullYear(), now.getMonth() - 1, 1);
        const lastDay = new Date(now.getFullYear(), now.getMonth(), 0);
        onChange(
          firstDay.toISOString().split('T')[0], 
          lastDay.toISOString().split('T')[0]
        );
      } 
    },
    { label: 'Last 3 Months', 
      action: () => {
        const now = new Date();
        const threeMonthsAgo = new Date(now);
        threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
        onChange(
          threeMonthsAgo.toISOString().split('T')[0], 
          now.toISOString().split('T')[0]
        );
      } 
    },
    { label: 'This Year', 
      action: () => {
        const now = new Date();
        const firstDay = new Date(now.getFullYear(), 0, 1);
        onChange(
          firstDay.toISOString().split('T')[0], 
          now.toISOString().split('T')[0]
        );
      } 
    },
  ];

  return (
    <div className="mb-4">
      <h3 className="text-lg font-medium mb-2">Date Range</h3>
      
      <div className="flex flex-wrap gap-2 mb-3">
        {presets.map((preset) => (
          <button
            key={preset.label}
            onClick={preset.action}
            className="px-3 py-1 text-sm bg-gray-700 rounded-full text-text-primary hover:bg-gray-600"
          >
            {preset.label}
          </button>
        ))}
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        <div>
          <label className="block text-sm text-text-secondary mb-1">From</label>
          <input
            type="date"
            value={localStartDate}
            onChange={handleStartDateChange}
            className="w-full p-2 bg-background border border-gray-700 rounded-md text-text-primary"
          />
        </div>
        <div>
          <label className="block text-sm text-text-secondary mb-1">To</label>
          <input
            type="date"
            value={localEndDate}
            onChange={handleEndDateChange}
            className="w-full p-2 bg-background border border-gray-700 rounded-md text-text-primary"
          />
        </div>
      </div>
    </div>
  );
}

export default DateRangeFilter;
