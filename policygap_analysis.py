from flask import Flask,request,jsonify
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import fitz
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from sentence_transformers.quantization import quantize_embeddings
import chromadb
from chromadb.config import Settings
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import textwrap
from IPython.display import display, Markdown
import tempfile
app = Flask(__name__)
dimensions = 512
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1", truncate_dim=dimensions)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
chroma_db_path = "content 3/policies_embeddings"
chroma_client = chromadb.PersistentClient(
    path=chroma_db_path,
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)
collection = chroma_client.get_or_create_collection(name="policy")
def extract_text_from_pdf(pdf_path):
    # Open the provided PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize a variable to store the extracted text
    text = ""

    # Iterate through all the pages in the PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Load each page
        text += page.get_text()  # Extract text from the page

    # Close the PDF document
    pdf_document.close()
    return text
def to_markdown(text):
    text.replace("."," *" )
    return textwrap.indent(text, "> ",predicate=lambda _:True)
@app.route("/compare", methods=["POST"])
def compare():
    framework1 = request.form.get("framework1","")
    framework2 = request.form.get("framework2","")
    framework3 = request.form.get("framework3","")
    policy_pdf = request.files.get("policy_pdf")
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        policy_pdf.save(temp_file.name)
        temp_file_path = temp_file.name
    policy_text = extract_text_from_pdf(temp_file_path)
    os.remove(temp_file_path)
    query = [framework1, framework2, framework3]
    query_embeddings = model.encode(query, truncate_dim=dimensions)
    results = collection.query(
    query_embeddings=query_embeddings,  # Pass the embeddings for multiple queries
    n_results=30,
    include=["documents", "distances"]  # Request documents and distances
)
    retrieved_context = ""
    # Print results for each query
    for i, query_result in enumerate(results['documents']):
        print(f"Query {i + 1}:")
        for j, doc in enumerate(query_result):
            retrieved_context+=doc
    prompt = """
You are AI model designed to gave gap analysis between the given policy_name
and the list of policy frameworks on the basis of the retrieved context.
Start the output result by Title Gap analysis between given policy name and
policy framework name.
if list of policy frameworks contain more than one policy give gap analysis
with each framework seperately in detail and covering all relevent points based on retrived context.
Don't use terms like Based on the provided context.
Given policy:
{policy_text}
Given Framework list:
{query}
Given context:
{retrieved_context}
"""
    prompt_template = PromptTemplate(
        input_variables=["policy_text", "query", "retrieved_context"],
        template=prompt,
    )
    llm_chain = LLMChain(llm=ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp",api_key=GEMINI_API_KEY, temperature=0.2), prompt=prompt_template)
    result = llm_chain.run(policy_text=policy_text, query=query, retrieved_context=retrieved_context)
    result = to_markdown(result)
    return jsonify({"result": result})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3500, debug=True)

        

    
