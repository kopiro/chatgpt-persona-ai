# ChatGPT AI Persona

Emulate an AI Persona using ChatGPT and provides a server to interact with it.

It _unofficialy_ uses the ChatGPT playground and uses Playwright to parse the HTML; for this reasons:

- Do not use it in production, only for development purposes
- I can only handle 1 (yes, ONE) request at the time, the other will be put in a FIFO queue
- You will be likely rate-limited if used extensively
- It can break at any time when OpenAI changes the HTML format

## Installation

```
touch ai_header.txt
touch ai_name.txt
pip install -r requirements.txt
playwright install
```

## Configuration

You have two text files that you can change:

- `ai_name.txt` - Your AI name
- `ai_header.txt` - The initial blob of text you can send to prime the AI

## Usage

```
python3 server.py
```

The server runs at port `8080`

## API

`POST /chat`

```sh
curl -X POST http://localhost:8080/chat -H "content-type: application/json" --data '{ "sender": "kopiro", "message": "Hello!" }'
```

# Credit

- Took [this repository](https://github.com/taranjeet/chatgpt-api) and repurposed for my AI persona use-case.
