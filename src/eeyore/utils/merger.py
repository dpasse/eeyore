from typing import List


class Merger():

    @staticmethod
    def combine_tag_lists(x1_list: List[str],
                          x2_list: List[str],
                          separator: str = '-') -> List[str]:
        x1_n = len(x1_list)
        x2_n = len(x2_list)

        if x1_n != x2_n:
            raise ValueError(
                f'length mismatch - x1 is {x1_n}, x2 is {x2_n}'
            )

        combination = []
        for i in range(x1_n):
            x1_item = x1_list[i]
            x2_item = x2_list[i]

            item = ''
            if len(x1_item) > 0 and len(x2_item) > 0:
                item = f'{x1_item}{separator}{x2_item}'
            elif len(x1_item) > 0:
                item = x1_item
            else:
                item = x2_item

            combination.append(item)

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
