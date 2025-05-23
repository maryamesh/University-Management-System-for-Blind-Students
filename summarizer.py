import torch
from transformers import BartForConditionalGeneration, BartTokenizer
from PyPDF2 import PdfReader

# Path to the PDF file (Update this path)
pdf_file_path = "D:\\UNI\\Semester 7\\AML\\Active Learning_ Strategies, Tools, and Real-World Use Cases.pdf"  # <-- Change this to your actual PDF path

# Load BART model
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BartForConditionalGeneration.from_pretrained(model_name).to(device)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() if page.extract_text() else ""

        text = " ".join(text.split())  # Clean extra whitespace
        if not text:
            raise ValueError("No readable text found in the PDF!")
        return text
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)  # Exit the script on error

# Function to summarize text using BART
def summarize_text(text):
    text_length = len(text.split())

    # Define the summary range (Always Long)
    min_length = int(0.20 * text_length)
    max_length = int(0.30 * text_length)

    # Tokenization and summary generation
    inputs = tokenizer.encode(text, max_length=1024, return_tensors="pt", truncation=True).to(device)
    summary_ids = model.generate(inputs, num_beams=4, min_length=min_length, max_length=max_length, early_stopping=True)
    
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Main execution
if __name__ == "__main__":
    text = extract_text_from_pdf(pdf_file_path)
    summary = summarize_text(text)
    print(summary)  # Print only the summarized text
