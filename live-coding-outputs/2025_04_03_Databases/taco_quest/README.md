# 🌮 Taco Quest

A community-driven taco discovery platform where users can explore tacos by location, share reviews, follow other taco lovers, and earn achievements.

## 🚀 Project Overview

Taco Quest is designed as a scalable application with:
- SQLModel-based database layer
- Flexible configuration
- Clean architecture principles
- Modular design for maintainability
- Supabase integration for cloud database

## 🛠️ Technology Stack

- **Python 3.8+**
- **SQLModel** - SQL database interaction with Python types
- **SQLite** - Development database
- **Supabase** - Cloud database for production
- **Python-dotenv** - Environment variable management

## 🏗️ Project Structure

```
taco_quest/
├── app/
│   ├── database/         # Database models and connection handling
│   ├── config/           # Application configuration
│   ├── seeds/            # Mock data generation
│   └── utils/            # Utility functions
├── tests/                # Unit tests
├── main.py               # Application entry point
└── .gitignore            # Git ignore configuration
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- uv (Python package manager)
- Supabase account (for cloud database)

### Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/taco-quest.git
   cd taco-quest
   ```

2. Set up a Python environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies with uv
   ```bash
   uv pip install sqlmodel pydantic python-dotenv typer
   # For Supabase integration
   uv pip install supabase
   ```

4. Configure environment variables in a `.env` file:
   ```ini
   # Database configuration
   DB_TYPE=sqlite  # or supabase
   DB_NAME=taco_quest.db
   
   # Supabase Configuration
   USE_SUPABASE=False  # Set to True to use Supabase
   SUPABASE_URL=https://your-project-ref.supabase.co
   SUPABASE_KEY=your-supabase-service-role-key
   SUPABASE_PUBLIC_KEY=your-supabase-anon-public-key
   
   # For direct database connection (optional)
   SUPABASE_DB_HOST=db.your-project-ref.supabase.co
   SUPABASE_DB_PORT=5432
   SUPABASE_DB_NAME=postgres
   SUPABASE_DB_USER=postgres
   SUPABASE_DB_PASSWORD=your-database-password
   
   # Application settings
   DEBUG=True
   ECHO_SQL=False
   ```

5. Initialize the database
   ```bash
   python main.py
   ```

### Supabase Integration

To use Supabase as your database backend:

1. Create a Supabase project at https://supabase.com
2. Get your API credentials from the project dashboard
3. Update your `.env` file with the Supabase credentials
4. Test the connection:
   ```bash
   python main.py --test-supabase
   ```
5. Migrate your data to Supabase:
   ```bash
   python main.py --migrate-to-supabase
   ```
6. Set `USE_SUPABASE=True` in your `.env` file to use Supabase

### Command-Line Options

```bash
# Reset the database (caution: deletes all data)
python main.py --reset

# Seed the database with mock data
python main.py --seed

# Specify number of users to create
python main.py --seed --users 20

# Run demo queries
python main.py --demo

# Show debug information
python main.py --debug

# Test Supabase connection only (no schema required)
python main.py --test-supabase

# Create Supabase schema (tables) for migration
python main.py --create-supabase-schema

# Migrate data from SQLite to Supabase
python main.py --migrate-to-supabase
```

## 📝 Next Steps

- Implement API endpoints
- Add user authentication
- Develop the frontend

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
