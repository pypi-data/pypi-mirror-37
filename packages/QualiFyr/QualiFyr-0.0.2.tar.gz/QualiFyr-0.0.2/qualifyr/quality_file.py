import sys
from qualifyr.utility import get_logger

logger = get_logger(__file__)
class QualityFile:
    file_type = None

    def __init__(self, file_path, file_id = None):
        self.file_path = file_path
        self.metrics = {}
        self.failure_reasons = None
        self.file_id = file_id
        
        self.parse()

    def parse(self):
        raise NotImplementedError
    
    def type_and_id(self):
        if self.file_id:
            return '{0} {1}'.format(self.file_type, self.file_id)
        else:
            return self.file_type

    def overall_qc_category(self):
        failure_categories = [failure_reason[0] for failure_reason in self.failure_reasons]
        if 'FAILURE' in failure_categories:
            return 'FAILURE'
        elif 'WARNING' in failure_categories:
            return 'WARNING'
        else:
            return 'PASS'

    def check(self, conditions):
        # check all condition keys exist
        # loop through conditions and apply condition, one of gt,lt,lt_gt,eq,ne
        # return  true, false ??? conditions that fail

        self.failure_reasons = []
        # extract conditions for file type
        try:
            conditions_for_file_type = conditions[self.file_type]
        except KeyError as e:
            logger.error("No such quality file type {0} in conditions. The available file types in the supplied condition file are {1}".format(e, ", ".join(conditions.keys())))

        self.conditions = conditions_for_file_type
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
                                self.failure_reasons.append((category.upper(), '{0} ({1}): > {2}'.format(metric_name, metric_value, condition_value)))
                                break
                        # less than
                        elif condition_type == 'lt':
                            if metric_value < condition_value:
                                self.failure_reasons.append((category.upper(), '{0} ({1}): < {2}'.format(metric_name, metric_value, condition_value)))
                                break
                        # less than and greater than
                        elif condition_type == 'lt_gt':
                            if (metric_value < condition_value[0] or metric_value > condition_value[1]):
                                self.failure_reasons.append((category.upper(), '{0} ({1}) < {2} and/or > {3}'.format(metric_name, metric_value, condition_value[0], condition_value[1])))
                                break
                        # equal to
                        elif condition_type == 'eq':
                            if metric_value == condition_value:
                                self.failure_reasons.append((category.upper(), '{0} ({1}): equals {2}'.format(metric_name,metric_value, condition_value)))
                                break
                        # less than and greater than
                        elif condition_type == 'ne':
                            if metric_value != condition_value:
                                self.failure_reasons.append((category.upper(), '{0} ({1}): does not equal {2}'.format(metric_name,metric_value, condition_value)))
                                break
                        # any
                        elif condition_type == 'any':
                            if metric_value in condition_value:
                                self.failure_reasons.append((category.upper(), '{0} ({1}): one of {2}'.format(metric_name,metric_value, ', '.join(condition_value))))
                                break
            except KeyError as e:
                logger.error("No such metric {0}. The available metrics are {1}".format(e, ", ".join(self.metrics.keys())))

    @staticmethod
    def check_multiple(quality_files, conditions):
        # returns multi_file_failure_reasons. key is quality file type (and if if supplied - e,g multiple fastqs)
        # value is a list of failure reasons - these are tuples of strings (failure level, failure reason)
        for quality_file in quality_files:
            quality_file.check(conditions)
    
    @staticmethod
    def multiple_overall_qc_category(quality_files):
        failure_categories = [quality_file.overall_qc_category() for quality_file in quality_files]
        if 'FAILURE' in failure_categories:
            return 'FAILURE'
        elif 'WARNING' in failure_categories:
            return 'WARNING'
        else:
            return 'PASS'

    @staticmethod
    def print_multiple_file_qc(quality_files, conditions):
        # update quality for each quality file object
        QualityFile.check_multiple(quality_files, conditions)
        sys.stdout.write('{0}\n'.format(QualityFile.multiple_overall_qc_category(quality_files)))
        for quality_file in quality_files:
            for failure_reason in quality_file.failure_reasons:
                sys.stderr.write('{0}\t{1}\t{2}\n'.format(quality_file.type_and_id(), failure_reason[0], failure_reason[1]))
            