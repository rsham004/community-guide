import prisma from '../../../lib/prisma';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const users = await prisma.user.findMany({
        include: {
          reviews: true,
          achievements: {
            include: {
              achievement: true
            }
          },
          followers: {
            include: {
              follower: true
            }
          }
        }
      });
      
      // Add computed fields
      const enhancedUsers = users.map(user => {
        return {
          ...user,
          reviewCount: user.reviews.length,
          achievementCount: user.achievements.length,
          followerCount: user.followers.length
        };
      });
      
      res.status(200).json(enhancedUsers);
    } catch (error) {
      console.error('Error fetching users:', error);
      res.status(500).json({ error: 'Failed to fetch users' });
    }
  } else {
    res.setHeader('Allow', ['GET']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
