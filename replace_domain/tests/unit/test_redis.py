from pytest_mock import MockerFixture
from redis.exceptions import RedisError

from replace_domain.redis import redis_health_check


def test_health_check_error(mocker: MockerFixture) -> None:
    mock_ping = mocker.patch('replace_domain.redis.r.ping')
    mock_ping.side_effect = RedisError()
    result = redis_health_check()
    assert result is False
