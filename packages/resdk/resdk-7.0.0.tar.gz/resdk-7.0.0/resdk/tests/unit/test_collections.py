"""
Unit tests for resdk/resources/collection.py file.
"""
# pylint: disable=missing-docstring, protected-access

import unittest

import six
from mock import MagicMock, patch

from resdk.resources.collection import BaseCollection, Collection
from resdk.resources.descriptor import DescriptorSchema
from resdk.resources.sample import Sample

DATA0 = MagicMock(**{'files.return_value': [], 'id': 0})

DATA1 = MagicMock(**{'files.return_value': ['reads.fq', 'arch.gz'], 'id': 1})

DATA2 = MagicMock(**{'files.return_value': ['outfile.exp'], 'id': 2})


class TestBaseCollection(unittest.TestCase):

    @patch('resdk.resources.collection.BaseCollection', spec=True)
    def test_data_types(self, collection_mock):
        payload = {
            'id': 123,
            'process_type': 'data:reads:fastq:single:',
            # ...
        }
        get_mock = MagicMock(**{'get.return_value': payload})
        api_mock = MagicMock(**{'data.return_value': get_mock})
        collection_mock.configure_mock(data=[1, 2], resolwe=MagicMock(api=api_mock))

        types = BaseCollection.data_types(collection_mock)
        self.assertEqual(types, [u'data:reads:fastq:single:'])

    @patch('resdk.resources.collection.BaseCollection', spec=True)
    def test_files(self, collection_mock):
        collection_mock.configure_mock(data=[DATA1, DATA2], resolwe=" ")

        flist = BaseCollection.files(collection_mock)
        self.assertEqual(set(flist), set(['arch.gz', 'reads.fq', 'outfile.exp']))


class TestBaseCollectionDownload(unittest.TestCase):

    @patch('resdk.resources.collection.BaseCollection', spec=True)
    def test_file_type(self, collection_mock):
        collection_mock.configure_mock(data=[DATA0, DATA2], resolwe=MagicMock())
        BaseCollection.download(collection_mock, file_type='output.exp')
        flist = [u'2/outfile.exp']
        collection_mock.resolwe._download_files.assert_called_once_with(flist, None)

        # Check if ok to also provide ``output_field`` that does not start with 'output'
        collection_mock.reset_mock()
        collection_mock.configure_mock(data=[DATA1, DATA0], resolwe=MagicMock())
        BaseCollection.download(collection_mock, file_type='fastq')
        flist = [u'1/reads.fq', u'1/arch.gz']
        collection_mock.resolwe._download_files.assert_called_once_with(flist, None)

    @patch('resdk.resources.collection.BaseCollection', spec=True)
    def test_bad_file_type(self, collection_mock):
        message = "Invalid argument value `file_type`."
        with six.assertRaisesRegex(self, ValueError, message):
            BaseCollection.download(collection_mock, file_type=123)


class TestCollection(unittest.TestCase):

    def test_descriptor_schema(self):
        collection = Collection(id=1, resolwe=MagicMock())
        collection._descriptor_schema = 1

        # test getting descriptor schema attribute
        collection.resolwe.descriptor_schema.get = MagicMock(return_value='descriptor_schema')
        self.assertEqual(collection.descriptor_schema, 'descriptor_schema')
        _, get_kwargs = collection.resolwe.descriptor_schema.get.call_args
        self.assertEqual(get_kwargs['id'], 1)

        # descriptor schema is not set
        collection._descriptor_schema = None
        self.assertEqual(collection.descriptor_schema, None)

        # cache is cleared at update
        collection._hydrated_descriptor_schema = 'descriptor_schema'
        collection.update()
        self.assertEqual(collection._hydrated_descriptor_schema, None)

        # new collection
        collection = Collection(resolwe=MagicMock())

        collection.descriptor_schema = 'my-schema'
        self.assertEqual(collection._descriptor_schema, 'my-schema')

        collection.resolwe.descriptor_schema.get = MagicMock(return_value='descriptor_schema')
        self.assertEqual(collection.descriptor_schema, 'descriptor_schema')
        _, get_kwargs = collection.resolwe.descriptor_schema.get.call_args
        self.assertEqual(get_kwargs['slug'], 'my-schema')

        # hidrated descriptor schema
        descriptor_schema = {
            "slug": "test-schema",
            "name": "Test schema",
            "version": "1.0.0",
            "schema": [
                {
                    "default": "56G",
                    "type": "basic:string:",
                    "name": "description",
                    "label": "Object description"
                }
            ],
            "id": 1,
        }
        collection = Collection(id=1, descriptor_schema=descriptor_schema, resolwe=MagicMock())
        self.assertTrue(isinstance(collection.descriptor_schema, DescriptorSchema))
        # pylint: disable=no-member
        self.assertEqual(collection.descriptor_schema.slug, 'test-schema')
        # pylint: enable=no-member

    def test_data(self):
        collection = Collection(id=1, resolwe=MagicMock())

        # test getting data attribute
        collection.resolwe.data.filter = MagicMock(return_value=['data_1', 'data_2', 'data_3'])
        self.assertEqual(collection.data, ['data_1', 'data_2', 'data_3'])

        # test caching data attribute
        self.assertEqual(collection.data, ['data_1', 'data_2', 'data_3'])
        self.assertEqual(collection.resolwe.data.filter.call_count, 1)

        # cache is cleared at update
        collection._data = ['data']
        collection.update()
        self.assertEqual(collection._data, None)

        # raising error if collection is not saved
        collection.id = None
        with self.assertRaises(ValueError):
            _ = collection.data

    def test_samples(self):
        collection = Collection(id=1, resolwe=MagicMock())

        # test getting samples attribute
        collection.resolwe.sample.filter = MagicMock(return_value=['sample1', 'sample2'])
        self.assertEqual(collection.samples, ['sample1', 'sample2'])

        # cache is cleared at update
        collection._samples = ['sample']
        collection.update()
        self.assertEqual(collection._samples, None)

        # raising error if data collection is not saved
        collection.id = None
        with self.assertRaises(ValueError):
            _ = collection.samples

    def test_relations(self):
        collection = Collection(id=1, resolwe=MagicMock())

        # test getting relations attribute
        collection.resolwe.relation.filter = MagicMock(return_value=['relation1', 'relation2'])
        self.assertEqual(collection.relations, ['relation1', 'relation2'])

        # cache is cleared at update
        collection._relations = ['relation']
        collection.update()
        self.assertEqual(collection._relations, None)

        # raising error if data collection is not saved
        collection.id = None
        with self.assertRaises(ValueError):
            _ = collection.relations


class TestSample(unittest.TestCase):

    def test_descriptor_schema(self):
        sample = Sample(id=1, resolwe=MagicMock())
        sample._descriptor_schema = 1

        # test getting descriptor schema attribute
        sample.resolwe.descriptor_schema.get = MagicMock(return_value='descriptor_schema')
        self.assertEqual(sample.descriptor_schema, 'descriptor_schema')
        _, get_kwargs = sample.resolwe.descriptor_schema.get.call_args
        self.assertEqual(get_kwargs['id'], 1)

        # descriptor schema is not set
        sample._descriptor_schema = None
        self.assertEqual(sample.descriptor_schema, None)

        # cache is cleared at update
        sample._hydrated_descriptor_schema = 'descriptor_schema'
        sample.update()
        self.assertEqual(sample._hydrated_descriptor_schema, None)

        # new collection
        sample = Sample(resolwe=MagicMock())

        sample.descriptor_schema = 'my-schema'
        self.assertEqual(sample._descriptor_schema, 'my-schema')

        sample.resolwe.descriptor_schema.get = MagicMock(return_value='descriptor_schema')
        self.assertEqual(sample.descriptor_schema, 'descriptor_schema')
        _, get_kwargs = sample.resolwe.descriptor_schema.get.call_args
        self.assertEqual(get_kwargs['slug'], 'my-schema')

        # hidrated descriptor schema
        descriptor_schema = {
            "slug": "test-schema",
            "name": "Test schema",
            "version": "1.0.0",
            "schema": [
                {
                    "default": "56G",
                    "type": "basic:string:",
                    "name": "description",
                    "label": "Object description"
                }
            ],
            "id": 1,
        }
        sample = Sample(id=1, descriptor_schema=descriptor_schema, resolwe=MagicMock())
        self.assertTrue(isinstance(sample.descriptor_schema, DescriptorSchema))
        # pylint: disable=no-member
        self.assertEqual(sample.descriptor_schema.slug, 'test-schema')
        # pylint: enable=no-member

    def test_data(self):
        sample = Sample(id=1, resolwe=MagicMock())

        # test getting data attribute
        sample.resolwe.data.filter = MagicMock(return_value=['data_1', 'data_2', 'data_3'])
        self.assertEqual(sample.data, ['data_1', 'data_2', 'data_3'])

        # test caching data attribute
        self.assertEqual(sample.data, ['data_1', 'data_2', 'data_3'])
        self.assertEqual(sample.resolwe.data.filter.call_count, 1)

        # cache is cleared at update
        sample._data = ['data']
        sample.update()
        self.assertEqual(sample._data, None)

        # raising error if sample is not saved
        sample.id = None
        with self.assertRaises(ValueError):
            _ = sample.data

    def test_collections(self):
        sample = Sample(id=1, resolwe=MagicMock())
        sample._original_values = {'collections': [1, 2, 3]}

        # test getting data attribute
        sample.resolwe.collection.filter = MagicMock(
            return_value=['collection_1', 'collection_2', 'collection_3'])
        self.assertEqual(sample.collections, ['collection_1', 'collection_2', 'collection_3'])

        # test caching data attribute
        self.assertEqual(sample.collections, ['collection_1', 'collection_2', 'collection_3'])
        self.assertEqual(sample.resolwe.collection.filter.call_count, 1)

        # cache is cleared at update
        sample._collections = ['collection']
        sample.update()
        self.assertEqual(sample._collections, None)

        # raising error if sample is not saved
        sample.id = None
        with self.assertRaises(ValueError):
            _ = sample.collections

    @patch('resdk.resources.sample.Sample', spec=True)
    def test_update_descriptor(self, sample_mock):
        sample_mock.configure_mock(id=42, api=MagicMock())
        Sample.update_descriptor(sample_mock, {'field': 'value'})
        sample_mock.api(42).patch.assert_called_once_with({u'descriptor': {'field': 'value'}})

    @patch('resdk.resources.sample.Sample', spec=True)
    def test_confirm_is_annotated(self, sample_mock):
        sample_mock.configure_mock(endpoint='sample', id=42, api=MagicMock(), logger=MagicMock())
        Sample.confirm_is_annotated(sample_mock)
        sample_mock.api(42).patch.assert_called_once_with({'descriptor_completed': True})


if __name__ == '__main__':
    unittest.main()
