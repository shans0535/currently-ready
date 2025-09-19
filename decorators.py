"""
decorators.py - A collection of production-ready Python decorators.
"""

import functools
import time
import threading
import logging
import asyncio


# ---------------------------------------------------------
# Logging & Performance
# ---------------------------------------------------------

def log_calls(func):
    """Log function calls with arguments, return values, and execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logging.info(
            f"{func.__name__}({args}, {kwargs}) -> {result} [{elapsed:.3f}s]")
        return result
    return wrapper


def timed(func):
    """Measure execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logging.info(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


# ---------------------------------------------------------
# Reliability & Caching
# ---------------------------------------------------------

def retry(times=3, delay=1):
    """Retry function on failure with fixed delay."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator


def retry_backoff(times=3, base_delay=1):
    """Retry with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    delay = base_delay * (2 ** attempt)
                    logging.warning(
                        f"Retry {attempt+1}/{times} in {delay}s due to {e}")
                    time.sleep(delay)
            raise RuntimeError("Max retries exceeded")
        return wrapper
    return decorator


def cache(func):
    """Simple in-memory cache decorator."""
    _cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in _cache:
            _cache[key] = func(*args, **kwargs)
        return _cache[key]
    return wrapper


def memoize_with_ttl(ttl: int):
    """Cache results with TTL (time-to-live)."""
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key not in cache or now - cache[key][1] > ttl:
                cache[key] = (func(*args, **kwargs), now)
            return cache[key][0]
        return wrapper
    return decorator


def circuit_breaker(fail_max=3, reset_timeout=10):
    """Stop calling a failing function until cooldown period passes."""
    def decorator(func):
        failures = [0]
        last_failure = [0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if failures[0] >= fail_max and (time.time() - last_failure[0]) < reset_timeout:
                raise RuntimeError("Circuit is open")
            try:
                result = func(*args, **kwargs)
                failures[0] = 0
                return result
            except Exception as e:
                failures[0] += 1
                last_failure[0] = time.time()
                raise e
        return wrapper
    return decorator


# ---------------------------------------------------------
# Access & Security
# ---------------------------------------------------------

def require_role(role):
    """Ensure user has required role before executing function."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if role not in user.get("roles", []):
                raise PermissionError("Access denied")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator


def audit(action: str):
    """Log security-sensitive actions for auditing."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            result = func(user, *args, **kwargs)
            logging.info(
                f"User={user.get('id')} performed {action} on {func.__name__}")
            return result
        return wrapper
    return decorator


def idempotent(func):
    """Prevent duplicate processing by enforcing idempotency keys."""
    seen = {}

    @functools.wraps(func)
    def wrapper(key, *args, **kwargs):
        if key in seen:
            return seen[key]
        result = func(key, *args, **kwargs)
        seen[key] = result
        return result
    return wrapper


# ---------------------------------------------------------
# Async Utilities
# ---------------------------------------------------------

def async_retry(times=3, base_delay=1):
    """Retry async functions with exponential backoff."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    delay = base_delay * (2 ** attempt)
                    logging.warning(
                        f"Retry {attempt+1}/{times} in {delay}s due to {e}")
                    await asyncio.sleep(delay)
            raise RuntimeError("Max retries exceeded")
        return wrapper
    return decorator


def with_timeout(seconds):
    """Enforce timeout on async function calls."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
        return wrapper
    return decorator


def async_rate_limit(calls_per_sec: int):
    """Throttle async function calls to N per second."""
    min_interval = 1.0 / calls_per_sec
    last_call = [0.0]

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                await asyncio.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# ---------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------

def singleton(cls):
    """Thread-safe singleton decorator for classes."""
    instances = {}
    lock = threading.Lock()

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


def timeit(expected_delay=None, logger=None, level=logging.INFO):
    """
    Decorator to measure execution time of sync or async functions.

    Args:
        expected_delay (float, optional): Expected delay in seconds.
        logger (logging.Logger, optional): Logger to use (default: module logger).
        level (int): Logging level (default: logging.INFO).
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            # Async version
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                t1 = time.perf_counter()
                result = await func(*args, **kwargs)
                t2 = time.perf_counter()
                elapsed = t2 - t1
                if expected_delay is not None:
                    logger.log(
                        level, f"[{func.__name__}] took {elapsed:.4f}s (expected ~{expected_delay}s)")
                else:
                    logger.log(level, f"[{func.__name__}] took {elapsed:.4f}s")
                return result
        else:
            # Sync version
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                t1 = time.perf_counter()
                result = func(*args, **kwargs)
                t2 = time.perf_counter()
                elapsed = t2 - t1
                if expected_delay is not None:
                    logger.log(
                        level, f"[{func.__name__}] took {elapsed:.4f}s (expected ~{expected_delay}s)")
                else:
                    logger.log(level, f"[{func.__name__}] took {elapsed:.4f}s")
                return result
        return wrapper
    return decorator


def async_timed(expected_delay=2, logger=None, level=logging.INFO):
    """
    Async-only decorator to measure execution time of coroutines.

    Args:
        expected_delay (float): Expected delay in seconds.
        logger (logging.Logger, optional): Logger to use (default: module logger).
        level (int): Logging level (default: logging.INFO).
    """
    if logger is None:
        logger = logging.getLogger(__name__)

    def decorator(func):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError(
                "async_timed can only be applied to async functions")

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            t1 = time.perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                t2 = time.perf_counter()
                elapsed = t2 - t1
                logger.log(
                    level, f"[{func.__name__}] took {elapsed:.2f}s (expected ~{expected_delay}s)")
        return wrapper
    return decorator
