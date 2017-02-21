const autoprefixer = require('gulp-autoprefixer');
const cleanCss = require('gulp-clean-css');
const gulp = require('gulp');
const plumber = require('gulp-plumber');
const sourcemaps = require('gulp-sourcemaps');
const less = require('gulp-less');

const paths = module.exports = {
	static: 'static/',
	src: 'src/styles/'
};

const onStreamError = module.exports = function(error) {
    console.error(error.message);
    this.emit('end');
};

/**
 * Builds CSS from LESS files and writes to static folder
 * Note that all LESS files are included manually in `index.less`
 *
 * - Plumber       Makes sure LESS errors don't result in the watcher crashing
 * - Sourcemaps    Writes external source map file in same folder as CSS
 * - Less          Compiles LESS into CSS; on error, outputs error message and
 *                 ends stream without watcher crashing
 * - Autoprefixer  Prefixes some CSS properties for older/incompatible browsers
 * - cleanCss      Minifies CSS to reduce file size
 *
 * @return {Stream}
 */
gulp.src(paths.src + 'index.less')
	.pipe(plumber())
	.pipe(sourcemaps.init())
	.pipe(less())
	.on('error', onStreamError)
	.pipe(autoprefixer({ browsers: ['> 1%', 'last 2 versions'] }))
	.pipe(cleanCss())
	.pipe(sourcemaps.write('./'))
	.pipe(gulp.dest(paths.static));
