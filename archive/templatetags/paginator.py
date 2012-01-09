#  Based on: http://www.djangosnippets.org/snippets/73/
#
#  Modified by Sean Reifschneider to be smarter about surrounding page
#  link context.  For usage documentation see:
#
#     http://www.tummy.com/Community/Articles/django-pagination/

from django import template

register = template.Library()

def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """
    startPage = max(context['page_obj'].number - adjacent_pages, 1)
    if startPage <= 3: startPage = 1
    endPage = context['page_obj'].number + adjacent_pages + 1
    if endPage >= context['paginator'].num_pages - 2: endPage = context['paginator'].num_pages
    page_numbers = [n for n in range(startPage, endPage)]
    page_obj = context['page_obj']
    paginator = context['paginator']

    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'page': page_obj.number,
        'pages': paginator.num_pages,
        'page_numbers': page_numbers,
        'next': page_obj.next_page_number,
        'previous': page_obj.previous_page_number,
        'has_next': page_obj.has_next,
        'has_previous': page_obj.has_previous,
        'show_first': 1 not in page_numbers,
        'show_last': paginator.num_pages not in page_numbers,
    }

register.inclusion_tag('paginator.html', takes_context=True)(paginator)
