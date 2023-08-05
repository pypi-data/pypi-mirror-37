# Copyright (c) Microsoft Corporation. All rights reserved.
from .engineapi.typedefinitions import FieldType
from typing import List, Dict


class TypeConverter:
    def __init__(self, data_type: FieldType):
        self.data_type = data_type


class DateTimeConverter(TypeConverter):
    def __init__(self, formats: List[str]):
        super().__init__(FieldType.DATE)
        self.formats = formats


class CandidateConverter:
    def __init__(self, data_type: FieldType):
        self.data_type = data_type

    @property
    def is_valid(self):
        return True

    def __repr__(self):
        return str(self.data_type)


class CandidateDateTimeConverter(CandidateConverter):
    def __init__(self, formats: List[str], ambiguous_formats: List[List[str]]):
        super().__init__(FieldType.DATE)
        self.formats = formats
        self.ambiguous_formats = ambiguous_formats

    @CandidateConverter.is_valid.getter
    def is_valid(self):
        return not self.ambiguous_formats

    def resolve_ambiguity(self, day_first: bool):
        def _pick_format(formats: List[str]) -> str:
            for candidate_format in formats:
                day_index = candidate_format.index('%d')
                month_index = candidate_format.index('%m')
                if day_first and day_index < month_index:
                    return candidate_format
                elif not day_first and month_index < day_index:
                    return candidate_format

            raise ValueError('Unable to resolve ambiguity.')

        picked_formats = [_pick_format(possible_formats) for possible_formats in self.ambiguous_formats]
        self.formats += picked_formats
        self.ambiguous_formats = []


class InferenceInfo:
    def __init__(self, converters: List[CandidateConverter]):
        self.candidate_converters = converters

    def __repr__(self):
        return repr(self.candidate_converters)


def converter_from_candidate(candidate: CandidateConverter) -> TypeConverter:
    if isinstance(candidate, CandidateDateTimeConverter):
        if not candidate.is_valid:
            raise ValueError('Invalid candidate cannot be turned into a converter.')

        return DateTimeConverter(candidate.formats)
    else:
        return TypeConverter(candidate.data_type)


def get_converters_from_candidates(column_candidates: Dict[str, List[CandidateConverter]]) -> Dict[str, TypeConverter]:
    def _pick_candidate(column: str, candidates: List[CandidateConverter]):
        try:
            return next(converter_from_candidate(candidate) for candidate in candidates if candidate.is_valid)
        except StopIteration:
            raise ValueError('No valid candidates for column ' + column)

    return {col: _pick_candidate(col, candidates) for col, candidates in column_candidates.items()}
