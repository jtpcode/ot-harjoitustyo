# Ohjelmistotekniikka, harjoitustyö

## Note on Python Version

The application's functionality has been tested with Python version `3.13`. Issues may arise, when using older Python versions.

## Documentation

- [Requirements Specification](./Documentation/requirements_specification.md)
- [Work Time Log](./Documentation/time_tracking.md)
- [Changelog](./Documentation/changelog.md)

## Installation

1. Install dependencies with the following command:

```bash
poetry install
```

2. Start the application with:

```bash
poetry run invoke start
```

## Command Line Functions

### Running the Application

The application can be started with:

```bash
poetry run invoke start
```

### Testing

Tests can be run with the following command:

```bash
poetry run invoke test
```

### Test Coverage

A test coverage report can be generated with:

```bash
poetry run invoke coverage-report
```

The report will be generated in the *htmlcov* directory.

