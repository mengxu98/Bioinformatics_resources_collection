# Bioinformatics Resources Web Admin Interface

This is a visual web management interface for managing various resource entries in the bioinformatics resources collection repository. Through this interface, you can easily add, view, and delete resource entries without manually editing YAML configuration files.

## 🆕 Latest Feature Updates

### 1. Smart Paper Information Extraction 2.0
- 🔍 **Title Only Required**: Simply enter the paper title to automatically retrieve complete information
- 🌐 **Multi-source Support**: Supports paper titles, DOIs, Semantic Scholar links, and more
- ⚡ **Smart Matching**: Paper matching algorithm based on semantic similarity
- 📊 **Rich Information**: Automatically extracts title, journal, year, authors, citation count, etc.
- 💡 **Smart Suggestions**: Provides similar paper suggestions when exact matches aren't found

### 2. Internationalization Support
- 🌍 **Bilingual Interface**: Complete Chinese-English interface
- 🔄 **One-click Switch**: Switch languages with one click in the navigation bar
- 💾 **Memory Settings**: Automatically saves user language preferences
- 📱 **Responsive**: All interface elements support bilingual display

### 3. Theme Management System
- 🌞 **Light Mode**: Bright theme suitable for daytime use
- 🌙 **Dark Mode**: Eye-friendly dark theme for nighttime
- 🔄 **Auto Mode**: Automatically switches following system theme
- ⚙️ **Manual Control**: Theme selector in navigation bar

## Features

- 🎯 **Visual Management**: Manage all resource categories through an intuitive web interface
- 📝 **Smart Forms**: Automatically adjusts form fields based on resource type
- 🔄 **Auto Updates**: Automatically updates Markdown files after adding resources
- 🧠 **Powerful Extraction**: Retrieve complete paper information with just the title
- 👀 **Real-time Preview**: Preview generated data structure while filling forms
- 🚀 **Seamless Integration**: Does not affect existing GitHub Actions deployment workflow
- 🌍 **Internationalization**: Complete Chinese-English interface support
- 🎨 **Theme Switching**: Supports light/dark/auto theme modes

## Installation and Startup

### 1. Install Dependencies

```bash
pip install -r requirements-web.txt
```

### 2. Start Management Interface

```bash
python start_web_admin.py
```

Or run directly:

```bash
python web_admin.py
```

### 3. Access Interface

Open in browser: http://localhost:5001

## Interface Functions

### Homepage
- Displays statistics for all resource categories
- Provides quick navigation and operation entries
- One-click update of all Markdown files

### Resource Management
Supports management of the following 6 resource categories:

1. **Research Articles**: Scientific papers and research articles
2. **Computational Methods**: Computational methods and algorithmic tools
3. **Recommended Books**: Learning materials and reference books
4. **Blog Articles**: Related blogs and personal websites
5. **Database Resources**: Bioinformatics databases
6. **Research Labs**: Related research institutions and laboratories

### Adding Resources

#### Common Fields
- **Title**: Name or title of the resource
- **Link**: Official website or resource link
- **Research Field**: Related research field classification
- **Description**: Brief description of the resource

#### Special Fields for Academic Resources (Articles/Methods)
- **Journal/Conference**: Name of the journal or conference where published
- **Publication Year**: Year the paper was published
- **Programming Language**: Main programming language for code implementation
- **Code Link**: GitHub or other code hosting links
- **Citation Link**: Semantic Scholar API link
- **Data Information**: Supports multiple data sources (GEO, Zenodo, etc.)

#### Special Fields for Labs
- **Masterpiece**: Representative work or tool of the lab
- **Masterpiece Link**: Link address of the masterpiece

#### Special Fields for Databases
- **Related Paper**: Link to related papers introducing the database

### Smart Extraction Feature

For article and method categories, supports automatic extraction of paper information from Semantic Scholar URLs or DOIs:

1. Enter the paper's Semantic Scholar link or DOI
2. Click the "Extract Paper Info" button
3. System automatically fills in title, journal, year, and other fields

### Data Preview

The right side of the form provides real-time data preview, showing the data structure to be saved to the YAML file, making it easy to confirm information accuracy.

## Workflow

1. **Add Resources** → Fill out web interface forms
2. **Save Data** → Automatically update corresponding YAML configuration files
3. **Generate Website** → Click "Update All Files" button to generate Markdown
4. **Auto Deploy** → GitHub Actions automatically deploys to GitHub Pages

## Technical Architecture

- **Backend**: Flask (Python)
- **Frontend**: Bootstrap 5 + JavaScript
- **Data Storage**: YAML configuration files
- **Integration**: Existing updater system

## File Description

```
├── web_admin.py              # Flask application main program
├── start_web_admin.py        # Startup script
├── requirements-web.txt      # Web interface dependencies
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── index.html           # Homepage
│   ├── category.html        # Category management page
│   └── add_form.html        # Add form page
└── WEB_ADMIN_README.md      # This documentation
```

## Security Considerations

- This web interface is designed for local development use
- When deploying in production environment, please:
  - Change Flask's secret_key
  - Add user authentication mechanism
  - Configure HTTPS
  - Restrict access IP range

## Troubleshooting

### Dependency Issues
If you encounter dependency installation issues, ensure Python version >= 3.7 and try:
```bash
pip install --upgrade pip
pip install -r requirements-web.txt
```

### Permission Issues
Ensure the current user has read/write permissions for configuration files and website directories.

### Port Occupied
Default uses port 5001. If still occupied, you can modify the port number in `web_admin.py`.
On macOS, port 5000 is usually occupied by AirPlay Receiver service.

## Compatibility with Existing Workflow

This web management interface is fully compatible with existing workflows:

- ✅ Does not modify existing YAML file structure
- ✅ Uses existing updater system
- ✅ Compatible with existing GitHub Actions deployment
- ✅ Can be used in combination with manual YAML file editing

## Support and Feedback

If you encounter problems or have improvement suggestions during use, please:

1. Check the troubleshooting section of this document
2. Review error messages in console output
3. Submit an Issue in the GitHub repository

---

## 🚀 Quick Start Guide

### First Time Use

1. **Start Interface**
   ```bash
   python start_web_admin.py
   ```

2. **Access Address**
   ```
   http://localhost:5001
   ```

3. **Set Preferences**
   - Click "Language" in the navigation bar to select Chinese or English
   - Click "Theme" to choose a suitable display mode

### Example: Adding Paper Resources

1. **Enter Add Page**
   - Click "Manage Resources" → "Research Articles" → "Add New Research Article"

2. **Use Smart Extraction**
   - In the "Smart Paper Information Extraction" area, enter:
     ```
     SpaTalk cell communication spatially resolved transcriptomic
     ```
   - Click "Extract Info" button
   - System will automatically fill all relevant fields

3. **Complete Information**
   - Check automatically filled information
   - Add code links (if GitHub repository exists)
   - Add data links (such as GEO datasets)

4. **Save and Update**
   - Click "Add Research Article" to save
   - Click "Update All Files" in navigation bar to generate website content

### Multilingual Experience

**Chinese Interface**:
- Smart paper information extraction
- Basic information, academic information modules
- Data preview, all buttons in Chinese

**English Interface**:
- Smart Paper Information Extraction
- Basic Information, Academic Information modules
- Data Preview, all buttons in English

### Theme Mode Comparison

**Light Mode** 🌞:
- White background, suitable for bright environments
- Black text, high contrast
- Blue primary color, fresh and professional

**Dark Mode** 🌙:
- Dark background, eye-friendly design
- Light text, reduces eye fatigue
- Suitable for nighttime or low-light environments

**Auto Mode** 🔄:
- Follows system theme settings
- Automatically light during day, dark at night
- No manual switching required

## 📝 Update Log

### v2.0.0 (2024-12-XX)
- ✨ Added smart paper title extraction feature
- 🌍 Added complete Chinese-English internationalization support
- 🎨 Added theme switching system (light/dark/auto)
- 🔍 Improved paper matching algorithm with fuzzy search support
- 💡 Added similar paper suggestion feature
- 📊 Display citation count and author information
- ⚡ Optimized interface response speed and user experience

### v1.0.0 (2024-12-XX)
- 🎉 First release of web management interface
- 📝 Support for 6 resource categories management
- 🔄 Integration with existing updater system
- 👀 Real-time data preview feature
- 🧠 Basic paper information extraction feature

**Note**: This management interface is a supplement to the existing workflow and will not replace or affect existing deployment mechanisms. You can still manually edit YAML files and run the main.py script in traditional ways. 