

def humanized_delta_from_dates(old_date, new_date, resolution=2):
    return _date_difference_to_human_readable.from_dates(old_date, new_date, resolution)


def humanized_delta_from_delta(delta, resolution=2):
    return _date_difference_to_human_readable.from_delta(delta, resolution)


class DateDifferenceToHumanReadable:
    def from_dates(self, old_date, new_date, resolution=2):
        return self.from_delta((new_date - old_date), resolution)

    def from_delta(self, delta, resolution=2):
        fragments = self._extract_fragments_from_timedelta(delta=delta)
        fragments = self._convert_fragment_list_to_humanized(fragments)
        return self._combine_humanized_fragments(fragments, resolution)

    @classmethod
    def _extract_fragments_from_timedelta(cls, delta):
        return [
            (delta.days, "day", "days"),
            (delta.seconds / 3600, "hour", "hours"),
            (delta.seconds % 3600 / 60, "minute", "minutes"),
            (delta.seconds % 3600 % 60, "second", "seconds"),
        ]

    @classmethod
    def _convert_fragment_list_to_humanized(cls, fragments):
        for index in range(len(fragments)):
            fragment = fragments[index]
            fragment = cls._convert_fragment_to_humanized(*fragment)
            fragments[index] = fragment
        return fragments

    @classmethod
    def _convert_fragment_to_humanized(cls, time_num, str_one, str_many, result_format="{} {}"):
        time_num = abs(int(time_num))

        if time_num == 0:
            return ""
        if time_num == 1:
            return result_format.format(time_num, str_one)
        return result_format.format(time_num, str_many)

    @classmethod
    def _combine_humanized_fragments(cls, fragments, resolution):
        string_representation = ""
        fragment_counter = 0

        for fragment in fragments:
            if len(string_representation) != 0:
                fragment_counter += 1

            if fragment_counter == resolution:
                break

            if len(fragment) != 0:
                string_representation += "{} ".format(fragment)

        if len(string_representation) == 0 and resolution != 0:
            return "now"

        return string_representation.strip()


_date_difference_to_human_readable = DateDifferenceToHumanReadable()
