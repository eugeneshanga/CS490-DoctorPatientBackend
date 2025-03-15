## CI Check: Verifying requirements.txt is Up-to-Date

We've added a GitHub CI workflow that automatically checks if requirements.txt is in sync with the project's installed dependencies. Whenever a pull request is made or code is pushed, this check ensures that any new Python packages installed via pip are properly recorded in requirements.txt.

### Why its here
As we begin to develop this project, we will be installing a variety of dependencies and libraries to aid us. As a result, the dependencies needed to run the project could change at any moment. Keeping requirments.txt up to date makes it easy for all of us to stay up to date with the needed dependencies.

With a single command: `pip install -r requirements.txt`

You can install everything needed to run the project

### How It Works:
The CI runs pip freeze > requirements_new.txt to generate a fresh list of installed dependencies.
It compares this file with the existing requirements.txt.
If there are differences, the check fails, meaning someone forgot to update requirements.txt after installing new packages.
🚀 What You Need to Do:
After installing new packages, always update requirements.txt using:
sh
Copy
Edit
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements.txt"
If the CI check fails on your PR, run the command above, commit the changes, and push again.
This helps keep our dependencies consistent across the team and prevents missing packages in deployments. ✅