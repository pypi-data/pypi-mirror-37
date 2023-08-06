import logging

from tests.common import SdkIntegrationTestCase, eventually


logger = logging.getLogger(__name__)


class SearchFunctionsTestCase(SdkIntegrationTestCase):

    def entities_are_returned_in_search(self, search_func, expected_min_count):
        def search():
            result = search_func()
            self.assertTrue(len(result) >= expected_min_count)
            return result
        
        return eventually(search)

    def test_search_all_raises_error_for_invalid_count(self):
        self.assert_page_count_is_valid_for_paginated_resource_actions(lambda c: self.client.search(term='searchable', count=c))

    def test_search_all(self):
        self.assertEqual(len(self.client.search(term="")), 0)

        self.create_package("searchable package")
        self.create_collection("searchable collection")

        search_term = "searchable"
        results = self.entities_are_returned_in_search(lambda: self.client.search(search_term), 2)
        self.assertTrue(all([search_term in p.name for p in results if hasattr(p, "package_id")]))
        self.assertTrue(all([search_term in c.name for c in results if hasattr(c, "collection_id")]))
        
    def test_search_packages_raises_error_for_invalid_count(self):
        self.assert_page_count_is_valid_for_paginated_resource_actions(lambda c: self.client.search_packages(term='searchable', count=c))

    def test_search_packages(self):
        self.assertEqual(len(self.client.search_packages(term="")), 0)

        self.create_package("searchable package")
        search_term = "searchable"

        results = self.entities_are_returned_in_search(lambda: self.client.search_packages(search_term), 1)
        self.assertTrue(all([hasattr(package, "package_id") and search_term in package.name for package in results]))

    def test_search_collections_raises_error_for_invalid_count(self):
        self.assert_page_count_is_valid_for_paginated_resource_actions(lambda c: self.client.search_collections(term='searchable', count=c))
        
    def test_search_collections(self):
        self.assertEqual(len(self.client.search_collections(term="")), 0)

        self.create_collection("searchable collection")
        search_term = "searchable"

        results = self.entities_are_returned_in_search(lambda: self.client.search_collections(search_term), 1)
        self.assertTrue(all([hasattr(collection, "collection_id") and search_term in collection.name for collection in results]))
