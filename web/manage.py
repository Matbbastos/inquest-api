import json
import coverage
import unittest
from flask.cli import FlaskGroup

from api import app, db
from api.model import Person, Company, Asset


COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'tests/*',
        'api/media/*',
        'api/static/*'
    ]
)
COV.start()

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    with open('seed.json') as f:
        data = json.load(f)
        # for user in data:
            # Update to use new database structure
            # db.session.add(Person(email=data[user].get('email', '')))
    db.session.commit()


@cli.command("cov")
def cov():
    """
    Runs the unit tests and generates a coverage report on success.
    While the application is running, you can run the following command in a new terminal:
    'docker-compose run --rm flask python manage.py cov' to run all the tests in the
    'tests' directory. If all the tests pass, it will generate a coverage report.
    :return int: 0 if all tests pass, 1 if not
    """

    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        # COV.html_report()
        COV.erase()
        return 0
    else:
        return 1


if __name__ == "__main__":
    cli()
