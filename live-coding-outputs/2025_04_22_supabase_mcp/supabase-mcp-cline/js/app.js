// Initialize Supabase client
const supabaseUrl = SUPABASE_CONFIG.url;
const supabaseKey = SUPABASE_CONFIG.anonKey;
const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);

// DOM Elements
const movieTitleInput = document.getElementById('movie-title');
const addMovieBtn = document.getElementById('add-movie-btn');
const watchlistContainer = document.getElementById('watchlist');
const authContainer = document.getElementById('auth-container');
const signinBtn = document.getElementById('signin-btn');
const signupBtn = document.getElementById('signup-btn');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');

// State
let currentUser = null;
let movies = []; // To store the fetched movies

// Initialize the application
function init() {
    // Add event listeners
    addMovieBtn.addEventListener('click', handleAddMovie);
    signinBtn.addEventListener('click', handleSignIn);
    signupBtn.addEventListener('click', handleSignUp);

    // Check if user is already logged in
    checkAuthState();
}

// Add Movie
async function handleAddMovie() {
    const title = movieTitleInput.value.trim();

    if (!title) {
        alert('Please enter a movie title.');
        return;
    }

    if (!currentUser) {
        showAuthModal();
        return;
    }

    addMovieBtn.disabled = true;
    addMovieBtn.textContent = 'Adding...';

    try {
        const { error } = await supabase.from('movies').insert([
            {
                title: title,
                user_id: currentUser.id,
                watched: false // Default to unwatched
            },
        ]);

        if (error) throw error;

        movieTitleInput.value = ''; // Clear input
        await fetchMovies(); // Refresh the list
        alert('Movie added successfully!');

    } catch (error) {
        console.error('Error adding movie:', error);
        alert('Failed to add movie. Please try again.');
    } finally {
        addMovieBtn.disabled = false;
        addMovieBtn.textContent = 'Add to Watchlist';
    }
}

// Fetch Movies
async function fetchMovies() {
    if (!currentUser) {
        watchlistContainer.innerHTML = '<p>Please sign in to see your watchlist.</p>';
        return;
    }

    watchlistContainer.innerHTML = '<p>Loading watchlist...</p>'; // Show loading state

    try {
        const { data, error } = await supabase
            .from('movies')
            .select('*')
            .eq('user_id', currentUser.id)
            .order('created_at', { ascending: false });

        if (error) throw error;

        movies = data || [];
        renderWatchlist();

    } catch (error) {
        console.error('Error fetching movies:', error);
        watchlistContainer.innerHTML = '<p>Failed to load watchlist. Please try again.</p>';
    }
}

// Render Watchlist
function renderWatchlist() {
    watchlistContainer.innerHTML = ''; // Clear previous content

    if (movies.length === 0) {
        watchlistContainer.innerHTML = '<p>Your watchlist is empty. Add a movie above!</p>';
        return;
    }

    movies.forEach(movie => {
        const item = document.createElement('div');
        item.className = 'watchlist-item';

        const details = document.createElement('div');
        details.className = 'watchlist-item-details';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.checked = movie.watched;
        checkbox.addEventListener('change', () => toggleWatched(movie.id, movie.watched));

        const titleSpan = document.createElement('span');
        titleSpan.className = 'watchlist-item-title';
        titleSpan.textContent = movie.title;
        if (movie.watched) {
            titleSpan.classList.add('watched');
        }

        details.appendChild(checkbox);
        details.appendChild(titleSpan);

        const actions = document.createElement('div');
        actions.className = 'watchlist-item-actions';

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'secondary-btn delete-btn';
        deleteBtn.textContent = 'Delete';
        deleteBtn.addEventListener('click', () => deleteMovie(movie.id));

        actions.appendChild(deleteBtn);

        item.appendChild(details);
        item.appendChild(actions);

        watchlistContainer.appendChild(item);
    });
}

// Toggle Watched Status
async function toggleWatched(id, currentStatus) {
    try {
        const { error } = await supabase
            .from('movies')
            .update({ watched: !currentStatus })
            .eq('id', id);

        if (error) throw error;
        await fetchMovies(); // Refresh list after update

    } catch (error) {
        console.error('Error updating watched status:', error);
        alert('Failed to update watched status.');
    }
}

// Delete Movie
async function deleteMovie(id) {
    if (!confirm('Are you sure you want to delete this movie?')) {
        return;
    }

    try {
        const { error } = await supabase
            .from('movies')
            .delete()
            .eq('id', id);

        if (error) throw error;
        await fetchMovies(); // Refresh list after delete
        alert('Movie deleted successfully!');

    } catch (error) {
        console.error('Error deleting movie:', error);
        alert('Failed to delete movie.');
    }
}


// --- Authentication Functions ---

function showAuthModal() {
    authContainer.style.display = 'flex';
}

function hideAuthModal() {
    authContainer.style.display = 'none';
    // Clear form
    emailInput.value = '';
    passwordInput.value = '';
}

async function handleSignIn() {
    const email = emailInput.value;
    const password = passwordInput.value;

    if (!email || !password) {
        alert('Please enter email and password');
        return;
    }

    signinBtn.disabled = true;
    signinBtn.textContent = 'Signing In...';

    try {
        const { data, error } = await supabase.auth.signInWithPassword({
            email,
            password
        });

        if (error) throw error;

        hideAuthModal();
        currentUser = data.user;
        updateAuthUI();
        fetchMovies(); // Load movies after sign in

    } catch (error) {
        console.error('Error signing in:', error);
        alert('Failed to sign in. Please check your credentials and try again.');
    } finally {
        signinBtn.disabled = false;
        signinBtn.textContent = 'Sign In';
    }
}

async function handleSignUp() {
    const email = emailInput.value;
    const password = passwordInput.value;

    if (!email || !password) {
        alert('Please enter email and password');
        return;
    }

    signupBtn.disabled = true;
    signupBtn.textContent = 'Signing Up...';

    try {
        const { data, error } = await supabase.auth.signUp({
            email,
            password
        });

        if (error) throw error;

        alert('Sign up successful! Please check your email for verification.');
        hideAuthModal();
        // Optionally sign in the user automatically or wait for verification
        // currentUser = data.user;
        // updateAuthUI();
        // fetchMovies();

    } catch (error) {
        console.error('Error signing up:', error);
        alert('Failed to sign up. Please try again.');
    } finally {
        signupBtn.disabled = false;
        signupBtn.textContent = 'Sign Up';
    }
}

async function handleSignOut() {
    try {
        const { error } = await supabase.auth.signOut();
        if (error) throw error;
        currentUser = null;
        movies = []; // Clear movies on sign out
        updateAuthUI();
        renderWatchlist(); // Clear the rendered list
    } catch (error) {
        console.error('Error signing out:', error);
        alert('Failed to sign out.');
    }
}

async function checkAuthState() {
    try {
        const { data, error } = await supabase.auth.getSession();

        if (error) throw error;

        if (data.session) {
            currentUser = data.session.user;
            fetchMovies();
        } else {
            watchlistContainer.innerHTML = '<p>Please sign in to see your watchlist.</p>';
        }
        updateAuthUI();

        // Listen for auth changes
        supabase.auth.onAuthStateChange((_event, session) => {
            currentUser = session?.user ?? null;
            updateAuthUI();
            if (currentUser) {
                fetchMovies();
            } else {
                movies = [];
                renderWatchlist(); // Clear list if user signs out
            }
        });

    } catch (error) {
        console.error('Error checking auth state:', error);
        watchlistContainer.innerHTML = '<p>Error loading application state.</p>';
    }
}

function updateAuthUI() {
    // Add a sign-out button if user is logged in
    const header = document.querySelector('header');
    let signOutBtn = document.getElementById('signout-btn');

    if (currentUser) {
        if (!signOutBtn) {
            signOutBtn = document.createElement('button');
            signOutBtn.id = 'signout-btn';
            signOutBtn.textContent = 'Sign Out';
            signOutBtn.className = 'secondary-btn';
            signOutBtn.style.position = 'absolute';
            signOutBtn.style.top = '20px';
            signOutBtn.style.right = '20px';
            signOutBtn.addEventListener('click', handleSignOut);
            header.style.position = 'relative'; // Needed for absolute positioning of button
            header.appendChild(signOutBtn);
        }
        addMovieBtn.disabled = false; // Enable add button
    } else {
        if (signOutBtn) {
            signOutBtn.remove();
        }
        addMovieBtn.disabled = true; // Disable add button if not logged in
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', init);
