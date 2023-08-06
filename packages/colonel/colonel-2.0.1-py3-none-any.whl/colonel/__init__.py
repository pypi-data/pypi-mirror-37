# Copyright 2018 The NLP Odyssey Authors.
# Copyright 2018 Marco Nicola <marconicola@disroot.org>
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

"""Colonel - a Python 3 library for handling CoNLL data formats"""

from colonel.sentence import Sentence
from colonel.word import Word
from colonel.emptynode import EmptyNode
from colonel.multiword import Multiword
from colonel.upostag import UposTag
from colonel import conllu

__all__ = [
    'Sentence',
    'Word',
    'EmptyNode',
    'Multiword',
    'UposTag',
    'conllu'
]
