# Data Export Tests

This directory contains unit and integration tests for the data_export project.

## Setup

1. Install test dependencies:
   ```bash
   pip install -r requirement.txt
   ```

2. Run all tests:
   ```bash
   pytest
   ```

3. Run tests with coverage:
   ```bash
   pytest --cov=data_export
   ```

4. Run specific test categories:
   ```bash
   # Unit tests only
   pytest -m unit

   # Integration tests only
   pytest -m integration

   # Skip slow tests
   pytest -m "not slow"
   ```

## Test Structure

- `test_xiv_client.py` - Tests for xivapy client wrapper and data service
- `conftest.py` - Shared pytest fixtures and configuration
- `pytest.ini` - Pytest configuration

## Writing Tests

### For async functions:
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

### For mocking xivapy:
```python
@patch('data_export.xiv_client.XivApiClient')
async def test_with_mock(mock_client):
    # Test implementation
```

## Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow-running tests