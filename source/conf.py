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
    "sphinx_sitemap",
]

templates_path = ['_templates']

# Sitemap
sitemap_url_scheme = "{link}"

# Sphinx Options
html_theme = 'conestack'
html_baseurl = 'https://techman83.me/'
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
blog_baseurl = "https://techman83.me"
blog_path = "posts/"
blog_default_author = 'techman83'
blog_authors = {'techman83': {'Leon Wright', 'https://techman83.me'}}
blog_feed_archives = True
post_show_prev_next = True

# Old format
old_pages = [
    "personal/2017/01/08/overhauling_techman83.me.html",
    "personal/2014/07/29/xperiaz_warranty.html",
    "personal/2014/02/12/refit_bb.html",
    "personal/2014/02/06/repair_bb.html",
    "personal/2014/03/23/repair_freehub.html",
    "personal/2014/01/19/first_post.html",
    "hardware/2018/01/29/the_hugs_strike_back.html",
    "hardware/2017/06/04/dont_underestimate_the_doorbell.html",
    "hardware/2017/01/11/automating_your_home_with_themachine.html",
    "hardware/2017/01/22/hacking_hugs_profit.html",
    "programming/2014/08/04/jira_automation.html",
    "programming/2014/08/26/webservice_strava.html",
    "programming/2014/02/11/bah_wrong_branch.html",
    "programming/2014/02/20/dancing_with_websockets.html",
    "programming/2014/01/20/eventstreamr.html",
    "programming/2015/04/16/eventstreamr-talk-at-plug.html",
    "programming/2015/06/09/powershell.html",
    "talks/2018/01/22/come_on_do_you_want_your_mods_to_live_forever.html",
]
tags_redirects = [
    "tag/lcagm.html",
    "tag/jira.html",
    "tag/homeautomation.html",
    "tag/win10.html",
    "tag/windows.html",
    "tag/vodafone.html",
    "tag/sony.html",
    "tag/esp8266.html",
    "tag/python.html",
    "tag/warranty.html",
    "tag/programming.html",
    "tag/strava.html",
    "tag/repair.html",
    "tag/programming2.html",
    "tag/defect.html",
    "tag/ksp.html",
    "tag/diy.html",
    "tag/lca.html",
    "tag/groovy.html",
    "tag/dancer.html",
    "tag/cycling.html",
    "tag/automation.html",
    "tag/websockets.html",
    "tag/scriptrunner.html",
    "tag/powershell.html",
    "tag/perl.html",
    "tag/update.html",
    "tag/git.html",
    "tag/machinelearning.html",
    "tag/hardware.html",
    "tag/linuxconfau.html",
    "tag/lca2018.html",
    "tag/plug.html",
    "tag/kerbalspaceprogram.html",
    "tag/lca2017.html",
    "tag/arduino.html",
    "tag/av.html",
    "tag/personal.html",
]
redirects = {
    "hardware/index.html": "../../posts/hardware.html",
    "personal/index.html": "../../posts/personal.html",
    "programming/index.html": "../../posts/programming.html",
    "talks/index.html": "../../posts/talks.html",
    "archives.html": "/posts/archive.html",
    "categories.html": "/posts/category.html",
    **{f"{x}": f"../posts/{x}" for x in tags_redirects},
}

for uri in old_pages:
    category, year, month, day, page = uri.split('/',4)
    source = page.replace('.html', '')
    redirects.update({
        f"{category}/{year}/{month}/{day}/{source}": f"../../../../posts/{year}/{year}-{month}-{day}-{page}"
    })

# Sphinx Contrib Images
images_config = {
    'default_image_width': 300,
    'default_group': 'default',
}
