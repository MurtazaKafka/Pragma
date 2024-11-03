const bcrypt = require('bcrypt'); // Import bcrypt
const jwt = require('jsonwebtoken'); // Import jsonwebtoken
const User = require('../../models/User'); // Import User schema

async function handleLogin(req, res, next) {
    try {
        // Find the user with the username provided
        const user = await User.findOne({ email: req.body.email });
        // Check if the user exists
        if (!user) {
            return res.status(401).json({ message: 'User not found' });
        }
        // Compare the password provided with the user's password
        const match = await bcrypt.compare(req.body.password, user.password);
        if (!match) {
            return res.status(401).json({ message: 'Invalid password' });
        }

        // Create a JWT token
        const token = jwt.sign(
            { userId: user._id },
            process.env.JWT_SECRET,
            { expiresIn: '24h' }
        )

        res.cookie('token', token, {
            httpOnly: true,
            maxAge: 24 * 60 * 60 * 1000, // 24 hours
        });

        res.status(200).send({
            message: 'Login successful',
            user: {
                name: user.name,
                email: user.email,
            },
            token,
        });

    } catch (error) {
        return res.status(500).json({
            message: 'Internal Server Error',
            error: error.message, // Optionally include error details
        });
    }
}

async function handleLogout(req, res, next) {
    try {
        res.clearCookie('token');
        res.status(200).send({ message: 'Logout successful' });
    } catch (error) {
        next(error);
    }
}

module.exports = { handleLogin, handleLogout };