def context_processor(request):
    site_name = 'DIETOLOGONLINE'
    footer_text = '© 2024 DIETOLOGONLINE. Усі права захищені.'
    return {
        'site_name': site_name,
        'footer_text': footer_text,
    }