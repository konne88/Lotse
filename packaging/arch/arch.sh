#!/bin/sh
cd ../../;
python setup.py sdist
cp dist/lotse*.tar.gz packaging/arch/
cd -
MD5=`md5sum lotse*.tar.gz | egrep -o "^[a-f0-9]*"`
sed -e "s/<<MD5SUM_FITS_HERE>>/$MD5/g" PKGBUILD.in > PKGBUILD
makepkg -cf
