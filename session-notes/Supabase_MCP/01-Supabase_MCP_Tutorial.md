# Tutorial: Building a Supabase App with an AI Agent via MCP

This guide provides a detailed walkthrough for using an AI-powered IDE (like Cursor or Klein) integrated with the official Supabase MCP (Model Context Protocol) server to build a web application. We'll use Cursor as the primary example.

## 🧰 Prerequisites

1.  **Supabase Account:** You need an account at [supabase.com](https://supabase.com).
2.  **AI-Powered IDE:**
    *   **Cursor:** Download and install from [cursor.sh](https://cursor.sh/).
    *   *(Alternatively) Cline:* An open-source VS Code extension providing similar capabilities.
3.  **Node.js & npm:** Ensure Node.js (which includes npm) is installed. Download from [nodejs.org](https://nodejs.org/). You can verify installation by running `node -v` and `npm -v` in your terminal.
4.  **Git (Optional but Recommended):** For version control and potentially cloning template repositories.

## 🚀 Step-by-Step Guide

### Step 1: Generate a Supabase Personal Access Token (PAT)

This token allows the MCP server (and thus the AI agent) to interact with the Supabase Management API on your behalf to perform actions like creating projects, managing databases, etc.

1.  **Log in to Supabase:** Go to [supabase.com](https://supabase.com) and log in.
2.  **Navigate to Access Tokens:** In your Supabase dashboard, click on your account icon/avatar in the top-right corner, then select "Access Tokens".
3.  **Generate New Token:** Click the "Generate New Token" button.
4.  **Name Your Token:** Give it a descriptive name, like `Cursor_MCP_Token` or `AI_Agent_Access`.
5.  **Copy the Token:** Click "Generate token". **Crucially, copy the generated token immediately.** Supabase will not show it to you again for security reasons.
6.  **Store Securely:** Paste the token into a secure temporary location (like a password manager or a local, temporary text file you'll delete later). **Do not commit this token to Git.**

### Step 2: Set Up Your Project Folder and MCP Configuration

1.  **Create Project Folder:** Create a new, empty folder on your computer where your application will reside (e.g., `my-supabase-app`).
2.  **Create `.cursor` Directory:** Inside your new project folder, create a hidden directory named `.cursor`.
    *   On Mac/Linux: `mkdir .cursor`
    *   On Windows (Command Prompt): `mkdir .cursor`
    *   On Windows (PowerShell): `New-Item -ItemType Directory -Name .cursor`
3.  **Create `mcp.json`:** Inside the `.cursor` directory, create a file named `mcp.json`.
4.  **Add Configuration:** Paste the following JSON structure into `mcp.json`, replacing `"your-token-here"` with the Supabase PAT you generated in Step 1:

    ```json
    {
      "server": "supabase",
      "accessToken": "your-token-here"
    }
    ```
    *   `"server": "supabase"` tells Cursor to use the official Supabase MCP server.
    *   `"accessToken"` provides the necessary authentication.

### Step 3: Configure and Enable the MCP Server in Cursor

1.  **Open Project in Cursor:** Launch Cursor and open the project folder you created (`my-supabase-app`).
2.  **Navigate to MCP Settings:**
    *   Go to `File > Settings` (or `Cursor > Settings` on Mac).
    *   Search for "MCP" or navigate to the MCP section (often under "Extensions" or a dedicated "MCP" category).
3.  **Verify Configuration:** Cursor should automatically detect the `mcp.json` file in your project's `.cursor` directory. You should see "supabase" listed as a server.
4.  **Ensure Token is Set:** Verify that the Access Token field is populated (it should read it from `mcp.json`). If not, paste your Supabase PAT here.
5.  **Enable the Server:** Find the toggle or checkbox next to the "supabase" server entry and enable it.
6.  **Check Status:** The server status indicator should turn green (or show a similar "connected" status), confirming that Cursor can communicate with the Supabase MCP server using your token.

### Step 4: Trigger the AI Agent to Build Your App

Now, you'll instruct Cursor's AI agent to build the application, leveraging the enabled Supabase MCP server.

1.  **Enter Agent Mode:** Use Cursor's interface to start a chat with the AI agent (often via a dedicated panel or keyboard shortcut like `Cmd+K` or `Ctrl+K`).
2.  **Prompt the AI:** Provide a clear instruction. For example:

    ```
    Create a simple web application using React and Supabase. It should be a Movie Watchlist where users can add movie titles, mark them as watched, and delete them. Include user authentication.
    ```
    *(Alternatively: "Make me a to-do list app using React and Supabase with user authentication.")*

3.  **AI Interaction with MCP:** The AI agent will now interact with the Supabase MCP server behind the scenes. You might see logs or status updates indicating actions like:
    *   **Authentication:** Using your PAT via the MCP connection.
    *   **Listing Organizations:** `list_organizations` tool call.
    *   **Creating Project:** `create_project` tool call (it might ask you to confirm the organization and region).
    *   **Creating Schema:** `run_sql_migration` tool call, likely executing SQL similar to the `001_initial_schema.sql` file (creating tables like `movies` or `todos`, setting up primary keys, foreign keys to `auth.users`, and RLS policies).
    *   **Applying Migrations:** Ensuring the database schema matches the requirements.

### Step 5: Observe the App Being Built (Code Generation)

The AI agent will generate the necessary code files for your application. Expect to see:

1.  **Project Scaffolding:** Creation of a standard project structure (e.g., using Vite with React and TypeScript, similar to the structure found in `/live-coding-outputs/2025_04_22_supabase_mcp/supabase-mcp`).
2.  **Package Installation:** The agent might prompt you to run `npm install` or run it automatically to install dependencies listed in `package.json` (e.g., `react`, `react-dom`, `@supabase/supabase-js`, `@chakra-ui/react` if using Chakra).
3.  **Supabase Client:** Creation of a file (e.g., `src/lib/supabase.ts`) to initialize the Supabase JavaScript client using environment variables.
4.  **Environment Variables:** Creation or modification of a `.env` file at the project root to store Supabase credentials:
    ```env
    VITE_SUPABASE_URL=YOUR_PROJECT_URL_FROM_SUPABASE
    VITE_SUPABASE_ANON_KEY=YOUR_PROJECT_ANON_KEY_FROM_SUPABASE
    ```
    *(Note: These are different from your PAT. They are the public URL and anon key for your specific Supabase project, found in Project Settings > API).*
5.  **Frontend Components:** Generation of React components for:
    *   Authentication (`Auth.tsx`): Login/Signup forms.
    *   Adding items (`AddTodo.tsx` or `AddMovie.tsx`).
    *   Displaying items (`TodoList.tsx` or `Watchlist.tsx`).
    *   Individual item display (`TodoItem.tsx` or `MovieItem.tsx`).
    *   Main application structure (`App.tsx`).
    *   Authentication context (`AuthContext.tsx`).
6.  **Logic:** Implementation of JavaScript/TypeScript functions to interact with Supabase for CRUD operations (Create, Read, Update, Delete) and authentication.

### Step 6: Run and Test the Application

1.  **Install Dependencies (if needed):** If the agent didn't run it, open a terminal in your project folder and run:
    ```bash
    npm install
    ```
2.  **Start the Development Server:**
    ```bash
    npm start
    ```
    *(Or `npm run dev` depending on the `package.json` scripts generated, often configured by Vite).*
3.  **Access the App:** Open your web browser and navigate to the local address provided (usually `http://localhost:5173` or `http://localhost:3000`).
4.  **Test Functionality:**
    *   Try adding a movie/todo item.
    *   Mark an item as watched/complete.
    *   Delete an item.
5.  **Verify in Supabase:** Go to your Supabase project dashboard.
    *   **Table Editor:** Check if the `movies` or `todos` table exists and if your test data appears there.
    *   *(Troubleshooting):* If adding items fails due to a missing table, the AI agent (if still active) might detect this and offer to create/recreate the table using the MCP `run_sql_migration` tool.

### Step 7: Add and Test Authentication

1.  **Prompt for Auth (if needed):** If the initial prompt didn't include authentication, ask the agent:
    ```
    Add user authentication (sign up and sign in) to the application using Supabase Auth. Only logged-in users should be able to see and manage their watchlist/todos.
    ```
2.  **Observe Auth UI:** The agent should generate or modify components to include login and signup forms (like `Auth.tsx`). It might wrap the main app component in an `AuthProvider`.
3.  **Test Signup/Login:**
    *   Use the UI in your running application to sign up for a new account.
    *   Try logging out and logging back in.
    *   Ensure you can only see/modify data when logged in.
4.  **Verify in Supabase:** Go to your Supabase project dashboard.
    *   Navigate to **Authentication > Users**. You should see the user account you created during testing.

### Step 8: Optional - Deploy or Expand

1.  **Add Features:** Ask the agent to add more features, such as:
    *   Fetching movie details from an external API (like TMDB). This might involve creating a Supabase Edge Function.
    *   Allowing users to upload movie posters (using Supabase Storage).
    *   Adding sorting or filtering options.
2.  **Deployment:** Ask the agent for deployment steps (e.g., building the app with `npm run build` and deploying to a hosting provider like Vercel or Netlify).
3.  **Explore Cline:** Try repeating the process using the Cline VS Code extension for an open-source alternative. Example output for Cline might be found in `/live-coding-outputs/2025_04_22_supabase_mcp/supabase-mcp-cline`.

---

This detailed guide should help you leverage the power of AI agents and Supabase MCP to rapidly build and iterate on your web applications. Remember that AI agent capabilities can vary, and you might need to guide or correct the agent occasionally.
