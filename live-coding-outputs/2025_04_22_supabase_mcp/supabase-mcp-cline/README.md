# Movie Watchlist

A simple web application for managing a personal movie watchlist, built with HTML, CSS, JavaScript, and Supabase for backend services.

## Features

- Add movies to your personal watchlist.
- Mark movies as watched or unwatched.
- Delete movies from your watchlist.
- User authentication via Supabase (Email/Password).
- Data persistence using Supabase database.
- Simple, responsive design.

## Demo

*(Demo files may need updating or removal)* To see a basic layout, open the `public/demo.html` file in your browser (note: this demo file might not reflect the final application structure).

## Setup Instructions

### Prerequisites

- [Supabase Account](https://supabase.com/)
- Web browser

### Local Development

1.  Clone this repository:
    ```
    git clone https://github.com/yourusername/movie-watchlist.git
    cd movie-watchlist
    ```

2.  Open `index.html` in your browser to use the application locally.

### Supabase Setup

1.  Create a new Supabase project at [https://app.supabase.com](https://app.supabase.com)

2.  Get your Supabase URL and anon key from the project settings (Project Settings > API).

3.  Update the Supabase configuration in `js/config.js`:
    ```javascript
    const SUPABASE_CONFIG = {
        url: 'YOUR_SUPABASE_URL',
        anonKey: 'YOUR_SUPABASE_ANON_KEY'
    };
    ```

4.  Apply the database migration:
    - Go to the SQL Editor in your Supabase dashboard.
    - Copy the contents of `migrations/001_initial_schema.sql`.
    - Paste and run the SQL in the editor.

5.  Enable Email Auth in Authentication > Providers settings within your Supabase project dashboard. Disable "Confirm email" if you want users to be able to log in immediately after signup, otherwise they will need to click a link in their email.

## How to Use

1.  Open the `index.html` file in your web browser.
2.  Sign up for a new account or sign in if you already have one.
3.  Enter a movie title in the input field and click "Add to Watchlist".
4.  Your added movies will appear in the "Your Watchlist" section.
5.  Click the checkbox next to a movie to mark it as watched/unwatched.
6.  Click the "Delete" button to remove a movie from your list.
7.  Click "Sign Out" (top right) to log out.

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Supabase (Authentication, Database)
- **Styling**: Custom CSS

## Project Structure

```
movie-watchlist/
├── index.html          # Main HTML file
├── css/
│   └── styles.css      # Stylesheet
├── js/
│   ├── app.js          # Application logic
│   └── config.js       # Supabase configuration
├── migrations/
│   └── 001_initial_schema.sql  # Database schema
├── public/             # Public assets (demo files might be outdated)
│   └── demo.html
├── supabase/           # Supabase specific files (functions removed/modified)
│   └── functions/
│       ├── .gitignore
│       ├── deno.json
│       └── deploy.sh   # Script to link project (no functions deployed)
├── .gitignore          # Git ignore file
├── LICENSE             # MIT License file
└── README.md           # Documentation (this file)
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
