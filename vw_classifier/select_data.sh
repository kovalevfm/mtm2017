cat <(cat ../OpenSubtitles2016/OpenSubtitles2016.en-pt.en.tok | shuf | head -50000 \
      | sed 's/:/COLON/g' | sed 's/|/PIPE/g' | awk '{print "-1 |", $0}') \
    <(cat ../news/News-Commentary11.en-pt.en.tok \
       | sed 's/:/COLON/g' | sed 's/|/PIPE/g' | awk '{print "1 |", $0}') \
    | shuf > en.vwcorpus.txt

cat <(cat ../OpenSubtitles2016/OpenSubtitles2016.en-pt.pt.tok | shuf | head -50000 \
      | sed 's/:/COLON/g' | sed 's/|/PIPE/g' | awk '{print "-1 |", $0}') \
    <(cat ../news/News-Commentary11.en-pt.pt.tok \
       | sed 's/:/COLON/g' | sed 's/|/PIPE/g' | awk '{print "1 |", $0}') \
    | shuf > pt.vwcorpus.txt


../scripts/vw-8.20170116 en.vwcorpus.txt --ngram 3 --skips 1 --loss_function logistic \
   -b 28 --binary --l1 1e-08 --l2 1e-07 --progress 10000 -c --spelling st \
   --affix +2,+2 --passes 5 -f en_vwmodel.vw --save_per_pass

../scripts/vw-8.20170116 pt.vwcorpus.txt --ngram 3 --skips 1 --loss_function logistic \
   -b 28 --binary --l1 1e-08 --l2 1e-07 --progress 10000 -c --spelling st \
   --affix +2,+2 --passes 5 -f pt_vwmodel.vw --save_per_pass

cat ../OpenSubtitles2016/OpenSubtitles2016.en-pt.en.tok \
    |  python ../mtm2017/vw_classifier/vw_apply.py -m en_vwmodel.vw | pv -l > en.vw.scores

cat ../OpenSubtitles2016/OpenSubtitles2016.en-pt.pt.tok \
    |  python ../mtm2017/vw_classifier/vw_apply.py -m pt_vwmodel.vw | pv -l > pt.vw.scores


paste en.vw.scores pt.vw.scores | awk awk '{print $1+$2}' > vw.scores_sum.txt


paste vw.scores_sum.txt \
    ../OpenSubtitles2016/OpenSubtitles2016.en-pt.en.tok \
    ../OpenSubtitles2016/OpenSubtitles2016.en-pt.pt.tok \
  | sort -gr -k1,1 -S8G | head -2010000 | cut -f2,3 | shuf > vw_corpus.tsv

