import express from 'express';
import { PrismaClient } from '@prisma/client';

const router = express.Router();
const prisma = new PrismaClient();

router.post('/api/auth/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      console.error('Missing email or password');
      return res.status(400).json({ message: 'Email and password are required' });
    }

    const user = await prisma.user.findUnique({
      where: { email },
    });

    if (!user) {
      console.error(`User not found: ${email}`);
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    // Упрощенная проверка пароля (замените на bcrypt в продакшене)
    if (password !== user.password) {
      console.error(`Invalid password for user: ${email}`);
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    console.info(`User logged in: ${email}`);
    return res.status(200).json({ message: 'Login successful', redirect: '/dashboard' });
  } catch (error: any) { // Явно указываем тип error
    console.error(`Login error: ${error.message}`);
    return res.status(500).json({ message: 'Internal server error' });
  }
});

export default router;