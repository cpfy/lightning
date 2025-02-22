# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
from torch import nn

from pytorch_lightning.core.module import LightningModule
from pytorch_lightning.demos.boring_classes import BoringModel
from pytorch_lightning.utilities.meta import init_meta_context, is_on_meta_device, materialize_module
from tests_pytorch.helpers.runif import RunIf


class MLP(nn.Module):
    def __init__(self, num_layers: int):
        super().__init__()
        self.layer = nn.Sequential(*[nn.Linear(1, 1) for _ in range(num_layers)] + [nn.Dropout(), nn.LayerNorm(1)])


class SimpleBoringModel(LightningModule):
    def __init__(self, num_layers: int):
        super().__init__()
        self.save_hyperparameters()
        self.layer = nn.Sequential(*[nn.Linear(1, 1) for _ in range(self.hparams.num_layers)])


@RunIf(min_torch="1.10.0", max_torch="1.12.0", standalone=True)
def test_init_meta_context():

    with init_meta_context():
        m = nn.Linear(in_features=1, out_features=1)
        assert isinstance(m, nn.Linear)
        assert m.weight.device.type == "meta"
        assert is_on_meta_device(m)
        mlp = MLP(4)
        assert mlp.layer[0].weight.device.type == "meta"

        mlp = materialize_module(mlp)
        assert mlp.layer[0].weight.device.type == "cpu"

        assert not is_on_meta_device(mlp)
        assert not is_on_meta_device(nn.Module())

        model = SimpleBoringModel(4)
        assert model.layer[0].weight.device.type == "meta"
        materialize_module(model)
        assert model.layer[0].weight.device.type == "cpu"

    mlp = MLP(4)
    assert mlp.layer[0].weight.device.type == "cpu"
    # no-op as already materialized.
    materialize_module(mlp)
    assert mlp.layer[0].weight.device.type == "cpu"

    m = nn.Linear(in_features=1, out_features=1)
    assert m.weight.device.type == "cpu"

    with init_meta_context():
        m = nn.Linear(in_features=1, out_features=1)
        assert m.weight.device.type == "meta"

    m = nn.Linear(in_features=1, out_features=1)
    assert m.weight.device.type == "cpu"


@RunIf(min_torch="1.10.0", max_torch="1.12.0", standalone=True)
def test_materialize_module_recursive_child():
    """Test materialize_module doesn't set a child recursively to a model instantiated within init_meta_context."""
    with init_meta_context():
        model = BoringModel()

    materialize_module(model)

    with pytest.raises(AttributeError, match="'Linear' object has no attribute 'layer'"):
        model.layer.layer
