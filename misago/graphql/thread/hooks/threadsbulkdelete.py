from typing import Any, Awaitable, Callable, Dict, List, Tuple

from ....context import Context
from ....hooks import FilterHook
from ....validation import ErrorsList, Validator

ThreadsBulkDeleteInput = Dict[str, Any]
ThreadsBulkDeleteInputAction = Callable[
    [Context, Dict[str, List[Validator]], ThreadsBulkDeleteInput, ErrorsList],
    Awaitable[Tuple[ThreadsBulkDeleteInput, ErrorsList]],
]
ThreadsBulkDeleteInputFilter = Callable[
    [ThreadsBulkDeleteInputAction, Context, ThreadsBulkDeleteInput],
    Awaitable[Tuple[ThreadsBulkDeleteInput, ErrorsList]],
]


class ThreadsBulkDeleteInputHook(
    FilterHook[ThreadsBulkDeleteInputAction, ThreadsBulkDeleteInputFilter]
):
    def call_action(
        self,
        action: ThreadsBulkDeleteInputAction,
        context: Context,
        validators: Dict[str, List[Validator]],
        data: ThreadsBulkDeleteInput,
        errors_list: ErrorsList,
    ) -> Awaitable[Tuple[ThreadsBulkDeleteInput, ErrorsList]]:
        return self.filter(action, context, validators, data, errors_list)


ThreadsBulkDeleteAction = Callable[[Context, ThreadsBulkDeleteInput], Awaitable[None]]
ThreadsBulkDeleteFilter = Callable[
    [ThreadsBulkDeleteAction, Context, ThreadsBulkDeleteInput], Awaitable[None]
]


class ThreadsBulkDeleteHook(
    FilterHook[ThreadsBulkDeleteAction, ThreadsBulkDeleteFilter]
):
    async def call_action(
        self,
        action: ThreadsBulkDeleteAction,
        context: Context,
        cleaned_data: ThreadsBulkDeleteInput,
    ):
        await self.filter(action, context, cleaned_data)


threads_bulk_delete_hook = ThreadsBulkDeleteHook()
threads_bulk_delete_input_hook = ThreadsBulkDeleteInputHook()