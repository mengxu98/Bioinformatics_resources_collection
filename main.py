import logging
import yaml
from functions.articles_updater import ArticlesUpdater
from functions.methods_updater import MethodsUpdater
from functions.books_updater import BooksUpdater
from functions.blogs_updater import BlogsUpdater
from functions.databases_updater import DatabasesUpdater
from functions.labs_updater import LabsUpdater
from functions.readme_updater import ReadmeUpdater

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_articles_data():
    """Get articles data from yaml file"""
    with open('config/articles.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    """Main function to update all files"""
    try:
        # Update articles
        logger.info("Updating articles.md...")
        articles_data = get_articles_data()
        articles_updater = ArticlesUpdater()
        if articles_updater.update_content(articles_data):
            logger.info("articles.md updated successfully")
        else:
            logger.error("Failed to update articles.md")
            return False

        # Update methods
        logger.info("Updating methods.md...")
        methods_updater = MethodsUpdater()
        if methods_updater.update_content():
            logger.info("methods.md updated successfully")
        else:
            logger.error("Failed to update methods.md")
            return False

        # Update books
        logger.info("Updating books.md...")
        books_updater = BooksUpdater()
        if books_updater.update_content():
            logger.info("books.md updated successfully")
        else:
            logger.error("Failed to update books.md")
            return False

        # Update blogs
        logger.info("Updating blogs.md...")
        blogs_updater = BlogsUpdater()
        if blogs_updater.update_content():
            logger.info("blogs.md updated successfully")
        else:
            logger.error("Failed to update blogs.md")
            return False

        # Update databases
        logger.info("Updating databases.md...")
        databases_updater = DatabasesUpdater()
        if databases_updater.update_content():
            logger.info("databases.md updated successfully")
        else:
            logger.error("Failed to update databases.md")
            return False

        # Update labs
        logger.info("Updating labs.md...")
        labs_updater = LabsUpdater()
        if labs_updater.update_content():
            logger.info("labs.md updated successfully")
        else:
            logger.error("Failed to update labs.md")
            return False

        # Update readme files
        logger.info("Updating readme files...")
        readme_updater = ReadmeUpdater()
        if readme_updater.update_content():
            logger.info("readme files updated successfully")
        else:
            logger.error("Failed to update readme files")
            return False

        return True

    except Exception as e:
        logger.error(f"Error during update: {str(e)}")
        logger.exception("Full traceback:")
        return False

if __name__ == '__main__':
    main()
