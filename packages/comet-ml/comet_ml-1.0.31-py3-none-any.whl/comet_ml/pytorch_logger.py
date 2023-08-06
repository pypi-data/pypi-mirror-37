# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2015-2019 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import logging
import sys

LOGGER = logging.getLogger(__name__)

PYTORCH_ALREADY_IMPORTED_MSG = (
    "Please import comet before importing any torch modules"
)

def tensor_backward(experiment, original, result, *args, **kwargs):
    # args[0] is self, the Tensor (loss):
    try:
        if experiment.curr_step is None:
            experiment.set_step(0)
        else:
            experiment.set_step(experiment.curr_step + 1)
        model = experiment._storage["torch"].get("model", None)
        if (experiment.curr_step == 0 and model is not None):
            experiment.set_model_graph(str(model))
        loss = args[0]
        experiment.log_metric("loss", loss.data.item(), step=experiment.curr_step)
    except Exception:
        LOGGER.info("Failed to run Tensor.backward logger")
    return result

def model_constructor(experiment, original, *args, **kwargs):
    ## Assume the first one is the model:
    try:
        model = experiment._storage["torch"].get("model", None)
        if model is None:
            experiment._storage["torch"]["model"] = args[1]
    except Exception:
        LOGGER.info("Failed to run Module.__init__ logger")

def patch(module_finder):
    ## For testing:
    if "torch" in sys.modules:
        LOGGER.warning(PYTORCH_ALREADY_IMPORTED_MSG)
    ## For each backpropagation of the gradient:
    module_finder.register_after("torch.tensor",
                                 "Tensor.backward",
                                 tensor_backward)
    ## For each model constructor:
    module_finder.register_after("torch.nn.modules.module",
                                 "Module.__init__",
                                 model_constructor)

if "torch" in sys.modules:
    raise SyntaxError(PYTORCH_ALREADY_IMPORTED_MSG)
