import openai
import asyncio
import aiohttp
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich.console import Console
import os

# Configura la API de OpenAI y Serper
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
SERPER_API_KEY = os.getenv('SERPER_API_KEY')

# Consola para mostrar respuestas en streaming
console = Console()

# Memoria de conversación
conversation_history = []

def add_to_history(user_message, bot_response):
    conversation_history.append({"user": user_message, "bot": bot_response})

# Búsqueda en Google
async def search_google(query):
    async with aiohttp.ClientSession() as session:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        payload = {"q": query}
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                return (await response.json()).get("organic", [])
            return []

# Extracción de contenido
async def fetch_page_text(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    return soup.get_text(strip=True)[:2000]
        except Exception as e:
            return ""

# Generación de respuesta
async def generate_response(question, context):
    import openai
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente que cita fuentes al final de sus respuestas."},
            {"role": "assistant", "content": context},
            {"role": "user", "content": question},
        ],
        stream=True,
    )

    if not response:  # Maneja respuestas vacías
        return []

    return response

# Streaming de respuesta
async def stream_response(response):
    final_response = ""
    
    for chunk in response:
        content = chunk["choices"][0]["delta"].get("content", "")
        console.print(content, end="")
        final_response += content
    console.print("\n")
    return final_response

async def main():
    console.print("[bold green]Bienvenido al chatbot. Escribe 'salir' para finalizar.[/bold green]")
    while True:
        user_input = input("> Usuario: ")
        if user_input.lower() == "salir":
            console.print("[bold red]¡Adiós![/bold red]")
            break
        
        # Búsqueda en Google
        console.print("** Búsqueda en Internet... **")
        results = await search_google(user_input)
        
        # Procesa los primeros 5 enlaces
        context = ""
        references = []
        for result in results[:5]:
            url = result.get("link")
            references.append(url)
            text = await fetch_page_text(url)
            context += f"\nFuente: {url}\n{text}\n"
        
        # Genera respuesta
        console.print("** Generando respuesta... **")
        response = await generate_response(user_input, context)
        bot_response = await stream_response(response)
        
        # Añadir al historial
        add_to_history(user_input, bot_response)
        
        # Mostrar referencias
        console.print("[bold blue]Referencias:[/bold blue]")
        for ref in references:
            console.print(f"- {ref}")

# Ejecuta la app
#if __name__ == "__main__":
asyncio.run(main())
