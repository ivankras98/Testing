import express from 'express';
import authRoutes from './routes/auth';

const app = express();
app.use(express.json());
app.use('/api', authRoutes);

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.info(`Server running on port ${PORT}`);
});