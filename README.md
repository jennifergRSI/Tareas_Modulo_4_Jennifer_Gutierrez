# Documentación del Código

Este código es un chatbot que utiliza la API de OpenAI y Serper para realizar búsquedas en Google y generar respuestas basadas en la información encontrada. La información se extrae de las páginas web a través de solicitudes HTTP, y las respuestas se generan y muestran en un formato interactivo. A continuación se describe el funcionamiento de cada componente.

## Requerimientos

- `openai`: Biblioteca para interactuar con la API de OpenAI.
- `asyncio`: Para manejar la ejecución de tareas asíncronas.
- `aiohttp`: Para realizar solicitudes HTTP asíncronas.
- `dotenv`: Para cargar variables de entorno desde un archivo `.env`.
- `bs4` (BeautifulSoup): Para analizar el contenido HTML de las páginas web.
- `rich`: Para mostrar información en la consola de manera estilizada.

## Descripción de Funciones

### `add_to_history(user_message, bot_response)`
Añade un mensaje del usuario y la respuesta del bot al historial de la conversación.

### `search_google(query)`
Realiza una búsqueda en Google utilizando la API de Serper. Recibe un término de búsqueda y devuelve los resultados orgánicos.

### `fetch_page_text(url)`
Obtiene el texto de una página web. Usa `BeautifulSoup` para extraer el contenido de la página y devuelve los primeros 2000 caracteres.

### `generate_response(question, context)`
Genera una respuesta utilizando la API de OpenAI (GPT-3.5). La función pasa el contexto de la conversación junto con la pregunta del usuario para generar la respuesta del bot.

### `stream_response(response)`
Maneja la respuesta generada por OpenAI de manera asíncrona, imprimiendo el contenido en la consola a medida que se recibe.

### `main()`
Función principal que ejecuta el chatbot en un bucle interactivo. Permite al usuario ingresar preguntas, realiza la búsqueda en Google, extrae contenido, genera una respuesta y muestra las referencias encontradas en el proceso.

## Flujo del Programa

1. **Inicio del Chatbot**: El chatbot le da la bienvenida al usuario y le explica cómo finalizar la conversación.
2. **Interacción**: El usuario ingresa una pregunta.
3. **Búsqueda en Google**: El chatbot realiza una búsqueda en Google utilizando la API de Serper.
4. **Extracción de Contenido**: El chatbot obtiene el contenido de las primeras 5 páginas encontradas y las utiliza como contexto.
5. **Generación de Respuesta**: La API de OpenAI genera una respuesta basada en el contexto proporcionado.
6. **Streaming de Respuesta**: La respuesta del bot se muestra en tiempo real mientras se recibe.
7. **Mostrar Referencias**: Se muestra una lista de los enlaces que sirvieron como fuente para generar la respuesta.
8. **Finalización**: El chatbot permite al usuario finalizar la conversación escribiendo "salir".

## Uso

1. **Variables de Entorno**:
    - `OPENAI_API_KEY`: La clave de la API de OpenAI.
    - `SERPER_API_KEY`: La clave de la API de Serper.

2. **Dependencias**:
   Instala las dependencias requeridas con el siguiente comando:
   ```bash
   pip install openai==0.28 serpapi aiohttp beautifulsoup4 rich python-dotenv
   ```

## Descarga de las dependencias

1. **Creación del Entorno Virtual**:
   Crea un entorno virtual para el proyecto.
   ```bash
   python -m venv venv
   ```

2. **Activación del Entorno Virtual**:
   Activa el entorno virtual.
   ```bash
   . venv\Scripts\activate
   ```

3. **Instalación de Dependencias**:
   Instala las dependencias requeridas. Ubicarse en la carpeta src del proyecto y ejecutar el siguiente comando
   ```bash
   pip install -r requirements.txt
   ```

## Ejecutar código
Ubicarse en la carpeta src del proyecto y ejecutar el siguiente comando
```bash 
python main.py
```

# Pruebas unitarias

## Requerimientos
Para ejecutar las pruebas unitarias es necesario desactivar la captura o llamada a input() globalmente de la función main(), nos ubicaremos en el archivo `main.py` y actualizaremos la ejecución de la app de la siguiente forma:
```python
# Ejecuta la app
if __name__ == "__main__":
    asyncio.run(main())
```

## Ejecutar pruebas unitarias
Ubicarse en la carpeta src del proyecto y ejecutar el siguiente comando 
```bash
python -m pytest -v test_main.py
```

### `test_search_google`
Prueba la funcionalidad de la función `search_google` asegurándose de que:
- Realiza correctamente una solicitud a la API de búsqueda de Google.
- Procesa la respuesta simulada, verificando que contiene los resultados esperados.

### `test_fetch_page_text`
Valida la función `fetch_page_text` para:
- Obtener correctamente el contenido HTML de una página web dada una URL.
- Simular una respuesta y verificar que el contenido esperado está incluido en el texto retornado.

### `test_fetch_page_text_exception`
Prueba el manejo de excepciones en la función `fetch_page_text` al:
- Simular una excepción en la solicitud a una URL.
- Validar que el texto retornado sea una cadena vacía cuando ocurre un error.

### `test_stream_response`
Evalúa la función `stream_response` asegurándose de que:
- Procesa correctamente una respuesta simulada de tipo streaming.
- Produce el texto final esperado mientras imprime las partes de la respuesta en la consola.

### `test_add_to_history`
Verifica la funcionalidad de `add_to_history`, validando que:
- Los mensajes del usuario y las respuestas del bot se agregan correctamente al historial de conversación.
- El historial contiene los datos esperados después de agregar una nueva interacción.

# Tareas_Modulo_4_Jennifer_Gutierrez
