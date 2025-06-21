#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Admin Interface for Bioinformatics Resources Collection
Provides a visual way to add new resource entries without affecting existing deployment processes
"""

import os
import sys
import yaml
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename

# Add project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from functions.smart_paper_extractor import SmartPaperExtractor
from functions.articles_updater import ArticlesUpdater
from functions.methods_updater import MethodsUpdater
from functions.books_updater import BooksUpdater
from functions.blogs_updater import BlogsUpdater
from functions.databases_updater import DatabasesUpdater
from functions.labs_updater import LabsUpdater
from functions.readme_updater import ReadmeUpdater
from i18n.translations import get_translation, get_all_translations

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Please use a more secure key in production

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global template variables
@app.context_processor
def inject_globals():
    """Inject global template variables"""
    lang = request.cookies.get('language', 'zh')
    theme = request.cookies.get('theme', 'auto')
    return {
        'lang': lang,
        'theme': theme,
        't': lambda key: get_translation(key, lang),
        'translations': get_all_translations(lang)
    }

# Configuration file paths
CONFIG_FILES = {
    'articles': 'config/articles.yaml',
    'methods': 'config/methods.yaml',
    'books': 'config/books.yaml',
    'blogs': 'config/blogs.yaml',
    'databases': 'config/databases.yaml',
    'labs': 'config/labs.yaml'
}

# Updater mapping
UPDATERS = {
    'articles': ArticlesUpdater,
    'methods': MethodsUpdater,
    'books': BooksUpdater,
    'blogs': BlogsUpdater,
    'databases': DatabasesUpdater,
    'labs': LabsUpdater
}


def load_yaml_file(category):
    """Load YAML file for specified category"""
    try:
        file_path = CONFIG_FILES.get(category)
        if not file_path or not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or []
        return data
    except Exception as e:
        logger.error(f"Failed to load {category} configuration file: {str(e)}")
        return []


def save_yaml_file(category, data):
    """Save data to specified category YAML file"""
    try:
        file_path = CONFIG_FILES.get(category)
        if not file_path:
            return False
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, 
                          default_flow_style=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"Failed to save {category} configuration file: {str(e)}")
        return False


def update_markdown_files(category=None):
    """Update Markdown files"""
    try:
        if category and category in UPDATERS:
            # Update specific category
            updater_class = UPDATERS[category]
            updater = updater_class()
            success = updater.update_content()
            logger.info(f"{category} update {'successful' if success else 'failed'}")
            return success
        else:
            # Update all categories
            all_success = True
            for cat, updater_class in UPDATERS.items():
                updater = updater_class()
                success = updater.update_content()
                logger.info(f"{cat} update {'successful' if success else 'failed'}")
                if not success:
                    all_success = False
            
            # Update README file
            readme_updater = ReadmeUpdater()
            readme_success = readme_updater.update_content()
            logger.info(f"README update {'successful' if readme_success else 'failed'}")
            
            return all_success and readme_success
    except Exception as e:
        logger.error(f"Failed to update Markdown files: {str(e)}")
        return False


@app.route('/')
def index():
    """Homepage - Display statistics for all categories"""
    stats = {}
    for category in CONFIG_FILES.keys():
        data = load_yaml_file(category)
        stats[category] = len(data)
    
    return render_template('index.html', stats=stats)


@app.route('/category/<category>')
def view_category(category):
    """View all entries in a specific category"""
    if category not in CONFIG_FILES:
        flash(f'Unknown category: {category}', 'error')
        return redirect(url_for('index'))
    
    data = load_yaml_file(category)
    return render_template('category.html', category=category, data=data)


@app.route('/add/<category>')
def add_form(category):
    """Display form for adding new entry"""
    if category not in CONFIG_FILES:
        flash(f'Unknown category: {category}', 'error')
        return redirect(url_for('index'))
    
    # Get existing data to understand field structure
    existing_data = load_yaml_file(category)
    sample_entry = existing_data[0] if existing_data else {}
    
    return render_template('add_form.html', category=category, sample_entry=sample_entry)


@app.route('/api/extract_paper_info', methods=['POST'])
def extract_paper_info():
    """API interface for intelligent paper information extraction"""
    try:
        data = request.get_json()
        input_text = data.get('input_text', '')
        
        if not input_text:
            return jsonify({'success': False, 'error': '请提供论文标题、DOI或URL'})
        
        # Use intelligent extractor
        extractor = SmartPaperExtractor()
        result = extractor.extract_paper_info(input_text)
        
        if result['success']:
            # Format data for frontend
            paper_data = result['data']
            formatted_data = {
                'title': paper_data.get('title', ''),
                'journal': paper_data.get('journal', ''),
                'date': paper_data.get('year', ''),
                'url': paper_data.get('url', ''),
                'field': paper_data.get('field', ''),
                'language': paper_data.get('language', 'Python'),
                'code': paper_data.get('code', ''),
                'citation': paper_data.get('citation', ''),
                'abstract': paper_data.get('abstract', ''),
                'authors': paper_data.get('authors', []),
                'citation_count': paper_data.get('citation_count', 0),
                'data': paper_data.get('data', [])
            }
            
            return jsonify({
                'success': True, 
                'data': formatted_data,
                'message': '论文信息提取成功！'
            })
        else:
            return jsonify({
                'success': False, 
                'error': result.get('error', '提取失败'),
                'suggestions': result.get('suggestions', [])
            })
        
    except Exception as e:
        logger.error(f"Failed to extract paper information: {str(e)}")
        return jsonify({'success': False, 'error': f'系统错误: {str(e)}'})


@app.route('/api/add_entry', methods=['POST'])
def add_entry():
    """API interface for adding new entry"""
    try:
        data = request.get_json()
        category = data.get('category')
        entry_data = data.get('entry_data')
        
        if not category or category not in CONFIG_FILES:
            return jsonify({'success': False, 'error': '无效的类别'})
        
        if not entry_data:
            return jsonify({'success': False, 'error': '条目数据不能为空'})
        
        # Load existing data
        existing_data = load_yaml_file(category)
        
        # Add new entry
        existing_data.append(entry_data)
        
        # Save data
        if save_yaml_file(category, existing_data):
            # Try to update corresponding Markdown file
            update_success = update_markdown_files(category)
            
            return jsonify({
                'success': True, 
                'message': f'条目已添加到 {category}',
                'markdown_updated': update_success
            })
        else:
            return jsonify({'success': False, 'error': '保存失败'})
            
    except Exception as e:
        logger.error(f"Failed to add entry: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/update_all', methods=['POST'])
def update_all():
    """API interface for updating all Markdown files"""
    try:
        success = update_markdown_files()
        return jsonify({
            'success': success,
            'message': '所有文件更新完成' if success else '更新过程中出现错误'
        })
    except Exception as e:
        logger.error(f"Failed to update all files: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/delete_entry', methods=['POST'])
def delete_entry():
    """API interface for deleting entry"""
    try:
        data = request.get_json()
        category = data.get('category')
        entry_index = data.get('index')
        
        if not category or category not in CONFIG_FILES:
            return jsonify({'success': False, 'error': '无效的类别'})
        
        # Load existing data
        existing_data = load_yaml_file(category)
        
        if entry_index is None or entry_index < 0 or entry_index >= len(existing_data):
            return jsonify({'success': False, 'error': '无效的条目索引'})
        
        # Delete entry
        deleted_entry = existing_data.pop(entry_index)
        
        # Save data
        if save_yaml_file(category, existing_data):
            # Update corresponding Markdown file
            update_success = update_markdown_files(category)
            
            return jsonify({
                'success': True,
                'message': f'条目已从 {category} 中删除',
                'markdown_updated': update_success,
                'deleted_entry': deleted_entry
            })
        else:
            return jsonify({'success': False, 'error': '保存失败'})
            
    except Exception as e:
        logger.error(f"Failed to delete entry: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/set_language', methods=['POST'])
def set_language():
    """Set interface language"""
    try:
        data = request.get_json()
        language = data.get('language', 'zh')
        
        if language not in ['zh', 'en']:
            return jsonify({'success': False, 'error': '不支持的语言'})
        
        response = jsonify({'success': True, 'message': '语言设置已保存'})
        response.set_cookie('language', language, max_age=30*24*60*60)  # 30 days
        return response
        
    except Exception as e:
        logger.error(f"Failed to set language: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/set_theme', methods=['POST'])
def set_theme():
    """Set interface theme"""
    try:
        data = request.get_json()
        theme = data.get('theme', 'auto')
        
        if theme not in ['light', 'dark', 'auto']:
            return jsonify({'success': False, 'error': '不支持的主题'})
        
        response = jsonify({'success': True, 'message': '主题设置已保存'})
        response.set_cookie('theme', theme, max_age=30*24*60*60)  # 30 days
        return response
        
    except Exception as e:
        logger.error(f"Failed to set theme: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    print("Starting Bioinformatics Resources Management Interface...")
    print("Access URL: http://localhost:5001")
    print("Press Ctrl+C to stop the service")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 