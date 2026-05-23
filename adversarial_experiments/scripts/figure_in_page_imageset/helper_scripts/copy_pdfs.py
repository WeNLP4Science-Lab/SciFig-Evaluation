import os
import json
import shutil
import logging
from pathlib import Path

# Configure logging to write to both console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("missing_pdfs.log"),
        logging.StreamHandler()
    ]
)

def main():
    # Define directories
    base_dir = Path(__file__).resolve().parent
    english_only_dir = base_dir / "english_only_annotations"
    downloaded_pdfs_dir = base_dir / "downloaded_arxiv_pdfs"
    output_dir = base_dir / "paper_pdfs"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    if not english_only_dir.exists():
        logging.error(f"Input directory '{english_only_dir}' does not exist.")
        return

    if not downloaded_pdfs_dir.exists():
        logging.warning(f"PDF directory '{downloaded_pdfs_dir}' does not exist. The script might not find any PDFs unless the path is updated.")

    # Process each JSON file in the english_only directory
    for json_path in english_only_dir.glob("*.json"):
        base_name = json_path.stem  # e.g., 'english_fig_001'
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logging.error(f"Failed to read {json_path}: {e}")
            continue

        arxiv_id = data.get("arxiv_id")
        if not arxiv_id:
            logging.error(f"No 'arxiv_id' found in {json_path.name}")
            continue

        # Look for the corresponding PDF in downloaded_arxiv_pdfs
        pdf_found = False
        if downloaded_pdfs_dir.exists():
            for pdf_path in downloaded_pdfs_dir.glob("*.pdf"):
                if arxiv_id in pdf_path.name:
                    # Found the PDF, copy and rename it
                    new_pdf_name = f"{base_name}_paper.pdf"
                    destination_path = output_dir / new_pdf_name
                    
                    try:
                        shutil.copy2(pdf_path, destination_path)
                        logging.info(f"Copied '{pdf_path.name}' to '{new_pdf_name}'")
                    except Exception as e:
                        logging.error(f"Failed to copy {pdf_path.name}: {e}")
                        
                    pdf_found = True
                    break

        if not pdf_found:
            logging.warning(f"Could not find PDF for arxiv_id '{arxiv_id}' (from {json_path.name})")

if __name__ == "__main__":
    main()
