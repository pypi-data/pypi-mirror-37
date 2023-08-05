# Releasing new versions

- Run `update_version.sh 1.0`, commit, and push (including tags).
- Run `pipenv run py.test` to run the tests one final time.
- Run `pipenv run ./setup.py sdist bdist_wheel` to create distribution files.
- Use [Twine](https://twine.readthedocs.io/en/latest/) to upload them,
  first as test, then for real. Note that test.pypi.org requires separate registration::

      pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*
      pipenv run twine upload dist/*
