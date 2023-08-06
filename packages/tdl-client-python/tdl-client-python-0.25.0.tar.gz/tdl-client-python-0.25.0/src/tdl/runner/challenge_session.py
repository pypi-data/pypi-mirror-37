from tdl.runner.challenge_server_client import ChallengeServerClient, ClientErrorException, OtherCommunicationException, \
    ServerErrorException
from tdl.runner.recording_system import RecordingEvent
from tdl.runner.recording_system import RecordingSystem
from tdl.runner.round_management import RoundManagement


class ChallengeSession:

    @staticmethod
    def for_runner(runner):
        return ChallengeSession(runner)

    def __init__(self, runner):
        self._runner = runner
        self._config = None
        self._audit_stream = None
        self._user_input_callback = None
        self._recording_system = None
        self._challenge_server_client = None

    def with_config(self, config):
        self._config = config
        self._audit_stream = config.get_audit_stream()
        return self

    def with_action_provider(self, callback):
        self._user_input_callback = callback
        return self

    def start(self):
        self._recording_system = RecordingSystem(self._config.get_recording_system_should_be_on())

        if not self._recording_system.is_recording_system_ok():
            self._audit_stream.log('Please run `record_screen_and_upload` before continuing.')
            return

        self._audit_stream.log('Connecting to {}'.format(self._config.get_hostname()))
        self.run_app()

    def run_app(self):
        self._challenge_server_client = ChallengeServerClient(
            self._config.get_hostname(),
            self._config.get_port(),
            self._config.get_journey_id(),
            self._config.get_use_colours())

        try:
            journey_progress = self._challenge_server_client.get_journey_progress()
            self._audit_stream.log(journey_progress)

            available_actions = self._challenge_server_client.get_available_actions()
            self._audit_stream.log(available_actions)

            no_actions_available = 'No actions available.' in available_actions
            if no_actions_available:
                self._recording_system.tell_to_stop()
                return

            user_input = self._user_input_callback()
            self._audit_stream.log('Selected action is: {}'.format(user_input))
            if user_input == 'deploy':
                self._runner.run()
                last_fetched_round = RoundManagement.get_last_fetched_round(self._config.get_working_directory())
                self._recording_system.notify_event(last_fetched_round, RecordingEvent.ROUND_SOLUTION_DEPLOY)

            action_feedback = self._challenge_server_client.send_action(user_input)
            if 'Round time for' in action_feedback:
                last_fetched_round = RoundManagement.get_last_fetched_round(self._config.get_working_directory())
                self._recording_system.notify_event(last_fetched_round, RecordingEvent.ROUND_COMPLETED)

            if 'All challenges have been completed' in action_feedback:
                self._recording_system.tell_to_stop()

            self._audit_stream.log(action_feedback)
            round_description = self._challenge_server_client.get_round_description()
            RoundManagement.save_description(
                self._recording_system,
                round_description,
                self._audit_stream,
                self._config.get_working_directory())

        except ClientErrorException as e:
            self._audit_stream.log(e)
        except ServerErrorException:
            self._audit_stream.log('Server experienced an error. Try again in a few minutes.')
        except OtherCommunicationException:
            self._audit_stream.log('Client threw an unexpected error. Try again.')

