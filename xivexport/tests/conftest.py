"""
Pytest configuration file for data_export tests.
"""
import pytest
import asyncio
from unittest.mock import Mock


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_xivapy_lang_dict():
    """Create a mock LangDict for testing"""
    return {
        'en': 'English Text',
        'ja': '日本語テキスト',
        'fr': 'Texte français',
        'de': 'Deutscher Text'
    }


@pytest.fixture
def mock_empty_lang_dict():
    """Create an empty LangDict for testing"""
    return {}


@pytest.fixture
def mock_xivapy_result():
    """Create a mock xivapy result object"""
    result = Mock()
    result.data = Mock()
    return result