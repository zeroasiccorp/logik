import pytest
import siliconcompiler

from logik.fpgas import logik_demo


@pytest.mark.parametrize(
    "part",
    [
        logik_demo,
    ])
def test_file_paths(part):
    chip = siliconcompiler.Chip("test")
    chip.use(part)

    assert chip.check_filepaths()
