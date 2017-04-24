import dateutil.parser
from django import template
from operator import itemgetter

from webapp.lib.feeds import get_json_feed_content, get_rss_feed_content
from webapp.lib.markdown import get_page_data as _get_page_data
from webapp.sitemap import sitemap
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_json_feed(feed_url, **kwargs):
    return get_json_feed_content(feed_url, **kwargs)


@register.simple_tag
def get_rss_feed(feed_url, **kwargs):
    return get_rss_feed_content(feed_url, **kwargs)


@register.simple_tag(takes_context=True)
def get_page_data(context, pages, **kwargs):
    request = context['request']
    page_data = _get_page_data(pages, request.path)
    return page_data


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
    page_data = _get_page_data(pages, request.path)
    return {
        'pages': page_data,
    }


@register.inclusion_tag(
    'includes/components/grid_cards.html', takes_context=True
)
def grid_cards(context, pages):
    request = context['request']
    page_data = _get_page_data(pages, request.path)
    return {
        'pages': page_data,
    }


@register.inclusion_tag(
    'includes/components/tutorial_cards.html'
)
def tutorial_cards(feed_config, limit=3):
    base_feed_url = (
        "https://tutorials.ubuntu.com/api/tutorials/{type}.json"
    )

    # Check for categories list, otherwise create an empty list to cycle
    if feed_config is not True and 'categories' in feed_config:
        categories = feed_config['categories']
    else:
        categories = ['']

    # Cycle through requested categories and aggregate results
    feed_data = []
    for category in categories:
        if not category:
            feed_type = 'recent'
        else:
            feed_type = '-'.join(['recent', category])
        feed_url = base_feed_url.format(type=feed_type)
        feed_data += get_json_feed_content(feed_url, limit=limit)

    # Sort tutorials by updated, descending. Grab limit from aggregated items.
    feed_data = sorted(feed_data, key=itemgetter('updated'), reverse=True)
    feed_data = feed_data[:limit]

    for item in feed_data:
        item['updated_datetime'] = dateutil.parser.parse(item['updated'])

    return {
        'feed': feed_data,
    }


@register.inclusion_tag(
    'includes/components/sidebar_nav.html', takes_context=True
)
def sidebar_nav(context):
    request = context['request']
    nav_items = sitemap.build_navigation(
        current_path=request.path,
    )
    return {
        'sitemap': nav_items,
    }


@register.filter
def truncate_chars(value, max_length):
    length = len(value)
    if length > max_length:
        truncated = value[:max_length]
        if not length == (max_length + 1) and value[max_length + 1] != " ":
            truncated = truncated[:truncated.rfind(" ")]
        escaped_html = conditional_escape(truncated)
        return mark_safe(escaped_html + "&hellip;")
    return value
