"""Badge formatting utilities for articles and methods"""

class BadgeFormatter:
    """Utility class for formatting various types of badges"""
    
    # Color mapping for different types
    LANGUAGE_COLORS = {
        "Python": "3572a5",
        "R": "198ce7",
        "MATLAB": "e16737",
        "Java": "b0721a",
        "Jupyter Notebook": "00008B",
        "Shell": "89e051",
        "R Python": "444444",
        "R Python Shell": "444444"
    }
    
    DATA_SOURCE_COLORS = {
        'figshare': 'c62764',
        'GEO': '336699',
        'Zenodo': '024dad',
        'Website': 'B03060',
        'Github': '336699',
        'PKU': '4B0082'
    }
    
    @staticmethod
    def create_badge(label, message, color, url):
        """Create a markdown badge with link"""
        badge = f'![{label}](https://img.shields.io/badge/-{message}-{color})'
        return f'[{badge}]({url})'
    
    @classmethod
    def format_code_badges(cls, entry):
        """Format code badges for different languages"""
        if not entry.get('code'):
            return ""
            
        badges = []
        codes = entry['code'] if isinstance(entry['code'], list) else [entry['code']]
        languages = entry['language'] if isinstance(entry.get('language'), list) else [entry.get('language', 'Code')]
        
        for i, code_url in enumerate(codes):
            lang = languages[i] if i < len(languages) else languages[-1]
            color = cls.LANGUAGE_COLORS.get(lang, "444444")
            lang_combined = lang.replace(" ", "%20")
            badges.append(cls.create_badge(lang_combined, lang_combined, color, code_url))
        
        return ' '.join(badges)
    
    @classmethod
    def format_data_badges(cls, data):
        """Format data badges from various sources"""
        if not data:
            return ""
            
        if isinstance(data, str):
            return cls.create_badge('Data', 'Data', '336699', data)
            
        badges = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    badge_type = item.get('type', 'Data')
                    url = item.get('url', '')
                    if url:
                        color = cls.DATA_SOURCE_COLORS.get(badge_type, '336699')
                        badges.append(cls.create_badge(badge_type, badge_type, color, url))
        
        return ' '.join(badges)
    
    @staticmethod
    def format_citation_badge(citation_url):
        """Format citation badge using semanticscholar API"""
        if not citation_url:
            return ""
            
        try:
            paper_id = citation_url.split('/')[-1]
            semanticscholar_api = (
                "https://img.shields.io/badge/dynamic/json?label=citation&query=citationCount&url="
                + "https%3A%2F%2Fapi.semanticscholar.org%2Fgraph%2Fv1%2Fpaper%2F"
                + paper_id
                + "%3Ffields%3DcitationCount"
            )
            
            return f'[![citation]({semanticscholar_api})]({citation_url})'
        except Exception as e:
            print(f"Error formatting citation badge: {str(e)}")
            return "" 