import threading
from logging import Logger
from typing import List, Dict

from blinker import Signal

from sidecar.const import AppNetworkStatus
from sidecar.utils import CallsLogger


class AppHealthCheckState:
    on_apps_deployment_complete = Signal()

    def __init__(self, app_names: List[str], logger: Logger):
        self._lock = threading.RLock()
        self._logger = logger
        self._app_states = {app_name: AppNetworkStatus.PENDING for app_name in app_names}  # type: Dict[str, str]

    @CallsLogger.wrap
    def set_app_state(self, app_name: str, status: str):
        with self._lock:
            self._app_states[app_name] = status

            all_apps_complete = all(AppNetworkStatus.is_end_status(status)
                                    for status
                                    in self._app_states.values())

        if all_apps_complete:
            self.on_apps_deployment_complete.send(self)

    @CallsLogger.wrap
    def all_complete_with_success(self) -> bool:
        with self._lock:
            return all(status == AppNetworkStatus.COMPLETED
                       for status
                       in self._app_states.values())

    @CallsLogger.wrap
    def get_apps_state(self, app_names: List[str]) -> Dict[str, str]:
        with self._lock:
            return {k: v for k, v in self._app_states.items() if k in app_names}
