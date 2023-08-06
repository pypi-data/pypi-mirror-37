from typing import Optional
from distutils.version import StrictVersion  # pylint: disable=E0611,E0401


def bump_version(
        version: str,
        position: int = -1,
        pre_release: Optional[str] = None
) -> str:
    """Increase the version number from a version number string.

    *New in version 0.3.0*

    Args:
        version (str): The version number to be bumped.
        position (int, optional): The position (starting with zero) of the
            version number component to be increased.  Defaults to: ``-1``
        pre_release (str, Optional): A value of ``a`` or ``alpha`` will
            create or increase an alpha version number.  A value of ``b`` or
            ``beta`` will create or increase a beta version number.

    Returns:
        The increased version number

    Raises:
        ValueError: if the given ``version`` is an invalid version number.
        ValueError: if the given ``position`` does not exist.
        ValueError: if the given ``prerelease`` is not in:
            ``a, alpha, b, beta``

    A version number consists of two or three dot-separated numeric components,
    with an optional "pre-release" tag on the end. The pre-release tag consists
    of the letter 'a' (alpha) or 'b' (beta) followed by a number. If the numeric
    components of two version numbers are equal, then one with a pre-release tag
    will always be deemed earlier (lesser) than one without.

    This function works with two and three component version numbers.

    The following are valid version numbers::

        0.4
        0.4.1
        0.5a1
        0.5b3
        0.5
        0.9.6
        1.0
        1.0.4a3
        1.0.4b1
        1.0.4

    The following are examples of invalid version numbers::

        1
        2.7.2.2
        1.3.a4
        1.3pl1
        1.3c4


    Examples:
        >>> from flutils import bump_version
        >>> bump_version('1.2.2')
        '1.2.3'

        >>> bump_version('1.2.3', position=1)
        '1.3.0

        >>> bump_version('1.3.4', position=0)
        '2.0.0'

        >>> bump_version('1.2.3', prerelease='a')
        '1.2.4a0'

        >>> bump_version('1.2.4a0', pre_release='a')
        '1.2.4a1'

        >>> bump_version('1.2.4a1', pre_release='beta')
        '1.2.4b0'

        >>> bump_version('1.2.4a1')
        '1.2.4'

        >>> bump_version('1.2.4b0')
        '1.2.4'

        >>> bump_version('2.1.3', position=1, pre_release='a')
        '1.3.0a0'

        >>> bump_version('1.2.b0', position=0, pre_release='b')
        '2.0.0b0'
    """
    ver: StrictVersion = StrictVersion(version)
    length = len(version.split('.'))

    if position < 0:
        index = length + position
    else:
        index = position

    last = length - 1
    if not 0 <= index <= last:
        raise ValueError('invalid position of %r' % position)

    if pre_release is None:
        pre_release = ''

    if pre_release not in ('', 'a', 'alpha', 'b', 'beta'):
        raise ValueError(
            "invalid pre_release: %r.  Must be one of: "
            "'a', 'alpha', 'b', 'beta', "
            % pre_release
        )
    if pre_release == 'alpha':
        pre_release = 'a'

    if pre_release == 'beta':
        pre_release = 'b'

    hold = list()
    tail = ''
    reset = False
    for i in range(length):
        val = ver.version[i]
        bump = True
        if i == last:
            if pre_release:
                if (reset is True or ver.prerelease is None or
                        ver.prerelease[0] != pre_release):
                    tail = '%s%s' % (pre_release, '0')
                else:
                    tail = '%s%s' % (pre_release, ver.prerelease[1] + 1)
                    bump = False
            else:
                if ver.prerelease:
                    bump = False

        if reset is True:
            val = 0
        else:
            if i == index and bump is True:
                val += 1
                reset = True
        hold.append('%s' % val)

    out = '%s%s' % ('.'.join(hold), tail)
    return out
