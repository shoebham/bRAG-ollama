from io import BytesIO
from PyPDF2 import PdfReader 

from app.settings import settings

from tqdm import tqdm
import openai
import uuid
from qdrant_client.http.models import PointStruct
from qdrant_client.http import models
from app.core.logs import logger
import semchunk
from transformers import AutoTokenizer # Neither `transformers` nor `tiktoken` are required,
import tiktoken                        # they are here for demonstration purposes.


def init_qdrant_client(client):
    client.recreate_collection(
        collection_name="pdfs",
        vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
    )
    #for checking collection information
    return client

def load_split_pdf(pdf_content):
    pdf_loader = PdfReader(BytesIO(pdf_content))
    pdf_text = ""
    for page_num in range(len(pdf_loader.pages)):
        pdf_page = pdf_loader.pages[page_num]
        pdf_text += pdf_page.extract_text()
    return pdf_text

def chunk_text(text):
    chunk_size = 200
    chunker = semchunk.chunkerify('umarbutler/emubert', chunk_size) or \
          semchunk.chunkerify('gpt-4', chunk_size) or \
          semchunk.chunkerify('cl100k_base', chunk_size) or \
          semchunk.chunkerify(AutoTokenizer.from_pretrained('umarbutler/emubert'), chunk_size) or \
          semchunk.chunkerify(tiktoken.encoding_for_model('gpt-4'), chunk_size) or \
          semchunk.chunkerify(lambda text: len(text.split()), chunk_size)
    return chunker(text)

def get_embedding(text_chunks, model_id="mxbai-embed-large"):
    from app.chat.services import ollama_client

    points = []
    for idx, chunk in enumerate(text_chunks):
        response= ollama_client.embeddings(
        model='mxbai-embed-large',
        prompt='text_chunks',
        )

        embeddings = response["embedding"]
        point_id = str(uuid.uuid4())  # Generate a unique ID for the point
        points.append(PointStruct(id=point_id, vector=embeddings, payload={"text": chunk}))

    return points

def insert_data(client,points):
    client.upsert(
        collection_name="pdfs",
        wait=True,
        points=points
    )
    

def start(client,pdf_content):
    print("in start client ",pdf_content)
    init_qdrant_client(client=client)
    pdf_text = load_split_pdf(pdf_content)
    chunked_pdf_text = chunk_text(pdf_text)
    embeddings = get_embedding(chunked_pdf_text)
    insert_data(client,embeddings)

