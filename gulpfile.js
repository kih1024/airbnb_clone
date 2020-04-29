const gulp = require("gulp");

// scss 파일을 css로 인식하기 위한 과정
const css = () => {
  const postCSS = require("gulp-postcss");
  const sass = require("gulp-sass");
  const minify = require("gulp-csso");
  sass.compiler = require("node-sass");
  return gulp
    .src("assets/scss/styles.scss") // 경로 설정
    .pipe(sass().on("error", sass.logError)) // scss 파일의 내용을 css로 바꾸는 과정
    .pipe(postCSS([require("tailwindcss"), require("autoprefixer")])) // tailwind의 룰을 인식하기 위한 과정, tailwind의 모든 룰을 주입한다.
    .pipe(minify()) // 코드를 짧게 만든다.
    .pipe(gulp.dest("static/css")); // 위 3라인의 결과를 해당 경로에 저장하기 위한 과정, 결국 브라우저에 보내는건 styles.css
    // aseetes는 프로그래머를 위한것, static은 브라우저를 위한것.
};

exports.default = css;
