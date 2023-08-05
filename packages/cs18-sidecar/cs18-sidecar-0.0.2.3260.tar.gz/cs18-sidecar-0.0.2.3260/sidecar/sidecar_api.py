import json
import logging.config
import os

from datetime import datetime
from typing import List, Tuple

from blinker import Namespace
from flask import Flask, request, Request

from werkzeug.exceptions import HTTPException, BadRequest
from sidecar.app_configuration_start_policy import AppConfigurationStartPolicy
from sidecar.app_instance_config_status_event_reporter import AppInstanceConfigStatusEventReporter
from sidecar.app_instance_event_handler import AppInstanceEventHandler
from sidecar.app_instance_events import AppInstanceEvents
from sidecar.app_instance_identifier import AppIdentifier
from sidecar.app_instance_identifier_creator import IAppInstanceIdentifierCreator
from sidecar.app_request_info import AppRequestInfo
from sidecar.app_services.app_service import K8sAppService, AWSAppService, AppService
from sidecar.app_status_maintainer import AppStatusMaintainer
from sidecar.apps_configuration_end_tracker import AppsConfigurationEndTracker
from sidecar.aws_app_instance_identifier_creator import AwsAppInstanceIdentifierCreator
from sidecar.aws_app_instance_service import AwsAppInstanceService
from sidecar.aws_sandbox_deployment_end_updater import AwsSandboxDeploymentEndUpdater
from sidecar.aws_sandbox_start_time_updater import AwsSandboxStartTimeUpdater
from sidecar.aws_session import AwsSession
from sidecar.aws_status_maintainer import AWSStatusMaintainer
from sidecar.cloud_logger import ICloudLogger, LogEntry, CloudLoggerFactory, FileLogger
from sidecar.const import Const, DateTimeProvider
from sidecar.azure_clp.azure_sidecar_api_initializer import AzureSidecarApiInitializer
from sidecar.file_system import FileSystemService
from sidecar.filters import LoggingFilter
from sidecar.health_check.app_health_check_monitor import AppHealthCheckMonitor
from sidecar.health_check.app_health_check_state import AppHealthCheckState
from sidecar.health_check.app_instance_health_check_monitor import AppInstanceHealthCheckMonitor
from sidecar.health_check.health_check_executor import HealthCheckExecutor
from sidecar.health_check.health_check_executor_logger import AppHealthCheckExecutorLogger, \
    AppInstanceHealthCheckExecutorLogger
from sidecar.health_check.health_check_preparer import HealthCheckPreparer
from sidecar.kub_api_service import KubApiService
from sidecar.kub_app_instance_identifier_creator import KubAppInstanceIdentifierCreator
from sidecar.kub_app_instance_service import KubAppInstanceService
from sidecar.kub_sandbox_deployment_end_updater import KubSandboxDeploymentEndUpdater
from sidecar.kub_sandbox_start_time_updater import KubSandboxStartTimeUpdater
from sidecar.kub_token_provider import KubTokenProvider, FakeKubTokenProvider
from sidecar.messaging_service import MessagingService, MessagingConnectionProperties
from sidecar.request_logger import RequestLogger
from sidecar.sandbox_deployment_state_tracker import SandboxDeploymentStateTracker
from sidecar.sandbox_end_deployment_notifier import SandboxEndDeploymentNotifier
from sidecar.sandbox_start_time_updater import ISandboxStartTimeUpdater
from sidecar.utils import CallsLogger

app = Flask(__name__)
cloud_logger = None  # type: ICloudLogger
_request_logger = None  # type: RequestLogger
_app_instance_health_check_monitor = None  # type: AppInstanceHealthCheckMonitor
_app_configuration_start_policy = None  # type: AppConfigurationStartPolicy
_app_instance_identifier_creator = None  # type: IAppInstanceIdentifierCreator
_app_instance_event_handler = None  # type: AppInstanceEventHandler
_app_signals = Namespace()
_kub_token_provider = None  # type: KubTokenProvider
_start_time_updater = None  # type: ISandboxStartTimeUpdater
_app_health_check_state = None  # type: AppHealthCheckState
_apps_configuration_end_tracker = None  # type: AppsConfigurationEndTracker
_app_health_check_monitor = None  # type: AppHealthCheckMonitor
_app_status_maintainer = None  # type: AppStatusMaintainer
_app_instance_health_check_executor = None  # type: HealthCheckExecutor
_app_sandbox_end_deployment_notifier = None  # type: SandboxEndDeploymentNotifier


def _load_config():
    with open(Const.get_config_file(), 'r') as conf:
        config_json = json.loads(conf.read())
        return config_json


def _convert_messaging_json_to_connection_props(messaging_json: dict()) -> MessagingConnectionProperties:
    return MessagingConnectionProperties(messaging_json["host"], messaging_json["user"], messaging_json["password"],
                                         messaging_json["queue"], messaging_json["exchange"],
                                         messaging_json["routingkey"],
                                         messaging_json["virtualhost"], messaging_json["port"],
                                         messaging_json["queuetype"],
                                         messaging_json["expires"], messaging_json["usessl"])


def _convert_apps_json_to_app_requests(apps_json: dict()) -> List[AppRequestInfo]:
    # TODO: remove the conditional assignment once all branches are up-to-date with issue #95
    app_requests = [AppRequestInfo(name=app_name,
                                   instances_count=app_value["instances_count"] if isinstance(app_value,
                                                                                              dict) else app_value,
                                   app_dependencies=app_value["dependencies"] if isinstance(app_value, dict) else [])
                    for app_name, app_value in apps_json.items()]
    return app_requests


def _get_apps_environment_variables(config_json: dict) -> dict:
    env = {app_name: app_config["env"] for app_name, app_config in config_json["apps"].items()}
    return env


def _get_apps_ports_to_test(config_json: dict) -> dict:
    env = {app_name: app_config["default_health_check_ports_to_test"] for app_name, app_config in
           config_json["apps"].items()}
    return env


def _get_apps_timeouts(config_json: dict) -> dict:
    env = {app_name: app_config["healthcheck_timeout"] for app_name, app_config in config_json["apps"].items()}
    return env


def get_status_updater(config_json,
                       app_instance_event_handler: AppInstanceEventHandler,
                       aws_session: AwsSession) \
        -> Tuple[SandboxDeploymentStateTracker, AppService]:
    global _app_configuration_start_policy
    global _app_instance_identifier_creator
    global _kub_token_provider
    global _start_time_updater
    global _app_health_check_state
    global _apps_configuration_end_tracker
    global _app_status_maintainer

    provider = config_json["provider"]
    sandbox_id = config_json['sandbox_id']
    space_id = config_json['space_id']
    apps_json = config_json['apps']
    app_requests = _convert_apps_json_to_app_requests(apps_json=apps_json)

    app_instance_status_event_reporter = AppInstanceConfigStatusEventReporter(
        app_instance_event_handler=app_instance_event_handler, logger=logger)
    time_provider = DateTimeProvider()

    _app_health_check_state = AppHealthCheckState(app_names=[app_name for app_name, app_value in apps_json.items()],
                                                  logger=logger)

    if provider == "kubernetes":
        if _kub_token_provider is None:
            _kub_token_provider = KubTokenProvider()

        hostname = config_json['kub_api_address']
        kas = KubApiService(hostname=hostname, namespace=sandbox_id, kub_token_provider=_kub_token_provider,
                            logger=logger)

        app_instance_service = KubAppInstanceService(logger=logger, kub_api_service=kas)
        _apps_configuration_end_tracker = AppsConfigurationEndTracker(logger=logger, app_requests=app_requests,
                                                                      app_instance_service=app_instance_service)

        _app_configuration_start_policy = AppConfigurationStartPolicy(app_health_check_state=_app_health_check_state,
                                                                      apps_config_end_tracker=_apps_configuration_end_tracker,
                                                                      app_requests=app_requests)

        _app_instance_identifier_creator = KubAppInstanceIdentifierCreator(kub_api_service=kas, logger=logger)

        sandbox_deployment_end_updater = KubSandboxDeploymentEndUpdater(
            kub_api_service=kas)

        sandbox_deployment_state_tracker = SandboxDeploymentStateTracker(
            logger=logger,
            app_requests=app_requests,
            apps_configuration_end_tracker=_apps_configuration_end_tracker,
            sandbox_deployment_end_updater=sandbox_deployment_end_updater,
            sandbox_id=sandbox_id,
            space_id=space_id)

        _app_status_maintainer = AppStatusMaintainer(logger=logger,
                                                     app_instance_service=app_instance_service,
                                                     apps_configuration_end_tracker=_apps_configuration_end_tracker,
                                                     sandbox_deployment_state_tracker=sandbox_deployment_state_tracker,
                                                     app_instance_status_event_reporter=app_instance_status_event_reporter)

        app_service = K8sAppService(api=kas, sandbox_id=sandbox_id, logger=logger)
        _start_time_updater = KubSandboxStartTimeUpdater(
            app_health_check_state=_app_health_check_state,
            date_time_provider=time_provider,
            logger=logger,
            kub_api_service=kas,
            apps_configuration_end_tracker=_apps_configuration_end_tracker)
        return sandbox_deployment_state_tracker, app_service

    if provider == "aws":
        aws_status_maintainer = AWSStatusMaintainer(aws_session, sandbox_id=sandbox_id, logger=logger)

        app_instance_service = AwsAppInstanceService(sandbox_id=sandbox_id,
                                                     logger=logger,
                                                     aws_session=aws_session,
                                                     aws_status_maintainer=aws_status_maintainer)
        _apps_configuration_end_tracker = AppsConfigurationEndTracker(logger=logger, app_requests=app_requests,
                                                                      app_instance_service=app_instance_service)

        _app_configuration_start_policy = AppConfigurationStartPolicy(app_health_check_state=_app_health_check_state,
                                                                      apps_config_end_tracker=_apps_configuration_end_tracker,
                                                                      app_requests=app_requests)
        _app_instance_identifier_creator = AwsAppInstanceIdentifierCreator(logger=logger)

        sandbox_deployment_end_updater = AwsSandboxDeploymentEndUpdater(aws_status_maintainer)

        sandbox_deployment_state_tracker = SandboxDeploymentStateTracker(
            logger=logger,
            app_requests=app_requests,
            apps_configuration_end_tracker=_apps_configuration_end_tracker,
            sandbox_deployment_end_updater=sandbox_deployment_end_updater,
            sandbox_id=sandbox_id,
            space_id=space_id)

        _app_status_maintainer = AppStatusMaintainer(logger=logger,
                                                     app_instance_service=app_instance_service,
                                                     apps_configuration_end_tracker=_apps_configuration_end_tracker,
                                                     sandbox_deployment_state_tracker=sandbox_deployment_state_tracker,
                                                     app_instance_status_event_reporter=app_instance_status_event_reporter)

        _start_time_updater = AwsSandboxStartTimeUpdater(app_health_check_state=_app_health_check_state,
                                                         sandbox_id=sandbox_id, aws_session=aws_session,
                                                         date_time_provider=time_provider, logger=logger,
                                                         apps_configuration_end_tracker=_apps_configuration_end_tracker,
                                                         aws_status_maintainer=aws_status_maintainer)
        app_service = AWSAppService(session=aws_session, sandbox_id=sandbox_id, logger=logger)

        return sandbox_deployment_state_tracker, app_service

    if provider == 'azure':
        _app_status_maintainer, \
        _app_configuration_start_policy, \
        _app_instance_identifier_creator, \
        _apps_configuration_end_tracker, \
        app_service, \
        sandbox_deployment_state_tracker, \
        _start_time_updater = \
            AzureSidecarApiInitializer(sandbox_id=sandbox_id,
                                       space_id=space_id,
                                       app_requests=app_requests,
                                       app_instance_status_event_reporter=app_instance_status_event_reporter,
                                       app_health_check_state=_app_health_check_state,
                                       logger=logger,
                                       config_json=config_json).initialize()
        return sandbox_deployment_state_tracker, app_service

    raise Exception('unknown provider {}'.format(provider))


@app.route("/")
def hello():
    logger.info("start")
    return "welcome cs18:sidecar-api", 200


@app.route("/application/<string:app_name>/health-check", methods=['POST'])
def start_health_check(app_name: str):
    ip_address = request.remote_addr
    req = safely_get_request_json(request=request)
    script_name = req['script']
    additional_data = req.get('additional_data')

    app_instance_identifier = _app_instance_identifier_creator.create(app_name=app_name,
                                                                      ip_address=ip_address,
                                                                      additional_data=additional_data)
    _app_instance_health_check_monitor.start(address=ip_address,
                                             identifier=app_instance_identifier,
                                             script_name=script_name)
    # fail here if validation fails ONLY
    return '', 202


@app.route('/application/<app_name>/<instance_id>/logs/<topic>', methods=['POST'])
def write_log(app_name: str, instance_id: str, topic: str):
    events = [(datetime.fromtimestamp(item["date"]), item["line"]) for item in safely_get_request_json(request=request)]
    log_entry = LogEntry(app_name, instance_id, topic, events, topic)
    cloud_logger.write(log_entry)

    return '', 200


@app.route('/application/<string:app_name>/<string:instance_id>/event', methods=['POST'])
def report_app_instance_event(app_name: str, instance_id: str):
    data_json = safely_get_request_json(request=request)
    event = data_json['event']
    if event not in AppInstanceEvents.ALL:
        error_message = "'{EVENT}' is not one of the known event types".format(EVENT=event)
        return error_message, 400

    app_instance_identifier = _app_instance_identifier_creator.create_from_instance_id(app_name=app_name,
                                                                                       instance_id=instance_id)
    _app_instance_event_handler.report_event(app_instance_identifier=app_instance_identifier,
                                             app_instance_event=event)
    return '', 200


@app.route("/application/<string:app_name>/config-start-status", methods=['GET'])
def get_application_configuration_start_status(app_name: str):
    start_status = _app_configuration_start_policy.get_app_configuration_start_status(app_name)
    return start_status, 200


@app.route("/is-api-alive", methods=['GET'])
def get_api_is_alive(app_name: str):
    return '', 200


@app.route("/application/<string:app_name>/whoami", methods=['POST'])
def get_who_am_i(app_name: str):
    ip_address = request.remote_addr
    req = safely_get_request_json(request=request)
    additional_data = req.get('additional_data')

    app_instance_identifier = _app_instance_identifier_creator.create(app_name=app_name,
                                                                      ip_address=ip_address,
                                                                      additional_data=additional_data)
    return app_instance_identifier.infra_id, 200


@app.errorhandler(Exception)
def unhandled_exception(e):
    status = e.code if isinstance(e, HTTPException) else 500
    _request_logger.log_request_failed(e, status)
    return str(e), status


def safely_get_request_json(request: Request):
    try:
        return request.get_json()
    except BadRequest as ex:
        err = "BadRequest {} {}".format(request.url, request.data.decode("utf-8"))
        logger.exception(err)
        raise


def run():
    global _app_instance_health_check_monitor
    global logger
    global cloud_logger
    global _request_logger
    global _app_instance_event_handler
    global _app_health_check_monitor
    global _app_instance_health_check_executor
    global _app_sandbox_end_deployment_notifier

    dir_name = os.path.dirname(os.path.abspath(__file__))

    logging.config.fileConfig(os.path.join(dir_name, 'logzio.conf'))
    logger = logging.getLogger("logger")

    try:
        config_json = _load_config()
        logger.addFilter(LoggingFilter(config_json))

        logger.info('starting sidecar from pypi')

        _request_logger = RequestLogger(app, logger, [write_log])
        CallsLogger.set_logger(logger)

        provider = config_json["provider"]
        sandbox_id = config_json['sandbox_id']
        aws_session = None
        if provider == "aws":
            region_name = config_json['region_name']
            aws_session = AwsSession(region_name=region_name, stack_name='sandbox-{}'.format(sandbox_id), logger=logger)

        cloud_logger_factory = CloudLoggerFactory(config_json, logger, aws_session, FileLogger(config_json))
        cloud_logger = cloud_logger_factory.create_instance()

        _app_instance_event_handler = AppInstanceEventHandler(cloud_logger=cloud_logger,
                                                              date_time_provider=DateTimeProvider(),
                                                              logger=logger)

        apps_env = _get_apps_environment_variables(config_json)

        apps_timeouts = _get_apps_timeouts(config_json)

        default_ports = _get_apps_ports_to_test(config_json)

        sandbox_deployment_state_tracker, app_service \
            = get_status_updater(config_json, _app_instance_event_handler, aws_session)

        preparer = HealthCheckPreparer(logger=logger, default_ports=default_ports, file_system=FileSystemService())

        _app_instance_health_check_executor = HealthCheckExecutor(env_vars=apps_env, app_timeouts=apps_timeouts,
                                                                  executor_logger=AppInstanceHealthCheckExecutorLogger(
                                                                      cloud_logger=cloud_logger, logger=logger),
                                                                  logger=logger)
        _app_instance_health_check_monitor = AppInstanceHealthCheckMonitor(
            executor=_app_instance_health_check_executor,
            preparer=preparer,
            logger=logger,
            cloud_logger=cloud_logger,
            status_maintainer=_app_status_maintainer)

        executor = HealthCheckExecutor(env_vars=apps_env,
                                       app_timeouts=apps_timeouts,
                                       executor_logger=AppHealthCheckExecutorLogger(cloud_logger=cloud_logger,
                                                                                    logger=logger),
                                       logger=logger)
        _app_health_check_monitor = AppHealthCheckMonitor(executor=executor,
                                                          preparer=preparer,
                                                          app_health_check_state=_app_health_check_state,
                                                          app_service=app_service,
                                                          app_timeouts=apps_timeouts,
                                                          apps_configuration_end_tracker=_apps_configuration_end_tracker,
                                                          logger=logger)

        messaging_props = _convert_messaging_json_to_connection_props(config_json['messaging'])

        messaging_service = MessagingService(messaging_props, logger)

        _app_sandbox_end_deployment_notifier = SandboxEndDeploymentNotifier(sandbox_deployment_state_tracker,
                                                                            messaging_service,
                                                                            _app_health_check_state,
                                                                            config_json['space_id'],
                                                                            sandbox_id)

        @_app_status_maintainer.on_instance_update_status.connect
        def on_instance_update_status(sender, **kwargs):
            identifier = kwargs.get("identifier")
            _app_health_check_monitor.start(identifier=AppIdentifier(name=identifier.name),
                                            infra_id=identifier.infra_id,
                                            script_name=kwargs.get("script_name"))

        @_app_health_check_state.on_apps_deployment_complete.connect
        def on_apps_deployment_complete(sender, **kwargs):
            _start_time_updater.on_app_instance_configuration_status_updated()
            _app_sandbox_end_deployment_notifier.notify_end_deployment()

    except Exception as exc:
        logger.exception("Sidecar failed to start")
        raise exc

    # server start status_updater
    app.run(host='0.0.0.0', port=4000)


def configure_debug():
    global _kub_token_provider
    _kub_token_provider = FakeKubTokenProvider()

    # create log folder: ~/sidecar
    api_log_folder = os.path.dirname(Const.get_log_file())
    file_system = FileSystemService()
    if not file_system.exists(api_log_folder):
        file_system.create_folders(api_log_folder)

    # setup the config file
    # apps_json = {
    #     "myApp": 1
    # }
    apps_json = {
        "fasty": {
            "instances_count": 1,
            "dependencies": [],
            "env": {"WELCOME_STRING": "Welcome to Quali Colony!", "PORT": "3001"},
            "healthcheck_timeout": 60,
            "default_health_check_ports_to_test": []
        }
    }

    messaging_json = {
        "host": "wombat.rmq.cloudamqp.com",
        "user": "rhpjvtoj",
        "password": "M7dZ2D5hWkIEOLPj6poiB4fF1t9cmNIf",
        "queue": "nefmwtza4r121",
        "exchange": "",
        "routingkey": "nefmwtza4r121",
        "virtualhost": "rhpjvtoj",
        "port": 5672,
        "queuetype": "fanout",
        "expires": 60000,
        "usessl": False
    }

    config_file_content = {
        "environment": "alberto-b",
        "provider": "kubernetes",
        "sandbox_id": "zrkq78yet8002",  # can set it to an existing sandbox
        "kub_api_address": "https://35.197.69.72",
        "region_name": "eu-west-1",
        "space_id": "d3cddb71-44ba-4f69-9d31-bf828d77ded3",
        "cloud_external_key": "8f70be32-3041-4a00-b96e-29f7a79cc854",
        "apps": apps_json,
        "messaging": messaging_json
    }
    with open(Const.get_config_file(), "w") as conf_file:
        conf_file.write(json.dumps(config_file_content))


if __name__ == "__main__":
    # configure_debug()
    run()
