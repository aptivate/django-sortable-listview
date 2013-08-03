from mock import MagicMock
from django.test import TestCase
from django.test.client import RequestFactory
from sortable_listview.views import SortableListView
from .models import TestModel


class TestSortableListView(SortableListView):
    # Required configuration
    model = TestModel


class TestDispatch(TestCase):

    def test_dispatch_calls_set_sort_with_request(self):
        view = TestSortableListView()
        view.set_sort = MagicMock(return_value=('-', 'id'))
        request = view.request = RequestFactory().get('/')
        # Calling the view calls the dispatch method
        view.dispatch(request)
        view.set_sort.assert_called_once_with(request)
