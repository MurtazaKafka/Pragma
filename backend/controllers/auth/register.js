const bcrypt = require('bcrypt'); // Import bcrypt
const User = require('../../models/User'); // Import User schema

async function handleRegister(
    req,
    res,
    next
) {
    try {
        // Hash the password
        const hash = await bcrypt.hash(req.body.password, 10);

        // Create a new user with hashed password
        const newUser = await User.create({
            email: req.body.email,
            name: req.body.name,
            password: hash,
        });

        // Send response with the created user (omit sensitive info like password)
        res.status(201).json({
            message: 'User registered successfully',
            user: {
                email: newUser.email,
                name: newUser.name,
                createdAt: newUser.createdAt,
                updatedAt: newUser.updatedAt,
            },
        });
    } catch (error) {
        // Pass any errors to the error handler middleware
        next(error);
    }
}

module.exports = { handleRegister };