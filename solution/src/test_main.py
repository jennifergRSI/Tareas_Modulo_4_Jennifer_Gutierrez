import pytest
from unittest.mock import AsyncMock, patch

# Test de la función search_google
@pytest.mark.asyncio
@patch("aiohttp.ClientSession.post")
async def test_search_google(mock_post):
    from main import search_google

    # Simula una respuesta de la API
    mock_post.return_value.__aenter__.return_value.status = 200
    mock_post.return_value.__aenter__.return_value.json = AsyncMock(
        return_value={"organic": [{"title": "Result 1", "link": "https://example.com"}]}
    )

    query = "test query"
    results = await search_google(query)

    # Validaciones
    assert len(results) == 1
    assert results[0]["link"] == "https://example.com"
    mock_post.assert_called_once()

# Test de la función fetch_page_text
@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_page_text(mock_get):
    from main import fetch_page_text

    # Simula una respuesta de la página web
    mock_get.return_value.__aenter__.return_value.status = 200
    mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value="<html><body>Sample text</body></html>")

    url = "https://example.com"
    text = await fetch_page_text(url)

    # Validaciones
    assert "Sample text" in text
    mock_get.assert_called_once()

# Test para manejo de excepciones en fetch_page_text
@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_fetch_page_text_exception(mock_get):
    from main import fetch_page_text

    # Simula una excepción al intentar acceder a una URL
    mock_get.side_effect = Exception("Connection error")

    url = "https://example.com"
    text = await fetch_page_text(url)

    # Validaciones
    assert text == ""
    mock_get.assert_called_once_with(url)

# Test de la función stream_response
@pytest.mark.asyncio
async def test_stream_response():
    from main import stream_response

    # Simula una respuesta de streaming
    response = [{"choices": [{"delta": {"content": "Hello!"}}]}]

    with patch("rich.console.Console.print") as mock_print:
        final_response = await stream_response(response)

    # Validaciones
    assert final_response == "Hello!"
    mock_print.assert_any_call("Hello!", end="")

def test_add_to_history():
    from main import add_to_history, conversation_history

    # Limpia la memoria de conversación antes de la prueba
    conversation_history.clear()

    # Datos de prueba
    user_message = "¿Qué es Python?"
    bot_response = "Python es un lenguaje de programación."

    # Llamada a la función
    add_to_history(user_message, bot_response)

    # Validaciones
    assert len(conversation_history) == 1
    assert conversation_history[0] == {"user": user_message, "bot": bot_response}