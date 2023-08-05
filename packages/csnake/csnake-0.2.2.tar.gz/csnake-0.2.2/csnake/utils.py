# -*- coding: utf-8 -*-
"""
Small utilities that simplify common tasks.
"""
from typing import Optional
from typing import Sequence


def assure_str(supposed_str) -> str:
    if not isinstance(supposed_str, str):
        raise TypeError(f"supposed_str ({supposed_str}) must be a str")
    return supposed_str


def assure_str_or_none(supposed_str) -> Optional[str]:
    if not isinstance(supposed_str, str) and supposed_str is not None:
        raise TypeError(f"supposed_str ({supposed_str}) must be a str")
    return supposed_str


def seq_get(seq: Sequence, defaults: Sequence, index: int):
    if index < 0:
        length = len(defaults)
        index = length + index
        if index < 0:
            raise IndexError(
                "sequence index out of range in both seq and defaults"
            )
    try:
        return seq[index]
    except IndexError:
        try:
            return defaults[index]
        except IndexError:
            raise IndexError(
                "sequence index out of range in both seq and defaults"
            )
