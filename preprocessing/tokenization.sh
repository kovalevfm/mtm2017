cat ../OpenSubtitles2016/OpenSubtitles2016.en-pt.en \
   | parallel -k --pipe -j4 -L 100000 th tools/tokenize.lua -mode aggressive \
   | python ../mtm2017/preprocessing/lower.py \
   | pv -l > ../OpenSubtitles2016/OpenSubtitles2016.en-pt.en.tok

cat ../OpenSubtitles2016/OpenSubtitles2016.en-pt.pt \
   | parallel -k --pipe -j4 -L 100000 th tools/tokenize.lua -mode aggressive \
   | python ../mtm2017/preprocessing/lower.py \
   | pv -l > ../OpenSubtitles2016/OpenSubtitles2016.en-pt.pt.tok

cat ../news/News-Commentary11.en-pt.en \
   | parallel -k --pipe -j4 -L 100000 th tools/tokenize.lua -mode aggressive \
   | python ../mtm2017/preprocessing/lower.py \
   | pv -l > .../news/News-Commentary11.en-pt.en.tok

cat ../news/News-Commentary11.en-pt.pt \
   | parallel -k --pipe -j4 -L 100000 th tools/tokenize.lua -mode aggressive \
   | python ../mtm2017/preprocessing/lower.py \
   | pv -l > .../news/News-Commentary11.en-pt.pt.tok