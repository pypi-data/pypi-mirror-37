# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import datetime

import dateutil
import dateutil.parser

from azureml._history.async_request import AsyncRequest
from azureml._history.utils.async_task import noraise_handler
from azureml._history.utils.daemon import Daemon
from azureml._history.utils.singleton import singleton


class ExpiringToken:
    def __init__(self, run_token, expiry_time_utc):
        self.run_token = run_token
        self.expiry_time_utc = expiry_time_utc


@singleton
class RefreshTokenService:

    # Use shorter interval_sec for testing
    def __init__(self, module_logger,
                 session,
                 account_token,
                 add_request,
                 run_id_to_url,
                 interval_sec=None,
                 TOKEN_REMAINING_PERCENT=0.2,
                 TOKEN_DURATION_MIN=60):
        self.TOKEN_REMAINING_PERCENT = TOKEN_REMAINING_PERCENT
        self.TOKEN_DURATION_MIN = TOKEN_DURATION_MIN
        self.module_logger = module_logger
        self.session = session
        self.add_request = add_request
        self.account_token = account_token
        if interval_sec is None:
            interval_sec = 30
        self.daemon = self._create_daemon(interval_sec)
        self.num_refresh = 0
        self.num_checks = 0
        self.run_id_to_expiring_token = {}
        self.run_id_to_url = run_id_to_url
        self.client = RefreshTokenClient(self.run_id_to_expiring_token)
        self.running = False

    def _should_refresh(self, current_expiry_time):
        if current_expiry_time is None:
            return True
        # Refresh when remaining duration < TOKEN_REMAINING_PERCENT of TOKEN_DURATION_MIN remaining
        current_time = datetime.datetime.utcnow()
        time_delta = current_expiry_time - current_time
        time_difference_in_minutes = time_delta / datetime.timedelta(minutes=1)  # converts TimeDelta unit to minutes
        out = time_difference_in_minutes < (self.TOKEN_REMAINING_PERCENT * self.TOKEN_REMAINING_PERCENT)
        return out

    def _get_refresh_token_url(self, run_id):
        url = self.run_id_to_url(run_id)
        return url

    def _create_daemon(self, interval_sec):
        daemon = Daemon('RefreshToken', interval_sec=interval_sec,
                        logger=self.module_logger,
                        work_func=self.check_and_refresh_tokens)
        return daemon

    def start_daemon(self):
        self.module_logger.debug("Starting refresh token daemon. Interval is {}s".format(self.daemon.interval))
        if not self.running:
            self.daemon.start()
            self.running = True

    def stop_daemon(self):
        self.module_logger.debug(
            "Stopping refresh token daemon.")
        if self.running:
            self.daemon.stop()
            self.running = False

    def change_daemon_interval(self, new_interval_sec, force_initial_refresh=False):
        """
        :param new_interval_sec:
        :param force_initial_refresh: By default, refresh is called when _should_refresh is True
        :return:
        """
        if force_initial_refresh:
            self._refresh_tokens()
        self.daemon._change_interval(new_interval_sec)

    def __enter__(self):
        pass

    def __exit__(self):
        pass

    def _refresh_tokens(self):
        for run_id in self.run_id_to_expiring_token.keys():
            self._refresh_token(run_id)

    def _refresh_token(self, run_id):
        """
        Example endpoint
        https://eastus2euap.experiments.azureml.net/history/swagger/#!/Run/HistoryV1_0SubscriptionsBySubscriptionIdResourceGroupsByResourceGroupNameProvidersMicrosoft_MachineLearningExperimentationAccountsByAccountNameWorkspacesByWorkspaceNameProjectsByProjectNameRunsByRunIdTokenGet
        :return:
        """
        self.module_logger.debug("Calling refresh token")
        url = self._get_refresh_token_url(run_id)

        token = self.run_id_to_expiring_token[run_id].run_token
        if token is None:
            token = self.account_token
        if not token:
            raise Exception("Token is missing")

        headers = {
            'content-type': "application/json",
            'Authorization': 'Bearer ' + token
        }
        self.module_logger.debug("Making refresh token call to {}".format(url))

        def bg_cb(session, response):
            try:
                response_json = response.json()
                if "token" in response_json:
                    run_token = response_json["token"]
                    expiry_time_utc = response_json["expiryTimeUtc"]
                    expiry_time_utc = dateutil.parser.parse(expiry_time_utc).replace(tzinfo=None)
                    self.run_id_to_expiring_token[run_id] = ExpiringToken(run_token, expiry_time_utc)
                    self.num_refresh += 1
                    self.module_logger.debug(
                        "Refresh expiry time {}, {}: {}".format(self.num_refresh, run_id, expiry_time_utc))
                    return True
                else:
                    raise Exception("Invalid token response json: {}".format(response_json))
            except Exception as ee:
                raise Exception("Exception. Got response:\n{}\n".format(response.content))

        req = self.session.get(url, headers=headers, background_callback=bg_cb)
        req = AsyncRequest(req, ident="RefreshTokenTask_{}".format(self.num_refresh), handler=noraise_handler)
        self.add_request(req, priority=0)
        return req

    def check_and_refresh_tokens(self):
        self.module_logger.debug("Checking and refreshing {} run_ids".format(len(self.run_id_to_expiring_token)))
        self.num_checks += 1
        for run_id, expiring_token in self.run_id_to_expiring_token.items():
            if self._should_refresh(expiring_token.expiry_time_utc):
                self._refresh_token(run_id)

    def add_run_id(self, run_id):
        if run_id not in self.run_id_to_expiring_token:
            self.run_id_to_expiring_token[run_id] = ExpiringToken(None, None)
            return True
        return False


class RefreshTokenClient:
    def __init__(self, run_id_to_expiring_token):
        self.run_id_to_expiring_token = run_id_to_expiring_token

    def get_authentication_header(self, run_id):
        token = self.get_token(run_id)
        header = {"Authorization": "Bearer {}".format(token)}
        return header

    def get_token(self, run_id):
        return self.run_id_to_expiring_token[run_id].run_token
