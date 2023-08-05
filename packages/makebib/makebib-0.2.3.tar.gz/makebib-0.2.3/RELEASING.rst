python setup.py sdist
git commit ChangeLog
git tag $VERSION
git push origin
python setup.py sdist
twine upload dist/*$VERSION.tar.gz
