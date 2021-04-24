from typing import Dict, List
from ..models import Context


class Merger():
    @staticmethod
    def combine(context: Context,
                attributes: List[str]) -> List[Dict[str, str]]:
        combination: List[Dict[str, str]] = [
            {} for _ in range(len(context))
        ]

        for attribute in attributes:
            for i, item in enumerate(context.get(attribute)):
                if len(item) > 0:
                    combination[i][attribute] = item

        return combination

    @staticmethod
    def take_first(x1_list: List[str],
                   x2_list: List[str]) -> List[str]:
        x1_n = len(x1_list)
        x2_n = len(x2_list)

        if x1_n != x2_n:
            raise ValueError(f'length mismatch - x1 is {x1_n}, x2 is {x2_n}')

        combination = []
        for i in range(x1_n):
            x1_item = x1_list[i]
            if len(x1_item):
                combination.append(x1_item)
            else:
                combination.append(x2_list[i])

        return combination

    @staticmethod
    def generate_sentence(tokens: List[str], spacings: List[str]) -> str:
        text = ''
        for i, token in enumerate(tokens):
            space = ' ' if spacings[i] == 'yes' else ''
            text += f'{token}{space}'

        return text
