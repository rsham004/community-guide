# Architecture Guide – Personal Finance Tracker (Frontend MVP with Mock Data)

## Architecture Pattern
**Pattern:** Monolithic Single-Page Application (SPA) with Mock Backend  
**Why:** Ideal for MVP and demo purposes with no real backend or database. Uses local mock data to simulate API responses for development and UI showcase.

- Entire application runs in the browser
- Backend API calls are simulated using mocked data responses (e.g., JSON files or utility functions)
- Fully frontend-based architecture for rapid prototyping and UX testing

## State Management
- **Frontend:** React with local state managed via hooks (`useState`, `useEffect`) and context (`useContext`)
- **Data Source:** In-memory mock data stored in local JSON files or JavaScript objects
- **Persistence:** No data persistence across page reloads; state resets on refresh (unless browser storage is added later)

## Technical Stack

### Frontend
- **Framework:** React (with Vite)
- **UI Library:** TailwindCSS for responsive layout and consistent styling
- **Charting:** Recharts for dynamic visualizations (bar, pie, and line charts)
- **Mocking:** Custom utility files (e.g., `mockExpenses.js`) simulate API behavior
- **Routing:** React Router DOM for multi-page views
- **Deployment:** AWS S3 + CloudFront (static site hosting)

### Backend
- **None implemented in MVP**
- Future upgrade path will use Express.js or FastAPI for real endpoints

### Authentication & Payments
- **Not required for frontend demo**

### Integrations
- **None in MVP**  
- Future integrations may include analytics, email alerts, or cloud database APIs

## Authentication Process
Not implemented. All features are available without login or session management.

## Route Design

### Frontend Routes
- `/` – Dashboard with total spend, budget usage ring, and category summary
- `/history` – Expense history list with filtering
- `/budgets` – Set mock budget limits per category and visualize usage

## API Design (Mocked)

### Simulated API calls using `setTimeout()` or mocked fetch utilities

- `GET /api/expenses` – Load mock expenses from a local JSON object
- `POST /api/expenses` – Simulate appending a new entry to mock data
- `GET /api/summary` – Return aggregate values and chart data
- `GET /api/budgets` – Load mock budget limits from local data

## Database Design
**None implemented in MVP** – mock data will be stored in memory or in local files like:

```js
// mockExpenses.js
export const expenses = [
  { id: "1", amount: 15.75, category: "Groceries", date: "2025-04-08", note: "Snacks" },
  { id: "2", amount: 120, category: "Rent", date: "2025-04-01", note: "April Rent" }
];
```

---

This architecture is optimized for demoing the user interface and validating design decisions with stakeholders before committing to backend development. Ideal for rapid iteration and feedback gathering.


## Proposed Folder Structure

```plaintext
finance-tracker-app/
├── public/                     # Static assets
│   └── index.html
├── src/
│   ├── assets/                 # Icons, images, logos
│   ├── components/             # Reusable UI components (Button, Card, Chart, etc.)
│   ├── features/               # Feature-based folders for app sections
│   │   ├── dashboard/          # Dashboard views and components
│   │   ├── history/            # Expense history list and filters
│   │   ├── budgets/            # Budget setting and progress views
│   ├── mock/                   # Mock data for simulating backend
│   │   ├── expenses.js
│   │   ├── budgets.js
│   ├── services/               # API abstraction layer for mock/future real APIs
│   │   ├── expenseService.js
│   │   ├── budgetService.js
│   ├── styles/                 # Tailwind config or global CSS overrides
│   ├── App.jsx                 # Main App component
│   ├── main.jsx                # App entry point
│   └── router.jsx              # React Router setup
├── .gitignore
├── tailwind.config.js
├── vite.config.js
├── package.json
└── README.md
```

---

This folder structure separates concerns cleanly for scalability and keeps mock data swappable with real services later. Feature-based structure ensures a smooth transition to larger teams or modular micro frontends.
