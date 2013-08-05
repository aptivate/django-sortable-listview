from mock import patch, MagicMock
from django.test import TestCase
from django.test.client import RequestFactory
from sortable_listview.views import SortableListView
from .models import TestModel


class TestSortableListView(SortableListView):
    # Required configuration
    model = TestModel


class TestGet(TestCase):

    def test_calls_set_sort_with_request(self):
        view = TestSortableListView.as_view()
        request = RequestFactory().get('/')
        with patch('tests.tests.TestSortableListView.set_sort') as set_sort:
            set_sort.return_value = ('-', 'id')
            view(request)
            set_sort.assert_called_once_with(request)

    def test_calls_sort_link_list_with_request(self):
        view = TestSortableListView.as_view()
        request = RequestFactory().get('/')
        with patch('tests.tests.TestSortableListView.get_sort_link_list') \
                as get_sort_link_list:
            view(request)
            get_sort_link_list.assert_called_once_with(request)

    def test_sets_sort_order_and_sort_field(self):
        view = TestSortableListView()
        request = RequestFactory().get('/')
        view.set_sort = MagicMock(return_value=('hola', 'mundo'))
        view.request = request
        view.get(request)
        self.assertEqual(view.sort_order, 'hola')
        self.assertEqual(view.sort_field, 'mundo')


class TestGetContextData(TestCase):

    def test_sets_sort_link_list_context(self):
        view = TestSortableListView()
        view.get_sort_string = MagicMock()
        view.sort_link_list = ['hola', 'mundo']
        context = view.get_context_data(object_list=[])
        self.assertEqual(context['sort_link_list'], ['hola', 'mundo'])

    def test_sets_current_sort_query_context(self):
        view = TestSortableListView()
        view.get_sort_string = MagicMock(return_value='sort=sortme')
        view.sort_link_list = []
        context = view.get_context_data(object_list=[])
        self.assertEqual(context['current_sort_query'], 'sort=sortme')

    def test_calls_get_sort_string(self):
        view = TestSortableListView()
        view.get_sort_string = MagicMock()
        view.sort_link_list = []
        view.get_context_data(object_list=[])
        view.get_sort_string.assert_called_once_with()


class TestSortProperty(TestCase):

    def test_assembles_sort_order_and_sort_field(self):
        view = TestSortableListView()
        view.sort_order = '-test'
        view.sort_field = 'sort'
        self.assertEqual(view.sort, '-testsort')


class TestGetQueryset(TestCase):

    def test_calls_order_by_with_self_sort(self):
        view = TestSortableListView()
        view.sort_order = 'testso'
        view.sort_field = 'rtstuff'
        with patch('django.db.models.query.QuerySet.order_by') as mock:
            view.get_queryset()
            mock.assert_called_once_with('testsortstuff')


class TestSetSort(TestCase):

    def test_if_not_reverse_sort_order_and_sort_field_set(self):
        view = TestSortableListView()
        view.allowed_sort_fields = {'sortfield': {}}
        request = RequestFactory().get('/', {'sort': 'sortfield'})
        actual = view.set_sort(request)
        self.assertTupleEqual(('', 'sortfield'), actual)

    def test_if_reverse_sort_order_set_reverse_and_sort_field_set(self):
        view = TestSortableListView()
        view.allowed_sort_fields = {'sortfield': {}}
        request = RequestFactory().get('/', {'sort': '-sortfield'})
        actual = view.set_sort(request)
        self.assertTupleEqual(('-', 'sortfield'), actual)

    def test_if_no_sort_parameter_provided_default_is_used(self):
        view = TestSortableListView()
        view.default_sort_field = 'sortfield2'
        view.allowed_sort_fields = {'sortfield1': {},
                                    'sortfield2': {}}
        request = RequestFactory().get('/')
        actual = view.set_sort(request)
        # NB The reverse default direction is inherited from defaults unless
        # you specify otherwise
        self.assertTupleEqual(('-', 'sortfield2'), actual)

    def test_if_sort_field_is_not_in_allowed_sort_fields_default_is_used(self):
        view = TestSortableListView()
        request = RequestFactory().get('/', {'sort': 'sortfield'})
        actual = view.set_sort(request)
        self.assertTupleEqual(('-', 'id'), actual)

    def test_respects_alternate_sort_parameter(self):
        view = TestSortableListView()
        view.allowed_sort_fields = {'sortfield': {}}
        view.sort_parameter = 's'
        request = RequestFactory().get('/', {'s': '-sortfield'})
        actual = view.set_sort(request)
        self.assertTupleEqual(('-', 'sortfield'), actual)


class TestGetSortString(TestCase):

    def test_self_sort_is_used_if_sort_not_passed(self):
        view = TestSortableListView()
        view.sort_order = '-test'
        view.sort_field = 'sort'
        sort_string = view.get_sort_string()
        self.assertEqual('sort=-testsort', sort_string)

    def test_empty_string_is_returned_if_sort_is_default_sort(self):
        view = TestSortableListView()
        view.default_sort = '-blob'
        sort_string = view.get_sort_string('-blob')
        self.assertEqual('', sort_string)


class TestGetNextSortString(TestCase):

    def temp_get_sort_string(self, field):
        return field

    def setUp(self):
        self.view = TestSortableListView()
        self.view.sort_field = 'title'
        # Just makes it easier to know what was passed
        self.view.get_sort_string = \
            MagicMock(side_effect=self.temp_get_sort_string)

    def test_if_field_is_not_current_sort_field_uses_fields_default_sort(self):
        field = 'name'
        self.view.allowed_sort_fields = {'name': {'default_direction': '-'}}
        self.assertEqual(self.view.get_next_sort_string(field), '-name')

    def test_if_field_is_current_sort_field_reverses_sort_direction(self):
        self.view.sort_order = '-'
        field = 'title'
        self.assertEqual(self.view.get_next_sort_string(field), 'title')

    def test_if_field_is_current_sort_field_toggle_sort_order_is_called(self):
        # Somewhat a duplicate of above
        field = 'title'
        self.view.toggle_sort_order = MagicMock()
        self.view.get_next_sort_string(field)
        self.view.toggle_sort_order.assert_called_once_with()

    def test_get_sort_string_is_called(self):
        self.view.get_next_sort_string('id')
        self.view.get_sort_string.assert_called_once()


class TestGetSortIndicator(TestCase):

    def test_if_field_is_not_current_field_then_no_indicator_returned(self):
        view = TestSortableListView()
        view.sort_field = 'title'
        self.assertEqual(view.get_sort_indicator('name'), '')

    def test_if_field_is_current_and_sort_is_asc_then_sortasc_returned(self):
        view = TestSortableListView()
        view.sort_field = 'name'
        view.sort_order = ''
        self.assertEqual(view.get_sort_indicator('name'), 'sort-asc')

    def test_if_field_is_current_and_sort_is_desc_then_sortdesc_returned(self):
        view = TestSortableListView()
        view.sort_field = 'name'
        view.sort_order = '-'
        self.assertEqual(view.get_sort_indicator('name'), 'sort-desc')


class TestToggleSortOrder(TestCase):

    def test_toggles_reverse_to_empty_string(self):
        view = TestSortableListView()
        view.sort_order = '-'
        toggled = view.toggle_sort_order()
        self.assertEqual(toggled, '')

    def test_toggles_empty_string_to_reverse(self):
        view = TestSortableListView()
        view.sort_order = ''
        toggled = view.toggle_sort_order()
        self.assertEqual(toggled, '-')
