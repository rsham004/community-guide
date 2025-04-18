import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import useSWR from 'swr';
import styles from '../../styles/Locations.module.css';

// Fetch function for SWR
const fetcher = (...args) => fetch(...args).then(res => res.json());

export default function Locations() {
  const { data, error, isLoading } = useSWR('/api/locations', fetcher);
  const [sortBy, setSortBy] = useState('rating');

  if (error) return <div>Failed to load locations</div>;
  if (isLoading) return <div>Loading...</div>;
  if (!data || !Array.isArray(data)) return <div>No locations found</div>;

  // Sort locations based on selected criteria
  const sortedLocations = [...data].sort((a, b) => {
    if (sortBy === 'rating') {
      // Sort by average rating (highest first)
      return (b.averageRating || 0) - (a.averageRating || 0);
    } else if (sortBy === 'reviews') {
      // Sort by number of reviews (highest first)
      return b.reviewCount - a.reviewCount;
    } else if (sortBy === 'tacos') {
      // Sort by number of tacos (highest first)
      return b.tacoCount - a.tacoCount;
    } else {
      // Sort by name (alphabetically)
      return a.name.localeCompare(b.name);
    }
  });

  return (
    <div className={styles.container}>
      <Head>
        <title>Taco Locations | Taco Quest</title>
        <meta name="description" content="Find the best taco locations near you" />
      </Head>

      <header className={styles.header}>
        <h1>Taco Locations</h1>
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
              <option value="tacos">Number of Tacos</option>
              <option value="name">Name (A-Z)</option>
            </select>
          </label>
        </div>
      </header>

      <div className={styles.grid}>
        {sortedLocations.map((location) => (
          <div key={location.id} className={styles.card}>
            <div className={styles.cardHeader}>
              <h2>{location.name}</h2>
              {location.averageRating ? (
                <div className={styles.rating}>
                  {location.averageRating} ⭐ ({location.reviewCount})
                </div>
              ) : (
                <div className={styles.noRating}>No ratings yet</div>
              )}
            </div>
            <div className={styles.address}>
              {location.address}
            </div>
            <div className={styles.tacoCount}>
              <strong>{location.tacoCount}</strong> {location.tacoCount === 1 ? 'taco' : 'tacos'} available
            </div>
            <div className={styles.coordinatesContainer}>
              <div className={styles.coordinates}>
                {location.lat.toFixed(4)}, {location.lon.toFixed(4)}
              </div>
            </div>
            <Link href={`/locations/${location.id}`} className={styles.viewButton}>
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
