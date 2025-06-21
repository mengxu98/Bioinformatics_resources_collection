#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Paper Information Extractor
Supports automatic extraction of complete paper information through various methods
including paper title, DOI, URL, etc., with code and data link extraction
"""

import re
import time
import logging
from typing import Dict, List, Optional, Tuple
from semanticscholar import SemanticScholar
import requests
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SmartPaperExtractor:
    """Smart Paper Information Extractor"""
    
    def __init__(self):
        """Initialize extractor"""
        self.sch = SemanticScholar()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Limit request frequency to avoid API limits
        self.request_delay = 1  # seconds
        
        # Code hosting platform patterns
        self.code_patterns = [
            r'https?://github\.com/[\w\-\.]+/[\w\-\.]+/?(?:\.git)?',
            r'https?://gitlab\.com/[\w\-\.]+/[\w\-\.]+/?',
            r'https?://bitbucket\.org/[\w\-\.]+/[\w\-\.]+/?',
            r'https?://code\.google\.com/p/[\w\-\.]+/?',
            r'https?://sourceforge\.net/projects/[\w\-\.]+/?'
        ]
        
        # Data-related keywords and patterns
        self.data_keywords = [
            'dataset', 'database', 'data availability', 'supplementary data',
            'gene expression omnibus', 'geo', 'ncbi', 'zenodo', 'figshare',
            'dryad', 'european nucleotide archive', 'ena', 'sequence read archive', 'sra'
        ]
        
        self.data_patterns = [
            r'https?://www\.ncbi\.nlm\.nih\.gov/geo/query/acc\.cgi\?acc=GSE\d+',
            r'https?://www\.ncbi\.nlm\.nih\.gov/sra/[\w\d]+',
            r'https?://zenodo\.org/record/\d+',
            r'https?://figshare\.com/[\w/\d]+',
            r'https?://datadryad\.org/stash/dataset/doi:[\w\./\-]+',
            r'https?://www\.ebi\.ac\.uk/ena/browser/view/[\w\d]+',
            r'GSE\d+',
            r'SRA\d+',
            r'PRJNA\d+',
            r'E-MTAB-\d+'
        ]
    
    def extract_paper_info(self, input_text: str) -> Dict:
        """
        Extract paper information from input text
        
        Args:
            input_text: Can be paper title, DOI, Semantic Scholar URL, etc.
            
        Returns:
            Dictionary containing paper information
        """
        try:
            input_text = input_text.strip()
            
            # 1. Check if it's a Semantic Scholar URL
            if 'semanticscholar.org' in input_text:
                return self._extract_from_semanticscholar_url(input_text)
            
            # 2. Check if it's a DOI
            doi_pattern = r'10\.\d+/[^\s]+'
            if re.search(doi_pattern, input_text):
                doi = re.search(doi_pattern, input_text).group()
                return self._extract_from_doi(doi)
            
            # 3. Search as paper title
            return self._search_by_title(input_text)
            
        except Exception as e:
            logger.error(f"Failed to extract paper information: {str(e)}")
            return {
                'success': False,
                'error': f'Information extraction failed: {str(e)}',
                'data': {}
            }
    
    def _search_by_title(self, title: str) -> Dict:
        """Search paper by title"""
        try:
            logger.info(f"Searching paper by title: {title}")
            
            results = self.sch.search_paper(title, limit=5)
            
            if not results:
                return {
                    'success': False,
                    'error': 'No matching papers found',
                    'data': {}
                }
            
            # Select the best matching result
            best_match = self._find_best_match(title, results)
            
            if best_match:
                return self._extract_paper_details(best_match)
            else:
                return {
                    'success': False,
                    'error': 'No papers with sufficient match found',
                    'data': {},
                    'suggestions': [self._format_paper_basic(paper) for paper in results[:3]]
                }
                
        except Exception as e:
            logger.error(f"Title search failed: {str(e)}")
            return {
                'success': False,
                'error': f'Search failed: {str(e)}',
                'data': {}
            }
    
    def _find_best_match(self, query_title: str, results: List) -> Optional:
        """Find the best matching paper"""
        query_title_clean = self._clean_title(query_title)
        best_score = 0
        best_match = None
        
        for paper in results:
            if not paper.title:
                continue
                
            paper_title_clean = self._clean_title(paper.title)
            score = self._calculate_similarity(query_title_clean, paper_title_clean)
            
            if score > best_score:
                best_score = score
                best_match = paper
        
        return best_match if best_score > 0.5 else None
    
    def _clean_title(self, title: str) -> str:
        """Clean title for matching"""
        title = re.sub(r'[^\w\s]', ' ', title.lower())
        title = ' '.join(title.split())
        return title
    
    def _calculate_similarity(self, title1: str, title2: str) -> float:
        """Calculate similarity between two titles"""
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _extract_from_doi(self, doi: str) -> Dict:
        """Extract paper information from DOI"""
        try:
            logger.info(f"Extracting paper information from DOI: {doi}")
            
            if doi.startswith('https://doi.org/'):
                doi = doi.replace('https://doi.org/', '')
            
            paper = self.sch.get_paper(doi)
            if paper:
                return self._extract_paper_details(paper)
            else:
                return {
                    'success': False,
                    'error': 'No corresponding paper found',
                    'data': {}
                }
                
        except Exception as e:
            logger.error(f"DOI extraction failed: {str(e)}")
            return {
                'success': False,
                'error': f'DOI extraction failed: {str(e)}',
                'data': {}
            }
    
    def _extract_from_semanticscholar_url(self, url: str) -> Dict:
        """Extract paper information from Semantic Scholar URL"""
        try:
            logger.info(f"Extracting paper information from Semantic Scholar URL: {url}")
            
            paper_id_match = re.search(r'/paper/([a-f0-9]+)', url)
            if not paper_id_match:
                return {
                    'success': False,
                    'error': 'Invalid Semantic Scholar URL',
                    'data': {}
                }
            
            paper_id = paper_id_match.group(1)
            paper = self.sch.get_paper(paper_id)
            
            if paper:
                return self._extract_paper_details(paper)
            else:
                return {
                    'success': False,
                    'error': 'Unable to retrieve paper information',
                    'data': {}
                }
                
        except Exception as e:
            logger.error(f"Semantic Scholar URL extraction failed: {str(e)}")
            return {
                'success': False,
                'error': f'URL extraction failed: {str(e)}',
                'data': {}
            }
    
    def _extract_paper_details(self, paper) -> Dict:
        """Extract detailed paper information"""
        try:
            data = {
                'title': paper.title or '',
                'journal': paper.venue or '',
                'year': str(paper.year) if paper.year else '',
                'doi': paper.externalIds.get('DOI', '') if paper.externalIds else '',
                'paper_id': paper.paperId or '',
                'abstract': paper.abstract or '',
                'citation_count': paper.citationCount or 0,
                'field': '',
                'language': 'Python',  # Default language
                'code': '',
                'data': []
            }
            
            # Build URLs
            if data['doi']:
                data['url'] = f"https://doi.org/{data['doi']}"
            else:
                data['url'] = f"https://www.semanticscholar.org/paper/{data['paper_id']}"
            
            data['citation'] = f"https://api.semanticscholar.org/graph/v1/paper/{data['paper_id']}?fields=citationCount"
            
            # Extract field information
            if hasattr(paper, 'fieldsOfStudy') and paper.fieldsOfStudy:
                fields = [field for field in paper.fieldsOfStudy if field]
                if fields:
                    data['field'] = ', '.join(fields[:2])
            
            # Extract author information
            authors = []
            if hasattr(paper, 'authors') and paper.authors:
                for author in paper.authors[:3]:
                    if hasattr(author, 'name') and author.name:
                        authors.append(author.name)
            data['authors'] = authors
            
            # Extract code and data links
            code_links, data_links = self._extract_links_from_paper(paper)
            if code_links:
                data['code'] = code_links[0]  # Take the first code link
            data['data'] = data_links
            
            # If no code link found, try to get it through other methods
            if not data['code']:
                additional_code_link = self._search_github_by_paper_info(data)
                if additional_code_link:
                    data['code'] = additional_code_link
            
            return {
                'success': True,
                'error': '',
                'data': data
            }
            
        except Exception as e:
            logger.error(f"Failed to extract detailed paper information: {str(e)}")
            return {
                'success': False,
                'error': f'Information extraction failed: {str(e)}',
                'data': {}
            }
    
    def _extract_links_from_paper(self, paper) -> Tuple[List[str], List[str]]:
        """Extract code and data links from paper"""
        code_links = []
        data_links = []
        
        # Collect all text sources that might contain links
        text_sources = []
        
        if hasattr(paper, 'abstract') and paper.abstract:
            text_sources.append(paper.abstract)
        
        if hasattr(paper, 'openAccessPdf') and paper.openAccessPdf:
            if hasattr(paper.openAccessPdf, 'url'):
                # Could try to extract links from PDF, but skip for now
                pass
        
        # Search from external IDs
        if hasattr(paper, 'externalIds') and paper.externalIds:
            for key, value in paper.externalIds.items():
                if key.lower() in ['arxiv', 'pubmed']:
                    # Could search further based on these IDs
                    pass
        
        # Extract links from all text sources
        for text in text_sources:
            if not text:
                continue
                
            # Extract code links
            for pattern in self.code_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    clean_link = self._clean_link(match)
                    if clean_link and clean_link not in code_links:
                        code_links.append(clean_link)
            
            # Extract data links
            for pattern in self.data_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    clean_link = self._format_data_link(match)
                    if clean_link and clean_link not in data_links:
                        data_links.append(clean_link)
        
        return code_links, data_links
    
    def _clean_link(self, link: str) -> str:
        """Clean and standardize links"""
        link = link.strip()
        
        # Remove trailing slashes and .git
        link = re.sub(r'(\.git)?/?$', '', link)
        
        # Ensure it's a valid URL
        if not link.startswith(('http://', 'https://')):
            return ''
        
        return link
    
    def _format_data_link(self, match: str) -> str:
        """Format data links"""
        match = match.strip()
        
        # If it's a complete URL, return directly
        if match.startswith(('http://', 'https://')):
            return match
        
        # Format common database IDs
        if match.startswith('GSE'):
            return f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={match}"
        elif match.startswith('SRA'):
            return f"https://www.ncbi.nlm.nih.gov/sra/{match}"
        elif match.startswith('PRJNA'):
            return f"https://www.ncbi.nlm.nih.gov/bioproject/{match}"
        elif match.startswith('E-MTAB-'):
            return f"https://www.ebi.ac.uk/arrayexpress/experiments/{match}"
        
        return match
    
    def _search_github_by_paper_info(self, paper_data: Dict) -> Optional[str]:
        """Search for related code repositories on GitHub using paper information"""
        try:
            # Multiple search strategies
            search_strategies = []
            
            # Strategy 1: Use key tool names from title
            if paper_data.get('title'):
                title = paper_data['title']
                # Extract possible tool names (usually uppercase or special format)
                tool_names = re.findall(r'\b[A-Z][a-zA-Z]*[A-Z][a-zA-Z]*\b', title)  # CamelCase
                tool_names.extend(re.findall(r'\b[A-Z]{2,}\b', title))  # All uppercase
                tool_names.extend(re.findall(r'\b\w*[A-Z]+\w*\b', title))  # Contains uppercase letters
                
                for tool_name in tool_names:
                    if len(tool_name) > 2:
                        search_strategies.append(tool_name)
            
            # Strategy 2: Author name + keywords
            if paper_data.get('authors'):
                first_author = paper_data['authors'][0]
                if ' ' in first_author:
                    last_name = first_author.split()[-1]
                    if paper_data.get('title'):
                        # Extract bioinformatics keywords from title
                        bio_keywords = ['scrna', 'seq', 'single', 'cell', 'rna', 'gene', 'network']
                        title_lower = paper_data['title'].lower()
                        for keyword in bio_keywords:
                            if keyword in title_lower:
                                search_strategies.append(f"{last_name} {keyword}")
                                break
            
            # Strategy 3: Journal + tool name
            if paper_data.get('journal') and tool_names:
                journal = paper_data['journal'].split()[0]  # Take first word of journal name
                search_strategies.append(f"{journal} {tool_names[0]}")
            
            # Try various search strategies
            for strategy in search_strategies:
                logger.info(f"GitHub search strategy: {strategy}")
                github_url = self._search_github_with_query(strategy)
                if github_url:
                    return github_url
                    
                # Add delay to avoid API limits
                time.sleep(0.5)
            
        except Exception as e:
            logger.warning(f"GitHub search failed: {str(e)}")
        
        return None
    
    def _search_github_with_query(self, query: str) -> Optional[str]:
        """Search on GitHub using specific query"""
        try:
            api_url = f"https://api.github.com/search/repositories"
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 3
            }
            
            response = self.session.get(api_url, params=params, timeout=10)
            if response.status_code == 200:
                results = response.json()
                if results.get('items'):
                    # Check if repository is relevant
                    for repo in results['items']:
                        if self._is_relevant_repo(repo, query):
                            return repo['html_url']
            
        except Exception as e:
            logger.warning(f"GitHub query failed: {str(e)}")
        
        return None
    
    def _is_relevant_repo(self, repo: dict, query: str) -> bool:
        """Determine if repository is relevant to the query"""
        query_lower = query.lower()
        
        # Check repository name
        if repo.get('name') and query_lower in repo['name'].lower():
            return True
        
        # Check description
        if repo.get('description') and query_lower in repo['description'].lower():
            return True
        
        # Check primary language
        if repo.get('language') and repo['language'].lower() in ['python', 'r', 'javascript']:
            return True
        
        # Check if repository has bioinformatics-related topics
        bio_topics = ['bioinformatics', 'computational-biology', 'single-cell', 'rna-seq', 'genomics']
        if repo.get('topics'):
            for topic in repo['topics']:
                if topic in bio_topics:
                    return True
        
        return False
    
    def _format_paper_basic(self, paper) -> Dict:
        """Format basic paper information for suggestions list"""
        return {
            'title': paper.title or '',
            'authors': [author.name for author in (paper.authors or [])[:3] if hasattr(author, 'name')],
            'year': paper.year,
            'venue': paper.venue or '',
            'paper_id': paper.paperId or ''
        }