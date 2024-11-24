from abc import ABC, abstractmethod
import yaml
import logging
from semanticscholar import SemanticScholar
import time
import random

class BaseUpdater(ABC):
    def __init__(self, config_file):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)

    def _load_yaml(self):
        """Load data from yaml file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Error loading YAML file: {str(e)}")
            return None

    def update_content(self, data=None):
        """
        Update content in yaml file
        Args:
            data: Optional data to update with
        Returns:
            bool: Success status
        """
        try:
            self.logger.info("Starting articles update")
            
            # If no new data provided, just read existing data
            if data is None:
                yaml_data = self._load_yaml()
                if yaml_data is None:
                    return False
                return True
                
            # Update yaml file if new data provided
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
            self.logger.info(f"Successfully updated {self.config_file}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating YAML file: {str(e)}")
            self.logger.exception("Full traceback:")
            return False