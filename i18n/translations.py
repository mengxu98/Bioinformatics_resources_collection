#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Internationalization Translation File
Supports Chinese-English bilingual interface
"""

TRANSLATIONS = {
    'zh': {
        # 导航和界面
        'site_title': '生物信息学资源管理',
        'home': '首页',
        'manage_resources': '管理资源',
        'update_all_files': '更新所有文件',
        'view_website': '查看网站',
        'language': '语言',
        'theme': '主题',
        'light_mode': '浅色模式',
        'dark_mode': '深色模式',
        'auto_mode': '自动模式',
        
        # 资源类别
        'articles': '研究文章',
        'methods': '计算方法',
        'books': '推荐书籍',
        'blogs': '博客文章',
        'databases': '数据库资源',
        'labs': '研究实验室',
        
        # 智能提取
        'smart_extract': '智能提取论文信息',
        'smart_extract_desc': '只需输入论文标题即可自动获取完整信息',
        'paper_input': '论文标题/DOI/URL',
        'paper_input_placeholder': '输入论文标题、DOI或Semantic Scholar链接',
        'extract_info': '提取信息',
        'extracting': '提取中...',
        
        # 表单
        'basic_info': '基本信息',
        'title': '标题',
        'url': '链接',
        'field': '研究领域',
        'description': '描述',
        'academic_info': '学术信息',
        'journal': '期刊/会议',
        'publication_year': '发表年份',
        'programming_language': '编程语言',
        'code_link': '代码链接',
        'citation_link': '引用链接',
        'data_info': '数据信息',
        'data_type': '数据类型',
        'data_link': '数据链接',
        'select_type': '选择类型',
        
        # 操作
        'submit': '提交',
        'save': '保存',
        'delete': '删除',
        'add': '添加',
        'update': '更新',
        'reset_form': '重置表单',
        
        # 状态消息
        'success': '成功',
        'error': '错误',
        'loading': '加载中...',
        
        # 数据预览
        'data_preview': '数据预览',
        'preview_desc': '请填写表单字段，这里将显示生成的数据结构',
        
        # 首页相关
        'resource_management_panel': '资源管理面板',
        'total_resources': '总计资源',
        'welcome_title': '欢迎使用生物信息学资源管理界面',
        'welcome_desc': '此界面允许您可视化地管理生物信息学资源，包括添加、编辑和删除各类资源条目。',
        'usage_instructions': '使用说明',
        'usage_desc': '点击下方卡片可查看各类别的资源，使用"添加新资源"按钮可快速添加条目。修改后请点击"更新所有文件"来生成最新的网站内容。',
        'manage': '管理',
        'quick_actions': '快速操作',
        'file_operations': '文件操作',
        'system_info': '系统信息',
        'config_location': '配置文件位置',
        'website_content': '网站内容',
        'auto_deploy': '自动部署',
        'view_generated_website': '查看生成的网站',
        'update_all_markdown': '更新所有Markdown文件',
        
        # 资源描述
        'articles_desc': '科学论文和研究文章，专注于生物学发现和单细胞组学数据分析',
        'methods_desc': '用于分析单细胞数据的计算方法和算法工具',
        'books_desc': '生物信息学和计算生物学相关的推荐书籍和学习材料',
        'blogs_desc': '关于scRNA-seq和相关主题的博客文章和个人网站',
        'databases_desc': '生物信息学研究中有用的数据库和数据资源',
        'labs_desc': '在该领域工作的研究实验室和研究小组',
        
        # 统计单位
        'article_count': '篇文章',
        'method_count': '个方法',
        'book_count': '本书籍',
        'blog_count': '篇博客',
        'database_count': '个数据库',
        'lab_count': '个实验室',
        
        # 类别管理页面
        'management': '管理',
        'add_new': '添加新',
        'return_home': '返回首页',
        'current_total': '当前共有',
        'entries_count': '个条目',
        'config_file_label': '配置文件',
        'no_data': '暂无数据',
        'no_resources_added': '还没有添加任何',
        'resources_suffix': '资源',
        'add_first': '添加第一个',
        'uncategorized': '未分类',
        'no_description': '暂无描述',
        'masterpiece': '代表作',
        'related_paper': '相关论文',
        
        # 表格列标题
        'title_column': '标题',
        'journal_column': '期刊', 
        'year_column': '年份',
        'field_column': '领域',
        'language_column': '语言',
        'action_column': '操作',
        'method_name': '方法名称',
        'database_name': '数据库名称',
        'description_column': '描述',
        'delete': '删除',
        'web_admin_interface': 'Web管理界面',
        'updating': '更新中',
        'all_markdown_updated': '所有Markdown文件已更新完成！',
        'update_failed': '更新失败',
        'network_error': '网络错误',
        'confirm_delete': '确定要删除条目',
        'delete_failed': '删除失败',
        'theme_saved': '主题设置已保存',
        'theme_failed': '设置主题失败',
        'language_failed': '设置语言失败',
    },
    
    'en': {
        # Navigation and Interface
        'site_title': 'Bioinformatics Resource Management',
        'home': 'Home',
        'manage_resources': 'Manage Resources',
        'update_all_files': 'Update All Files',
        'view_website': 'View Website',
        'language': 'Language',
        'theme': 'Theme',
        'light_mode': 'Light Mode',
        'dark_mode': 'Dark Mode',
        'auto_mode': 'Auto Mode',
        
        # Resource Categories
        'articles': 'Research Articles',
        'methods': 'Computational Methods',
        'books': 'Recommended Books',
        'blogs': 'Blog Posts',
        'databases': 'Database Resources',
        'labs': 'Research Labs',
        
        # Smart Extraction
        'smart_extract': 'Smart Paper Information Extraction',
        'smart_extract_desc': 'Just input the paper title to automatically get complete information',
        'paper_input': 'Paper Title/DOI/URL',
        'paper_input_placeholder': 'Enter paper title, DOI, or Semantic Scholar link',
        'extract_info': 'Extract Info',
        'extracting': 'Extracting...',
        
        # Forms
        'basic_info': 'Basic Information',
        'title': 'Title',
        'url': 'URL',
        'field': 'Research Field',
        'description': 'Description',
        'academic_info': 'Academic Information',
        'journal': 'Journal/Conference',
        'publication_year': 'Publication Year',
        'programming_language': 'Programming Language',
        'code_link': 'Code Link',
        'citation_link': 'Citation Link',
        'data_info': 'Data Information',
        'data_type': 'Data Type',
        'data_link': 'Data Link',
        'select_type': 'Select Type',
        
        # Actions
        'submit': 'Submit',
        'save': 'Save',
        'delete': 'Delete',
        'add': 'Add',
        'update': 'Update',
        'reset_form': 'Reset Form',
        
        # Status Messages
        'success': 'Success',
        'error': 'Error',
        'loading': 'Loading...',
        
        # Data Preview
        'data_preview': 'Data Preview',
        'preview_desc': 'Fill in the form fields, and the generated data structure will be displayed here',
        
        # Homepage Related
        'resource_management_panel': 'Resource Management Panel',
        'total_resources': 'Total Resources',
        'welcome_title': 'Welcome to Bioinformatics Resource Management Interface',
        'welcome_desc': 'This interface allows you to visually manage bioinformatics resources, including adding, editing, and deleting various resource entries.',
        'usage_instructions': 'Usage Instructions',
        'usage_desc': 'Click on the cards below to view resources by category. Use the "Add New Resource" button to quickly add entries. After making changes, please click "Update All Files" to generate the latest website content.',
        'manage': 'Manage',
        'quick_actions': 'Quick Actions',
        'file_operations': 'File Operations',
        'system_info': 'System Information',
        'config_location': 'Config File Location',
        'website_content': 'Website Content',
        'auto_deploy': 'Auto Deploy',
        'view_generated_website': 'View Generated Website',
        'update_all_markdown': 'Update All Markdown Files',
        
        # Resource Descriptions
        'articles_desc': 'Scientific papers and research articles focusing on biological discoveries and single-cell omics data analysis',
        'methods_desc': 'Computational methods and algorithmic tools for analyzing single-cell data',
        'books_desc': 'Recommended books and learning materials related to bioinformatics and computational biology',
        'blogs_desc': 'Blog posts and personal websites about scRNA-seq and related topics',
        'databases_desc': 'Useful databases and data resources for bioinformatics research',
        'labs_desc': 'Research laboratories and groups working in the field',
        
        # Statistical Units
        'article_count': 'articles',
        'method_count': 'methods',
        'book_count': 'books',
        'blog_count': 'blogs',
        'database_count': 'databases',
        'lab_count': 'labs',
        
        # Category Management Page
        'management': 'Management',
        'add_new': 'Add New',
        'return_home': 'Return Home',
        'current_total': 'Currently',
        'entries_count': 'entries',
        'config_file_label': 'Config File',
        'no_data': 'No Data',
        'no_resources_added': 'No',
        'resources_suffix': 'resources added yet',
        'add_first': 'Add First',
        'uncategorized': 'Uncategorized',
        'no_description': 'No Description',
        'masterpiece': 'Masterpiece',
        'related_paper': 'Related Paper',
        
        # Table Column Headers
        'title_column': 'Title',
        'journal_column': 'Journal',
        'year_column': 'Year',
        'field_column': 'Field',
        'language_column': 'Language',
        'action_column': 'Action',
        'method_name': 'Method Name',
        'database_name': 'Database Name',
        'description_column': 'Description',
        'delete': 'Delete',
        'web_admin_interface': 'Web Admin Interface',
        'updating': 'Updating',
        'all_markdown_updated': 'All Markdown files updated successfully!',
        'update_failed': 'Update failed',
        'network_error': 'Network error',
        'confirm_delete': 'Are you sure you want to delete entry',
        'delete_failed': 'Delete failed',
        'theme_saved': 'Theme settings saved',
        'theme_failed': 'Failed to set theme',
        'language_failed': 'Failed to set language',
    }
}

def get_translation(key: str, lang: str = 'zh') -> str:
    """Get translation text"""
    return TRANSLATIONS.get(lang, {}).get(key, key)

def get_all_translations(lang: str = 'zh') -> dict:
    """Get all translations for specified language"""
    return TRANSLATIONS.get(lang, {})