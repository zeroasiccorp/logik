# Copyright 2024 Zero ASIC Corporation
# Licensed under the MIT License (see LICENSE for details)

import pytest
import siliconcompiler

from logiklib.demo.logik_demo import logik_demo


@pytest.mark.parametrize(
    "part",
    [
        logik_demo,
    ])
def test_file_paths(part):
    chip = siliconcompiler.Chip("test")
    chip.use(part)

    assert chip.check_filepaths()
