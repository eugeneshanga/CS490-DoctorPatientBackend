## What is Flake8 and Why Are We Using It?

Flake8 is a Python linter that helps enforce coding standards, catch potential bugs, and improve code readability. It checks for stylistic issues (PEP 8), logical errors, and complexity problems, making our codebase more consistent and maintainable. 

Since many of us may not have used a linter before, think of Flake8 as an extra pair of eyes that ensures our code follows best practices. Moving forward, all new code should pass the Flake8 checks before being merged. Don’t worry if you run into errors—Flake8 provides clear feedback on what to fix, making it easy to follow


`ChatGPT wrote the above for me I do not talk that way but its a nice explanation lol`

If you want to run the linter locally before pushing changes to github

Install the linter
`pip install flake8`

Run it
`flake8 *.py`