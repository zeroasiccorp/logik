# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import pytest
import siliconcompiler

from logiklib.demo.K4_N8_6x6 import K4_N8_6x6


@pytest.mark.parametrize(
    "part",
    [
        K4_N8_6x6,
    ])
def test_file_paths(part):
    chip = siliconcompiler.Chip("test")
    chip.use(part)

    assert chip.check_filepaths()
