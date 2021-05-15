from functools import total_ordering
from re import findall


@total_ordering
class Version:
    """
        Compares version numbers
    """

    def __init__(self, version):
        self.split_version = findall(r'(\d+|[A-Za-z]+)', version)

    def __eq__(self, other):
        if isinstance(other, Version):
            if len(self.split_version) == len(other.split_version):
                return self.split_version == other.split_version
            return False

    def __gt__(self, other):
        if isinstance(other, Version):
            return self._compare_versions_gt(self.split_version, other.split_version)

    def __lt__(self, other):
        if isinstance(other, Version):
            return self._compare_versions_lt(self.split_version, other.split_version)

    def _compare_versions_gt(self, version_1, version_2):
        if len(version_1) == len(version_2):
            return version_1 > version_2
        elif len(version_1) > len(version_2):
            return self._compare_common_part(version_1, version_2)
        elif len(version_1) < len(version_2):
            return self._compare_common_part(version_2, version_1)

    def _compare_versions_lt(self, version_1, version_2):
        if len(version_1) == len(version_2):
            return version_1 < version_2
        elif len(version_1) > len(version_2):
            return self._compare_common_part(version_1, version_2)
        elif len(version_1) < len(version_2):
            return self._compare_common_part(version_2, version_1)

    @staticmethod
    def _compare_common_part(version_1, version_2):
        if version_1[:len(version_2)] == version_2:
            if not version_1[len(version_2)].isdigit():
                return version_1 > version_2
            return version_1 < version_2
        return version_1[:len(version_2)] > version_2


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        # additional tests
        ('1.0-rc2', '1.0-rc3'),
        ('1.0.alpha12', '1.0'),
        ('1.0.beta-2', '1.0.beta.3')
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
