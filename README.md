# Inquest API
The goal of this repository is to store and document the Assets-API.

## Commits
For commit messages in this repository, the following prefix convention is used:

* FEAT: new feature added to a particular application
* FIX: bug fix
* STYLE: feature and updates related to styling
* REFACTOR: refactoring a specific section of the codebase
* TEST: everything related to testing
* DOCS: everything related to documentation
* CHORE: regular code maintenance

## Docker
```bash
# Build and run container in 'detached' mode
docker-compose up -d --build
# Create database for testing
docker-compose exec web python manage.py create_db
# Populate database with test data
docker-compose exec web python manage.py seed_db
# Run unit tests and coverage report (if successful)
docker-compose exec web python manage.py cov
# Run psql to access database
docker-compose exec db psql --username=admin --dbname=test_db
# Bring down all containers and volumes
docker-compose down -v
```
