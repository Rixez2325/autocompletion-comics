source devops.env

git remote rm origin

git remote add GitHub $GitHub_URL
git remote add AWS $AWS_URL

git remote add all $GitHub_URL
git remote set-url --add --push all $GitHub_URL
git remote set-url --add --push all $AWS_URL