from datarobot.utils import encode_utf8_if_py2

from datarobot.models.api_object import APIObject
import trafaret as t


class MissingValuesReport(APIObject):
    """ A Missing Values report for a particular model

    The report breaks down for each relevant feature how many missing values it had and how each
    task treated missing values.

    The report is an iterable containing
    :py:class:`datarobot.models.missing_report.MissingReportPerFeature`
    """
    _converter = t.Dict({
        t.Key('missing_values_report'):
            t.List(t.Dict({
                'feature': t.String,
                'type': t.String,
                'missing_count': t.Int,
                'missing_percentage': t.Float(),
                'tasks': t.Mapping(t.String, t.Dict({'name': t.String,
                                                     'descriptions': t.List(t.String)
                                                     }).ignore_extra('*')
                                   )
            }).ignore_extra('*'))
    }).ignore_extra('*')

    def __init__(self, missing_values_report):
        self._reports_per_feature = [MissingReportPerFeature(data) for data in
                                     missing_values_report]

    def __iter__(self):
        return iter(self._reports_per_feature)

    @classmethod
    def get(cls, project_id, model_id):
        """ Retrieve a missing report.

        Parameters
        ----------
        project_id : str
            The project's id.
        model_id : str
            The model's id.

        Returns
        -------
        MissingValuesReport
            The queried missing report.
        """
        url = 'projects/{}/models/{}/missingReport/'.format(project_id, model_id)
        return cls.from_location(url)


class MissingReportPerTask(object):
    """Represents how a particular task handled missing values

    Attributes
    ----------
    id : basestring
        the id of the task, corresponding to the same ids used by
        :py:class:`datarobot.models.blueprint.BlueprintChart`
    name : basestring
        the name of the task, e.g. "One-Hot Encoding". These are values that appear in the
        :py:class:`datarobot.models.Model`'s `processes` attribute.
    descriptions : list of basestring
        human readable aggregated information about how the task handles
        missing values. The following descriptions may be present: what value is imputed for
        missing values, whether the feature being missing is itself treated as a feature by the
        task, whether missing values are treated as infrequent values, whether infrequent values
        are treated as missing values, and whether missing values are ignored.
    """

    def __init__(self, task_id, info):
        self.id = task_id
        self.name = info['name']
        self.descriptions = info['descriptions']

    def __repr__(self):
        return encode_utf8_if_py2(u'MissingReportPerTask(id={}, name={}, descriptions={})'
                                  .format(self.id, self.name, self.descriptions))

    def __eq__(self, other):
        return all([self.id == other.id,
                    self.name == other.name,
                    self.descriptions == other.descriptions])


class MissingReportPerFeature(object):
    """Represents how missing values were handled for a particular feature

    Attributes
    ----------
    feature : basestring
        the name of the feature
    type : str
        the type of the feature, e.g. 'Categorical' or 'Numeric'
    missing_count : int
        the number of rows from the model's training data where the feature was missing
    missing_percentage : float
        the percentage of the model's training data where the feature was missing, as a float
        between 0.0 and 100.0
    tasks : list of MissingReportPerTask
        information about how tasks within the model handled missing values for this feature
    """
    def __init__(self, report_per_feature_dict):
        self.feature = report_per_feature_dict['feature']
        self.type = report_per_feature_dict['type']
        self.missing_count = report_per_feature_dict['missing_count']
        self.missing_percentage = report_per_feature_dict['missing_percentage'] * 100
        self.tasks = [MissingReportPerTask(task_id, task_info) for task_id, task_info in
                      report_per_feature_dict['tasks'].items()]

    def __repr__(self):
        return encode_utf8_if_py2(
            u'MissingReportPerFeature(feature={}, type={})'.format(self.feature, self.type)
        )

    def __eq__(self, other):
        return all([self.feature == other.feature,
                    self.type == other.type,
                    self.missing_count == other.missing_count,
                    self.missing_percentage == other.missing_percentage,
                    self.tasks == other.tasks])
