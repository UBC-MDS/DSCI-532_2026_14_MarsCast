# Contributing

We welcome input, feedback, bug reports, and contributions to the **Mars Weather Dashboard** project.  
This project aims to provide an interactive Shiny dashboard to better understand weather conditions on Mars—supporting rover operations, mission planning, and the design of future exploration systems.

Your contributions can help us:

- Improve performance, clarity, and usability
- Add new analytical or visualization features
- Refine existing plots and interactions
- Expand documentation and scientific context

All contributions, suggestions, and feedback are accepted under the [project license](LICENSE).  
By contributing, you confirm that you have the right to submit your work under this license. Contributions are not treated as confidential.

---

## Ways to Contribute

You can contribute in many ways, including:

- [Report bugs](#report-bugs)
- [Fix bugs](#fix-bugs)
- [Implement features](#implement-features)
- [Improve documentation](#improve-documentation)
- [Submit feedback or ideas](#submit-feedback)

---

## Report Bugs

If you encounter a bug, please open an issue on GitHub:

👉 **Issues:** <https://github.com/UBC-MDS/DSCI-532_2026_14_MarsCast/issues>

When reporting a bug, please include:

- A clear description of the issue
- Steps to reproduce it
- Expected vs. actual behavior
- Screenshots or error messages (if applicable)

The more detail you provide, the easier it is to diagnose and fix the problem.

---

## Fix Bugs

Browse the issue tracker for items labeled `bug` or `help wanted`.

If you decide to work on an issue:

1. Comment on the issue to let others know
2. Assign yourself if possible
3. Reference the issue number in your pull request

---

## Implement Features

Feature requests and enhancements are tracked in GitHub issues under labels such as `enhancement` or `feature`.

If you plan to implement a new feature:

- Check existing issues first to avoid duplication
- Open a new issue to discuss the idea if needed
- Coordinate with maintainers before large changes

---

## Improve Documentation

Documentation is just as important as code. You can help by:

- Improving the README or `description.md`
- Clarifying assumptions or limitations
- Adding comments or docstrings in the code
- Improving explanations in notebooks

If you plan significant documentation changes, feel free to open an issue to discuss them first.

---

## Submit Feedback

General feedback, ideas, or questions are welcome.

👉 **Submit feedback here:** <https://github.com/UBC-MDS/DSCI-532_2026_14_MarsCast/issues>

Please use the appropriate issue template when available.  
This is a community-driven project, so thoughtful and constructive feedback is greatly appreciated.

---

## Getting Started

### 1. Fork the Repository

Fork the repository on GitHub, then clone your fork locally:

```bash
git clone git@github.com:UBC-MDS/DSCI-532_2026_14_MarsCast.git
cd mars-weather-dashboard
```

### 2. Set Up the Environment

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate mars_weather_dash_env
```

### 3. Create a Branch

Create a new branch from main. Use a clear prefix such as fix/ or feat/:

```bash
git checkout main
git checkout -b feat/add-seasonal-view
```

### 4. Make Your Changes

- Keep changes focused and well-scoped
- Follow existing code and formatting conventions
- Prefer clarity and scientific interpretability over cleverness

### 5. Test Your Changes

Before submitting, ensure that:

- The dashboard runs without errors (python src/app.py)
- Notebooks execute cleanly if modified
- New dependencies are reflected in environment.yml

### 6. Commit and Push

Use clear, descriptive commit messages (semantic commits are encouraged):

```bash
git add .
git commit -m "feat: add seasonal temperature comparison view"
git push -u origin feat/add-seasonal-view
```

### 7. Open a Pull Request

When opening a pull request, please include:

- A clear summary of what changed
- The motivation behind the change
- Any limitations, assumptions, or open questions

Your pull request will be reviewed, and you may be asked to make adjustments.

## Code of Conduct

This project follows a Code of Conduct to ensure a welcoming and inclusive environment.
Please review and adhere to the guidelines outlined in CODE_OF_CONDUCT.md

We expect all contributors to:

- Be respectful and professional
- Welcome newcomers
- Accept constructive feedback graciously

## Questions and Discussions

If you’re unsure about an idea or want feedback before implementing it:

- Open an issue labeled question or discussion
- Share your proposal and context
- Engage with maintainers and other contributors

## Retrospective Reflexion on M3

Overall, the team has worked smoothly throughout the project. Since M1, we have maintained strong collaboration. Our typical workflow looks like this:

- Understanding the objectives, scope, and tasks of each milestone as a team, including a brief review of the previous milestone's outcomes
- Brainstorming ideas and solutions
- Task distribution and dependency review
- Individual work on assigned tasks
- Final review to ensure completeness and timely delivery
- Work submission

Thanks to this workflow we have maintained good collaboration and feel proud of what we've accomplished.

### What worked well in this milestone

- Rebeca and Sasha paid close attention to milestone requirements we might have overlooked
- All team members actively reviewed each other's pull requests and provided constructive feedback
- Everyone contributed to coding tasks
- Organization and planning through github issues has been working great. We always split the tasks on the first day of the milestone, giving us a clear vision of what needs to be done, highlighting dependencies, and minimizing communication issues.
- Branching strategy worked smoothly and effectively prevented merge conflicts

### What didn't worked and will be improved

Milestone 3 was particularly challenging due to external circumstances. It coincided with quiz week, which added extra pressure on the whole team. As a result, individual tasks were pushed closer to the deadline than we would have liked, and the final submission came in with very little time to spare.

This was understandable given the circumstances and was not due to bad teamwork. However, for future milestones, we will plan more carefully to ensure tasks are completed earlier, leaving enough room before the deadline.

## Acknowledgments

Thank you for your interest in contributing to the Mars Weather Dashboard.
Every bug report, suggestion, or enhancement, no matter how small helps improve the quality and usefulness of this project.

By contributing, you help transform planetary data into actionable insight for space exploration.
