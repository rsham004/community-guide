#!/bin/bash

# Supabase Project Link Script (Edge Functions removed)

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "Supabase CLI is not installed. Please install it first:"
    echo "npm install -g supabase"
    exit 1
fi

# Check if user is logged in
if ! supabase status &> /dev/null; then
    echo "You are not logged in to Supabase CLI or not inside a linked project. Please login and link your project first:"
    echo "supabase login"
    echo "supabase link --project-ref YOUR_PROJECT_REF"
    # Attempt to link if not linked
    PROJECT_REF="mtrdeegsedalhmrmqdwl" # Replace with placeholder or prompt if needed
    echo "Attempting to link project reference: $PROJECT_REF"
    supabase link --project-ref $PROJECT_REF
    if [ $? -ne 0 ]; then
        echo "Failed to link project. Please link it manually."
        exit 1
    fi
fi

# Get project reference if already linked
LINKED_PROJECT_REF=$(supabase status | grep 'Project Ref' | awk '{print $3}')
if [ -z "$LINKED_PROJECT_REF" ]; then
    echo "Could not determine linked project reference. Please ensure the project is linked."
    exit 1
fi
echo "Project linked: $LINKED_PROJECT_REF"

# No Edge Functions to deploy in this version.
echo ""
echo "Project is linked. No Edge Functions to deploy for the basic Movie Watchlist."
echo "You can now apply the database migration using the Supabase dashboard's SQL Editor:"
echo "1. Go to your Supabase project dashboard."
echo "2. Navigate to the SQL Editor."
echo "3. Paste the content of 'migrations/001_initial_schema.sql' and run it."
echo ""
echo "Setup is ready for the database."
