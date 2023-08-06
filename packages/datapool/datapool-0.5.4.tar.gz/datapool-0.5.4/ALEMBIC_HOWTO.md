# How to create and apply migrations

1. Create and test db model changes in development environment.
2. Push changes to git.
3. Login to productive machine
4. `cd /opt/eawag_datapool`
5. `git pull`
2. `alembic -c alembic-productive.ini revision --autogenerate -m "MESSAGE HERE"`
3. `alembic -c alembic-productive.ini upgrade head`
4. Commit changes from alembic/ folder to git.
