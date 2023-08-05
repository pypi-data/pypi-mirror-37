from xvector.XRequest import XRequest
import pandas


class DataSetException(Exception):
    pass


class DataSet:
    _id = None
    _type = None
    _column_metadata = None
    _published = None
    _keywords = None
    _derived = None
    _measures = None
    _dimensions = None
    _name = None

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def column_metadata(self):
        return self._column_metadata

    @property
    def published(self):
        return self._published

    @property
    def keywords(self):
        return self._keywords

    @property
    def derived(self):
        return self._derived

    @property
    def measures(self):
        return self._measures

    @property
    def dimensions(self):
        return self._dimensions

    @property
    def name(self):
        return self._name

    def __init__(self, **kwargs):
        if 'id' in kwargs:
            self._id = kwargs.get('id')
        if 'type' in kwargs:
            self._type = kwargs.get('type')
        if 'column_metadata' in kwargs:
            self._column_metadata = kwargs.get('column_metadata')
        if 'published' in kwargs:
            self._published = kwargs.get('published')
        if 'keywords' in kwargs:
            self._keywords = kwargs.get('keywords')
        if 'derived' in kwargs:
            self._derived = kwargs.get('derived')
        if 'measures' in kwargs:
            self._measures = kwargs.get('measures')
        if 'dimensions' in kwargs:
            self._dimensions = kwargs.get('dimensions')
        if 'name' in kwargs:
            self._name = kwargs.get('name')

    @property
    def row_count(self):
        if not self.id:
            raise DataSetException("Dataset id not found; cannot perform operation")
        r = XRequest.get('/api/xdata/{xdata_id}/row-count'.format(xdata_id=self.id))
        return r.get('rows')

    def to_pandas(self, rows=100):
        if not self.id:
            raise DataSetException('Dataset id is not found, please assign Id to dataset')
        r = XRequest.get('/api/xdata/{xdata_id}/dataframe?n={rows}'.format(xdata_id=self.id, rows=rows))
        df = pandas.DataFrame(data=r.get('rows'), columns=[column.get('name') for column in r.get('column_metadata')])
        return df

    @staticmethod
    def get_all_datasets():
        datasets = XRequest.get('/api/xdata')
        _dataset_list = []
        for dataset in datasets:
            _dataset = DataSet(**dataset)
            _dataset_list.append(_dataset)
        return _dataset_list
