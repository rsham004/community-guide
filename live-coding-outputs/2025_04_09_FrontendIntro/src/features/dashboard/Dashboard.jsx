import { useEffect, useState } from "react";
import { expenseService } from "../../services/expenseService";
import { budgetService } from "../../services/budgetService";

import MetricCard from "../../components/dashboard/MetricCard";
import ProgressRing from "../../components/dashboard/ProgressRing";
import PieChart from "../../components/charts/PieChart";
import LineChart from "../../components/charts/LineChart";

function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [totalSpent, setTotalSpent] = useState(0);
  const [categoryData, setCategoryData] = useState([]);
  const [budgetUsage, setBudgetUsage] = useState([]);
  const [spendingTrend, setSpendingTrend] = useState([]);
  const [overallBudgetPercentage, setOverallBudgetPercentage] = useState(0);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      try {
        // Fetch total expenses
        const total = await expenseService.getTotalExpenses();
        setTotalSpent(total);

        // Fetch category breakdown
        const categories = await expenseService.getCategorySummary();
        setCategoryData(categories);

        // Fetch budget usage
        const usage = await budgetService.getBudgetUsage();
        setBudgetUsage(usage);

        // Calculate overall budget usage
        const totalBudget = usage.reduce((sum, item) => sum + item.limit, 0);
        setOverallBudgetPercentage((total / totalBudget) * 100);

        // Generate mock spending trend (this would normally come from API)
        const mockTrend = [
          { date: '2025-04-01', amount: 150 },
          { date: '2025-04-05', amount: 220 },
          { date: '2025-04-10', amount: 320 },
          { date: '2025-04-15', amount: 410 },
          { date: '2025-04-20', amount: 550 },
          { date: '2025-04-25', amount: 580 },
          { date: '2025-04-30', amount: 650 },
        ];
        setSpendingTrend(mockTrend);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-full">Loading dashboard data...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      
      {/* Top metrics row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <MetricCard 
          title="Total Spent" 
          value={`$${totalSpent.toFixed(2)}`} 
          subtitle="This Month" 
          color="primary" 
        />
        <MetricCard 
          title="Categories" 
          value={categoryData.length} 
          subtitle="Spending Areas" 
          color="secondary" 
        />
        <MetricCard 
          title="Highest Category" 
          value={categoryData.length > 0 
            ? `$${Math.max(...categoryData.map(c => c.amount)).toFixed(2)}` 
            : '$0.00'
          } 
          subtitle={categoryData.length > 0 
            ? categoryData.reduce((max, cat) => cat.amount > max.amount ? cat : max, categoryData[0]).category 
            : 'None'
          }
          color="accent1" 
        />
        <div className="card flex flex-col items-center justify-center">
          <h3 className="text-lg font-semibold mb-2">Budget Usage</h3>
          <ProgressRing percentage={overallBudgetPercentage} />
        </div>
      </div>
      
      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Spending by Category</h3>
          <PieChart data={categoryData} dataKey="amount" nameKey="category" />
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">Monthly Spending Trend</h3>
          <LineChart data={spendingTrend} dataKey="amount" xAxisKey="date" />
        </div>
      </div>
      
      {/* Budget progress section */}
      <div className="card mb-6">
        <h3 className="text-lg font-semibold mb-4">Budget Progress</h3>
        <div className="space-y-4">
          {budgetUsage.map(budget => (
            <div key={budget.category} className="mb-2">
              <div className="flex justify-between mb-1">
                <span>{budget.category}</span>
                <span>${budget.spent.toFixed(2)} / ${budget.limit.toFixed(2)}</span>
              </div>
              <div className="w-full bg-background rounded-full h-2.5">
                <div 
                  className={`h-2.5 rounded-full ${
                    budget.percentage > 90 ? 'bg-red-500' : 
                    budget.percentage > 75 ? 'bg-yellow-500' : 
                    'bg-primary'
                  }`} 
                  style={{ width: `${Math.min(100, budget.percentage)}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
