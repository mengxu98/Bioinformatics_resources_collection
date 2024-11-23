import logging
from functions.books_updater import BooksUpdater
from functions.blogs_updater import BlogsUpdater
from functions.databases_updater import DatabasesUpdater
from functions.labs_updater import LabsUpdater
from functions.readme_updater import ReadmeUpdater
from functions.articles_updater import ArticlesUpdater
from functions.methods_updater import MethodsUpdater


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
        updaters = [
            ("articles.md", ArticlesUpdater(), "update_articles"),
            ("methods.md", MethodsUpdater(), "update_methods"),
            ("books.md", BooksUpdater(), "update_books"),
            ("blogs.md", BlogsUpdater(), "update_blogs"),
            ("databases.md", DatabasesUpdater(), "update_databases"),
            ("labs.md", LabsUpdater(), "update_labs"),
            ("readme files", ReadmeUpdater(), "update_readme"),
        ]

        for name, updater, method_name in updaters:
            logger.info(f"Updating {name}...")
            update_method = getattr(updater, method_name)
            update_method()
            logger.info(f"{name} updated successfully")

    except Exception as e:
        logger.error(f"Error during update: {str(e)}")
        raise


if __name__ == "__main__":
    setup_logging()
    main()
