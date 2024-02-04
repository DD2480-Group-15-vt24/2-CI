# 2-CI

## File structure

```
2-CI/
│
├── src/                        # Source files
│   ├── __init__.py             # Makes `src` a Python package
│   ├── ci.py                   # Main CI logic
│   └── ...                     # Source code
│
├── tests/                      # Automated tests
│   ├── __init__.py             # Makes tests a Python package
│   └── ...                     # Unittests
│
├── docs/                       # Documentation
│   └── README.md               # Technical documentatoion
│
├── main.py                 	# Main entry point of the program
├── requirements.txt            # Project dependencies
└── README.md                   # This file. General project documentation
```

## Quickstart

### 1. Create a virtual envrionment called `venv`

`python3 -m venv venv`

### 2. Activate the venv

`source venv/bin/activate`

### 3. Install the dependencies

`python3 -m pip install -r requirements.txt`

### 4. Run the program

`python3 main.py`

## Code style

Ruff is used for linting the project. Lint the code by using `ruff .`

Black is used for formatting the procjet. Format the code by using `black .`

## Running the test suite

Run `pystest` from the root

## How to contribute

1. **Create a new branch**: New branches should be created from an issue on the project board. to ensure that each PR is properly atomic and linked to an issue. Checkout the branch locally after fetching with `git fetch origin`
2. **Write Code**: Make your changes or additions to the codebase. Ensure you follow the coding standards and styles of the project.
3. **Use Linter and Formatter**: Before committing your changes, run the linter and formatter to ensure your code adheres to the project's coding standards.

- `black .`
- `ruff .`

4. **Write Tests**: If you are adding new features or fixing bugs, write tests to cover your changes. Ensure all tests pass locally before pushing your changes.
5. **Commit**: Commit your changes and push to the origin branch
6. **Open a Pull Request (PR)**: Go to the original repository on GitHub and open a pull request from your branch to the main branch. Provide a clear description of the changes and link **the** related issues. This is an requirement.

## Contribution guidlines

Open a Pull Request (PR): Go to the original repository on GitHub and open a pull request from your branch to the main branch. Provide a clear description of the changes and link any related issues.

- Stable Branch Protection Rules: The main branch is protected. Direct pushes are not allowed, and changes must go through the PR process.
- Checks Must Pass: Your PR must pass all automated checks, including tests, linting, and formatting.
- Conversation Resolution: Ensure all PR comments and conversations are resolved before merging.
- Review Requirements: At least one approval from the project maintainers is required before a PR can be merged.
- Atomic PRs: Each PR should reference 1 issue. This is done with the "Closes #65" format.
- Squash Merge: We use squash merging to keep the commit history clean. Ensure your PR title starts with a label "Feat:", "Fix:", "Doc: ", "Refactor: " as this will be the commit message.

## Way of working

TODO...

## Contributors

- Olle Jenrström
- Love Lindgren
- Selma Özdere
- Siham Shahoud

# Statement of contribution

The work was devided as follows:

Olle Jenrström:

Love Lindgren:

Siham Shahoud:

Selma Özdere:
