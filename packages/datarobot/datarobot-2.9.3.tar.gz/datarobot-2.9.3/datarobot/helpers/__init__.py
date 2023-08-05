from .partitioning_methods import *  # noqa


class AdvancedOptions(object):
    """
    Used when setting the target of a project to set advanced options of modeling process.

    Parameters
    ----------
    weights : string, optional
        The name of a column indicating the weight of each row
    response_cap : float in [0.5, 1), optional
        Quantile of the response distribution to use for response capping.
    blueprint_threshold : int, optional
        Number of hours models are permitted to run before being excluded from later autopilot
        stages
        Minimum 1
    seed : int
        a seed to use for randomization
    smart_downsampled : bool
        whether to use smart downsampling to throw away excess rows of the majority class.  Only
        applicable to classification and zero-boosted regression projects.
    majority_downsampling_rate : float
        the percentage between 0 and 100 of the majority rows that should be kept.  Specify only if
        using smart downsampling.  May not cause the majority class to become smaller than the
        minority class.
    offset : list of str, optional
        (New in version v2.6) the list of the names of the columns containing the offset
        of each row
    exposure : string, optional
        (New in version v2.6) the name of a column containing the exposure of each row
    accuracy_optimized_mb : bool, optional
        (New in version v2.6) Include additional, longer-running models that will be run by the
        autopilot and available to run manually.
    scaleout_modeling_mode : string, optional
        (New in version v2.8) Specifies the behavior of Scaleout models for the project.
        This is one of ``datarobot.enums.SCALEOUT_MODELING_MODE``.
        If ``datarobot.enums.SCALEOUT_MODELING_MODE.DISABLED``, no
        models will run during autopilot or show in the list of available blueprints.
        Scaleout models must be disabled for some partitioning settings including projects
        using datetime partitioning or projects using offset or exposure columns.
        If ``datarobot.enums.SCALEOUT_MODELING_MODE.REPOSITORY_ONLY``,
        scaleout models will be in the list of available blueprints
        but not run during autopilot.
        If ``datarobot.enums.SCALEOUT_MODELING_MODE.AUTOPILOT``,
        scaleout models will run during autopilot and be in the list of
        available blueprints.
        Scaleout models are only supported in the Hadoop enviroment with
        the corresponding user permission set.
    events_count : string, optional
        (New in version v2.8) the name of a column specifying events count.

    Examples
    --------
    .. code-block:: python

        import datarobot as dr
        advanced_options = dr.AdvancedOptions(
            weights='weights_column',
            offset=['offset_column'],
            exposure='exposure_column',
            response_cap=0.7,
            blueprint_threshold=2,
            smart_downsampled=True, majority_downsampling_rate=75.0)

    """
    def __init__(self, weights=None, response_cap=None, blueprint_threshold=None,
                 seed=None, smart_downsampled=False, majority_downsampling_rate=None,
                 offset=None, exposure=None, accuracy_optimized_mb=None,
                 scaleout_modeling_mode=None, events_count=None):
        self.weights = weights
        self.response_cap = response_cap
        self.blueprint_threshold = blueprint_threshold
        self.seed = seed
        self.smart_downsampled = smart_downsampled
        self.majority_downsampling_rate = majority_downsampling_rate
        self.offset = offset
        self.exposure = exposure
        self.accuracy_optimized_mb = accuracy_optimized_mb
        self.scaleout_modeling_mode = scaleout_modeling_mode
        self.events_count = events_count

    def collect_payload(self):

        payload = dict(
            weights=self.weights,
            response_cap=self.response_cap,
            blueprint_threshold=self.blueprint_threshold,
            seed=self.seed,
            smart_downsampled=self.smart_downsampled,
            majority_downsampling_rate=self.majority_downsampling_rate,
            offset=self.offset,
            exposure=self.exposure,
            accuracy_optimized_mb=self.accuracy_optimized_mb,
            scaleout_modeling_mode=self.scaleout_modeling_mode,
            events_count=self.events_count,
        )
        return payload
