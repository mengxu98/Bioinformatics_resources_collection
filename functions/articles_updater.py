from .base_updater import BaseUpdater

class ArticlesUpdater(BaseUpdater):
    def __init__(self):
        """Initialize articles updater"""
        super().__init__('config/articles.yaml')
    
    def update_content(self, data=None):
        """
        Update articles.yaml file
        Args:
            data: Optional data to update with
        Returns:
            bool: Success status
        """
        try:
            # Load existing YAML data
            existing_data = self._load_yaml()
            
            # Create title to index mapping
            title_map = {item['title'].lower(): i for i, item in enumerate(existing_data)}
            
            # Check each entry
            for i, item in enumerate(existing_data):
                # Try to complete missing information
                if not item.get('citation') or not item.get('field'):
                    updated_info = self._get_paper_info(item['title'])
                    if updated_info:
                        # Only update missing fields
                        for key, value in updated_info.items():
                            if not item.get(key):
                                existing_data[i][key] = value

            # Save updated data
            self._save_yaml(existing_data)
            self.logger.info("Successfully updated articles.yaml")
            return True

        except Exception as e:
            self.logger.error(f"Error updating articles.yaml: {str(e)}")
            return False
