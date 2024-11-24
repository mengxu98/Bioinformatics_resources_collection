from abc import ABC, abstractmethod
import yaml
import logging
from semanticscholar import SemanticScholar
import time
import random

class BaseUpdater(ABC):
    def __init__(self, yaml_file):
        """Initialize the updater with yaml file path"""
        self.logger = logging.getLogger(__name__)
        self.sch = SemanticScholar()
        self.yaml_file = yaml_file
        
    def _load_yaml(self):
        """Load existing YAML file"""
        try:
            with open(self.yaml_file, 'r') as f:
                return yaml.safe_load(f) or []
        except FileNotFoundError:
            return []

    def _save_yaml(self, data):
        """Save data to YAML file"""
        with open(self.yaml_file, 'w') as f:
            yaml.dump(data, f, allow_unicode=True)

    def _get_paper_info(self, title):
        """
        Get paper information from Semantic Scholar API
        Args:
            title: Paper title to search for
        Returns:
            dict: Paper information or None if not found
        """
        try:
            # Add delay to avoid rate limiting
            time.sleep(random.uniform(1, 2))
            papers = self.sch.search_paper(title, limit=1)
            
            if not papers:
                return None

            paper = papers[0]
            paper_detail = self.sch.get_paper(paper.paperId)

            if not paper_detail:
                return None

            return {
                'title': str(paper_detail.title),
                'url': str(paper_detail.url),
                'date': str(paper_detail.year),
                'journal': str(paper_detail.venue),
                'field': str(paper_detail.fieldsOfStudy[0]) if paper_detail.fieldsOfStudy else '',
                'citation': f"https://api.semanticscholar.org/graph/v1/paper/{paper_detail.paperId}",
                'code': '',  # Keep empty for manual input
                'data': [],  # Keep empty for manual input
                'language': []  # Keep empty for manual input
            }

        except Exception as e:
            self.logger.error(f"Error getting info for paper {title}: {str(e)}")
            return None

    @abstractmethod
    def update_content(self, data=None):
        """
        Update the content file
        Args:
            data: Optional data to update with
        Returns:
            bool: Success status
        """
        pass