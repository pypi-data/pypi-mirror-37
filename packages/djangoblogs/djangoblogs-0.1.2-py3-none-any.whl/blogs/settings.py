from django.conf import settings as project_settings

class BlogSettings(object):
    def __init__(self):
        pass

settings = BlogSettings()

settings.SHOW_FOOTER_LINK = getattr(project_settings, 'BLOGS_SHOW_FOOTER_LINK', True)
settings.PARENT_SITE_NAME = getattr(project_settings, 'BLOGS_PARENT_SITE_NAME', 'Email Gardener')