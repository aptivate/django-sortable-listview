from mock import patch
from django.test import TestCase
from django.test.client import RequestFactory
from sortable_listview.views import SortableListView
from .models import TestModel


class TestSortableListView(SortableListView):
    # Required configuration
    model = TestModel


class TestGet(TestCase):

    def setUp(self):
        self.view = TestSortableListView.as_view()
        self.request = RequestFactory().get('/')

    def test_get_calls_set_sort_with_request(self):
        with patch('tests.tests.TestSortableListView.set_sort') as set_sort:
            set_sort.return_value = ('-', 'id')
            self.view(self.request)
            set_sort.assert_called_once_with(self.request)

    def test_get_calls_sort_link_list_with_request(self):
        with patch('tests.tests.TestSortableListView.set_sort') as set_sort:
            set_sort.return_value = ('-', 'id')
            self.view(self.request)
            set_sort.assert_called_once_with(self.request)
