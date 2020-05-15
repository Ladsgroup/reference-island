HOME="/data/project/wd-ref-island"

git -C "$HOME/reference-island/" checkout master
git -C "$HOME/reference-island/" pull
cp "$HOME/reference-island/wikidata_game/api.php" "$HOME/public_html/api.php"
echo 'api.php updated successfuly'