from django.utils.translation import gettext as _


def context_processor(request):
    """
    Context processor for adding site-wide context variables.
    """
    site_name = _('DIETOLOGONLINE')
    footer_text = _('© 2024 DIETOLOGONLINE. Усі права захищені.')
    return {
        'site_name': site_name,
        'footer_text': footer_text,
    }
