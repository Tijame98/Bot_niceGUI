#!/usr/bin/env python3
from langchain_openai import ChatOpenAI
from log_callback_handler import NiceGuiLogElementCallbackHandler

from nicegui import ui

OPENAI_API_KEY = "sk-proj-i3eIo6ujjtATFRz4RQvRT3BlbkFJfxr9nY3u5ofM3FrDOfP3"  # TODO: set your OpenAI API key here


@ui.page('/')
def main():
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', streaming=True, max_tokens=150, openai_api_key=OPENAI_API_KEY)

    # Define the system prompt
    system_prompt = (
        "You are an expert in Mercedes-Benz car sales. Provide purchase advice "
        "for someone looking for information about a car. Be clear, brief, and creative. "
        "Your goal is to book a test drive for the client. Include key points such as car features, "
        "benefits, and unique selling points. End with a call to action to schedule a test drive."
    )

    async def send() -> None:
        question = text.value
        text.value = ''

        with message_container:
            ui.chat_message(text=question, name='You', sent=True)
            response_message = ui.chat_message(name='Sales Bot', sent=False)
            spinner = ui.spinner(type='dots')

        response = ''
        # Include system prompt in each API request
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        async for chunk in llm.astream(messages, config={'callbacks': [NiceGuiLogElementCallbackHandler(log)]}):
            response += chunk.content
            response_message.clear()
            with response_message:
                ui.html(response)
            ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')
        message_container.remove(spinner)


    ui.add_css(r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}')

    # the queries below are used to expand the contend down to the footer (content can then use flex-grow to expand)
    ui.query('.q-page').classes('flex')
    ui.query('.nicegui-content').classes('w-full')

    with ui.tabs().classes('w-full') as tabs:
        chat_tab = ui.tab('Chat')
        logs_tab = ui.tab('Logs')
    with ui.tab_panels(tabs, value=chat_tab).classes('w-full max-w-2xl mx-auto flex-grow items-stretch'):
        message_container = ui.tab_panel(chat_tab).classes('items-stretch')
        with ui.tab_panel(logs_tab):
            log = ui.log().classes('w-full h-full')

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message' if OPENAI_API_KEY != "sk-proj-i3eIo6ujjtATFRz4RQvRT3BlbkFJfxr9nY3u5ofM3FrDOfP3" else \
                'Please provide your OPENAI key in the Python script first!'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)
        ui.markdown('simple chat bot built with [NiceGUI](https://nicegui.io) by Houssine Majite') \
            .classes('text-xs self-end mr-8 m-[-1em] text-primary')


ui.run(title='Chat with GPT-3 (example)')