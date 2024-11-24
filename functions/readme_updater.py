import os
from datetime import datetime
import logging
from typing import Dict, List, Optional
import yaml
import re
from .base_updater import BaseUpdater


class ReadmeUpdater(BaseUpdater):
    def __init__(self):
        """Initialize readme updater"""
        super().__init__('config/readme.yaml')
        self.readme_files = [
            'README.md',
            'website/content/_index.md'
        ]
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)

    def update_content(self, data=None):
        """
        Update readme files with content from articles and methods
        Args:
            data: Optional data to update with
        Returns:
            bool: Success status
        """
        try:
            # Get entries from articles and methods files
            articles_entries = self._get_entries_from_file('website/content/posts/articles.md')
            methods_entries = self._get_entries_from_file('website/content/posts/methods.md')

            # Update each readme file
            updated_files = []
            for readme_file in self.readme_files:
                success = self._update_readme_file(readme_file, articles_entries, methods_entries)
                if success:
                    updated_files.append(readme_file)

            # Log summary instead of individual file updates
            if updated_files:
                self.logger.info(f"Updated readme files: {', '.join(updated_files)}")
            else:
                self.logger.warning("No readme files were updated")
            
            return bool(updated_files)

        except Exception as e:
            self.logger.error(f"Error updating readme files: {str(e)}")
            return False

    def _get_entries_from_file(self, file_path):
        """
        Extract entries from markdown file
        Args:
            file_path: Path to markdown file
        Returns:
            list: List of valid entries
        """
        entries = {}
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                if '|' in line and '[' in line and ']' in line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        journal = parts[1].strip()
                        title = parts[3].strip()
                        title_match = re.search(r'\[(.*?)\]', title)
                        if title_match:
                            article_title = title_match.group(1)
                            key = f"{journal} - {article_title}"
                            
                            if key not in entries:
                                display_title = (
                                    f"{key[:77]}..." if len(key) > 80 else key
                                )
                                if not any(display_title.startswith(k[:77]) for k in entries.keys()):
                                    self.logger.info(f"Found article: {display_title}")
                                entries[key] = line.strip()
            
            return list(entries.values())
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {str(e)}")
            return []

    def _update_readme_file(self, file_path, articles_entries, methods_entries):
        """Update a readme file with content from articles and methods
        Args:
            file_path: Path to readme file
            articles_entries: List of article entries
            methods_entries: List of method entries
        """
        try:
            # Read current content
            with open(file_path, 'r') as f:
                content = f.read()

            # Find sections (support both ### [Articles] and ## Articles formats)
            articles_start = -1
            methods_start = -1
            
            # Try different possible section headers
            for header in ['### [Articles]', '## Articles', '### Articles']:
                pos = content.find(header)
                if pos != -1:
                    articles_start = pos
                    break
                
            for header in ['### [Methods]', '## Methods', '### Methods']:
                pos = content.find(header)
                if pos != -1:
                    methods_start = pos
                    break

            if articles_start == -1 or methods_start == -1:
                self.logger.warning(f"Could not find required sections in {file_path}, skipping update")
                return

            # Find next section after Articles
            next_section_start = content.find('\n###', articles_start + 1)
            if next_section_start == -1:
                next_section_start = len(content)

            # Create new content
            new_content = content[:articles_start] + content[articles_start:next_section_start]
            new_content += '\n'.join(articles_entries) + '\n\n'
            
            # Add content between Articles and Methods
            between_sections = content[next_section_start:methods_start]
            new_content += between_sections
            
            # Add Methods section content
            next_section_after_methods = content.find('\n###', methods_start + 1)
            if next_section_after_methods != -1:
                new_content += content[methods_start:next_section_after_methods] + '\n'
                new_content += '\n'.join(methods_entries) + '\n\n'
                new_content += content[next_section_after_methods:]
            else:
                new_content += content[methods_start:] + '\n'
                new_content += '\n'.join(methods_entries) + '\n'

            # Write updated content
            with open(file_path, 'w') as f:
                f.write(new_content)

            self.logger.info(f"Successfully updated {file_path}")

        except Exception as e:
            self.logger.error(f"Error updating {file_path}: {str(e)}")
            raise
