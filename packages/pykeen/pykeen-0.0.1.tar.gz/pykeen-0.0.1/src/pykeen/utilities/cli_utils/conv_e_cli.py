# -*- coding: utf-8 -*-

"""Implementation the command line interface needed for TransE."""

from pykeen.constants import EMBEDDING_DIMENSION_PRINT_MSG, EMBEDDING_DIMENSION_PROMPT_MSG, EMBEDDING_DIMENSION_ERROR_MSG, \
    MARGIN_LOSS_PRINT_MSG, MARGIN_LOSS_PROMPT_MSG, MARGIN_LOSS_ERROR_MSG, NORM_SCORING_FUNCTION_PRINT_MSG, \
    NORM_SCORING_FUNCTION_PROMPT_MSG, NORM_SCORING_FUNCTION_ERROR_MSG, ENTITIES_NORMALIZATION_PRINT_MSG, \
    ENTITIES_NORMALIZATION_PROMPT_MSG, ENTITIES_NORMALIZATION_ERROR_MSG, LEARNING_RATE_PRINT_MSG, \
    LEARNING_RATE_PROMPT_MSG, LEARNING_RATE_ERROR_MSG, BATCH_SIZE_PRINT_MSG, BATCH_SIZE_PROMPT_MSG, \
    BATCH_SIZE_ERROR_MSG, EPOCH_PRINT_MSG, EPOCH_PROMPT_MSG, EPOCH_ERROR_MSG, EMBEDDING_DIM, SCORING_FUNCTION_NORM, \
    NORM_FOR_NORMALIZATION_OF_ENTITIES, LEARNING_RATE, BATCH_SIZE, NUM_EPOCHS, MARGIN_LOSS, \
    CONV_E_INPUT_CHANNEL_PRINT_MSG, CONV_E_INPUT_CHANNEL_PROMPT_MSG, CONV_E_INPUT_CHANNEL_ERROR_MSG, \
    CONV_E_KERNEL_HEIGHT_PRINT_MSG, CONV_E_KERNEL_HEIGHT_PROMPT_MSG, CONV_E_KERNEL_HEIGHT_ERROR_MSG, \
    CONV_E_KERNEL_WIDTH_PRINT_MSG, CONV_E_KERNEL_WIDTH_PROMPT_MSG, CONV_E_KERNEL_WIDTH_ERROR_MSG, \
    CONV_E_INPUT_DROPOUT_PRINT_MSG, CONV_E_INPUT_DROPOUT_PROMPT_MSG, CONV_E_INPUT_DROPOUT_ERROR_MSG, \
    CONV_E_OUTPUT_DROPOUT_PRINT_MSG, CONV_E_OUTPUT_DROPOUT_PROMPT_MSG, CONV_E_OUTPUT_DROPOUT_ERROR_MSG, \
    CONV_E_FEATURE_MAP_DROPOUT_PRINT_MSG, CONV_E__FEATURE_MAP_DROPOUT_PROMPT_MSG, CONV_E_FEATURE_MAP_DROPOUT_ERROR_MSG
from pykeen.utilities.cli_utils.cli_print_msg_helper import print_training_embedding_dimension_message, \
    print_embedding_dimension_info_message, print_training_margin_loss_message, print_scoring_fct_message, \
    print_section_divider, print_entity_normalization_message, print_learning_rate_message, print_batch_size_message, \
    print_number_epochs_message, print_conv_width_height_message, print_conv_input_channels_message, \
    print_conv_kernel_height_message, print_conv_kernel_width_message, print_input_dropout_message
from pykeen.utilities.cli_utils.cli_training_query_helper import select_integer_value, select_float_value, \
    query_height_and_width_for_conv_e, query_kernel_param, select_zero_one_float_value
from pykeen.utilities.cli_utils.utils import get_config_dict


def configure_conv_e_training_pipeline(model_name):
    # TODO: Finish
    exit(0)
    """Configure TransE from pipeline.

    :param str model_name: name of the model
    :rtype: OrderedDict
    :return: configuration dictionary
    """
    config = get_config_dict(model_name)

    # Step 1: Query embedding dimension
    print_training_embedding_dimension_message()
    print_embedding_dimension_info_message()
    embedding_dimension = select_integer_value(
        print_msg=EMBEDDING_DIMENSION_PRINT_MSG,
        prompt_msg=EMBEDDING_DIMENSION_PROMPT_MSG,
        error_msg=EMBEDDING_DIMENSION_ERROR_MSG
    )
    config[EMBEDDING_DIM] = embedding_dimension
    print_section_divider()

    # Step 2: Query height and width
    print_conv_width_height_message()
    height, width = query_height_and_width_for_conv_e(embedding_dimension)

    # Step 3: Query number of input channels
    print_conv_input_channels_message()
    num_input_channels = select_integer_value(CONV_E_INPUT_CHANNEL_PRINT_MSG,
                                              CONV_E_INPUT_CHANNEL_PROMPT_MSG,
                                              CONV_E_INPUT_CHANNEL_ERROR_MSG)
    print_section_divider()

    # Step 4: Query kernel height
    print_conv_kernel_height_message()
    kernel_height = query_kernel_param(depending_param=height,
                                       print_msg=CONV_E_KERNEL_HEIGHT_PRINT_MSG,
                                       prompt_msg=CONV_E_KERNEL_HEIGHT_PROMPT_MSG,
                                       error_msg=CONV_E_KERNEL_HEIGHT_ERROR_MSG)
    print_section_divider()

    # Step 5: Query kernel width
    print_conv_kernel_width_message()
    kernel_width = query_kernel_param(depending_param=height,
                                      print_msg=CONV_E_KERNEL_WIDTH_PRINT_MSG,
                                      prompt_msg=CONV_E_KERNEL_WIDTH_PROMPT_MSG,
                                      error_msg=CONV_E_KERNEL_WIDTH_ERROR_MSG)
    print_section_divider()

    # Step 6: Query dropout for input layer
    print_input_dropout_message()
    input_dropout = select_zero_one_float_value(print_msg=CONV_E_INPUT_DROPOUT_PRINT_MSG,
                                                prompt_msg=CONV_E_INPUT_DROPOUT_PROMPT_MSG,
                                                error_msg=CONV_E_INPUT_DROPOUT_ERROR_MSG)
    print_section_divider()

    # Step 7: Query dropout for output layer
    output_dropout = select_zero_one_float_value(print_msg=CONV_E_OUTPUT_DROPOUT_PRINT_MSG,
                                                 prompt_msg=CONV_E_OUTPUT_DROPOUT_PROMPT_MSG,
                                                 error_msg=CONV_E_OUTPUT_DROPOUT_ERROR_MSG)
    print_section_divider()

    # Step 8: Query feature map dropout for output layer
    feature_map_dropout = select_zero_one_float_value(print_msg=CONV_E_FEATURE_MAP_DROPOUT_PRINT_MSG,
                                                      prompt_msg=CONV_E__FEATURE_MAP_DROPOUT_PROMPT_MSG,
                                                      error_msg=CONV_E_FEATURE_MAP_DROPOUT_ERROR_MSG)
    print_section_divider()

    # Step 2: Query margin loss
    print_training_margin_loss_message()
    magin_loss = select_float_value(
        print_msg=MARGIN_LOSS_PRINT_MSG,
        prompt_msg=MARGIN_LOSS_PROMPT_MSG,
        error_msg=MARGIN_LOSS_ERROR_MSG
    )
    config[MARGIN_LOSS] = magin_loss
    print_section_divider()

    # Step 3: Query L_p norm as scoring function
    print_scoring_fct_message()
    scoring_fct_norm = select_integer_value(
        print_msg=NORM_SCORING_FUNCTION_PRINT_MSG,
        prompt_msg=NORM_SCORING_FUNCTION_PROMPT_MSG,
        error_msg=NORM_SCORING_FUNCTION_ERROR_MSG
    )
    config[SCORING_FUNCTION_NORM] = scoring_fct_norm
    print_section_divider()

    # Step 4: Query L_p norm for normalizing the entities
    print_entity_normalization_message()
    entity_normalization_norm = select_integer_value(
        print_msg=ENTITIES_NORMALIZATION_PRINT_MSG,
        prompt_msg=ENTITIES_NORMALIZATION_PROMPT_MSG,
        error_msg=ENTITIES_NORMALIZATION_ERROR_MSG
    )
    config[NORM_FOR_NORMALIZATION_OF_ENTITIES] = entity_normalization_norm
    print_section_divider()

    # Step 5: Query learning rate
    print_learning_rate_message()
    learning_rate = select_float_value(
        print_msg=LEARNING_RATE_PRINT_MSG,
        prompt_msg=LEARNING_RATE_PROMPT_MSG,
        error_msg=LEARNING_RATE_ERROR_MSG
    )
    config[LEARNING_RATE] = learning_rate
    print_section_divider()

    # Step 6: Query batch size
    print_batch_size_message()
    batch_size = select_integer_value(
        print_msg=BATCH_SIZE_PRINT_MSG,
        prompt_msg=BATCH_SIZE_PROMPT_MSG,
        error_msg=BATCH_SIZE_ERROR_MSG
    )
    config[BATCH_SIZE] = batch_size
    print_section_divider()

    # Step 7: Query number of epochs
    print_number_epochs_message()
    number_epochs = select_integer_value(
        print_msg=EPOCH_PRINT_MSG,
        prompt_msg=EPOCH_PROMPT_MSG,
        error_msg=EPOCH_ERROR_MSG
    )
    config[NUM_EPOCHS] = number_epochs
    print_section_divider()

    return config


def configure_trans_e_hpo_pipeline():
    pass
