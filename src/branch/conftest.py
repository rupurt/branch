import pytest
from result import Ok, Err
import branch.core


@pytest.fixture()
def storage_location(tmp_path):
    return f"local://{tmp_path}"


@pytest.fixture()
def local_adapter(tmp_path):
    match branch.core.adapter(location=f"local://{tmp_path}"):
        case Ok(adapter):
            return adapter
        case Err(reason):
            raise reason
