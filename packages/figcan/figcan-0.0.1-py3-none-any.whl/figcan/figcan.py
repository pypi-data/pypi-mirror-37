"""Fig Can - Simple Python Configuration Management
"""
# Copyright (c) 2018 Shoppimon LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from collections.abc import Mapping as BaseMapping
from copy import deepcopy
from typing import Iterable  # noqa: F401
from typing import Any, Dict, Generator, Iterator, Optional, Tuple


class Configuration(BaseMapping):
    """Configuration container
    """
    def __init__(self, base_config: dict):
        self._data = deepcopy(base_config)
        self._flat_pointers = {}  # type: Dict[Tuple[str, ...], Tuple[Dict[str, Any], str]]

    def apply(self, config: dict, raise_on_unknown_key: bool = True) -> None:
        """Apply additional configuration from a dictionary

        This will look for dictionary items that exist in the base_config any apply their values on the current
        configuration object
        """
        _recursive_merge(self._data, config, raise_on_unknown_key)

    def apply_object(self, config_obj: Any, apply_on: Optional[Tuple[str, ...]] = None) -> None:
        """Apply additional configuration from any Python object

        This will look for object attributes that exist in the base_config and apply their values  on the current
        configuration object
        """
        self._init_flat_pointers()
        try:
            config_obj_keys = vars(config_obj).keys()  # type: Iterable[str]
        except TypeError:
            config_obj_keys = filter(lambda k: k[0] != '_', dir(config_obj))

        for config_key in config_obj_keys:
            if apply_on:
                flat_key = apply_on + (config_key, )
            else:
                flat_key = (config_key, )

            if flat_key in self._flat_pointers:
                container, orig_key = self._flat_pointers[flat_key]
                container[orig_key] = getattr(config_obj, config_key)

    def apply_flat(self, config: dict, namespace_separator: str = '_', prefix: str = ''):
        """Apply additional configuration from a flattened dictionary

        This will look for dictionary items that match flattened keys from base_config and apply their values on the
        current configuration object.

        This can be useful for applying configuration from environment variables and flat configuration file formats
        such as INI files.
        """
        self._init_flat_pointers()
        for key_stack, (container, orig_key) in self._flat_pointers.items():
            flat_key = '{prefix}{joined_key}'.format(prefix=prefix, joined_key=namespace_separator.join(key_stack))
            if flat_key in config:
                container[orig_key] = config[flat_key]

    def _init_flat_pointers(self):
        if len(self._flat_pointers) > 0:
            return
        self._flat_pointers = {ks: (container, k) for ks, container, k in _create_flat_pointers(self._data)}

    def __getitem__(self, k: str) -> Any:
        return self._data[k]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)


def _recursive_merge(dct: Dict[str, Any], merge_dct: Dict[str, Any], raise_on_missing: bool) -> dict:
    """Recursive dict merge

    This modifies `dct` in place. Use `copy.deepcopy` if this behavior is not desired.
    """
    for k, v in merge_dct.items():
        if k in dct:
            if isinstance(dct[k], dict) and isinstance(merge_dct[k], BaseMapping):
                dct[k] = _recursive_merge(dct[k], merge_dct[k], raise_on_missing)
            else:
                dct[k] = merge_dct[k]
        else:
            message = "Unknown configuration key: '{k}'".format(k=k)
            if raise_on_missing:
                raise KeyError(message)
            else:
                logging.getLogger(__name__).warning(message)

    return dct


def _create_flat_pointers(dct: Dict[str, Any], key_stack: Tuple[str, ...] = ()) -> \
        Generator[Tuple[Tuple[str, ...], Dict[str, Any], str], None, None]:
    """Create a flattened dictionary of "key stacks" -> (value container, key)
    """
    for k in dct.keys():
        current_key = key_stack + (k,)
        if isinstance(dct[k], BaseMapping):
            yield from _create_flat_pointers(dct[k], current_key)
        else:
            yield (current_key, dct, k)
