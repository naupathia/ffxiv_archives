import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from ..src.xivexport.xivclient import XivDataService, get_localized_text, ENGLISH_LANG


class TestGetLocalizedText:
    """Test the get_localized_text helper function"""

    def test_get_localized_text_with_english(self):
        """Test getting English text from LangDict"""
        lang_dict = {'en': 'Hello', 'ja': 'こんにちは', 'fr': 'Bonjour'}
        result = get_localized_text(lang_dict)
        assert result == 'Hello'

    def test_get_localized_text_with_specific_language(self):
        """Test getting specific language text from LangDict"""
        lang_dict = {'en': 'Hello', 'ja': 'こんにちは', 'fr': 'Bonjour'}
        result = get_localized_text(lang_dict, 'ja')
        assert result == 'こんにちは'

    def test_get_localized_text_fallback_to_english(self):
        """Test fallback to English when requested language is not available"""
        lang_dict = {'en': 'Hello', 'fr': 'Bonjour'}
        result = get_localized_text(lang_dict, 'ja')
        assert result == 'Hello'

    def test_get_localized_text_empty_dict(self):
        """Test with empty LangDict"""
        lang_dict = {}
        result = get_localized_text(lang_dict)
        assert result == ''

    def test_get_localized_text_none_input(self):
        """Test with None input"""
        result = get_localized_text(None)
        assert result == ''

    def test_get_localized_text_no_english_fallback(self):
        """Test when neither requested language nor English are available"""
        lang_dict = {'fr': 'Bonjour', 'de': 'Hallo'}
        result = get_localized_text(lang_dict, 'ja')
        assert result == ''


class TestXivDataService:
    """Test the XivDataService class"""

    @pytest.fixture
    def mock_client(self):
        """Mock XivApiClient for testing"""
        client = Mock()
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock()
        return client

    @pytest.fixture
    def mock_quest_result(self):
        """Mock quest result from xivapy"""
        result = Mock()
        result.data.row_id = 1
        result.data.name = {'en': 'Test Quest'}
        result.data.id = 'TestQuest001'
        result.data.expansion = {'Name': {'en': 'A Realm Reborn'}}
        result.data.previous_quest = []
        result.data.issuer_start = Mock()
        result.data.place_name = {'Name': {'en': 'Limsa Lominsa'}}
        result.data.journal_genre = {'Name': {'en': 'Main Scenario'}}
        return result

    @pytest.mark.asyncio
    async def test_get_all_quests_success(self, mock_client, mock_quest_result):
        """Test successful quest data retrieval"""
        with patch('data_export.src.xiv_client.XivApiClient', return_value=mock_client):
            # Mock the sheet method to return our test quest
            mock_client.client.sheet = AsyncMock()
            mock_client.client.sheet.return_value.__aiter__ = AsyncMock(
                return_value=iter([mock_quest_result])
            )

            result = await XivDataService.get_all_quests()

            assert len(result) == 1
            assert result[0]['row_id'] == 1
            assert result[0]['name'] == 'Test Quest'
            assert result[0]['id'] == 'TestQuest001'

    @pytest.mark.asyncio
    async def test_get_all_quests_filters_empty_names(self, mock_client):
        """Test that quests without names are filtered out"""
        # Create quest with empty name
        empty_quest = Mock()
        empty_quest.data.name = {'en': ''}

        with patch('data_export.src.xiv_client.XivApiClient', return_value=mock_client):
            mock_client.client.sheet = AsyncMock()
            mock_client.client.sheet.return_value.__aiter__ = AsyncMock(
                return_value=iter([empty_quest])
            )

            result = await XivDataService.get_all_quests()

            assert len(result) == 0

    @pytest.fixture
    def mock_item_result(self):
        """Mock item result from xivapy"""
        result = Mock()
        result.data.row_id = 1
        result.data.name = {'en': 'Test Item'}
        result.data.description = {'en': 'A test item description'}
        result.data.icon = 'test_icon.png'
        result.data.item_ui_category = {'Name': {'en': 'Materials'}}
        return result

    @pytest.mark.asyncio
    async def test_get_all_items_success(self, mock_client, mock_item_result):
        """Test successful item data retrieval"""
        with patch('data_export.src.xiv_client.XivApiClient', return_value=mock_client):
            mock_client.client.sheet = AsyncMock()
            mock_client.client.sheet.return_value.__aiter__ = AsyncMock(
                return_value=iter([mock_item_result])
            )

            result = await XivDataService.get_all_items()

            assert len(result) == 1
            assert result[0]['row_id'] == 1
            assert result[0]['name'] == 'Test Item'
            assert result[0]['description'] == 'A test item description'
            assert result[0]['icon'] == 'test_icon.png'


if __name__ == '__main__':
    pytest.main([__file__])