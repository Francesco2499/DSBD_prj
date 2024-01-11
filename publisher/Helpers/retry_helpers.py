import time
from pybreaker import CircuitBreaker, CircuitBreakerError

MAX_RETRIES = 3
BACKOFF_FACTOR = 2


def exponential_backoff_retry(fn):
    circuit_breaker = CircuitBreaker(fail_max=3, reset_timeout=10)

    def retry_with_backoff(*args, **kwargs):
        retries = 0
        while retries < MAX_RETRIES:
            @circuit_breaker
            def wrapped_fn():
                return fn(*args, **kwargs)

            try:
                return wrapped_fn()
            except CircuitBreakerError:
                print({'message': 'Fallback data while the service is unavailable'})
            except Exception as e:
                print(f"Errore durante la chiamata: {e}")
                if retries == MAX_RETRIES - 1:
                    raise
                wait_time = (2 ** retries) * BACKOFF_FACTOR
                print(f"Riprova tra {wait_time} secondi...")
                time.sleep(wait_time)
                retries += 1
    return retry_with_backoff
