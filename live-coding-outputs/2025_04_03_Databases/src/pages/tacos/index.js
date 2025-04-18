import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import useSWR from 'swr';
import styles from '../../styles/Tacos.module.css';

// Fetch function for SWR
const fetcher = (...args) => fetch(...args).then(res => res.json());

export default function Tacos() {
  const { data, error, isLoading } = useSWR('/api/tacos', fetcher);
  const [sortBy, setSortBy] = useState('rating');

  if (error) return <div>Failed to load tacos</div>;
  if (isLoading) return <div>Loading...</div>;
  if (!data || !Array.isArray(data)) return <div>No tacos found</div>;

  // Sort tacos based on selected criteria
  const sortedTacos = [...data].sort((a, b) => {
    if (sortBy === 'rating') {
      // Sort by average rating (highest first)
      return (b.averageRating || 0) - (a.averageRating || 0);
    } else if (sortBy === 'reviews') {
      // Sort by number of reviews (highest first)
      return b.reviewCount - a.reviewCount;
    } else {
      // Sort by name (alphabetically)
      return a.name.localeCompare(b.name);
    }
  });

  return (
    <div className={styles.container}>
      <Head>
        <title>Tacos | Taco Quest</title>
        <meta name="description" content="Discover amazing tacos near you" />
      </Head>

      <header className={styles.header}>
        <h1>Explore Tacos</h1>
        <div className={styles.controls}>
          <label>
            Sort by:
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              className={styles.select}
            >
              <option value="rating">Rating (Highest First)</option>
              <option value="reviews">Number of Reviews</option>
              <option value="name">Name (A-Z)</option>
            </select>
          </label>
        </div>
      </header>

      <div className={styles.grid}>
        {sortedTacos.map((taco) => (
          <div key={taco.id} className={styles.card}>
            <div className={styles.cardHeader}>
              <h2>{taco.name}</h2>
              {taco.averageRating ? (
                <div className={styles.rating}>
                  {taco.averageRating} ⭐ ({taco.reviewCount})
                </div>
              ) : (
                <div className={styles.noRating}>No ratings yet</div>
              )}
            </div>
            <p className={styles.description}>{taco.description}</p>
            <div className={styles.location}>
              <strong>Location:</strong> {taco.location.name}
            </div>
            <div className={styles.address}>
              {taco.location.address}
            </div>
            <Link href={`/tacos/${taco.id}`} className={styles.viewButton}>
              View Details
            </Link>
          </div>
        ))}
      </div>

      <Link href="/" className={styles.backButton}>
        Back to Home
      </Link>
    </div>
  );
}
