To implement a small Continuous Integration (CI) server in Python that meets the core features and grading criteria outlined, we'll need to follow a structured approach. Here's a high-level guide on how we can achieve this, focusing on the mandatory features for a "Pass" and the optional features for a "Pass with distinction".

### Mandatory Features for a Pass

#### P0a & P0b: Repository Structure and Valid State

- [ ] **Structure the repository** with clear folders for source code, tests, and documentation. Include a comprehensive `README.md` that explains the project setup, how to run tests, and a statement of contributions.
- [ ] Ensure your repository is in a **valid state** by making it easy to clone, build, and test. Document standard commands like `pip install` and `python3 run` in the `README.md`.

#### P1: Formatting check

- [ ] Implement a webhook in a Python CI server that triggers compilation of the project upon receiving a push event from the repository. I am thinking Flask or FastAPI.
- [ ] Use Python's subprocess module to format check the python commands.
- [ ] Document the setup and testing of this feature in the `README.md`.

#### P2: Testing

- [ ] Extend the webhook functionality to execute automated tests (pytest).
- [ ] Document how this is implemented and tested.

#### P3: Notification

- [ ] Implement a notification mechanism. For commit status updates, use the GitHub API to post statuses. For email notifications, use Python's `smtplib`.
- [ ] Document the notification mechanism setup and testing.

#### P4 & P5: Software Engineering (SE) Practices

- [ ] Ensure commits are atomic, with clear messages. Document the commit message convention.
- [ ] Document all public classes and methods. Generate and include API documentation (e.g., using Sphinx for Python).

#### P6: SEMAT

- [ ] Assess and document the team's state according to the Essence standard. Include this in your `README.md` or a separate document.

### Optional Features for a Pass with Distinction

#### P7: Build History

- [ ] Implement functionality to log build history and make it persistent, even after server reboots. Consider using a lightweight database like SQLite.
- [ ] Provide a unique URL for each build and a list URL in the `README.md`.

#### P8: Creativity and Proactivity

- [ ] Document any unique, valuable features or approaches your team has implemented in the "Statement of contributions".

#### P9: Issue Linking

- [ ] Ensure most commits are linked to issues that describe the feature or bug fix. This requires disciplined use of your repository's issue tracker.

### Development Tips

- [ ] **Dogfooding**: Use your CI server to build and test its own code.
- [ ] **Multiple CI Services**: Consider using GitHub Actions alongside your CI server for additional reliability during development.
- [ ] **Server Setup**: If using ngrok for tunneling, document the setup process for future reference and ease of grading.

### Python Specifics

- [ ] Use Flask, Django, or FastAPI for the web server component to handle webhooks.
- [ ] Utilize existing libraries for GitHub API interaction, like PyGithub, for setting commit statuses or posting comments.
- [ ] For email notifications, explore the `email` and `smtplib` modules in Python's standard library.

> Author: Olle Jernström
