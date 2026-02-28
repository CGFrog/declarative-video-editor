
<h3>Git Strategies</h3>
<h5>Branching</h5>
Branch names should be kebab case, for example, "syntax-highlighting." When creating a new branch, always branch off `prod`.

To branch locally, follow these steps:

```
git switch prod
```

```
git checkout -b <new-branch-name>
```

You will now be switched to your new branch. 

> [!NOTE]
> Make sure to periodically run `git fetch` (fetches remote changes) and `git pull` (applies fetched changes to local branch) to bring new changes from prod to your local branch

<h5> Committing and Pushing </h5>
To bring local changes to the remote repository:

```
git add <file to add>
OR
git add *<suffix of file you want to add>
EXAMPLE:
git add *.py
```
  
Then you will type:

```
git commit -m "<commit message>"
```

To send your changes to the remote repository type:

```
git push
```

<h5> Pull Requests </h5>
When your code is ready to be merged, merge into `dev` and have 1 reviewer conduct an initial code review. Once this is done, you may merge into `prod`.

> [!WARNING]
> Always ensure that changes that are merged into prod have previously been already merged into dev.
