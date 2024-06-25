## bRAG (Basic Retrieval Augmented Generation) for ollama


Following [this](https://grski.pl/pdf-brag) to create a RAG without langchain.

This project implements streaming and RAG over pdf,  and gives answer according to the pdf provided.
Implemented using:
- FastAPI
- Postgres
- Ollama
- SvelteKit
- Docker

I wanted to create a app that didn't use langchain, although using it would have been quite easy. Since langchain is a framework and hides away a lot of complexities behind its abstractions customizing it can be a pain.

Here is how it works in **normal** chat (It's a little slow in the first response):

https://github.com/shoebham/bRAG-ollama/assets/25881429/c5f99911-4019-4d0a-9711-1c1858d0e350

Here is how it works in **Pdf** chat, I used the famous overleaf [software engineer resume](https://www.overleaf.com/latex/templates/software-engineer-resume/gqxmqsvsbdjf):


https://github.com/shoebham/bRAG-ollama/assets/25881429/bd6d3c7c-0cae-40d7-918b-d77cc09a0e87



## Installation and Running this

To run this just run
``` 
docker compose up --build
```

it will start front end and backend on the same host  
Frontend: http://localhost:5173/  
Backend: http://localhost:8000/docs (FastAPI)

# Features
- [X] Response streaming (typing words as soon as it is recived from server)
- [X] Pdf Chat (upload a pdf and ask questions about it)
- [X] Normal Chat (you can chat normally, Currently using llama3 model but can be customized)

## To-Do
- [ ] Preserving context over chats (after uploading pdf, its context should be cached or saved) 
- [ ] Caching responses to produce better results
- [ ] Make UI more good looking
- [ ] Add support for images, videos etc.
- [ ] Fast responses
