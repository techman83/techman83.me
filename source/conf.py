project = "Techman83's meandering thoughts"
copyright = '2024, Leon Wright'
author = 'Leon Wright'

extensions = [
    "ablog",
    "sphinx.ext.intersphinx",
    "myst_parser",
    "sphinx_reredirects",
    "sphinxcontrib.images",
    "sphinxcontrib.youtube",
    "sphinxcontrib.jquery",
]

templates_path = ['_templates']

# Sphinx Options
html_theme = 'conestack'
html_static_path = ['_static']
html_extra_path = ['favicon.ico', 'leon-vr.webp', 'feed-icon.png']
html_css_files = ['custom.css']
html_title = "Techman83's meandering thoughts"
html_theme_options = {
    'logo_url': '/leon-vr.webp',
    'logo_title': "Techman83's meandering thoughts",
    'logo_width': '40px',
    'logo_height': '40px',
    'github_url': 'https://github.com/Techman83',
    'sidebar_left_width': 'calc(250px - 2rem)',
    'sidebar_right_width': '150px',
}
html_sidebars = {
    "*": [
        "navigationtoc.html",
        "ablog/archives.html",
    ],
    "posts/**": [
        "ablog/postcard.html",
        "navigationtoc.html",
        "ablog/archives.html",
    ]
}

# Ablog configuration
blog_baseurl = "https://www.techman83.me"
blog_path = "posts/"
blog_default_author = 'techman83'
blog_authors = {'techman83': {'Leon Wright', 'https://techman83.me'}}
blog_feed_archives = True
post_show_prev_next = True

# Old format
redirects = {
     "personal/2014/01/19/first_post": "../../../../posts/2014/2014-01-19-first_post.html"
}

# Sphinx Contrib Images
images_config = {
    'default_image_width': 300,
    'default_group': 'default',
}
