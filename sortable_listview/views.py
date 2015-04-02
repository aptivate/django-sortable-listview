from __future__ import unicode_literals

try:
    from urllib import urlencode
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlencode, urlparse, parse_qs

from django.views.generic import ListView


class SortableListView(ListView):
    # Defaults, you probably want to specify these when you subclass
    default_sort_field = 'id'
    allowed_sort_fields = {default_sort_field: {'default_direction': '-',
                                                'verbose_name': 'ID'}}
    sort_parameter = 'sort'  # the get parameter e.g. ?page=1&sort=2
    del_query_parameters = ['page']  # get paramaters we don't want to preserve
    # End of Defaults

    @property
    def sort(self):
        return self.sort_order + self.sort_field

    @property
    def default_sort_order(self):
        return self.allowed_sort_fields[
            self.default_sort_field]['default_direction']

    @property
    def default_sort(self):
        return self.default_sort_order + self.default_sort_field

    def get(self, request, *args, **kwargs):
        self.sort_order, self.sort_field = self.set_sort(request)
        self.sort_link_list = self.get_sort_link_list(request)
        return super(SortableListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SortableListView,
                        self).get_context_data(**kwargs)
        context['current_sort_query'] = self.get_sort_string()
        context['current_querystring'] = self.get_querystring()
        context['sort_link_list'] = self.sort_link_list
        return context

    def get_queryset(self):
        qs = super(SortableListView, self).get_queryset()
        qs = qs.order_by(self.sort)
        return qs

    def get_querystring_parameter_to_remove(self):
        """
        Return list of GET parameters that should be removed from querystring
        """
        return self.del_query_parameters + [self.sort_parameter]

    def get_querystring(self):
        """
        Clean existing query string (GET parameters) by removing
        arguments that we don't want to preserve (sort parameter, 'page')
        """
        to_remove = self.get_querystring_parameter_to_remove()
        query_string = urlparse(self.request.get_full_path()).query
        query_dict = parse_qs(query_string)
        for arg in to_remove:
            if arg in query_dict:
                del query_dict[arg]
        clean_query_string = urlencode(query_dict, doseq=True)
        return clean_query_string

    def set_sort(self, request):
        """
        Take the sort parameter from the get parameters and split it into
        the field and the prefix
        """
        # Look for 'sort' in get request. If not available use default.
        sort_request = request.GET.get(self.sort_parameter, self.default_sort)
        if sort_request.startswith('-'):
            sort_order = '-'
            sort_field = sort_request.split('-')[1]
        else:
            sort_order = ''
            sort_field = sort_request
        # Invalid sort requests fail silently
        if not sort_field in self.allowed_sort_fields:
            sort_order = self.default_sort_order
            sort_field = self.default_sort_field
        return (sort_order, sort_field)

    def get_sort_string(self, sort=None):
        if not sort:
            sort = self.sort
        sort_string = ''
        if not sort == self.default_sort:
            sort_string = self.sort_parameter + '=' + sort
        return sort_string

    def get_next_sort_string(self, field):
        """
        If we're already sorted by the field then the sort query
        returned reverses the sort order.
        """
        # self.sort_field is the currect sort field
        if field == self.sort_field:
            next_sort = self.toggle_sort_order() + field
        else:
            default_order_for_field = \
                self.allowed_sort_fields[field]['default_direction']
            next_sort = default_order_for_field + field
        return self.get_sort_string(next_sort)

    def get_sort_indicator(self, field):
        """
        Returns a sort class for the active sort only. That is, if field is not
        sort_field, then nothing will be returned becaues the sort is not
        active.
        """
        indicator = ''
        if field == self.sort_field:
            indicator = 'sort-asc'
            if self.sort_order == '-':
                indicator = 'sort-desc'
        return indicator

    def toggle_sort_order(self):
        if self.sort_order == '-':
            toggled_sort_order = ''
        if self.sort_order == '':
            toggled_sort_order = '-'
        return toggled_sort_order

    def get_sort_link_list(self, request):
        sort_links = []
        for sort_field in self.allowed_sort_fields:
            sort_link = {
                'attrs': sort_field,
                'path': self.get_basic_sort_link(request, sort_field),
                'indicator': self.get_sort_indicator(sort_field),
                'title': self.allowed_sort_fields[sort_field]['verbose_name']}
            sort_links.append(sort_link)
        return sort_links

    def get_basic_sort_link(self, request, field):
        """
        Thanks to del_query_parameters and get_querystring, we build the link
        with preserving interesting get parameters and removing the others
        """
        query_string = self.get_querystring()
        sort_string = self.get_next_sort_string(field)
        if sort_string:
            sort_link = request.path + '?' + sort_string
            if query_string:
                sort_link += '&' + query_string
        else:
            sort_link = request.path
            if query_string:
                sort_link += '?' + query_string
        return sort_link
