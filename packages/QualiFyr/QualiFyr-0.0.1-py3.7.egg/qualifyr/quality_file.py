from qualifyr.utility import get_logger

logger = get_logger(__file__)
class QualityFile:
    file_type = None

    def __init__(self, file_path):
        self.file_path = file_path
        self.metrics = {}
    
    def check(self, conditions):
        # check all condition keys exist
        # loop through conditions and apply condition, one of gt,lt,lt_gt,eq,ne
        # return  true, false ??? conditions that fail

        failure_reasons = []

        # extract conditions for file type
        try:
            conditions_for_file_type = conditions[self.file_type]
        except KeyError as e:
            logger.error("No such quality file type {0} in conditions. The available file types in the supplied condition file are {1}".format(e, ", ".join(conditions.keys())))

        for metric_name in conditions_for_file_type:
            try:
                metric_value = self.metrics[metric_name]
                for category in ['warning', 'failure']:
                    if category in conditions_for_file_type[metric_name]:
                        condition_type = conditions_for_file_type[metric_name][category]['condition_type']
                        condition_value = conditions_for_file_type[metric_name][category]['condition_value']
                        # possible conditions
                        # greater than
                        if condition_type == 'gt':
                            if metric_value > condition_value:
                                failure_reasons.append('{0}. {1} ({2}): > {3}'.format(category.upper(), metric_name, metric_value, condition_value))
                                break
                        # less than
                        elif condition_type == 'lt':
                            if metric_value < condition_value:
                                failure_reasons.append('{0}. {1} ({2}): < {3}'.format(category.upper(), metric_name, metric_value, condition_value))
                                break
                        # less than and greater than
                        elif condition_type == 'lt_gt':
                            if (metric_value < condition_value[0] or metric_value > condition_value[1]):
                                failure_reasons.append('{0}. {1} ({2}) < {3} and/or > {4}'.format(category.upper(), metric_name, metric_value, condition_value[0], condition_value[1]))
                                break
                        # equal to
                        elif condition_type == 'eq':
                            if metric_value == condition_value:
                                failure_reasons.append('{0}. {1} ({2}): equals {3}'.format(category.upper(), metric_name,metric_value, condition_value))
                                break
                        # less than and greater than
                        elif condition_type == 'ne':
                            if metric_value != condition_value:
                                failure_reasons.append('{0}: {1} ({2}): does not equal {3}'.format(category.upper(), metric_name,metric_value, condition_value))
                                break
                        # any
                        elif condition_type == 'any':
                            if metric_value in condition_value:
                                failure_reasons.append('{0}: {1} ({2}): one of {3}'.format(category.upper(), metric_name,metric_value, ', '.join(condition_value)))
                                break
            except KeyError as e:
                logger.error("No such metric {0}. The available metrics are {1}".format(e, ", ".join(self.metrics.keys())))
        return failure_reasons

    @staticmethod
    def check_multiple(quality_files, conditions):
        multi_file_failure_reasons = {}
        for quality_file in quality_files:
            failure_reasons = quality_file.check(conditions)
            if len(failure_reasons) != 0:
                multi_file_failure_reasons[quality_file.file_type] = failure_reasons
        return multi_file_failure_reasons
