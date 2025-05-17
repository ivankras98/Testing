"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const client_1 = require("@prisma/client");
const router = express_1.default.Router();
const prisma = new client_1.PrismaClient();
router.post('/api/auth/login', (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const { email, password } = req.body;
        if (!email || !password) {
            console.error('Missing email or password');
            return res.status(400).json({ message: 'Email and password are required' });
        }
        const user = yield prisma.user.findUnique({
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
    }
    catch (error) { // Явно указываем тип error
        console.error(`Login error: ${error.message}`);
        return res.status(500).json({ message: 'Internal server error' });
    }
}));
exports.default = router;
