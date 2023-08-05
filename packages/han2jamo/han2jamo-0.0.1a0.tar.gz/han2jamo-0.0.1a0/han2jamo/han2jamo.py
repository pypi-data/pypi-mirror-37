from .utils import *
import typing


class Han2Jamo:
    def char_to_jamo(self, x: str) -> str:
        """
        Splits a given korean character into components.
        :param x: A complete korean character.
        :return: A tuple of basic characters that constitutes the given characters.
        """
        if len(x) != 1:
            raise ValueError("Input string must have exactly one character.")

        if not check_syllable(x):
            raise ValueError(
                "Input string does not contain a valid Korean character.")

        diff = ord(x) - 0xAC00
        _m = diff % 28
        _d = (diff - _m) // 28

        initial_index = _d // 21
        medial_index = _d % 21
        final_index = _m

        if not final_index:
            result = (INITIALS[initial_index], MEDIALS[medial_index])
        else:
            result = (
                INITIALS[initial_index], MEDIALS[medial_index],
                FINALS[final_index - 1])

        return result

    def jamo_to_char(self, initial: str, medial: str, final: str = None) -> typing.Tuple[str]:
        """
        Combines jamos to produce a single syllable.
        :param initial: initial jamo.
        :param medial: medial jamo.
        :param final: final jamo.
        :return: A syllable.
        """
        if initial not in CHAR_SETS[TYPE_INITIAL] or medial not in CHAR_SETS[
            TYPE_MEDIAL] or (final and final not in CHAR_SETS[TYPE_FINAL]):
            raise ValueError("Given Jamo characters are not valid.")

        initial_ind = CHAR_INDICES[TYPE_INITIAL][initial]
        medial_ind = CHAR_INDICES[TYPE_MEDIAL][medial]
        final_ind = CHAR_INDICES[TYPE_FINAL][final] + 1 if final else 0

        b = 0xAC00 + 28 * 21 * initial_ind + 28 * medial_ind + final_ind

        result = to_unichr(b)

        assert check_syllable(result)

        return result

    def str_to_jamo(self, string: str) -> str:
        """
        Splits a sequence of Korean syllables to produce a sequence of jamos.
        Irrelevant characters will be ignored.
        :param string: A unicode string.
        :return: A converted unicode string.
        """
        new_string = ""
        for c in string:
            if not check_syllable(c):
                new_c = c
            else:
                new_c = "".join(self.char_to_jamo(c))
            new_string += new_c

        return new_string

    def jamo_to_str(self, string: str) -> str:
        """
        Combines a sequence of jamos to produce a sequence of syllables.
        Irrelevant characters will be ignored.
        :param string: A unicode string.
        :return: A converted unicode string.
        """
        last_t = 0
        queue = []
        new_string = ""

        def flush(queue, n=0):
            new_queue = []

            while len(queue) > n:
                new_queue.append(queue.pop())

            if len(new_queue) == 1:
                result = new_queue[0]
            elif len(new_queue) >= 2:
                try:
                    result = self.jamo_to_char(*new_queue)
                except ValueError:
                    # Invalid jamo combination
                    result = "".join(new_queue)
            else:
                result = None

            return result

        for c in string:
            if c not in CHARSET:
                if queue:
                    new_c = flush(queue) + c
                else:
                    new_c = c

                last_t = 0
            else:
                t = jamo_type(c)
                new_c = None

                if t & TYPE_FINAL == TYPE_FINAL:
                    if not (last_t == TYPE_MEDIAL):
                        new_c = flush(queue)
                elif t == TYPE_INITIAL:
                    new_c = flush(queue)
                elif t == TYPE_MEDIAL:
                    if last_t & TYPE_INITIAL == TYPE_INITIAL:
                        new_c = flush(queue, 1)
                    else:
                        new_c = flush(queue)

                last_t = t
                queue.insert(0, c)

            if new_c:
                new_string += new_c

        if queue:
            new_string += flush(queue)

        return new_string
