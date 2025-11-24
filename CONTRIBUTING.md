# Contributing to Project Insight 🚀

Welcome to the team! If you are new to GitHub or working in a team, this guide is for you.

## ⚠️ The Golden Rules

-   NEVER push to `main` directly. (The system won't let you anyway).
-   NEVER upload large files. (No `.mp4` videos, no `.pt` AI models, no `venv` folders).
-   ALWAYS pull before you start working.

## 🛠️ How to Contribute (The Workflow)

### Step 1: Get the Latest Code

Before writing a single line of code, make sure you have the latest changes from your teammates.

```bash
git checkout main
git pull origin main
```

### Step 2: Create a Branch

Give your branch a descriptive name.

✅ Good: `vision/fix-face-tracking`
✅ Good: `nlp/add-summarization`
❌ Bad: `ahmed-work`, `test`, `changes`

```bash
git checkout -b vision/your-feature-name
```

### Step 3: Do Your Magic

Write your code. Run your tests. Make sure `python main.py` doesn't crash.

### Step 4: Commit and Push

```bash
git add .
git commit -m "Added gaze estimation logic using MediaPipe"
git push origin vision/your-feature-name
```

### Step 5: Open a Pull Request (PR)

1.  Go to the GitHub page for this repo.
2.  You will see a yellow box saying "Compare & pull request". Click it.
3.  **Title:** Describe what you did briefly.
4.  **Reviewers:** Select your Squad Lead (Mohamed Bakr or Demiana) on the right sidebar.
5.  Click `Create Pull Request`.

Once your lead reviews and approves your code, it will be merged into the main system!

## 🆘 Troubleshooting

-   **"Permission Denied" on push?** You might be trying to push to `main`. Check your branch: `git branch`.
-   **Merge Conflicts?** This happens when two people edit the same file. Ask your Squad Lead for help resolving them.
