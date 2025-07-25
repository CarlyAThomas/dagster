# ruff: isort: skip_file


# start_alert_sensor_marker
import os
import dagster as dg
from slack_sdk import WebClient


@dg.run_failure_sensor
def my_slack_on_run_failure(context: dg.RunFailureSensorContext):
    slack_client = WebClient(token=os.environ["SLACK_DAGSTER_ETL_BOT_TOKEN"])

    slack_client.chat_postMessage(
        channel="#alert-channel",
        text=(
            f'Job "{context.dagster_run.job_name}" failed. Error:'
            f" {context.failure_event.message}"
        ),
    )


# end_alert_sensor_marker


def email_alert(_):
    pass


# start_simple_fail_sensor
@dg.run_failure_sensor
def my_email_failure_sensor(context: dg.RunFailureSensorContext):
    message = (
        f'Job "{context.dagster_run.job_name}" failed. Error:'
        f" {context.failure_event.message}"
    )
    email_alert(message)


# end_simple_fail_sensor


# start_failure_sensor_testing_with_context_setup
import dagster as dg


@dg.op
def fails():
    raise Exception("failure!")


@dg.job
def my_job_fails():
    fails()


# end_failure_sensor_testing_with_context_setup

# start_alert_sensor_testing_with_context_marker
import dagster as dg

# execute the job
instance = dg.DagsterInstance.ephemeral()
result = my_job_fails.execute_in_process(instance=instance, raise_on_error=False)

# retrieve the DagsterRun
dagster_run = result.dagster_run

# retrieve a failure event from the completed job execution
dagster_event = result.get_run_failure_event()

# create the context
run_failure_sensor_context = dg.build_run_status_sensor_context(
    sensor_name="my_email_failure_sensor",
    dagster_instance=instance,
    dagster_run=dagster_run,
    dagster_event=dagster_event,
).for_run_failure()

# run the sensor
my_email_failure_sensor(run_failure_sensor_context)

# end_alert_sensor_testing_with_context_marker


# start_slack_marker
from dagster_slack import make_slack_on_run_failure_sensor

slack_on_run_failure = make_slack_on_run_failure_sensor(
    "#my_channel",
    os.getenv("MY_SLACK_TOKEN"),  # type: ignore[arg-type]
)


# end_slack_marker


# start_email_marker
from dagster import make_email_on_run_failure_sensor


email_on_run_failure = make_email_on_run_failure_sensor(
    email_from="no-reply@example.com",
    email_password=os.getenv("ALERT_EMAIL_PASSWORD"),  # type: ignore[arg-type]
    email_to=["xxx@example.com", "xyz@example.com"],
)

# end_email_marker

# start_success_sensor_marker
import dagster as dg


@dg.run_status_sensor(run_status=dg.DagsterRunStatus.SUCCESS)
def my_slack_on_run_success(context: dg.RunStatusSensorContext):
    slack_client = WebClient(token=os.environ["SLACK_DAGSTER_ETL_BOT_TOKEN"])

    slack_client.chat_postMessage(
        channel="#alert-channel",
        text=f'Job "{context.dagster_run.job_name}" succeeded.',
    )


# end_success_sensor_marker


# start_simple_success_sensor
@dg.run_status_sensor(run_status=dg.DagsterRunStatus.SUCCESS)
def my_email_sensor(context: dg.RunStatusSensorContext):
    message = f'Job "{context.dagster_run.job_name}" succeeded.'
    email_alert(message)


# end_simple_success_sensor


# start_run_status_sensor_testing_with_context_setup
@dg.op
def succeeds():
    return 1


@dg.job
def my_job_succeeds():
    succeeds()


# end_run_status_sensor_testing_with_context_setup

# start_run_status_sensor_testing_marker
# execute the job
instance = dg.DagsterInstance.ephemeral()
result = my_job_succeeds.execute_in_process(instance=instance)

# retrieve the DagsterRun
dagster_run = result.dagster_run

# retrieve a success event from the completed execution
dagster_event = result.get_run_success_event()

# create the context
run_status_sensor_context = dg.build_run_status_sensor_context(
    sensor_name="my_email_sensor",
    dagster_instance=instance,
    dagster_run=dagster_run,
    dagster_event=dagster_event,
)

# run the sensor
my_email_sensor(run_status_sensor_context)

# end_run_status_sensor_testing_marker

import dagster as dg

my_jobs: list[dg.SensorDefinition] = []


@dg.job
def my_sensor_job():
    succeeds()
