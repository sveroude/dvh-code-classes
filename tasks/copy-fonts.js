const gulp = require('gulp');
const path = require('path');

const paths = module.exports = {
	static: 'static/',
	src: 'src/fonts/'
};

/**
 * Copies new(er) files in assets folder to static folder
 * @return {Stream}
 */
gulp.src(paths.src + '**/*')
    .pipe(gulp.dest(path.join(paths.static, 'fonts')));
