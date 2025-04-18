# Plan.md – Implementation Plan for Personal Finance Tracker (Frontend MVP)

## Phase Breakdown

### Phase 1: Project Setup & Design Foundation
- [x] Initialize Vite + React project structure (Easy)
- [x] Set up TailwindCSS for styling (Easy)
- [x] Create basic folder structure as per architecture guide (Easy)
- [x] Integrate React Router with base routes: `/`, `/history`, `/budgets` (Easy)
- [x] Implement dark mode theming (Easy)

### Phase 2: Mock Data & Service Layer
- [x] Create mock data files: `expenses.js`, `budgets.js` (Easy)
- [x] Implement mock service functions for CRUD operations (Easy)
- [x] Connect service layer to mock data (Easy)

### Phase 3: Core Feature – Dashboard
- [x] Build dashboard layout with metric cards and progress ring (Medium)
- [x] Add chart components (e.g., Pie Chart for category spend) (Medium)
- [x] Display summary of this month's total spend and top categories (Medium)

### Phase 4: Core Feature – Add Expense Flow
- [x] Create Add Expense modal with category buttons and input fields (Medium)
- [x] Implement form validation and UI feedback (Medium)
- [x] Simulate saving new expenses to mock data (Easy)

### Phase 5: Core Feature – Expense History
- [x] Create scrollable list for recent expenses (Easy)
- [x] Add category filters and date filter (Medium)
- [x] Display expenses using mock API (Easy)

### Phase 6: Core Feature – Budget View
- [x] Build progress bars per category for budget tracking (Medium)
- [x] Display budget usage from mock budget data (Easy)
- [x] Allow budget values to be adjusted in UI (Medium)

### Phase 7: Final Touches & Deployment
- [ ] Refactor components for reusability (Medium)
- [ ] Add transitions, loading states, and tooltips (Medium)
- [ ] Test app responsiveness across mobile/tablet/desktop (Medium)
- [ ] Deploy frontend to AWS S3 + CloudFront (Medium)

