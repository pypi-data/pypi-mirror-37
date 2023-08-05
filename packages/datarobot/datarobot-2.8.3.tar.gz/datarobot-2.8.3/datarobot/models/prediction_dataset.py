import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils import parse_time


class PredictionDataset(APIObject):

    """ A dataset uploaded to make predictions

    Typically created via `project.upload_dataset`

    Attributes
    ----------
    id : str
        the id of the dataset
    project_id : str
        the id of the project the dataset belongs to
    created : str
        the time the dataset was created
    name : str
        the name of the dataset
    num_rows : int
        the number of rows in the dataset
    num_columns : int
        the number of columns in the dataset
    forecast_point : datetime.datetime or None
        Only specified in time series projects.  The point relative to which predictions will be
        generated, based on the forecast window of the project.
    """

    _path_template = 'projects/{}/predictionDatasets/{}/'

    _converter = t.Dict({
        t.Key('id'): t.String(),
        t.Key('project_id'): t.String(),
        t.Key('created'): t.String(),
        t.Key('name'): t.String(),
        t.Key('num_rows'): t.Int(),
        t.Key('num_columns'): t.Int(),
        t.Key('forecast_point', optional=True): parse_time
    }).allow_extra('*')

    def __init__(self, project_id, id, name, created, num_rows, num_columns, forecast_point=None):
        self.project_id = project_id
        self.id = id
        self.name = name
        self.created = created
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.forecast_point = forecast_point
        self._path = self._path_template.format(project_id, id)

    def __repr__(self):
        return 'PredictionDataset({!r})'.format(self.name)

    @classmethod
    def get(cls, project_id, dataset_id):
        """
        Retrieve information about a dataset uploaded for predictions

        Parameters
        ----------
        project_id:
            the id of the project to query
        dataset_id:
            the id of the dataset to retrieve

        Returns
        -------
        dataset: PredictionDataset
            A dataset uploaded to make predictions
        """
        path = cls._path_template.format(project_id, dataset_id)
        return cls.from_location(path)

    def delete(self):
        """ Delete a dataset uploaded for predictions

        Will also delete predictions made using this dataset and cancel any predict jobs using
        this dataset.
        """
        self._client.delete(self._path)
