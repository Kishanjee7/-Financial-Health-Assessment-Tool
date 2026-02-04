"""
PDF file handler for financial data ingestion.
Extracts tabular data from text-based PDF financial documents.
"""
import fitz  # PyMuPDF
import pandas as pd
import re
import io
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class PDFHandler:
    """Handles PDF file parsing and table extraction."""
    
    # Patterns for identifying financial document sections
    SECTION_PATTERNS = {
        'income_statement': [
            r'profit\s*(?:and|&)\s*loss',
            r'income\s*statement',
            r'statement\s*of\s*(?:profit|income)',
            r'revenue\s*statement'
        ],
        'balance_sheet': [
            r'balance\s*sheet',
            r'statement\s*of\s*(?:financial\s*)?position',
            r'assets\s*(?:and|&)\s*liabilities'
        ],
        'cash_flow': [
            r'cash\s*flow',
            r'statement\s*of\s*cash',
            r'funds\s*flow'
        ],
        'notes': [
            r'notes\s*to\s*(?:the\s*)?(?:financial\s*)?statements',
            r'significant\s*accounting\s*policies'
        ]
    }
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def parse_file(
        self, 
        file_content: bytes, 
        filename: str
    ) -> Tuple[Dict, Dict]:
        """
        Parse a PDF file and extract financial data.
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
        
        Returns:
            Tuple of (extracted data dict, metadata dict)
        """
        self.errors = []
        self.warnings = []
        metadata = {
            'filename': filename,
            'format': 'pdf',
            'parsed_at': datetime.utcnow().isoformat(),
            'pages': 0,
            'sections_found': []
        }
        
        extracted_data = {
            'text_content': [],
            'tables': [],
            'sections': {},
            'key_figures': {}
        }
        
        try:
            # Open PDF
            doc = fitz.open(stream=file_content, filetype="pdf")
            metadata['pages'] = len(doc)
            
            all_text = []
            all_tables = []
            
            for page_num, page in enumerate(doc):
                # Extract text
                text = page.get_text()
                all_text.append({
                    'page': page_num + 1,
                    'text': text
                })
                
                # Extract tables
                tables = self._extract_tables_from_page(page, page_num + 1)
                all_tables.extend(tables)
            
            doc.close()
            
            # Combine all text
            full_text = '\n'.join([t['text'] for t in all_text])
            
            # Identify sections
            sections = self._identify_sections(full_text)
            metadata['sections_found'] = list(sections.keys())
            
            # Extract key financial figures
            key_figures = self._extract_key_figures(full_text)
            
            extracted_data['text_content'] = all_text
            extracted_data['tables'] = all_tables
            extracted_data['sections'] = sections
            extracted_data['key_figures'] = key_figures
            
            metadata['table_count'] = len(all_tables)
            metadata['errors'] = self.errors
            metadata['warnings'] = self.warnings
            
            return extracted_data, metadata
            
        except Exception as e:
            self.errors.append(f"Failed to parse PDF: {str(e)}")
            metadata['errors'] = self.errors
            return extracted_data, metadata
    
    def _extract_tables_from_page(self, page, page_num: int) -> List[Dict]:
        """Extract tables from a PDF page using text analysis."""
        tables = []
        
        try:
            # Get text blocks with position info
            blocks = page.get_text("dict")["blocks"]
            
            # Look for table-like structures
            # Tables typically have aligned columns of text/numbers
            text_blocks = []
            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        line_text = ""
                        positions = []
                        for span in line["spans"]:
                            line_text += span["text"] + " "
                            positions.append(span["bbox"][0])  # x-position
                        
                        if line_text.strip():
                            text_blocks.append({
                                'text': line_text.strip(),
                                'y': line["bbox"][1],
                                'x_positions': positions
                            })
            
            # Group lines that could form tables
            current_table_lines = []
            for block in text_blocks:
                # Check if line contains numbers (likely table data)
                if re.search(r'\d+\.?\d*', block['text']):
                    current_table_lines.append(block['text'])
                elif current_table_lines and len(current_table_lines) >= 3:
                    # We found a potential table
                    table_data = self._parse_table_lines(current_table_lines)
                    if table_data:
                        tables.append({
                            'page': page_num,
                            'data': table_data
                        })
                    current_table_lines = []
            
            # Check remaining lines
            if current_table_lines and len(current_table_lines) >= 3:
                table_data = self._parse_table_lines(current_table_lines)
                if table_data:
                    tables.append({
                        'page': page_num,
                        'data': table_data
                    })
                    
        except Exception as e:
            self.warnings.append(f"Table extraction error on page {page_num}: {str(e)}")
        
        return tables
    
    def _parse_table_lines(self, lines: List[str]) -> Optional[List[Dict]]:
        """Parse lines into table rows."""
        try:
            parsed_rows = []
            for line in lines:
                # Split by multiple spaces or tabs
                cells = re.split(r'\s{2,}|\t', line)
                cells = [c.strip() for c in cells if c.strip()]
                
                if cells:
                    # Try to identify which cells are numeric
                    row = {}
                    numeric_count = 0
                    for i, cell in enumerate(cells):
                        # Clean and check for numeric value
                        clean_val = re.sub(r'[₹$,()]', '', cell)
                        try:
                            num_val = float(clean_val.replace('(', '-').replace(')', ''))
                            row[f'col_{i}'] = num_val
                            numeric_count += 1
                        except ValueError:
                            row[f'col_{i}'] = cell
                    
                    # Only include rows with at least one numeric value
                    if numeric_count > 0:
                        parsed_rows.append(row)
            
            return parsed_rows if len(parsed_rows) >= 2 else None
            
        except Exception:
            return None
    
    def _identify_sections(self, text: str) -> Dict[str, str]:
        """Identify financial statement sections in the text."""
        sections = {}
        text_lower = text.lower()
        
        for section_type, patterns in self.SECTION_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    # Extract text around the match
                    start = max(0, match.start() - 100)
                    end = min(len(text), match.end() + 2000)
                    sections[section_type] = text[start:end]
                    break
        
        return sections
    
    def _extract_key_figures(self, text: str) -> Dict[str, float]:
        """Extract key financial figures from text."""
        key_figures = {}
        
        # Patterns for common financial metrics
        patterns = {
            'total_revenue': [
                r'total\s*(?:revenue|sales|income)[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)',
                r'(?:revenue|sales)\s*from\s*operations[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)'
            ],
            'total_expenses': [
                r'total\s*(?:expenses?|expenditure)[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)'
            ],
            'net_profit': [
                r'(?:net\s*)?profit\s*(?:after\s*tax|for\s*the\s*(?:year|period))?[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)',
                r'net\s*income[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)'
            ],
            'total_assets': [
                r'total\s*assets?[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)'
            ],
            'total_liabilities': [
                r'total\s*liabilities?[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)'
            ],
            'shareholders_equity': [
                r'(?:total\s*)?(?:shareholders?|owners?)[\'\s]*equity[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)',
                r'net\s*worth[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)'
            ],
            'cash_balance': [
                r'cash\s*(?:and\s*cash\s*equivalents?|balance)[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+(?:\.\d+)?)'
            ]
        }
        
        text_lower = text.lower()
        
        for metric, patterns_list in patterns.items():
            for pattern in patterns_list:
                match = re.search(pattern, text_lower)
                if match:
                    try:
                        value = match.group(1).replace(',', '')
                        key_figures[metric] = float(value)
                        break
                    except (ValueError, IndexError):
                        continue
        
        return key_figures
    
    def extract_financial_data(self, data: Dict, metadata: Dict) -> Dict:
        """
        Structure extracted PDF data into financial format.
        
        Args:
            data: Raw extracted data
            metadata: Parsing metadata
        
        Returns:
            Structured financial data
        """
        financial_data = {
            'source': 'pdf',
            'pages': metadata.get('pages', 0),
            'key_figures': data.get('key_figures', {}),
            'sections': {},
            'tables': []
        }
        
        # Process identified sections
        for section_type, content in data.get('sections', {}).items():
            financial_data['sections'][section_type] = {
                'found': True,
                'preview': content[:500] if content else None
            }
        
        # Process tables
        for table in data.get('tables', []):
            if table.get('data'):
                financial_data['tables'].append({
                    'page': table.get('page'),
                    'row_count': len(table['data']),
                    'data': table['data']
                })
        
        return financial_data


# Create global instance
pdf_handler = PDFHandler()
