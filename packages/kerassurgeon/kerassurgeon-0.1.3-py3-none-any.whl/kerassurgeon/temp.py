import numpy as np
from kerassurgeon import utils
from keras import backend as k
from keras.models import Model

def get_apoz(model, layer, x_val, node_indices=None):
    """Identify neurons with high Average Percentage of Zeros (APoZ).

    The APoZ a.k.a. (A)verage (P)ercentage (o)f activations equal to (Z)ero,
    is a metric for the usefulness of a channel defined in this paper:
    "Network Trimming: A Data-Driven Neuron Pruning Approach towards Efficient
    Deep Architectures" - [Hu et al. (2016)][]
    `high_apoz()` enables the pruning methodology described in this paper to be
    replicated.

    If node_indices are not specified and the layer is shared within the model
    the APoZ will be calculated over all instances of the shared layer.

    Args:
        model: A Keras model.
        layer: The layer whose channels will be evaluated for pruning.
        x_val: The input of the validation set. This will be used to calculate
            the activations of the layer of interest.
        node_indices(list[int]): (optional) A list of node indices.

    Returns:
        List of the APoZ values for each channel in the layer.
    """

    if isinstance(layer, str):
        layer = model.get_layer(name=layer)

    # Check that layer is in the model
    if layer not in model.layers:
        raise ValueError('layer is not a valid Layer in model.')

    layer_node_indices = utils.find_nodes_in_model(model, layer)
    # If no nodes are specified, all of the layer's inbound nodes which are
    # in model are selected.
    if not node_indices:
        node_indices = layer_node_indices
    # Check for duplicate node indices
    elif len(node_indices) != len(set(node_indices)):
        raise ValueError('`node_indices` contains duplicate values.')
    # Check that all of the selected nodes are in the layer
    elif not set(node_indices).issubset(layer_node_indices):
        raise ValueError('One or more nodes specified by `layer` and '
                         '`node_indices` are not in `model`.')

    data_format = getattr(layer, 'data_format', 'channels_last')
    # Perform the forward pass and get the activations of the layer.
    mean_calculator = utils.MeanCalculator(sum_axis=0)
    for node_index in node_indices:
        act_layer, act_index = utils.find_activation_layer(layer, node_index)
        # Get activations
        get_activations = k.function(
            [utils.single_element(model.inputs), k.learning_phase()],
            [act_layer.get_output_at(act_index)])

        if hasattr(x_val, "__iter__"):
            max_steps = x_val.n // x_val.batch_size
            steps = 0
            for batch in x_val:
                zeros = get_zeros(batch, data_format, get_activations)
                mean_calculator.add(zeros)
                steps += 1
                if steps == max_steps:
                    break

        else:
            zeros = get_zeros(x_val, data_format, get_activations)
            mean_calculator.add(zeros)

    return mean_calculator.calculate()


def get_zeros(batch, data_format, get_activations):
    a = get_activations([batch, 0])[0]
    activations = make_activations_uniform(a, data_format)
    zeros = (activations == 0).astype(int)
    return zeros


def make_activations_uniform(activations, data_format):
    # Ensure that the channels axis is last
    if data_format == 'channels_first':
        activations = np.swapaxes(activations, 1, -1)
    # Flatten all except channels axis
    return np.reshape(activations, [-1, activations.shape[-1]])