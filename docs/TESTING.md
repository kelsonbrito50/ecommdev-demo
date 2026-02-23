# Testing Guide

## Overview

EcommDev uses pytest with pytest-django for backend testing.

## Setup

```bash
pip install -r requirements-dev.txt
```

## Running Tests

```bash
# All tests
pytest

# With coverage report
pytest --cov=. --cov-report=html

# Specific module
pytest apps/products/tests/

# Specific test
pytest apps/products/tests/test_models.py::TestProduct::test_str
```

## Test Organization

```
apps/
├── products/
│   └── tests/
│       ├── test_models.py
│       ├── test_views.py
│       └── test_api.py
├── orders/
│   └── tests/
└── users/
    └── tests/
```

## Fixtures

Shared fixtures are in `/conftest.py`:

```python
@pytest.fixture
def user(db):
    return User.objects.create_user(...)

@pytest.fixture
def product(db):
    return Product.objects.create(
        name='Test Product',
        price=Decimal('99.99'),
        stock=10
    )
```

## Coverage Target

Aim for >80% coverage on business logic (models, services, API handlers).

```bash
pytest --cov=apps --cov-report=term-missing
```
