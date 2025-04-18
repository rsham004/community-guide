import prisma from '../../../lib/prisma';
import { supabase } from '../../../lib/supabase';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    console.log('GET /api/locations request received');
    
    try {
      // First try using Prisma
      console.log('Attempting to retrieve locations via Prisma...');
      
      // Debug database connection
      console.log('Database URL:', process.env.DATABASE_URL ? 
        `Set (starts with ${process.env.DATABASE_URL.split('://')[0]})` : 
        'Not set! This will cause connection errors.');
      
      // First try with Prisma
      try {
        const locations = await prisma.location.findMany({
          include: {
            tacos: {
              include: {
                reviews: true
              }
            }
          }
        });
        
        console.log('Fetched locations via Prisma:', locations?.length || 0);
        
        if (locations && locations.length > 0) {
          // Add taco count and average rating to each location
          const enhancedLocations = locations.map(location => {
            const allReviews = location.tacos.flatMap(taco => taco.reviews);
            const avgRating = allReviews.length > 0
              ? allReviews.reduce((sum, review) => sum + review.rating, 0) / allReviews.length
              : null;
            
            return {
              ...location,
              tacoCount: location.tacos.length,
              reviewCount: allReviews.length,
              averageRating: avgRating ? parseFloat(avgRating.toFixed(1)) : null
            };
          });
          
          console.log('Sending response with', enhancedLocations.length, 'locations from Prisma');
          return res.status(200).json(enhancedLocations);
        }
      } catch (prismaError) {
        console.error('Prisma error:', prismaError);
        console.log('Falling back to Supabase API...');
      }
      
      // If we're here, Prisma failed - try Supabase directly
      console.log('Attempting to retrieve locations directly from Supabase...');
      
      const { data: locations, error } = await supabase
        .from('location')
        .select(`
          *,
          tacos:taco (
            *,
            reviews:review (*)
          )
        `);
      
      if (error) throw error;
      
      console.log('Fetched locations via Supabase:', locations?.length || 0);
      
      // Add taco count and average rating to each location
      const enhancedLocations = locations.map(location => {
        const allReviews = (location.tacos || []).flatMap(taco => taco.reviews || []);
        const avgRating = allReviews.length > 0
          ? allReviews.reduce((sum, review) => sum + review.rating, 0) / allReviews.length
          : null;
        
        return {
          ...location,
          tacoCount: (location.tacos || []).length,
          reviewCount: allReviews.length,
          averageRating: avgRating ? parseFloat(avgRating.toFixed(1)) : null
        };
      });
      
      console.log('Sending response with', enhancedLocations.length, 'locations from Supabase');
      res.status(200).json(enhancedLocations);
      
    } catch (error) {
      console.error('Error fetching locations:', error);
      console.error('Error name:', error.name);
      console.error('Error code:', error.code);
      console.error('Error stack:', error.stack);
      
      // Return an empty array instead of an error to simplify client handling
      res.status(200).json([]);
    } finally {
      try {
        await prisma.$disconnect();
        console.log('Disconnected from database');
      } catch (e) {
        console.error('Error disconnecting from database:', e);
      }
    }
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
