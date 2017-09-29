#!/bin/sh
cd static;
cd css;
echo Compressing CSS Files...
saved=0
for f in `find -name "*.css" -not -name "*.min.css"`;
do
        target=${f%.*}.min.css
        echo "\t- "$f to $target
        echo "" > $target
sudo  chmod  777 $target
        FILESIZE=$(stat -c%s "$f")
         pwd
        sudo java -jar yuicompressor-2.4.8.jar  --type css --nomunge -o $target $f
        FILESIZEC=$(stat -c%s "$target")
        diff=$(($FILESIZE - $FILESIZEC))
        saved=$(($saved + $diff))
        echo "\t  $diff bytes saved"
done
echo "Done ! Total saved: $saved bytes"
