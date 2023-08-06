from keen.hyper_parameter_optimizer.random_search_optimizer import RandomSearchHPO
from keen.utilities import CLASS_NAME


def get_hyper_parameter_optimizer(config, evaluator):
    class_name = config[CLASS_NAME]
    if class_name == 'RandomSearchHPO':
        return RandomSearchHPO(evaluator=evaluator)
