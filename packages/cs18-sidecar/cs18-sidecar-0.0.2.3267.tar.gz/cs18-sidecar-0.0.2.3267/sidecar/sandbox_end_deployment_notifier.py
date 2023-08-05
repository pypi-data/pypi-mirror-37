import threading

from sidecar.apps_configuration_end_tracker import AppConfigurationEndStatus
from sidecar.health_check.app_health_check_state import AppHealthCheckState
from sidecar.messaging_service import MessagingService
from sidecar.sandbox_deployment_state_tracker import SandboxDeploymentStateTracker


class SandboxEndDeploymentNotifier:
    def __init__(self,
                 deployment_state_tracker: SandboxDeploymentStateTracker,
                 messaging_service: MessagingService,
                 app_health_state_checker: AppHealthCheckState,
                 space_id: str,
                 sandbox_id: str):
        self._sandbox_id = sandbox_id
        self._space_id = space_id
        self._app_health_state_checker = app_health_state_checker
        self._messaging_service = messaging_service
        self._deployment_state_tracker = deployment_state_tracker
        self._is_message_sent = False
        self._lock = threading.RLock()

    # please never use git history on this, it's not my fault.
    def notify_end_deployment(self):

        with self._lock:
            if self._is_message_sent:
                return

            if self._deployment_state_tracker.all_apps_deployment_ended_with_status(AppConfigurationEndStatus.COMPLETED) \
                    and self._app_health_state_checker.all_complete_with_success():

                end_status = self._deployment_state_tracker.get_deployment_end_status()

                message = {
                    'SpaceId': self._space_id,
                    'SandboxId': self._sandbox_id,
                    'Status': end_status
                }

                self._messaging_service.publish('CSMSCommon.Model.Events:SandboxDeployed', message)
                self._is_message_sent = True
