# IR Pattern Analyzer

This project analyzes the patterns of IR (Investor Relations) pages of companies to build a smarter web scraper.

## Overview

The goal of this project is to systematically analyze the structure and patterns of corporate IR pages. By understanding these patterns, we can create a more efficient and robust web scraper for downloading IR documents, such as integrated reports.

### Features

-   `analyze_ir_patterns.py`: This script analyzes a list of company websites to identify common patterns for linking to IR pages and PDF documents.
-   `smart_ir_downloader.py`: This script (to be implemented) will use the analysis results to intelligently locate and download IR documents.

## How to Use

1.  **Install Dependencies:**

    ```bash
    pip install pandas requests beautifulsoup4
    ```

2.  **Prepare Company List:**

    Create a `topix_companies.csv` file with the following columns:

    -   `Ticker`: Stock ticker symbol
    -   `Name`: Company name
    -   `URL`: Company website URL

3.  **Run the Analysis:**

    ```bash
    python analyze_ir_patterns.py
    ```

    This will generate two files:

    -   `ir_pattern_analysis.json`: A summary of the identified patterns.
    -   `ir_pattern_details.csv`: Detailed analysis results for each company.

4.  **Develop the Smart Downloader:**

    Use the generated `ir_pattern_analysis.json` to implement the `smart_ir_downloader.py` script.
