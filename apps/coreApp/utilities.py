import os
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_file(file_field):
    file_path = file_field.path
    file_extension = os.path.splitext(file_path)[1].lower()

    try:
        if file_extension == '.pdf':
            text = extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            text = extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = extract_text_from_txt(file_path)
        else:
            return "Unsupported file type."

        if not text.strip():
            return "No text found in the file."

        return text

    except Exception as e:
        return f"Error extracting text: {e}"


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

    
# just for testing purposes, you can uncomment the following lines to test the function
# from .models import Content
# content = Content.objects.get(id=2)  # Replace with the actual content ID
# print(extract_text_from_file(content.file_saved))

from gtts import gTTS

def transform_text_to_speech(file_field, output_dir='media/audios'):
    """
    Extract text from a file, convert it to speech, and save the audio file in the specified directory.
    """
    try:
        # Extract text from the file
        text = extract_text_from_file(file_field)

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Generate a unique filename for the audio file
        file_name = os.path.splitext(os.path.basename(file_field.name))[0]
        audio_file_path = os.path.join(output_dir, f"{file_name}.mp3")

        # Convert text to speech
        if text.strip():  # Ensure there's text to convert
            tts = gTTS(text=text, lang='en')  # Convert text to speech
            tts.save(audio_file_path)  # Save the audio file
            return audio_file_path
        else:
            return "No text found in the file to convert to speech."

    except Exception as e:
        return f"Error converting text to speech: {e}"
    
# from .models import Content
# content = Content.objects.get(id=2)

# # Convert the file to speech and store it in media/audios
# audio_file_path = transform_text_to_speech(content.file_saved)

# # Print the result
# print(f"Audio file generated at: {audio_file_path}")