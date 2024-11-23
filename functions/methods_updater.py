import os
import logging
import yaml
from datetime import datetime
from itertools import groupby
from .extract_information import extract_paper_infor
import urllib.parse
from .badge_formatter import BadgeFormatter

class MethodsUpdater:
    """Handler for updating methods.md"""
    def __init__(self, config_dir="config", content_dir="website/content/posts"):
        self.config_dir = config_dir
        self.content_dir = content_dir
        self.yaml_path = os.path.join(config_dir, "methods.yaml")
        self.md_path = os.path.join(content_dir, "methods.md")
        self.logger = logging.getLogger(__name__)

    def update_methods(self):
        """Main method to update methods.md file"""
        try:
            # Read existing methods
            methods_data = self._read_methods_yaml()
            
            # Complete missing information
            for method in methods_data:
                if self._needs_info_update(method):
                    self._complete_method_info(method)
            
            # Update yaml with completed information
            self._write_methods_yaml(methods_data)
            
            # Generate markdown
            grouped_methods = self._group_methods_by_field(methods_data)
            md_content = self._generate_methods_md(grouped_methods)
            self._write_methods_md(md_content)
            
        except Exception as e:
            self.logger.error(f"Error updating methods: {str(e)}")
            raise

    def _needs_info_update(self, method):
        """Check if method needs information update"""
        required_fields = ['journal', 'date', 'title', 'url']
        optional_fields = ['code', 'language', 'data', 'citation']
        
        # Check if any required field is missing
        if not all(field in method and method[field] for field in required_fields):
            return True
            
        # Check if any optional field that should be available is missing
        if method.get('code') and not method.get('language'):
            return True
            
        return False

    def _complete_method_info(self, method):
        """Complete missing information for a method"""
        try:
            if not method.get('url'):
                self.logger.warning(f"No URL provided for method: {method.get('title', 'Unknown')}")
                return

            # Create temporary file for extraction
            temp_file = "temp_method.md"
            extract_paper_infor(
                url_paper=method['url'],
                doi_paper=[''],
                code_language=method.get('code_language', []),
                url_code=[method.get('code', '')],
                data_database=[d.get('type', '') for d in method.get('data', [])],
                url_data=[d.get('url', '') for d in method.get('data', [])],
                file=temp_file
            )

            # Read and parse extracted information
            if os.path.exists(temp_file):
                with open(temp_file, 'r') as f:
                    content = f.read()
                os.remove(temp_file)
                
                # Update only missing information
                if not method.get('title'):
                    method['title'] = self._extract_between(content, "Title: ", "\n")
                if not method.get('date'):
                    method['date'] = self._extract_between(content, "Published date: ", "\n")
                if not method.get('journal'):
                    method['journal'] = self._extract_between(content, "Journal: ", "\n")
                
                # Handle code information
                if not method.get('code') or not method.get('language'):
                    code_info = self._extract_between(content, "The code provided by ", "...")
                    if code_info:
                        code_parts = code_info.split(", and from ")
                        if not method.get('language'):
                            method['language'] = code_parts[0] if len(code_parts) > 0 else ""
                        if not method.get('code'):
                            method['code'] = code_parts[1] if len(code_parts) > 1 else ""
                
                # Handle data information
                if not method.get('data'):
                    data_info = self._extract_between(content, "The dataset provided by ", "...")
                    if data_info:
                        data_parts = data_info.split(", and from ")
                        if len(data_parts) > 1:
                            method['data'] = [{
                                'type': data_parts[0],
                                'url': data_parts[1]
                            }]
                
        except Exception as e:
            self.logger.error(f"Error completing info for method {method.get('url')}: {str(e)}")

    def _extract_between(self, text, start, end):
        """Helper function to extract text between two markers"""
        try:
            s = text.index(start) + len(start)
            e = text.index(end, s)
            return text[s:e].strip()
        except:
            return ""

    def _read_methods_yaml(self):
        """Read methods from yaml file"""
        try:
            if os.path.exists(self.yaml_path):
                with open(self.yaml_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or []
            return []
        except Exception as e:
            self.logger.error(f"Error reading methods yaml: {str(e)}")
            return []

    def _write_methods_yaml(self, methods_data):
        """Write updated methods back to yaml"""
        try:
            os.makedirs(os.path.dirname(self.yaml_path), exist_ok=True)
            with open(self.yaml_path, 'w', encoding='utf-8') as f:
                yaml.dump(methods_data, f, default_flow_style=False)
        except Exception as e:
            self.logger.error(f"Error writing methods yaml: {str(e)}")

    def _group_methods_by_field(self, methods):
        """Group methods by their field"""
        if not methods:
            return {}
        sorted_methods = sorted(methods, key=lambda x: (x['field'].lower(), x['date'], x['title']))
        return {k: list(g) for k, g in groupby(sorted_methods, key=lambda x: x['field'])}

    def _generate_methods_md(self, grouped_methods):
        """Generate content for methods.md with fields as sections"""
        current_time = datetime.now().strftime('%Y-%m-%d')
        header = f"""---
title: "Methods"
author: "Mengxu"
date: {current_time}
---
<!--more-->
| **Journal** | **Date** | **Title** | **Code** | **Data** | **Citation** |
| -- | -- | -- | -- | -- | -- |"""
        
        content = [header]
        
        for field, methods in grouped_methods.items():
            content.append(f"| **`{field}`** |  |  |  |  |  |")
            
            for method in methods:
                # Format all badges using BadgeFormatter
                code_badges = BadgeFormatter.format_code_badges(method)
                data_badges = BadgeFormatter.format_data_badges(method.get('data'))
                citation_badge = BadgeFormatter.format_citation_badge(method.get('citation'))
                
                row = (f"| {method['journal']} | {method['date']} | "
                      f"[{method['title']}]({method['url']}) | "
                      f"{code_badges} | {data_badges} | {citation_badge} |")
                
                content.append(row)
        
        return '\n'.join(content)

    def _write_methods_md(self, content):
        """Write content to methods.md file"""
        try:
            os.makedirs(os.path.dirname(self.md_path), exist_ok=True)
            with open(self.md_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            self.logger.error(f"Error writing methods md: {str(e)}")
            raise 