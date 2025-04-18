import { createBrowserRouter } from 'react-router-dom';
import Layout from './components/Layout';

// Feature pages
import Dashboard from './features/dashboard/Dashboard';
import History from './features/history/History';
import Budgets from './features/budgets/Budgets';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Dashboard />
      },
      {
        path: 'history',
        element: <History />
      },
      {
        path: 'budgets',
        element: <Budgets />
      }
    ]
  }
]);

export default router;
