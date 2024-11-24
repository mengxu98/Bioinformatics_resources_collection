import logging
from functions.books_updater import BooksUpdater
from functions.blogs_updater import BlogsUpdater
from functions.databases_updater import DatabasesUpdater
from functions.labs_updater import LabsUpdater
from functions.readme_updater import ReadmeUpdater
from functions.articles_updater import ArticlesUpdater
from functions.methods_updater import MethodsUpdater
import yaml
import os


def setup_logging():
    """Configure logging settings"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def main():
    """Main function to update all resource files"""
    logger = logging.getLogger(__name__)

    try:
        yaml_path = os.path.join("config", "articles.yaml")
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                articles_data = yaml.safe_load(f) or []
        except Exception as e:
            logger.error(f"Error reading articles.yaml: {str(e)}")
            articles_data = []

        updaters = [
            ("articles.md", ArticlesUpdater(), "update_content", articles_data),
            ("methods.md", MethodsUpdater(), "update_content"),
            ("books.md", BooksUpdater(), "update_books"),
            ("blogs.md", BlogsUpdater(), "update_blogs"),
            ("databases.md", DatabasesUpdater(), "update_databases"),
            ("labs.md", LabsUpdater(), "update_labs"),
            ("readme files", ReadmeUpdater(), "update_content"),
        ]

        for update_info in updaters:
            name = update_info[0]
            updater = update_info[1]
            method_name = update_info[2]
            logger.info(f"Updating {name}...")
            
            if isinstance(updater, ArticlesUpdater):
                getattr(updater, method_name)(articles_data)
            else:
                getattr(updater, method_name)()
                
            logger.info(f"{name} updated successfully")

    except Exception as e:
        logger.error(f"Error during update: {str(e)}")
        raise


if __name__ == "__main__":
    setup_logging()
    main()
