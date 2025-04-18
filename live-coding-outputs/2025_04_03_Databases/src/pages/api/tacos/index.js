import prisma from '../../../lib/prisma';
import { supabase } from '../../../lib/supabase';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    console.log('GET /api/tacos request received');
    
    try {
      // First try using Prisma
      console.log('Attempting to retrieve tacos via Prisma...');
      
      // Debug database connection
      console.log('Database URL:', process.env.DATABASE_URL ? 
        `Set (starts with ${process.env.DATABASE_URL.split('://')[0]})` : 
        'Not set! This will cause connection errors.');
      
      // First try with Prisma
      try {
        const tacos = await prisma.taco.findMany({
          include: {
            location: true,
            reviews: {
              include: {
                user: true
              }
            }
          }
        });
        
        console.log('Fetched tacos via Prisma:', tacos?.length || 0);
        
        if (tacos && tacos.length > 0) {
          // Calculate average rating for each taco
          const tacosWithRatings = tacos.map(taco => {
            const ratings = taco.reviews.map(review => review.rating);
            const avgRating = ratings.length > 0 
              ? ratings.reduce((sum, rating) => sum + rating, 0) / ratings.length 
              : null;
            
            return {
              ...taco,
              reviewCount: taco.reviews.length,
              averageRating: avgRating ? parseFloat(avgRating.toFixed(1)) : null
            };
          });
          
          console.log('Sending response with', tacosWithRatings.length, 'tacos from Prisma');
          return res.status(200).json(tacosWithRatings);
        }
      } catch (prismaError) {
        console.error('Prisma error:', prismaError);
        console.log('Falling back to Supabase API...');
      }
      
      // If we're here, Prisma failed - try Supabase directly
      console.log('Attempting to retrieve tacos directly from Supabase...');
      
      const { data: tacos, error } = await supabase
        .from('taco')
        .select(`
          *,
          location:location_id (*),
          reviews:review (
            *,
            user:user_id (*)
          )
        `);
      
      if (error) throw error;
      
      console.log('Fetched tacos via Supabase:', tacos?.length || 0);
      
      // Calculate average rating for each taco
      const tacosWithRatings = tacos.map(taco => {
        const ratings = (taco.reviews || []).map(review => review.rating);
        const avgRating = ratings.length > 0 
          ? ratings.reduce((sum, rating) => sum + rating, 0) / ratings.length 
          : null;
        
        return {
          ...taco,
          reviewCount: (taco.reviews || []).length,
          averageRating: avgRating ? parseFloat(avgRating.toFixed(1)) : null
        };
      });
      
      console.log('Sending response with', tacosWithRatings.length, 'tacos from Supabase');
      res.status(200).json(tacosWithRatings);
      
    } catch (error) {
      console.error('Error fetching tacos:', error);
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
