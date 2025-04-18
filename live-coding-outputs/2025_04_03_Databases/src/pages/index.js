import Head from 'next/head';
import Link from 'next/link';
import styles from '../styles/Home.module.css';

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Taco Quest</title>
        <meta name="description" content="Discover amazing tacos near you" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <span className={styles.highlight}>Taco Quest</span>
        </h1>

        <p className={styles.description}>
          Your community-driven platform to discover the best tacos around!
        </p>

        <div className={styles.grid}>
          <Link href="/tacos" className={styles.card}>
            <h2>Explore Tacos &rarr;</h2>
            <p>Discover amazing tacos near you and see what others think.</p>
          </Link>

          <Link href="/locations" className={styles.card}>
            <h2>Find Locations &rarr;</h2>
            <p>Find the best taco spots in your area.</p>
          </Link>

          <Link href="/users" className={styles.card}>
            <h2>Taco Community &rarr;</h2>
            <p>Connect with other taco lovers and share your experiences.</p>
          </Link>

          <Link href="/profile" className={styles.card}>
            <h2>Your Profile &rarr;</h2>
            <p>
              View your reviews, achievements, and connections.
            </p>
          </Link>
        </div>
      </main>

      <footer className={styles.footer}>
        <a href="https://github.com/yourusername/taco-quest" target="_blank" rel="noopener noreferrer">
          Powered by Taco Quest
        </a>
      </footer>
    </div>
  );
}
