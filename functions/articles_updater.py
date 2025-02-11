from .base_updater import BaseUpdater
import yaml
import re


class ArticlesUpdater(BaseUpdater):
    def __init__(self):
        """Initialize articles updater"""
        super().__init__("config/articles.yaml")
        self.md_file = "website/content/posts/articles.md"

    def update_content(self, data=None):
        """
        Update content in both yaml and md files
        Args:
            data: Optional data to update yaml with
        Returns:
            bool: Success status
        """
        try:
            self.logger.info("Starting articles update")

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

            # Update MD file
            self.logger.info(f"Reading MD file: {self.md_file}")
            with open(self.md_file, "r", encoding="utf-8") as f:
                content = f.readlines()

            # Find table section
            table_start = None
            for i, line in enumerate(content):
                if line.startswith("| **Journal**"):
                    table_start = i
                    self.logger.debug(f"Found table start at line {i}")
                    break

            if table_start is None:
                self.logger.error("Could not find table in MD file")
                return False

            # Create new table content
            self.logger.info("Creating new table content")
            new_table = [
                "| **Journal** | **Date** | **Title** | **Code** | **Data** | **Citation** |\n",
                "| -- | -- | -- | -- | -- | -- |\n",
            ]

            # Group entries by field
            entries_by_field = {}
            for entry in yaml_data:
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

                    # Create entry line with all badges
                    code_badge = ""
                    if entry.get("code"):
                        lang = entry.get("language", "Code")
                        if isinstance(lang, list):
                            lang = " ".join(lang)
                        code_badge = f"[![{lang}](https://img.shields.io/badge/-{lang.replace(' ', '%20')}-444444)]({entry['code']})"

                    data_badges = []
                    if entry.get("data"):
                        for data in entry["data"]:
                            data_badges.append(
                                f"[![{data['type']}](https://img.shields.io/badge/-{data['type']}-B03060)]({data['url']})"
                            )

                    citation_id = entry["citation"].split("/")[-1]
                    citation_badge = f"[![citation](https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url=https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F{citation_id}%3Ffields%3DcitationCount)]({entry['citation']})"

                    line = f"| {entry['journal']} | {entry['date']} | [{entry['title']}]({entry['url']}) | {code_badge} | {' '.join(data_badges)} | {citation_badge} |\n"
                    new_table.append(line)

            # Replace old table with new one
            table_end = table_start
            while table_end < len(content) and content[table_end].startswith("|"):
                table_end += 1

            self.logger.info(
                f"Replacing table content from line {table_start} to {table_end}"
            )
            content[table_start:table_end] = new_table

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

    def _update_md_files(self, updates):
        """
        Update markdown files with the changes
        Args:
            updates: List of updated entries with their changes
        Returns:
            bool: Success status
        """
        try:
            md_file = "website/content/posts/articles.md"
            self.logger.info(f"Processing {md_file}")

            with open(md_file, "r", encoding="utf-8") as f:
                content = f.readlines()

            # Load yaml data
            with open(self.config_file, "r", encoding="utf-8") as f:
                yaml_data = yaml.safe_load(f)
            self.logger.info(f"Loaded {len(yaml_data)} entries from YAML")

            # Track existing entries
            existing_entries = set()
            table_start_index = None
            table_end_index = None

            # Find table boundaries and existing entries
            for i, line in enumerate(content):
                if "| **Journal**" in line:
                    table_start_index = i
                    self.logger.debug(f"Found table start at line {i}")
                elif table_start_index is not None and line.startswith("|"):
                    if "**`" in line:  # Category line
                        continue
                    parts = line.split("|")
                    if len(parts) >= 4:
                        title_part = parts[3].strip()
                        title_match = re.search(r"\[(.*?)\]", title_part)
                        if title_match:
                            title = title_match.group(1).strip()
                            existing_entries.add(title)
                            self.logger.debug(f"Found existing entry: {title}")
                elif table_start_index is not None and not line.startswith("|"):
                    table_end_index = i
                    self.logger.debug(f"Found table end at line {i}")
                    break

            self.logger.info(f"Found {len(existing_entries)} existing entries")

            # Add new entries
            new_entries = []
            current_category = None

            for entry in yaml_data:
                title = entry["title"].strip()
                if title not in existing_entries:
                    self.logger.info(f"Processing new entry: {title}")

                    # Determine category
                    category = entry.get("field", "Other")
                    if current_category != category:
                        current_category = category
                        new_entries.append(f"| **`{category}`** |  |  |  |  |  |\n")
                        self.logger.debug(f"Added category: {category}")

                    # Create entry line
                    code_badge = ""
                    if entry.get("code"):
                        lang = entry.get("language", "Code")
                        if isinstance(lang, list):
                            lang = " ".join(lang)
                        code_badge = f"[![{lang}](https://img.shields.io/badge/-{lang.replace(' ', '%20')}-444444)]({entry['code']})"

                    data_badges = []
                    if entry.get("data"):
                        for data in entry["data"]:
                            data_badges.append(
                                f"[![{data['type']}](https://img.shields.io/badge/-{data['type']}-B03060)]({data['url']})"
                            )

                    citation_badge = f"[![citation](https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url=https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F{entry['citation'].split('/')[-1]}%3Ffields%3DcitationCount)]({entry['citation']})"

                    new_line = f"| {entry['journal']} | {entry['date']} | [{entry['title']}]({entry['url']}) | {code_badge} | {' '.join(data_badges)} | {citation_badge} |\n"
                    new_entries.append(new_line)
                    self.logger.info(f"Created new entry line for: {title}")

            if new_entries:
                self.logger.info(f"Adding {len(new_entries)} new entries")
                # Insert new entries at the end of the table
                if table_end_index:
                    content[table_end_index:table_end_index] = new_entries
                else:
                    content.extend(new_entries)

                # Write back to file
                with open(md_file, "w", encoding="utf-8") as f:
                    f.writelines(content)
                self.logger.info(f"Successfully updated {md_file}")
            else:
                self.logger.info("No new entries to add")

            return True

        except Exception as e:
            self.logger.error(f"Error updating markdown files: {str(e)}")
            self.logger.exception("Full traceback:")
            return False
