import time
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Protocol


@dataclass(slots=True)
class Report:
    author: str
    start: int | None = field(init=False, default=None)
    end: int | None = field(init=False, default=None)
    result: Any | None = field(init=False, default=None)

    def __str__(self) -> str:
        return f"""Report(
        Result: {self.result}
        In {self.time_taken_in_s:.2f}s,
        By {self.author},\n)"""

    @staticmethod
    def current_time() -> int:
        return time.perf_counter_ns()

    @property
    def time_taken_in_s(self) -> float:
        return self.time_taken * 1e-9

    @property
    def time_taken(self) -> float:
        if not self.start is None and self.end is None:
            return Report.current_time() - self.start
        elif self.start is None:
            return float("+inf")
        else:
            return self.end - self.start  # type: ignore


class ReportManager:
    @staticmethod
    def time(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(instance: Reportable, *args: Any, **kwargs: Any) -> Any:
            instance.report.start = Report.current_time()
            result = func(instance, *args, **kwargs)
            instance.report.end = Report.current_time()
            return result

        return wrapper

    @staticmethod
    def as_result(
        modifier: Callable[..., Any], if_failed: bool = True, default: Any = None
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(instance: Reportable, *args: Any, **kwargs: Any) -> Any:
                result = func(instance, *args, **kwargs)

                if not result is None or if_failed:
                    try:
                        instance.report.result = modifier(result)
                    except Exception:
                        instance.report.result = default
                return result

            return wrapper

        return decorator


class Reportable(Protocol):
    report: Report
