import os
import requests

# --- Settings ---
PDF_SAVE_DIR = 'downloaded_pdfs'

def download_pdf(url, save_path):
    """Download a PDF from a URL."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Successfully downloaded {save_path}')
        return True
    except requests.exceptions.RequestException as e:
        print(f'Error downloading {url}: {e}')
        return False

def main():
    """Main function to download PDFs from a list of URLs."""
    if not os.path.exists(PDF_SAVE_DIR):
        os.makedirs(PDF_SAVE_DIR)

    # This list will be populated based on the analysis from analyze_html.py
    pdf_urls = [
        # Example: {'name': 'toyota_2023_report', 'url': 'https://.../report.pdf'}
    ]

    if not pdf_urls:
        print("The `pdf_urls` list is empty. Please populate it with the URLs found from your analysis.")
        return

    for pdf_info in pdf_urls:
        file_name = pdf_info['name'] + '.pdf'
        save_path = os.path.join(PDF_SAVE_DIR, file_name)
        download_pdf(pdf_info['url'], save_path)

if __name__ == '__main__':
    main()
