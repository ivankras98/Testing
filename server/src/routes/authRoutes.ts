import express from 'express';
import { localSignup, localLogin, logout } from '../controllers/authController';

const router = express.Router();

router.post('/api/auth/signup', localSignup);
router.post('/api/auth/login', localLogin);
router.post('/api/auth/logout', logout);

export default router;