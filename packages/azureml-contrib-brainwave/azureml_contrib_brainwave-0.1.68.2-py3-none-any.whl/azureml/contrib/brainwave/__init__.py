# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Accelerate deep neural networks on FPGAs with Project Brainwave.
"""
from .brainwave_image import BrainwaveImage
from .brainwave_webservice import BrainwaveWebservice


__all__ = ["BrainwaveWebservice", "BrainwaveImage"]
