git filter-branch --commit-filter 'if [ "$GIT_AUTHOR_NAME" = "Josue Kouka" ]; then export GIT_AUTHOR_EMAIL=josuebrunel@gmail.com; fi; git commit-tree "$@"'
