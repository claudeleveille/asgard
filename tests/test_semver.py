import pytest

from asgard.semver import SemVer


@pytest.mark.parametrize(
    "params",
    [
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1),
        (-1, -1, -1),
        (-1, -1, 0),
        (-1, 0, 0),
        (0, -1, -1),
        (-1, 0, -1),
    ],
)
def test_negative_numbers_raise_valueerror(params):
    with pytest.raises(ValueError):
        SemVer(params[0], params[1], params[2])


@pytest.mark.parametrize(
    "params",
    [
        (1.0, 0, 0),
        (1.0, 1.0, 0),
        (1.0, 1.0, 1.0),
        (1.0, 1.0, 0),
        (1.0, 0, 0),
        (0, 0, 1.0),
        (0, 1.0, 1.0),
        (1.0, 0, 1.0),
    ],
)
def test_floats_raise_valueerror(params):
    with pytest.raises(ValueError):
        SemVer(params[0], params[1], params[2])


def test_repr_gives_properly_formatted_string():
    assert repr(SemVer()) == "0.1.0"


@pytest.mark.parametrize(
    "p1,p2,p3",
    [
        (SemVer(), SemVer(), "0.1.0"),
        (
            SemVer(13, 24, 24, False, suffix="rc", suffix_number="24"),
            SemVer(13, 24, 24, False, suffix="rc", suffix_number="24"),
            "13.24.24rc24",
        ),
    ],
)
def test_equality(p1, p2, p3):
    assert p1 == p2 == p3


@pytest.mark.parametrize(
    "p1,p2",
    [
        (SemVer(), SemVer(0, 1, 2)),
        (SemVer(13, 24, 24, False, suffix="rc", suffix_number="25"), "13.24.24rc24"),
        ("1.0.1-rc.13", "13.1.3rc3"),
        (
            SemVer(1, 33, 15, True, "alpha", False, 23),
            SemVer(1, 33, 15, True, "mistake", 23),
        ),
    ],
)
def test_inequality(p1, p2):
    assert p1 != p2


def test_string_parameters():
    s = SemVer("1", "1", "1")
    assert s == "1.1.1"


@pytest.mark.parametrize(
    "params,semver",
    [
        (("1", 0, 0), "1.0.0"),
        (("1", "1", 0), "1.1.0"),
        (("1", "1", "0"), "1.1.0"),
        (("0", "1", 1), "0.1.1"),
    ],
)
def test_mixed_string_and_numeric_params(params, semver):
    assert SemVer(params[0], params[1], params[2]) == semver


def test_default_semver_is_0_1_0():
    s = SemVer()
    assert s == "0.1.0"


def test_incrementing_major_resets_minor_and_micro():
    s = SemVer()
    s.increment_major()
    assert s == "1.0.0"


def test_incrementing_minor_resets_micro_leaves_major():
    s = SemVer(1, 1, 1)
    s.increment_minor()
    assert s == "1.2.0"


def test_incrementting_micro_leaves_major_and_minor():
    s = SemVer(1, 1, 1)
    s.increment_micro()
    assert s == "1.1.2"


@pytest.mark.parametrize(
    "param",
    [
        "0.1.0",
        "0.1.1",
        "1.0.0",
        "1.1.1",
        "1.1.1rc10",
        "1.1.1RC113",
        "1.2.0",
        "100.100.100",
        "100.1123.13",
        "12.0.0",
        "123.14.0-rc.12",
        "123.34.0-alpha.1",
        "190.123.123",
        "2.0.0",
        "5.3.5",
        "88.234252.23",
        "99.99.99-rc.890",
        "99.99.99-rc890",
        "999.999.999",
    ],
)
def test_fromstr(param):
    assert SemVer.fromstr(param) == param


@pytest.mark.parametrize(
    "param",
    [
        "-1.1.1",
        "-1.1.423",
        "-30.234.2-sd.9",
        "",
        "0.-24.23-",
        "0..23.23",
        "0.1.-1",
        "0.1.01-rc.1",
        "0.1.1-rc",
        "00.23.2",
        "000.1.01-rc.1",
        "100.1.1rc01",
        "234.23.2-",
        "234.23j.23",
        "24.-24.24",
        "5.1.0-",
        "99.99.99-rc01",
        "hello",
        "invalid",
        "v1.0.0",
        "1.0.0rc-1",
    ],
)
def test_bad_param_in_fromstr_raises_valueerror(param):
    with pytest.raises(ValueError):
        SemVer.fromstr(param)
