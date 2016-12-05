from django import template

from webapp.lib.markdown import get_page_data

register = template.Library()


@register.inclusion_tag(
    'includes/components/page_cards.html', takes_context=True
)
def page_cards(context, pages):
    request = context['request']
    page_data = get_page_data(pages, request.path)
    return {
        'pages': page_data,
    }
