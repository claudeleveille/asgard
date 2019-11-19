import re


class ConventionalCommitMsg:
    def __init__(self, msg):
        if (
            len(msg) < 4
            or re.search(r"([^:]+):", msg).group(1).isupper()
            or not msg[0].isalpha()
            or re.search(r"[^:]+:(.{1})", msg).group(1) != " "
        ):
            raise ValueError()
        self.msg = msg

    @property
    def msg_type(self):
        if re.search(r"BREAKING CHANGE: ", self.msg):
            return "BREAKING CHANGE"
        return re.search(r"([^:]+):", self.msg).group(1)

    def __repr__(self):
        return self.msg

    def __eq__(self, other):
        if (self.msg == other) or (self.msg == other.msg):
            return True
