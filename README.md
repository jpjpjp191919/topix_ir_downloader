# TOPIX IR Downloader

This project aims to download integrated reports from the IR pages of all TOPIX-listed companies.

## Project Structure

- `src/`: Contains the Python scripts.
  - `html_downloader.py`: Downloads the HTML of IR pages.
  - `analyze_html.py`: (Placeholder) Analyzes the downloaded HTML to find patterns for report links.
  - `pdf_downloader.py`: (Placeholder) Downloads the actual PDF reports based on the patterns found.
- `data/`: Contains the input data.
  - `topix_companies.csv`: A CSV file with the list of companies, their ticker symbols, and IR page URLs.
- `saved_html/`: Stores the downloaded HTML files.
- `logs/`: Stores log files, such as lists of failed URLs.

## How to Use

### Step 1: Download HTML

1.  Place your CSV file of TOPIX companies and their IR URLs in the `data` directory. The file should be named `topix_companies.csv` and have the columns `Ticker`, `Name`, and `URL`.
2.  Install the required libraries:
    ```
    pip install -r requirements.txt
    ```
3.  Run the HTML downloader script:
    ```
    python src/html_downloader.py
    ```

    This will save the HTML content of each company's IR page into the `saved_html` directory.
