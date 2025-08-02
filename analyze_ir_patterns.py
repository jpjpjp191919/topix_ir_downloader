# analyze_ir_patterns.py
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time
import re
from collections import Counter, defaultdict
import os

class IRPatternAnalyzer:
    def __init__(self):
        self.ir_patterns = defaultdict(list)
        self.pdf_patterns = defaultdict(list)
        self.results = []
        
    def analyze_company(self, ticker, name, url):
        """1社分のIRページパターンを分析"""
        print(f"\n分析中: {ticker} {name}")
        result = {
            'ticker': ticker,
            'name': name,
            'url': url,
            'ir_page_patterns': [],
            'pdf_link_patterns': [],
            'html_structure': {}
        }
        
        try:
            # メインページを取得
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; IRPatternAnalyzer/1.0)'
            })
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # IRページへのリンクパターンを収集
            ir_links = self.find_ir_links(soup, url)
            result['ir_page_patterns'] = ir_links
            
            # IRページの構造を分析
            for ir_link in ir_links[:1]:  # 最初のIRページだけ詳細分析
                ir_structure = self.analyze_ir_page(ir_link['url'])
                result['html_structure'] = ir_structure
                result['pdf_link_patterns'] = ir_structure.get('pdf_patterns', [])
                
        except Exception as e:
            result['error'] = str(e)
            
        self.results.append(result)
        return result
    
    def find_ir_links(self, soup, base_url):
        """IRページへのリンクパターンを抽出"""
        ir_links = []
        
        # パターン1: URLベース
        url_patterns = [
            r'/ir/?',
            r'/investor/?',
            r'/investors/?',
            r'/IR/?',
            r'/investor[-_]?relations/?',
            r'/株主.*投資家',
            r'/投資家情報/?'
        ]
        
        # パターン2: テキストベース
        text_patterns = [
            r'IR情報?',
            r'投資家.*情報',
            r'株主.*投資家',
            r'Investor\s*Relations?',
            r'IR\s*Information',
            r'投資家の皆様へ'
        ]
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            full_url = urljoin(base_url, href)
            
            # URLパターンマッチ
            for pattern in url_patterns:
                if re.search(pattern, href, re.IGNORECASE):
                    ir_links.append({
                        'url': full_url,
                        'text': text,
                        'pattern_type': 'url',
                        'pattern': pattern,
                        'tag_location': self.get_tag_location(link)
                    })
                    break
                    
            # テキストパターンマッチ
            for pattern in text_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    ir_links.append({
                        'url': full_url,
                        'text': text,
                        'pattern_type': 'text',
                        'pattern': pattern,
                        'tag_location': self.get_tag_location(link)
                    })
                    break
                    
        return ir_links
    
    def get_tag_location(self, tag):
        """タグの位置情報を取得（ヘッダー、フッター、サイドバーなど）"""
        parents = [p.name for p in tag.parents if p.name]
        
        # 一般的な位置パターン
        if any(p in ['header', 'nav'] for p in parents):
            return 'header'
        elif any(p in ['footer'] for p in parents):
            return 'footer'
        elif any(p in ['aside', 'sidebar'] for p in parents):
            return 'sidebar'
        elif any('nav' in str(p.get('class', [])) for p in tag.parents):
            return 'navigation'
        else:
            return 'main_content'
    
    def analyze_ir_page(self, ir_url):
        """IRページの構造を分析"""
        try:
            time.sleep(1)  # サーバー負荷対策
            response = requests.get(ir_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            structure = {
                'url': ir_url,
                'title': soup.title.string if soup.title else '',
                'pdf_patterns': [],
                'navigation_structure': {},
                'content_sections': []
            }
            
            # PDFリンクパターンを分析
            pdf_links = soup.find_all('a', href=re.compile(r'\.pdf', re.IGNORECASE))
            
            for pdf_link in pdf_links:
                href = pdf_link.get('href', '')
                text = pdf_link.get_text(strip=True)
                
                # 統合報告書かどうかの判定パターン
                is_integrated = False
                report_year = None
                
                integrated_patterns = [
                    r'統合報告書',
                    r'統合レポート',
                    r'integrated\s*report',
                    r'annual\s*report',
                    r'アニュアルレポート'
                ]
                
                for pattern in integrated_patterns:
                    if re.search(pattern, text + href, re.IGNORECASE):
                        is_integrated = True
                        # 年度を抽出
                        year_match = re.search(r'20\d{2}', text + href)
                        if year_match:
                            report_year = year_match.group()
                        break
                
                if is_integrated:
                    structure['pdf_patterns'].append({
                        'url': urljoin(ir_url, href),
                        'text': text,
                        'year': report_year,
                        'parent_tag': pdf_link.parent.name,
                        'container_class': pdf_link.parent.get('class', []),
                        'link_structure': self.analyze_link_structure(pdf_link)
                    })
            
            # ナビゲーション構造を分析
            nav_elements = soup.find_all(['nav', 'ul', 'div'], class_=re.compile(r'nav|menu', re.IGNORECASE))
            structure['navigation_structure'] = {
                'count': len(nav_elements),
                'locations': [self.get_tag_location(nav) for nav in nav_elements]
            }
            
            return structure
            
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_link_structure(self, link_tag):
        """リンクの構造を詳細分析"""
        structure = {
            'has_image': bool(link_tag.find('img')),
            'has_icon': bool(link_tag.find(['i', 'svg'])),
            'parent_list': link_tag.find_parent('li') is not None,
            'parent_table': link_tag.find_parent('table') is not None,
            'siblings_count': len(list(link_tag.parent.children))
        }
        return structure
    
    def generate_report(self):
        """分析結果をレポート化"""
        report = {
            'total_companies': len(self.results),
            'ir_page_patterns': self.aggregate_patterns('ir_page_patterns'),
            'pdf_patterns': self.aggregate_patterns('pdf_link_patterns'),
            'common_structures': self.find_common_structures()
        }
        
        return report
    
    def aggregate_patterns(self, pattern_type):
        """パターンを集計"""
        all_patterns = []
        for result in self.results:
            patterns = result.get(pattern_type, [])
            if isinstance(patterns, list):
                all_patterns.extend(patterns)
        
        # パターンの頻度を集計
        pattern_counter = Counter()
        location_counter = Counter()
        
        for pattern in all_patterns:
            if isinstance(pattern, dict):
                pattern_counter[pattern.get('pattern', '')] += 1
                location_counter[pattern.get('tag_location', '')] += 1
        
        return {
            'total': len(all_patterns),
            'pattern_frequency': dict(pattern_counter.most_common(10)),
            'location_frequency': dict(location_counter.most_common())
        }
    
    def find_common_structures(self):
        """共通の構造パターンを発見"""
        structures = []
        for result in self.results:
            if 'html_structure' in result and 'pdf_patterns' in result['html_structure']:
                for pdf in result['html_structure']['pdf_patterns']:
                    structures.append(pdf.get('link_structure', {}))
        
        # 共通パターンを見つける
        common = {
            'has_image': sum(1 for s in structures if s.get('has_image', False)),
            'in_list': sum(1 for s in structures if s.get('parent_list', False)),
            'in_table': sum(1 for s in structures if s.get('parent_table', False))
        }
        
        return common

# 実行スクリプト
def main():
    # CSVファイル読み込み
    df = pd.read_csv('topix_companies.csv')
    
    # 分析器を初期化
    analyzer = IRPatternAnalyzer()
    
    # 最初の100社で分析（テスト）
    test_df = df.head(100)
    
    # 各社を分析
    for idx, row in test_df.iterrows():
        analyzer.analyze_company(row['Ticker'], row['Name'], row['URL'])
        time.sleep(2)  # サーバー負荷対策
        
        # 定期的に保存
        if idx % 10 == 0:
            save_intermediate_results(analyzer.results)
    
    # 最終レポート生成
    report = analyzer.generate_report()
    
    # 結果を保存
    with open('ir_pattern_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 詳細結果も保存
    pd.DataFrame(analyzer.results).to_csv('ir_pattern_details.csv', index=False)
    
    print("\n=== 分析完了 ===")
    print(f"分析企業数: {report['total_companies']}")
    print(f"\nIRページパターン:")
    for pattern, count in report['ir_page_patterns']['pattern_frequency'].items():
        print(f"  {pattern}: {count}回")

def save_intermediate_results(results):
    """中間結果を保存"""
    with open('ir_analysis_intermediate.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
