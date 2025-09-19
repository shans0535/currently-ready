# test_decorators.py
import pytest
import asyncio
import time

import decorators


# ---------------------------------------------------------
# Logging & Performance
# ---------------------------------------------------------

def test_timed_and_log_calls(capsys):
    @decorators.timed
    @decorators.log_calls
    def add(a, b):
        return a + b

    result = add(2, 3)
    captured = capsys.readouterr()
    assert result == 5
    assert "add" in captured.out or "add" in captured.err


# ---------------------------------------------------------
# Reliability & Caching
# ---------------------------------------------------------

def test_retry_success():
    calls = {"count": 0}

    @decorators.retry(times=3, delay=0)
    def flaky():
        calls["count"] += 1
        if calls["count"] < 2:
            raise ValueError("fail")
        return "ok"

    assert flaky() == "ok"
    assert calls["count"] == 2


def test_retry_backoff_failure():
    @decorators.retry_backoff(times=2, base_delay=0)
    def always_fail():
        raise ValueError("nope")

    with pytest.raises(RuntimeError):
        always_fail()


def test_cache_decorator():
    calls = {"count": 0}

    @decorators.cache
    def slow(x):
        calls["count"] += 1
        return x * 2

    assert slow(3) == 6
    assert slow(3) == 6  # cached
    assert calls["count"] == 1


def test_memoize_with_ttl():
    calls = {"count": 0}

    @decorators.memoize_with_ttl(ttl=1)
    def slow(x):
        calls["count"] += 1
        return x

    assert slow(5) == 5
    assert slow(5) == 5  # cached
    assert calls["count"] == 1
    time.sleep(1.1)
    assert slow(5) == 5  # cache expired
    assert calls["count"] == 2


def test_circuit_breaker():
    calls = {"count": 0}

    @decorators.circuit_breaker(fail_max=2, reset_timeout=1)
    def flaky():
        calls["count"] += 1
        raise ValueError("fail")

    with pytest.raises(ValueError):
        flaky()
    with pytest.raises(ValueError):
        flaky()
    with pytest.raises(RuntimeError):  # circuit open
        flaky()


# ---------------------------------------------------------
# Access & Security
# ---------------------------------------------------------

def test_require_role_success():
    user = {"roles": ["admin"]}

    @decorators.require_role("admin")
    def protected(u):
        return "ok"

    assert protected(user) == "ok"


def test_require_role_failure():
    user = {"roles": ["user"]}

    @decorators.require_role("admin")
    def protected(u):
        return "ok"

    with pytest.raises(PermissionError):
        protected(user)


def test_audit_logs(capsys):
    user = {"id": 123, "roles": ["admin"]}

    @decorators.audit("DELETE")
    def delete(u):
        return "done"

    assert delete(user) == "done"
    captured = capsys.readouterr()
    assert "User=123" in captured.out or "User=123" in captured.err


def test_idempotent():
    @decorators.idempotent
    def process(key, x):
        return x * 2

    assert process("abc", 2) == 4
    assert process("abc", 3) == 4  # same result as first call


# ---------------------------------------------------------
# Async Utilities
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_async_retry_success():
    calls = {"count": 0}

    @decorators.async_retry(times=3, base_delay=0)
    async def flaky():
        calls["count"] += 1
        if calls["count"] < 2:
            raise ValueError("fail")
        return "ok"

    assert await flaky() == "ok"
    assert calls["count"] == 2


@pytest.mark.asyncio
async def test_async_retry_failure():
    @decorators.async_retry(times=2, base_delay=0)
    async def always_fail():
        raise ValueError("fail")

    with pytest.raises(RuntimeError):
        await always_fail()


@pytest.mark.asyncio
async def test_with_timeout():
    @decorators.with_timeout(0.5)
    async def slow():
        await asyncio.sleep(1)
        return "done"

    with pytest.raises(asyncio.TimeoutError):
        await slow()


@pytest.mark.asyncio
async def test_async_rate_limit():
    timestamps = []

    @decorators.async_rate_limit(5)
    async def fast():
        timestamps.append(time.time())
        return "ok"

    await fast()
    await fast()
    assert len(timestamps) == 2
    assert timestamps[1] - timestamps[0] >= 0.2  # 5 per sec => 0.2s spacing


# ---------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------

def test_singleton():
    @decorators.singleton
    class Config:
        def __init__(self):
            self.value = time.time()

    c1 = Config()
    c2 = Config()
    assert c1 is c2
