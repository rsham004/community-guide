import { useEffect } from 'react';
import { RouterProvider } from 'react-router-dom';
import router from './router';
import { ToastProvider } from './context/ToastContext';
import AddExpenseButton from './components/expense/AddExpenseButton';

function App() {
  // Set dark mode by default and log mount for debugging
  useEffect(() => {
    console.log('App mounted!');
    document.documentElement.classList.add('dark');
  }, []);

  return (
    <ToastProvider>
      <div className="min-h-screen bg-background text-text-primary">
        <RouterProvider router={router} />
        <AddExpenseButton />
      </div>
    </ToastProvider>
  );
}

export default App;
