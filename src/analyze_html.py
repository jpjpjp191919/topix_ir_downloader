import os
from bs4 import BeautifulSoup

# --- Settings ---
HTML_DIR = 'saved_html'

def find_report_links(html_path):
    """Analyze a single HTML file to find potential report links."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # --- Pattern Matching Examples ---
    # This is where you will add your logic to find links.
    # Below are some example patterns to get you started.

    # Pattern A: Find links with text like 'Integrated Report' or 'Annual Report'
    report_keywords = ['統合報告書', 'Integrated Report', 'アニュアルレポート', 'Annual Report']
    for keyword in report_keywords:
        links = soup.find_all('a', string=lambda text: text and keyword in text)
        for link in links:
            print(f'Found potential link in {os.path.basename(html_path)}: {link.get("href")}')

    # Pattern B: Find links in a section with a title like 'IR Library'
    # This is more complex and will require inspecting the HTML structure

    # Pattern C: Find links where the URL contains keywords
    url_keywords = ['integrated_report', 'annual_report', 'library']
    for keyword in url_keywords:
        links = soup.find_all('a', href=lambda href: href and keyword in href)
        for link in links:
            print(f'Found potential link by URL in {os.path.basename(html_path)}: {link.get("href")}')

def main():
    """Main function to analyze all downloaded HTML files."""
    if not os.path.exists(HTML_DIR):
        print(f'Error: Directory not found - {HTML_DIR}')
        return

    # This example analyzes just one file. You can loop through all files.
    # for filename in os.listdir(HTML_DIR):
    #     if filename.endswith('.html'):
    #         html_path = os.path.join(HTML_DIR, filename)
    #         find_report_links(html_path)

    # For demonstration, we'll just try to analyze the first HTML file found.
    try:
        first_html_file = next(f for f in os.listdir(HTML_DIR) if f.endswith('.html'))
        print(f'--- Analyzing {first_html_file} as an example ---')
        find_report_links(os.path.join(HTML_DIR, first_html_file))
    except StopIteration:
        print('No HTML files found in the saved_html directory.')

if __name__ == '__main__':
    main()
