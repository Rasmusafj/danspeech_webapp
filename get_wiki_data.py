from datasets import load_dataset
from tqdm import tqdm
from transformers import pipeline, AutoTokenizer

# Load the Danish subset of the Wikipedia dataset from Hugging Face
dataset = load_dataset("olm/wikipedia", language="da", date="20230320", split="train")

# Initialize the sentiment classification model and tokenizer
model_name = "alexandrainst/da-offensive-detection-base"
model = pipeline("sentiment-analysis", model=model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
word_tokenizer = AutoTokenizer.from_pretrained("vesteinn/DanskBERT")

def check_sent(text):
    # Check if chunk contains two whitespace characters in a row, which indicates a new paragraph or section in the text
    if "  " in text:
        return False

    # Check if the chunk is more than 6 tokens long and less than 40 tokens long
    if len(tokenizer.tokenize(text)) < 8 or len(tokenizer.tokenize(text)) > 25:
        return False

    # Check if the chunk contains a URL
    if "http" in text:
        return False

    # Check if the chunk contains non-alphanumeric characters
    no_space_text = text.replace(" ", "")
    if not no_space_text.isalnum():
        return False
    
    return True

# Define a function to split the text into chunks that take at most 10 seconds to read out loud
def chunk_text(text):
    speaking_rate = 120  # average speaking rate in words per minute
    max_duration = 10  # maximum duration of each chunk in seconds
    chunk_texts = []
    text = text.replace("\n", " ")
    # Split the text into sentences
    for sent in text.split(". "):
        duration = len(tokenizer.tokenize(sent)) / speaking_rate * 60
        if duration > max_duration:
            # Split the sentence on ","
            for sub_sent in sent.split(", "):
                if check_sent(sub_sent):
                    chunk_texts.append(sub_sent.strip().capitalize())
        else:
            if check_sent(sent):
                chunk_texts.append(sent.strip().capitalize())
    return chunk_texts

# Process each article in the dataset
chunks_to_keep = []
for article in tqdm(dataset):
    # Split the text into chunks
    chunks = chunk_text(article["text"])
    # Classify the sentiment of each chunk
    for j, chunk in enumerate(chunks):
        result = model(chunk)
        if not result[0]["label"] == "Offensive":
            # Keep the chunk if it is not offensive
            chunks_to_keep.append(chunk)
    
    # Save the chunks to a text file
    with open("da_wiki.txt", "a") as f:
        f.write("\n".join(chunks_to_keep))