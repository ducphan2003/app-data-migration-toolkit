import pytest
from unittest.mock import Mock
from app.services import PromptingService


@pytest.fixture
def mock_claude_repository():
    return Mock()


@pytest.fixture
def mock_gemini_repository():
    return Mock()


@pytest.fixture
def mock_gpt_repository():
    return Mock()


@pytest.fixture
def prompting_service(mock_claude_repository, mock_gemini_repository, mock_gpt_repository):
    return PromptingService(mock_claude_repository, mock_gemini_repository, mock_gpt_repository)


def test_get_prompt(prompting_service, mock_claude_repository, mock_gemini_repository, mock_gpt_repository):
    # Arrange
    input_text = "test input"
    mock_claude_repository.get_response.return_value = "Claude response"
    mock_gemini_repository.get_response.return_value = "Gemini response"
    mock_gpt_repository.get_response.return_value = "GPT response"

    # Act
    result = prompting_service.get_prompt(input_text)

    # Assert
    assert result == "Claude: Claude response, Gemini: Gemini response, GPT: GPT response"
    mock_claude_repository.get_response.assert_called_once_with(input_text)
    mock_gemini_repository.get_response.assert_called_once_with(input_text)
    mock_gpt_repository.get_response.assert_called_once_with(input_text)
