# Copyright 2018 Cristian Mattarei
#
# Licensed under the modified BSD (3-clause BSD) License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cosa.encoders.factory import ModelParsersFactory, VERILOG_INTERNAL, VERILOG_YOSYS_BTOR


def config_system():
    ModelParsersFactory.verilog_encoder = VERILOG_INTERNAL
