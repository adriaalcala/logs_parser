"""Nox sessions."""
import tempfile

import nox
from nox.sessions import Session


package = "log_parser"
locations = "log_parser", "tests", "noxfile.py", "docs/conf.py"


@nox.session(python="3.8")
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.run("flake8", *args, external=True)


@nox.session(python="3.8")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "pip", "freeze", ">", f"{requirements.name}", external=True,
        )
        print(requirements.name)
        session.run("safety", "check", external=True)


@nox.session(python="3.8")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.run("mypy", *args, external=True)


@nox.session(python="3.8")
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "log_parser", "--cov-report", "term-missing"]
    session.run("pytest", f"--typeguard-packages={package}", *args, external=True)


@nox.session(python="3.8")
def pytype(session: Session) -> None:
    """Type-check using pytype."""
    args = session.posargs or ["--disable=import-error", *locations]
    session.run("pytype", *args, external=True)


@nox.session(python="3.8")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.run("coverage", "xml", "--fail-under=100")


@nox.session(python="3.8")
def docs(session: Session) -> None:
    """Build the documentation."""
    session.run("sphinx-build", "docs", "docs/_build", "-E", "-a", external=True)
