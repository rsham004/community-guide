import { Outlet, NavLink } from 'react-router-dom';

function Layout() {
  return (
    <div className="flex h-screen">
      {/* Left Sidebar */}
      <aside className="w-64 bg-surface p-4 flex flex-col">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-primary">Finance Tracker</h1>
        </div>
        
        <nav className="flex flex-col gap-2">
          <NavLink 
            to="/" 
            className={({ isActive }) => 
              `p-2 rounded-md ${isActive ? 'bg-primary text-background' : 'text-text-primary hover:bg-surface/80'}`
            }
            end
          >
            Dashboard
          </NavLink>
          <NavLink 
            to="/history" 
            className={({ isActive }) => 
              `p-2 rounded-md ${isActive ? 'bg-primary text-background' : 'text-text-primary hover:bg-surface/80'}`
            }
          >
            Expense History
          </NavLink>
          <NavLink 
            to="/budgets" 
            className={({ isActive }) => 
              `p-2 rounded-md ${isActive ? 'bg-primary text-background' : 'text-text-primary hover:bg-surface/80'}`
            }
          >
            Budgets
          </NavLink>
        </nav>
        
        <div className="mt-auto">
          <div className="p-4 bg-background rounded-md">
            <p className="text-sm text-text-secondary">
              Finance Tracker v0.1.0
            </p>
          </div>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="flex-1 overflow-auto p-6">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
