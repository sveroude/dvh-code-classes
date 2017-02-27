const gulp = require('gulp');
const concat = require('gulp-concat');
const plumber = require('gulp-plumber');
const sourcemaps = require('gulp-sourcemaps');
const uglify = require('gulp-uglify');

const paths = module.exports = {
	static: 'static/',
	src: 'src/scripts/**/*.js',
};


gulp.src([paths.src])
  .pipe(plumber())
	.pipe(sourcemaps.init())
	.pipe(concat('index.js'))
	.pipe(uglify())
	.pipe(sourcemaps.write('./'))
    .pipe(gulp.dest(paths.static));
