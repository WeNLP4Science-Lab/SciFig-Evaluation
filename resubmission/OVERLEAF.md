# Overleaf Source

The paper source in `6a143a4c382eafd7ee52e0c7/` was cloned from Overleaf:

```
https://git@git.overleaf.com/6a143a4c382eafd7ee52e0c7
```

Inner `.git` was removed to embed the paper as regular tracked files in the ARI repo. To re-establish Overleaf sync later:

```bash
cd resubmission/6a143a4c382eafd7ee52e0c7
git init
git remote add origin https://git@git.overleaf.com/6a143a4c382eafd7ee52e0c7
git fetch origin
git reset --hard origin/master   # or main
```
