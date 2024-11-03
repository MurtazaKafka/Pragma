var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var dotenv = require('dotenv');
var cors = require('cors');
var createError = require('http-errors');
var router = require('./routes/routes.js')
var { catch404, errorHandler } = require('./middlewares/error.middleware');
dotenv.config();

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');
var dbConnect = require('./db/dbConnect');

var app = express();
const port = process.env.PORT || 3001

// Connect to the database
dbConnect();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use(cors({
  origin: process.env.CORS_ORIGIN,
  credentials: true
}))

app.use('/', router);
app.use('/users', usersRouter);
// Catch 404 and forward to error handler
app.use(catch404);

// Error handler
app.use(errorHandler);

// catch 404 and forward to error handler
// app.use(function(req, res, next) {
//   next(createError(404));
// });
//
// // error handler
// app.use(function(err, req, res, next) {
//   // set locals, only providing error in development
//   res.locals.message = err.message;
//   res.locals.error = req.app.get('env') === 'development' ? err : {};
//
//   // render the error page
//   res.status(err.status || 500);
//   res.render('error');
// });

app.listen(port, () => {
  console.log(`Server is running on port ${port}`)
})

module.exports = app;
