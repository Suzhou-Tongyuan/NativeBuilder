export PACKAGE=safe_config
cd src
fable --lang Python App.fsproj --outDir $PACKAGE --fableLib $PACKAGE/fable_modules/fable_library
rm -rf ../$PACKAGE
mv -T $PACKAGE ../$PACKAGE
rm -rf $PACKAGE
cd ..
python genheader.py $PACKAGE
rm safe_config/fable_modules/.gitignore
rm safe_config/fable_modules/project_cracked.json
