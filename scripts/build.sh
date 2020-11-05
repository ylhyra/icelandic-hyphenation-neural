#!/bin/bash
set -e

rm -f build/index.html
# rm -f build/css.css

npm run build

npm run styles

cp website/frontend/index.html build/index.html


sed -i -E "s/http:\/\/localhost:3100\/website.js/js\/website.js/" build/index.html
sed -i -E "s/http:\/\/localhost:5000\///" build/index.html

# cp website/frontend/css.css build/css.css

# JS_HASH=($(sha1sum build/js/website.js))
# CSS_HASH=($(sha1sum build/css.css))
JS_HASH=($(shasum build/js/website.js))
CSS_HASH=($(shasum build/css.css))
sed -i -E "s/website\.js\?build=[[:alnum:]]*/website.js?build=${JS_HASH:0:8}/" build/index.html
sed -i -E "s/css\.css\?build=[[:alnum:]]*/css.css?build=${CSS_HASH:0:8}/" build/index.html
rm -f build/index.html-E
