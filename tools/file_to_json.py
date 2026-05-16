import pandas as pd
from pydantic import BaseModel,Field
from pathlib import Path
from model.config import Settings as settings

data_list = []
settings.logging_config()

# Allowed file extensions
ALLOWED_EXTENSIONS = [".csv",".md",".txt",".pdf",".docx",".xlsx"]

class FileInfo(BaseModel):
    file_name:str
    file_type:str
    file_content:str

def read_file_content(file_path:Path) -> str:
    suffix = file_path.suffix.lower()

    if  suffix == ".txt" or suffix == ".md":
        return file_path.read_text(encoding="utf-8");
    elif suffix == ".csv":
        df = pd.read_csv(file_path)
        return df.to_json(orient="records")
    elif suffix == ".xlsx":
        df = pd.read_excel(file_path)
        return df.to_json(orient="records")
    elif suffix == ".pdf":
        from PyPDF2 import PdfReader
        reader = PdfReader(str(file_path))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    elif suffix == ".docx":
        from docx import Document
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        logger.error(f"{file_suffix} is not allowed.")
        raise ValueError(f"Unsupported file type:{suffix}")


def file_to_json(file_path: Path, file_name: str, file_type: str, file_content: str) -> dict:
    '''
    Convert a file to JSON
    :Param file_path: Path to the file
    :Param file_name: Name of the file
    :Param file_type: Type of the file
    :Param file_content: Content of the file
    return: JSON representation of the file content
    '''

    # Check if the file exists
    if not file_path.exists():
        logger.error(f"File {file_path} does not exist.")
        raise FileNotFoundError(f"File {file_path} not found.")

    # Check if the file type is allowed
    suffix = file_path.suffix.lower()
    if file_suffix not in ALLOWED_EXTENSIONS:
        logger.error(f"{file_suffix} is not allowed.")
        raise ValueError(f"Unsupported file type: {file_path}")

    content = read_file_content(file_path)

    data = FileInfo{
        file_name = file_path.name,
        file_type = suffix,
        file_content = content
    }
    return data.dict()

   

    



