from typing import Any


class NonePointerException(BaseException):
    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)

    def with_traceback(self, tb: Any) -> BaseException:
        return super().with_traceback(tb)
