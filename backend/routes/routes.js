const express = require('express');
const { handleRegister } = require('../controllers/auth/register');
const { handleLogin, handleLogout } = require('../controllers/auth/login');


const router = express.Router();

const asyncHandler = fn => (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next)
}

router.post('/register', asyncHandler(handleRegister))
router.post('/login', asyncHandler(handleLogin))
router.post('/logout', asyncHandler(handleLogout))

module.exports = router;