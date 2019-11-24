import re


class SemVer:
    regex_pattern = (
        r"^(0|[1-9]+0*)\.(0|[1-9]+0*)\.(0|[1-9]+0*)((-)?([a-zA-Z]+)(\.)?(0|[1-9]+0*))?$"
    )

    def __init__(
        self,
        major=0,
        minor=1,
        micro=0,
        suffix_dash_prefix=False,
        suffix=None,
        suffix_dot_suffix=False,
        suffix_number=None,
    ):
        if (
            int(major) < 0
            or int(minor) < 0
            or int(micro) < 0
            or isinstance(major, float)
            or isinstance(minor, float)
            or isinstance(micro, float)
        ):
            raise ValueError()
        self.major = int(major)
        self.minor = int(minor)
        self.micro = int(micro)
        self.suffix_dash_prefix = suffix_dash_prefix
        self.suffix = suffix
        self.suffix_dot_suffix = suffix_dot_suffix
        self._suffix_number = suffix_number

    @classmethod
    def fromstr(cls, str):
        if not re.match(cls.regex_pattern, str):
            raise ValueError()
        s = re.search(cls.regex_pattern, str)
        suffix_dash_prefix = False
        suffix = None
        suffix_dot_suffix = False
        suffix_number = None
        if s.group(5):
            suffix_dash_prefix = True
        if s.group(6):
            suffix = s.group(6)
        if s.group(7):
            suffix_dot_suffix = True
        if s.group(8):
            suffix_number = s.group(8)
        return cls(
            major=s.group(1),
            minor=s.group(2),
            micro=s.group(3),
            suffix_dash_prefix=suffix_dash_prefix,
            suffix=suffix,
            suffix_dot_suffix=suffix_dot_suffix,
            suffix_number=suffix_number,
        )

    @property
    def suffix_number(self):
        if isinstance(self._suffix_number, str):
            return int(self._suffix_number)
        else:
            return self._suffix_number

    def increment_major(self):
        self.major += 1
        self.minor = 0
        self.micro = 0

    def increment_minor(self):
        self.minor += 1
        self.micro = 0

    def increment_micro(self):
        self.micro += 1

    def increment_suffix_number(self):
        if isinstance(self._suffix_number, int):
            self._suffix_number += 1
        else:
            raise ValueError(
                "Tried to increment suffix_number when it was set to None."
            )

    def isprerelease(self):
        if self.suffix != None:
            return True
        return False

    @classmethod
    def isvalid(cls, subject):
        if re.match(cls.regex_pattern, subject):
            return True
        return False

    def __repr__(self):
        rv = f"{self.major}.{self.minor}.{self.micro}"
        if self.suffix_dash_prefix:
            rv += "-"
        if self.suffix:
            rv += self.suffix
        if self.suffix_dot_suffix:
            rv += "."
        if self.suffix_number:
            rv += str(self.suffix_number)
        return rv

    def __eq__(self, other):
        if self.__repr__() == other or self.__repr__() == other.__repr__():
            return True
