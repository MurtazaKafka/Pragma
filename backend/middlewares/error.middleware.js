// Catch 404 and forward to error handler
const catch404 = (req, res, next) => {
    next(createError(404));
};

// Error handler
const errorHandler = (err, req, res, next) => {
    // Set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // Send JSON response
    res.status(err.status || 500).json({
        status: err.status || 500,
        message: res.locals.message,
        error: res.locals.error,
    });
};

// Export the middleware functions
module.exports = {
    catch404,
    errorHandler,
};