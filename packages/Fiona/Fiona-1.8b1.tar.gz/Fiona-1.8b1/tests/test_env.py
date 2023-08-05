# Tests requiring S3 credentials.
# Collected here to make them easier to skip/xfail.

import logging
import sys

import boto3
import pytest

import fiona
from fiona._env import del_gdal_config, get_gdal_config, set_gdal_config
from fiona.env import Env, defenv, delenv, getenv, setenv, ensure_env, ensure_env_with_credentials
from fiona.env import GDALVersion, require_gdal_version
from fiona.errors import EnvError, GDALVersionError
from fiona.fio.main import main_group
from fiona.session import AWSSession, Session

from .conftest import requires_gdal21


# Custom markers.
mingdalversion = pytest.mark.skipif(
    fiona.gdal_version < (2, 1, 0),
    reason="S3 raster access requires GDAL 2.1")

credentials = pytest.mark.skipif(
    not(boto3.Session()._session.get_credentials()),
    reason="S3 raster access requires credentials")


def test_gdalversion_class_parse():
    v = GDALVersion.parse('1.9.0')
    assert v.major == 1 and v.minor == 9

    v = GDALVersion.parse('1.9')
    assert v.major == 1 and v.minor == 9

    v = GDALVersion.parse('1.9a')
    assert v.major == 1 and v.minor == 9


def test_gdalversion_class_parse_err():
    invalids = ('foo', 'foo.bar', '1', '1.', '1.a', '.1')

    for invalid in invalids:
        with pytest.raises(ValueError):
            GDALVersion.parse(invalid)


def test_gdalversion_class_runtime():
    """Test the version of GDAL from this runtime"""
    GDALVersion.runtime().major >= 1


def test_gdalversion_class_cmp():
    assert GDALVersion(1, 0) == GDALVersion(1, 0)
    assert GDALVersion(2, 0) > GDALVersion(1, 0)
    assert GDALVersion(1, 1) > GDALVersion(1, 0)
    assert GDALVersion(1, 2) < GDALVersion(2, 2)

    # Because we don't care about patch component
    assert GDALVersion.parse('1.0') == GDALVersion.parse('1.0.10')

    assert GDALVersion.parse('1.9') < GDALVersion.parse('2.2.0')
    assert GDALVersion.parse('2.0.0') > GDALVersion(1, 9)


def test_gdalversion_class_repr():
    assert (GDALVersion(2, 1)).__repr__() == 'GDALVersion(major=2, minor=1)'


def test_gdalversion_class_str():
    assert str(GDALVersion(2, 1)) == '2.1'


def test_gdalversion_class_at_least():
    assert GDALVersion(2, 1).at_least(GDALVersion(1, 9))
    assert GDALVersion(2, 1).at_least((1, 9))
    assert GDALVersion(2, 1).at_least('1.9')

    assert not GDALVersion(2, 1).at_least(GDALVersion(2, 2))
    assert not GDALVersion(2, 1).at_least((2, 2))
    assert not GDALVersion(2, 1).at_least('2.2')


def test_gdalversion_class_at_least_invalid_type():
    invalids_types = ({}, {'major': 1, 'minor': 1}, [1, 2])

    for invalid in invalids_types:
        with pytest.raises(TypeError):
            GDALVersion(2, 1).at_least(invalid)


def test_require_gdal_version():
    @require_gdal_version('1.0')
    def a():
        return 1

    assert a() == 1


def test_require_gdal_version_too_low():
    """Functions that are too low raise a GDALVersionError"""
    version = '10000000.0'

    @require_gdal_version(version)
    def b():
        return 2

    with pytest.raises(GDALVersionError) as exc_info:
        b()

    message = 'GDAL version must be >= {0}'.format(version)
    assert message in exc_info.value.args[0]


def test_require_gdal_version_is_max_version():
    """Functions that are less than the required version are allowed, those that
    are too high raise a GDALVersionError"""
    @require_gdal_version('10000000.0', is_max_version=True)
    def a():
        return 1

    assert a() == 1

    @require_gdal_version('1.0', is_max_version=True)
    def b():
        return 2

    with pytest.raises(GDALVersionError):
        b()


def test_require_gdal_version_reason():
    reason = 'This totally awesome new feature is was introduced in GDAL 10000'

    @require_gdal_version('10000.0', reason=reason)
    def b():
        return 2

    with pytest.raises(GDALVersionError) as exc_info:
        b()

    assert reason in exc_info.value.args[0]


def test_require_gdal_version_err():
    """version is a required parameter and must be valid"""

    for invalid_version in ['bogus', 'a.b', '1.a.b']:
        with pytest.raises(ValueError):
            @require_gdal_version(invalid_version)
            def a():
                return 1


def test_require_gdal_version_param():
    """Parameter is allowed for all versions >= 1.0"""
    @require_gdal_version('1.0', param='foo')
    def a(foo=None):
        return foo

    assert a() is None
    assert a('bar') == 'bar'


def test_require_gdal_version_param_version_too_low():
    """Parameter is not allowed since runtime is too low a version"""

    version = '10000000.0'

    @require_gdal_version(version, param='foo')
    def a(foo=None):
        return foo

    assert a() is None  # param is not used, OK
    assert a(None) is None  # param is default, OK
    assert a(foo=None) is None  # param is keyword with default, OK

    with pytest.raises(GDALVersionError):
        a("not None")  # parameter passed as a position argument and not default

    with pytest.raises(GDALVersionError) as exc_info:
        a(foo='bar')  # parameter passed as a keyword argument and not default

    message = 'usage of parameter "foo" requires GDAL >= {0}'.format(version)
    assert message in exc_info.value.args[0]


def test_require_gdal_version_param_version_too_high():
    """Parameter is not allowed since runtime is too low a version"""

    version = '1.0'

    @require_gdal_version(version, param='foo', is_max_version=True)
    def a(foo=None):
        return foo

    assert a() is None  # param is not used, OK
    assert a(None) is None  # param is default, OK
    assert a(foo=None) is None  # param is keyword with default, OK

    with pytest.raises(GDALVersionError):
        a("not None")

    with pytest.raises(GDALVersionError) as exc_info:
        a(foo='bar')

    message = 'usage of parameter "foo" requires GDAL <= {0}'.format(version)
    assert message in exc_info.value.args[0]


def test_require_gdal_version_param_values():
    """Parameter values are allowed for all versions >= 1.0"""

    for values in [('bar',), ['bar'], {'bar'}]:
        @require_gdal_version('1.0', param='foo', values=values)
        def a(foo=None):
            return foo

        assert a() is None
        assert a('bar') == 'bar'
        assert a(foo='bar') == 'bar'


def test_require_gdal_version_param_values_err():
    """Parameter values must be tuple, list, or set, otherwise raises
    ValueError"""

    for invalid_values in ['bar', 1, 1.5, {'a': 'b'}]:
        with pytest.raises(ValueError):
            @require_gdal_version('1.0', param='foo', values=invalid_values)
            def func_a(foo=None):
                return foo

        with pytest.raises(ValueError):
            @require_gdal_version('1.0', values=invalid_values)
            def func_b(foo=None):
                return foo


def test_require_gdal_version_param_values_version_too_low():
    """Parameter values not allowed since runtime is too low a version"""
    version = '10000000.0'

    @require_gdal_version(version, param='foo', values=['bar'])
    def a(foo=None):
        return foo

    assert a('ok') == 'ok'  # param value allowed if not in values
    assert a(foo='ok') == 'ok'

    with pytest.raises(GDALVersionError) as exc_info:
        a(foo='bar')

    message = 'parameter "foo=bar" requires GDAL >= {0}'.format(version)
    assert message in exc_info.value.args[0]


def test_require_gdal_version_param_values_version_too_high():
    """Parameter values not allowed since runtime is too low a version"""
    version = '1.0'

    @require_gdal_version(version, param='foo', values=['bar'],
                          is_max_version=True)
    def a(foo=None):
        return foo

    assert a(foo='ok') == 'ok'  # param value allowed if not in values

    with pytest.raises(GDALVersionError):
        a('bar')

    with pytest.raises(GDALVersionError) as exc_info:
        a(foo='bar')

    message = 'parameter "foo=bar" requires GDAL <= {0}'.format(version)
    assert message in exc_info.value.args[0]


def test_require_gdal_version_chaining():
    version = '10000000.0'

    @require_gdal_version(version, param='foo', values=['bar'])
    @require_gdal_version(version, param='something', values=['else'])
    def a(foo=None, something=None):
        return foo, something

    # param values allowed if not in values
    assert a(foo='ok', something='not else') == ('ok', 'not else')

    # first decorator causes this to fail
    with pytest.raises(GDALVersionError) as exc_info:
        a(foo='bar', something='else')

    message = 'parameter "foo=bar" requires GDAL >= {0}'.format(version)
    assert message in exc_info.value.args[0]

    # second decorator causes this to fail
    with pytest.raises(GDALVersionError) as exc_info:
        a(foo='ok', something='else')

    message = 'parameter "something=else" requires GDAL >= {0}'.format(version)
    assert message in exc_info.value.args[0]

def test_gdal_config_accessers():
    """Low level GDAL config access."""
    assert get_gdal_config('foo') is None
    set_gdal_config('foo', 'bar')
    assert get_gdal_config('foo') == 'bar'
    del_gdal_config('foo')
    assert get_gdal_config('foo') is None


def test_gdal_config_accessors_no_normalize():
    """Disables casting keys to upper case and normalizing values to boolean
    Python values.
    """
    assert get_gdal_config('foo') is None
    set_gdal_config('foo', 'ON', normalize=False)
    assert get_gdal_config('foo', normalize=False) == 'ON'
    del_gdal_config('foo')
    assert get_gdal_config('foo') is None


def test_gdal_config_accessors_capitalization():
    """GDAL normalizes config names to upper case so Fiona does not
    need to do it on its own.  This test serves as a canary in case GDAL
    changes its behavior, which is an important part of reinstating
    discovered environment variables when ``fiona.Env()`` starts.
    GDAL does not alter config values.
    """
    assert get_gdal_config('foo') is None
    assert get_gdal_config('FOO') is None

    set_gdal_config('foo', 'bar')

    assert get_gdal_config('foo') == 'bar'
    assert get_gdal_config('FOO') == 'bar'

    del_gdal_config('foo')
    assert get_gdal_config('foo') is None
    assert get_gdal_config('FOO') is None

    set_gdal_config('upper', 'UPPER')
    assert get_gdal_config('upper') == 'UPPER'
    del_gdal_config('upper')


# The 'gdalenv' fixture ensures that gdal configuration is deleted
# at the end of the test, making tests as isolates as GDAL allows.

def test_env_accessors(gdalenv):
    """High level GDAL env access."""
    defenv()
    setenv(foo='1', bar='2')
    expected = {'foo': '1', 'bar': '2'}
    items = getenv()
    assert items == fiona.env.local._env.options
    # Comparison below requires removal of GDAL_DATA.
    items.pop('GDAL_DATA', None)
    assert items == expected
    assert get_gdal_config('foo') == 1
    assert get_gdal_config('bar') == 2
    delenv()
    with pytest.raises(EnvError):
        getenv()
    assert get_gdal_config('foo') is None
    assert get_gdal_config('bar') is None


def test_env_accessors_no_env():
    """Sould all raise an exception."""
    with pytest.raises(EnvError):
        delenv()
    with pytest.raises(EnvError):
        setenv()
    with pytest.raises(EnvError):
        getenv()


def test_ensure_env_decorator(gdalenv):
    @ensure_env
    def f():
        return getenv()['RASTERIO_ENV']
    assert f() is True


def test_ensure_env_with_credentials_decorator(monkeypatch, gdalenv):
    """Credentialization is ensured by wrapper"""
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'id')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'key')
    monkeypatch.setenv('AWS_SESSION_TOKEN', 'token')

    @ensure_env_with_credentials
    def f(path):
        return getenv()

    config = f('s3://foo/bar')
    assert config['AWS_ACCESS_KEY_ID'] == 'id'
    assert config['AWS_SECRET_ACCESS_KEY'] == 'key'
    assert config['AWS_SESSION_TOKEN'] == 'token'

    monkeypatch.undo()


def test_no_aws_gdal_config(gdalenv):
    """Trying to set AWS-specific GDAL config options fails."""
    with pytest.raises(EnvError):
        fiona.Env(AWS_ACCESS_KEY_ID='x')
    with pytest.raises(EnvError):
        fiona.Env(AWS_SECRET_ACCESS_KEY='y')


def test_env_empty(gdalenv):
    """Empty env has no defaults"""
    env = fiona.Env(foo='x')
    assert env.options['foo'] == 'x'
    assert not env.context_options
    with env:
        assert get_gdal_config('CHECK_WITH_INVERT_PROJ') is None
        assert get_gdal_config('GTIFF_IMPLICIT_JPEG_OVR') is None
        assert get_gdal_config("RASTERIO_ENV") is None


def test_env_defaults(gdalenv):
    """Test env defaults."""
    env = fiona.Env.from_defaults(foo='x')
    assert env.options['foo'] == 'x'
    assert not env.context_options
    with env:
        assert get_gdal_config('CHECK_WITH_INVERT_PROJ') is True
        assert get_gdal_config('GTIFF_IMPLICIT_JPEG_OVR') is False
        assert get_gdal_config("RASTERIO_ENV") is True


def test_aws_session(gdalenv):
    """Create an Env with a boto3 session."""
    aws_session = boto3.Session(
        aws_access_key_id='id', aws_secret_access_key='key',
        aws_session_token='token', region_name='null-island-1')
    with fiona.env.Env(session=Session.from_foreign_session(aws_session, cls=AWSSession)) as s:
        assert s.session._creds.access_key == 'id'
        assert s.session._creds.secret_key == 'key'
        assert s.session._creds.token == 'token'
        assert s.session._session.region_name == 'null-island-1'


def test_aws_session_credentials(gdalenv):
    """Create an Env with a boto3 session."""
    aws_session = boto3.Session(
        aws_access_key_id='id', aws_secret_access_key='key',
        aws_session_token='token', region_name='null-island-1')
    with fiona.env.Env(session=Session.from_foreign_session(aws_session, cls=AWSSession)) as s:
        s.credentialize()
        assert getenv()['AWS_ACCESS_KEY_ID'] == 'id'
        assert getenv()['AWS_REGION'] == 'null-island-1'
        assert getenv()['AWS_SECRET_ACCESS_KEY'] == 'key'
        assert getenv()['AWS_SESSION_TOKEN'] == 'token'


def test_session_env_lazy(monkeypatch, gdalenv):
    """Create an Env with AWS env vars."""
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'id')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'key')
    monkeypatch.setenv('AWS_SESSION_TOKEN', 'token')
    with fiona.Env(session=AWSSession()) as s:
        s.credentialize()
        assert getenv() == fiona.env.local._env.options
        expected = {
            'AWS_ACCESS_KEY_ID': 'id',
            'AWS_SECRET_ACCESS_KEY': 'key',
            'AWS_SESSION_TOKEN': 'token'}
        for k, v in expected.items():
            assert getenv()[k] == v

    monkeypatch.undo()


def test_aws_unsigned(gdalenv):
    """Create an Env with no AWS signing."""
    with fiona.env.Env(session=AWSSession(aws_unsigned=True)) as s:
        s.credentialize()
        assert getenv()['AWS_NO_SIGN_REQUEST'] == 'YES'
        assert getenv().get('AWS_ACCESS_KEY_ID') is None


@pytest.mark.xfail(
    reason="Turning off signing in an inner env does not work in Fiona 1.8")
def test_aws_unsigned_subenv(gdalenv):
    """Create an Env with no AWS signing."""
    with fiona.Env(
            aws_access_key_id='id', aws_secret_access_key='key',
            aws_session_token='token', region_name='null-island-1'):
        with fiona.env.Env(aws_unsigned=True) as inner:
            inner.credentialize()
            assert getenv()['AWS_NO_SIGN_REQUEST'] == 'YES'
            assert getenv().get('AWS_ACCESS_KEY_ID') is None


def test_open_with_default_env(path_coutwildrnp_shp, gdalenv):
    """Read from a dataset with a default env."""
    with fiona.open(path_coutwildrnp_shp) as col:
        assert len(col) == 67


def test_open_with_env(path_coutwildrnp_shp, gdalenv):
    """Read from a dataset with an explicit env."""
    with fiona.Env():
        with fiona.open(path_coutwildrnp_shp) as col:
            assert len(col) == 67


# CLI tests.

@requires_gdal21(reason="S3 access requires 2.1+")
@credentials
@pytest.mark.network
def test_s3_fio_info(runner):
    """S3 is supported by fio-info."""
    result = runner.invoke(main_group, ['info', 'zip+s3://fiona-testing/coutwildrnp.zip'])
    assert result.exit_code == 0
    assert '"count": 67' in result.output


def test_fio_env_credentials_options(tmpdir, monkeypatch, runner):
    """Confirm that --aws-profile option works."""
    credentials_file = tmpdir.join('credentials')
    credentials_file.write("[testing]\n"
                           "aws_access_key_id = foo\n"
                           "aws_secret_access_key = bar\n"
                           "aws_session_token = baz")
    monkeypatch.setenv('AWS_SHARED_CREDENTIALS_FILE', str(credentials_file))
    monkeypatch.setenv('AWS_SESSION_TOKEN', 'ignore_me')
    result = runner.invoke(
        main_group, ['--aws-profile', 'testing', 'env', '--credentials'])
    assert result.exit_code == 0
    assert '"aws_access_key_id": "foo"' in result.output
    assert '"aws_secret_access_key": "bar"' in result.output
    assert '"aws_session_token": "baz"' in result.output
    monkeypatch.undo()


def test_ensure_defaults_teardown(gdalenv):

    """This test guards against a regression.  Previously ``fiona.Env()``
    would quietly reinstate any ``fiona.env.default_options`` that was
    not modified by the environment.

    https://github.com/mapbox/fiona/issues/968
    """

    def _check_defaults():
        for key in Env.default_options().keys():
            assert get_gdal_config(key) is None

    _check_defaults()
    with fiona.Env():
        pass

    _check_defaults()
    assert fiona.env.local._env is None


@pytest.mark.parametrize("key,val", [
    ('key', 'ON'),
    ('CHECK_WITH_INVERT_PROJ', 'ON'),
    ('key', 'OFF'),
    ('CHECK_WITH_INVERT_PROJ', 'OFF')])
def test_env_discovery(key, val):
    """When passing options to ``fiona.Env()`` Fiona first checks
    to see if they were set in the environment and reinstates on exit.
    The discovered environment should only be reinstated when the outermost
    environment exits.  It's really important that this test use an
    environment default.
    """

    assert fiona.env.local._discovered_options is None, \
        "Something has gone horribly wrong."

    try:
        # This should persist when all other environment managers exit.
        set_gdal_config(key, val)

        # Start an environment and overwrite the value that should persist
        with fiona.Env(**{key: True}):
            assert get_gdal_config(key) is True
            assert fiona.env.local._discovered_options == {key: val}

            # Start another nested environment, again overwriting the value
            # that should persist
            with fiona.Env(**{key: False}):
                assert fiona.env.local._discovered_options == {key: val}
                assert get_gdal_config(key) is False

            # Ensure the outer state is restored.
            assert fiona.env.local._discovered_options == {key: val}
            assert get_gdal_config(key) is True

        # Ensure the discovered value remains unchanged.
        assert fiona.env.local._discovered_options is None
        assert get_gdal_config(key, normalize=False) == val

    # Leaving this option in the GDAL environment could cause a problem
    # for other tests.
    finally:
        del_gdal_config(key)


def test_have_registered_drivers():
    """Ensure drivers are only registered once, otherwise each thread will
    acquire a threadlock whenever an environment is started."""
    with fiona.Env():
        assert fiona.env.local._env._have_registered_drivers


def test_gdal_cachemax():
    """``GDAL_CACHEMAX`` is a special case."""
    original_cachemax = get_gdal_config('GDAL_CACHEMAX')
    assert original_cachemax != 4321
    # GDALSetCacheMax() has a limit of somewhere between 2 and 3 GB.
    # We use GDALSetCacheMax64(), so use a value that is outside the 32 bit
    # range to verify it is not being truncated.
    set_gdal_config('GDAL_CACHEMAX', 4321)
    assert get_gdal_config('GDAL_CACHEMAX', 4321) == 4321

    # On first read the number will be in bytes.  Drop to MB if necessary.
    try:
        set_gdal_config('GDAL_CACHEMAX', original_cachemax)
    except OverflowError:
        set_gdal_config('GDAL_CACHEMAX', int(original_cachemax / 1000000))


def test_fio_env_no_credentials(tmpdir, monkeypatch, runner):
    """Confirm that we can get drivers without any credentials"""
    credentials_file = tmpdir.join('credentials')
    monkeypatch.setenv('AWS_SHARED_CREDENTIALS_FILE', str(credentials_file))
    monkeypatch.delenv('AWS_ACCESS_KEY_ID', raising=False)
    # Assert that we don't have any AWS credentials by accident.
    with pytest.raises(Exception):
        fiona.open("s3://mapbox/fiona/RGB.byte.tif")

    with fiona.Env() as env:
        assert env.drivers()


@credentials
@mingdalversion
@pytest.mark.network
def test_open_s3():
    ds = fiona.open('zip+s3://fiona-testing/coutwildrnp.zip')
    assert len(ds) == 67


@pytest.mark.network
def test_open_zip_https():
    ds = fiona.open('zip+https://s3.amazonaws.com/fiona-testing/coutwildrnp.zip')
    assert len(ds) == 67
