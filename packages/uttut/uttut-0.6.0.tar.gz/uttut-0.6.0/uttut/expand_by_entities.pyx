# cython: profile=True
# cython: linetrace=False
import random
from typing import List, Tuple, Union
import numpy as np

from .elements import (
    Datum,
    Entity,
)
from .toolkits.get_kth_combination import get_kth_combination


__all__ = [
    'expand_by_entities',
]


def partition_by_entities(
        datum: Datum,
        include_orig: bool,
    ) -> Tuple[List[List[str]], List[Union[None, str]]]:
    start = 0
    parts = []
    entity_names = []
    utt = datum.utterance

    for entity in datum.entities:
        if start != entity.start:
            parts.append([utt[start: entity.start]])
            entity_names.append(None)

        if entity.no_replacements():
            part_candidates = [entity.value]
        else:
            part_candidates = sorted(list(entity.replacements))
            if include_orig:
                part_candidates.append(entity.value)
        parts.append(part_candidates)
        entity_names.append(entity.name)

        start = entity.end

    if start != len(utt):
        parts.append([utt[start:]])
        entity_names.append(None)

    return parts, entity_names


def _aggregate_entities(
        list segments,
        list entity_names,
    ):
    cdef list entities = []
    cdef int pointer = 0
    cdef int len_segment

    for seg, entity_name in zip(segments, entity_names):
        len_seg = len(seg)
        if entity_name is None:
            pointer += len_seg
            continue

        entity = Entity(
            name=entity_name,
            value=seg,
            start=pointer,
            end=pointer + len_seg
        )
        entities.append(entity)
        pointer += len_seg
    return entities


def expand_by_entities(
        datum,
        sampling_method = None,
        bint include_orig = False,
    ):
    if not datum.has_entities():
        return [datum]

    if sampling_method is None:
        sampling_method = lambda n_combinations: list(range(n_combinations))
        # return all possible combinations

    parts, entity_names = partition_by_entities(datum, include_orig)

    n_combinations = np.prod([len(part) for part in parts])
    ints = sampling_method(n_combinations)

    result = []
    for idx in ints:
        segments = get_kth_combination(parts, idx)

        utterance = ''.join(segments)
        entities = _aggregate_entities(segments, entity_names)
        new_datum = Datum(
            utterance=utterance,
            intents=datum.copy_intents(),
            entities=entities,
        )
        result.append(new_datum)
    return result
