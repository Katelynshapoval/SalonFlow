from unittest.mock import MagicMock, patch

from app.services.bot_service import BotService


@patch("app.services.bot_service.ApplicationBuilder")
def test_bot_service_builds_app(mock_builder_cls):
    # Prepare fake app and builder.
    mock_app = MagicMock()
    mock_builder = MagicMock()

    mock_builder_cls.return_value = mock_builder
    mock_builder.token.return_value = mock_builder
    mock_builder.build.return_value = mock_app

    # Build the bot service.
    service = BotService("fake-token")
    app = service.build()

    # Check the app is built and returned.
    assert service.token == "fake-token"
    assert app == mock_app

    # Check the Telegram app is built with the token.
    mock_builder.token.assert_called_once_with("fake-token")
    mock_builder.build.assert_called_once()

    # Check all handlers were added.
    assert mock_app.add_handler.call_count == 10