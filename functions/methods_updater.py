from .base_updater import BaseUpdater
import yaml


class MethodsUpdater(BaseUpdater):
    def __init__(self):
        """Initialize methods updater"""
        super().__init__("config/methods.yaml")
        self.md_file = "website/content/posts/methods.md"

    def update_content(self, data=None):
        """
        Update content in both yaml and md files
        Args:
            data: Optional data to update yaml with
        Returns:
            bool: Success status
        """
        try:
            self.logger.info("Starting methods update")

            # If no new data provided, just read existing data
            if data is None:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    yaml_data = yaml.safe_load(f)
            else:
                # Update yaml file if new data provided
                with open(self.config_file, "w", encoding="utf-8") as f:
                    yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
                yaml_data = data

            self.logger.info(f"Loaded {len(yaml_data)} entries from YAML")

            # Validate entries
            valid_entries = []
            for entry in yaml_data:
                if not isinstance(entry, dict):
                    self.logger.warning(f"Skipping invalid entry: {entry}")
                    continue

                # Check required fields
                if "title" not in entry:
                    self.logger.warning(f"Skipping entry without title: {entry}")
                    continue

                valid_entries.append(entry)

            self.logger.info(f"Found {len(valid_entries)} valid entries")

            # Create or update MD file
            try:
                with open(self.md_file, "r", encoding="utf-8") as f:
                    content = f.readlines()
                self.logger.info(f"Reading existing MD file: {self.md_file}")
            except FileNotFoundError:
                # Create new file with default content
                content = [
                    "---\n",
                    'title: "Methods"\n',
                    'author: "Mengxu"\n',
                    "date: 2024-11-23\n",
                    "---\n",
                    "<!--more-->\n",
                ]
                self.logger.info(f"Creating new MD file: {self.md_file}")

            # Find table section
            table_start = None
            for i, line in enumerate(content):
                if line.startswith("| **Journal**"):
                    table_start = i
                    self.logger.debug(f"Found table start at line {i}")
                    break

            # Create new table content
            self.logger.info("Creating new table content")
            new_table = [
                "| **Journal** | **Date** | **Title** | **Code** | **Data** | **Citation** |\n",
                "| -- | -- | -- | -- | -- | -- |\n",
            ]

            # Group entries by field
            entries_by_field = {}
            for entry in valid_entries:
                field = entry.get("field", "Other")
                if field not in entries_by_field:
                    entries_by_field[field] = []
                entries_by_field[field].append(entry)

            self.logger.info(f"Found {len(entries_by_field)} fields")

            # Add entries by field
            for field in sorted(entries_by_field.keys()):
                self.logger.debug(f"Processing field: {field}")
                new_table.append(f"| **`{field}`** |  |  |  |  |  |\n")
                for entry in sorted(entries_by_field[field], key=lambda x: x["title"]):
                    self.logger.debug(f"Processing entry: {entry['title']}")

                    # Create code badge
                    code_badge = ""
                    if entry.get("code"):
                        lang = entry.get("language", "Code")
                        if isinstance(lang, list):
                            lang = " ".join(lang)
                        # Use language-specific colors
                        color_map = {
                            "Python": "3572a5",
                            "R": "198ce7", 
                            "Java": "b0721a",
                            "JavaScript": "f1e05a",
                            "MATLAB": "e16737",
                            "R Python": "444444"
                        }
                        color = color_map.get(lang, "444444")
                        code_badge = f"[![{lang}](https://img.shields.io/badge/-{lang.replace(' ', '%20')}-{color})]({entry['code']})"

                    # Create data badges
                    data_badges = []
                    if entry.get("data") and isinstance(entry["data"], list):
                        for data_item in entry["data"]:
                            if isinstance(data_item, dict) and "type" in data_item and "url" in data_item:
                                # Use different colors for different data types
                                data_color_map = {
                                    "GEO": "336699",
                                    "Website": "B03060",
                                    "Github": "336699",
                                    "Zenodo": "336699",
                                    "UK Biobank": "336699",
                                    "ADNI": "336699"
                                }
                                data_color = data_color_map.get(data_item["type"], "336699")
                                data_badges.append(
                                    f"[![{data_item['type']}](https://img.shields.io/badge/-{data_item['type'].replace(' ', '%20')}-{data_color})]({data_item['url']})"
                                )

                    # Create citation badge
                    citation_badge = ""
                    if entry.get("citation"):
                        citation_id = entry["citation"].split("/")[-1].split("?")[0]  # Remove query parameters
                        citation_badge = f"[![citation](https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url=https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F{citation_id}%3Ffields%3DcitationCount)]({entry['citation']})"

                    # Create the table row
                    journal = entry.get("journal", "")
                    date = entry.get("date", "")
                    title = entry.get("title", "")
                    url = entry.get("url", "")
                    
                    title_link = f"[{title}]({url})" if url else title
                    
                    line = f"| {journal} | {date} | {title_link} | {code_badge} | {' '.join(data_badges)} | {citation_badge} |\n"
                    new_table.append(line)

            # Replace or append table
            if table_start is not None:
                # Find table end
                table_end = table_start
                while table_end < len(content) and content[table_end].startswith("|"):
                    table_end += 1

                self.logger.info(
                    f"Replacing table content from line {table_start} to {table_end}"
                )
                content[table_start:table_end] = new_table
            else:
                # Append table to end of file
                self.logger.info("Appending new table to end of file")
                if content and not content[-1].endswith("\n"):
                    content.append("\n")
                content.extend(new_table)

            # Write back to file
            self.logger.info(f"Writing updated content to {self.md_file}")
            with open(self.md_file, "w", encoding="utf-8") as f:
                f.writelines(content)

            self.logger.info(f"Successfully updated {self.md_file}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating content: {str(e)}")
            self.logger.exception("Full traceback:")
            return False
