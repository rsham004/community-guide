-- Create movies table to store watchlist items
CREATE TABLE IF NOT EXISTS movies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    watched BOOLEAN NOT NULL DEFAULT false,
    -- Optional fields for future enhancement (e.g., TMDB integration)
    -- tmdb_id INTEGER,
    -- poster_path TEXT,
    -- overview TEXT,
    -- release_year INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- Create index for faster queries by user_id
CREATE INDEX IF NOT EXISTS movies_user_id_idx ON movies(user_id);

-- Create index for sorting by creation date
CREATE INDEX IF NOT EXISTS movies_created_at_idx ON movies(created_at);

-- Enable Row Level Security
ALTER TABLE movies ENABLE ROW LEVEL SECURITY;

-- Create policy to allow users to view only their own movies
CREATE POLICY movies_select_policy ON movies
    FOR SELECT USING (auth.uid() = user_id);

-- Create policy to allow users to insert only their own movies
CREATE POLICY movies_insert_policy ON movies
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create policy to allow users to update only their own movies (title and watched status)
CREATE POLICY movies_update_policy ON movies
    FOR UPDATE USING (auth.uid() = user_id);

-- Create policy to allow users to delete only their own movies
CREATE POLICY movies_delete_policy ON movies
    FOR DELETE USING (auth.uid() = user_id);

-- Remove previous storage bucket and policies if they exist (optional, for cleanup)
-- Note: Manually check if 'wallpapers' bucket exists before running these in production
-- DELETE FROM storage.buckets WHERE id = 'wallpapers';
-- DROP POLICY IF EXISTS wallpapers_storage_select_policy ON storage.objects;
-- DROP POLICY IF EXISTS wallpapers_storage_insert_policy ON storage.objects;
-- DROP POLICY IF EXISTS wallpapers_storage_update_policy ON storage.objects;
-- DROP POLICY IF EXISTS wallpapers_storage_delete_policy ON storage.objects;

-- Create function to update updated_at timestamp (if not already existing from previous schema)
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop previous trigger if it exists
DROP TRIGGER IF EXISTS update_wallpapers_updated_at ON wallpapers;

-- Create trigger to automatically update updated_at timestamp for movies table
CREATE TRIGGER update_movies_updated_at
BEFORE UPDATE ON movies
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
