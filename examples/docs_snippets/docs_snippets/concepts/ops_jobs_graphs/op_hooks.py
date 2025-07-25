# ruff: isort: skip_file
from unittest import mock

import yaml
from dagster_slack import slack_resource

# start_repo_marker_0
import dagster as dg


@dg.success_hook(required_resource_keys={"slack"})
def slack_message_on_success(context: dg.HookContext):
    message = f"Op {context.op.name} finished successfully"
    context.resources.slack.chat_postMessage(channel="#foo", text=message)


@dg.failure_hook(required_resource_keys={"slack"})
def slack_message_on_failure(context: dg.HookContext):
    message = f"Op {context.op.name} failed"
    context.resources.slack.chat_postMessage(channel="#foo", text=message)


# end_repo_marker_0

slack_resource_mock = mock.MagicMock()


@dg.op
def a():
    pass


@dg.op
def b():
    raise Exception()


# start_repo_marker_1
@dg.job(resource_defs={"slack": slack_resource}, hooks={slack_message_on_failure})
def notif_all():
    # the hook "slack_message_on_failure" is applied on every dg.op instance within this dg.graph
    a()
    b()


# end_repo_marker_1


# start_repo_marker_3
@dg.graph
def slack_notif_all():
    a()
    b()


notif_all_dev = slack_notif_all.to_job(
    name="notif_all_dev",
    resource_defs={
        "slack": dg.ResourceDefinition.hardcoded_resource(
            slack_resource_mock, "do not send messages in dev"
        )
    },
    hooks={slack_message_on_failure},
)

notif_all_prod = slack_notif_all.to_job(
    name="notif_all_prod",
    resource_defs={"slack": slack_resource},
    hooks={slack_message_on_failure},
)


# end_repo_marker_3


# start_repo_marker_2
@dg.job(resource_defs={"slack": slack_resource})
def selective_notif():
    # only dg.op "a" triggers hooks: a slack message will be sent when it fails or succeeds
    a.with_hooks({slack_message_on_failure, slack_message_on_success})()
    # dg.op "b" won't trigger any hooks
    b()


# end_repo_marker_2


@dg.repository
def repo():
    return [notif_all, selective_notif]


# start_repo_main
if __name__ == "__main__":
    prod_op_hooks_run_config_yaml = dg.file_relative_path(
        __file__, "prod_op_hooks.yaml"
    )
    with open(prod_op_hooks_run_config_yaml, encoding="utf8") as fd:
        run_config = yaml.safe_load(fd.read())

    notif_all_prod.execute_in_process(run_config=run_config, raise_on_error=False)
# end_repo_main


# start_testing_hooks
import dagster as dg


@dg.success_hook(required_resource_keys={"my_conn"})
def my_success_hook(context):
    context.resources.my_conn.send("foo")


# end_testing_hooks


# start_testing_hooks_tests
def test_my_success_hook():
    my_conn = mock.MagicMock()
    # construct dg.HookContext with mocked ``my_conn`` resource.
    context = dg.build_hook_context(resources={"my_conn": my_conn})

    my_success_hook(context)

    assert my_conn.send.call_count == 1


# end_testing_hooks_tests


# start_repo_marker_1_with_configured
@dg.job(
    resource_defs={
        "slack": slack_resource.configured(
            {"token": "xoxp-1234123412341234-12341234-1234"}
        )
    },
    hooks={slack_message_on_failure},
)
def notif_all_configured():
    # the hook "slack_message_on_failure" is applied on every dg.op instance within this dg.graph
    a()
    b()


# end_repo_marker_1_with_configured
