# Development Setup Instruction

A complete guide to setup your development environment :D

---

### Requirements

`python 3.7` or higher

Make sure you also already installed `pip` and `venv` for your Python

---

### Create Virtual Environment

Start by creating your isolated Python environment with `venv`:

```bash
$ python3 -m venv .venv
```
In this case, `.venv` is the name of the directory containing your Python executable and other files. You can name it anything you want, but `.venv` is the most common name.

Next, activate your virutal environment:

```bash
$ source .venv/bin/activate
```
You can verify your virutal environment is properly activated by running `python -V` which will either have your regular path (incorrectly activated) or your virutal environment path (correctly activated).

---

### Install Packages

You will notice there are 2 files named `requirements-dev.txt` and `requirements.txt`. These files contain the name of the `pip` packages.

`requirements-dev.txt` contains the packages needed to enhance developer's experience. While `requirements.txt` contains the packages needed for the application to run.

Install all of these by running:

```bash
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

---

### Pre-commit

Inorder to make sure the codebase is clean and the style is consistent between many developers, we use a few lint tools to detect and auto-fix (if possible). These can be found in `.pre-commit-config.yaml`.

To install git hooks in your `.git` directory, run:
```
pre-commit install
```

These lint tools will be run when you commit your code and you can only successfully commit if . You can also run it without commiting: `pre-commit run --all-files`

---

### You're good to run the program or to write your code now! :)
