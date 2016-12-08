from django import template

from webapp.lib.feeds import get_json_feed_content, get_rss_feed_content
from webapp.lib.markdown import get_page_data

register = template.Library()


@register.simple_tag
def get_json_feed(feed_url, **kwargs):
    return get_json_feed_content(feed_url, **kwargs)


@register.simple_tag
def get_rss_feed(feed_url, **kwargs):
    return get_rss_feed_content(feed_url, **kwargs)


@register.inclusion_tag(
    'includes/components/feed_cards.html'
)
def feed_cards(feed_url, **kwargs):
    context = kwargs
    context['feed_url'] = feed_url
    return context


@register.inclusion_tag(
    'includes/components/page_cards.html', takes_context=True
)
def page_cards(context, pages):
    request = context['request']
    page_data = get_page_data(pages, request.path)
    return {
        'pages': page_data,
    }
