git init
git remote add origin https://github.com/ZangraN/photoset-ai.git
git fetch origin
git branch -M main
git reset --mixed origin/main
git add .
git commit -m "Оптимизация: вынесены CSS и JS, исправлена семантика HTML"
git push -u origin main
