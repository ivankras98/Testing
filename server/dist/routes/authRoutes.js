"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const authController_1 = require("../controllers/authController");
const router = express_1.default.Router();
router.post('/api/auth/signup', authController_1.localSignup);
router.post('/api/auth/login', authController_1.localLogin);
router.post('/api/auth/logout', authController_1.logout);
exports.default = router;
