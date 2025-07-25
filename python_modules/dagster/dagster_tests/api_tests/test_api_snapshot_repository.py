import asyncio
import sys
from contextlib import contextmanager

import dagster as dg
import pytest
from dagster import job
from dagster._api.snapshot_repository import (
    gen_streaming_external_repositories_data_grpc,
    sync_get_streaming_external_repositories_data_grpc,
)
from dagster._core.errors import DagsterUserCodeProcessError
from dagster._core.instance import DagsterInstance
from dagster._core.remote_representation import (
    ManagedGrpcPythonEnvCodeLocationOrigin,
    RepositorySnap,
)
from dagster._core.remote_representation.external import RemoteRepository
from dagster._core.remote_representation.external_data import (
    DISABLE_FAST_EXTRACT_ENV_VAR,
    JobDataSnap,
    JobRefSnap,
    extract_serialized_job_snap_from_serialized_job_data_snap,
)
from dagster._core.remote_representation.handle import RepositoryHandle
from dagster._core.remote_representation.origin import RemoteRepositoryOrigin
from dagster._core.storage.tags import EXTERNAL_JOB_SOURCE_TAG_KEY
from dagster._core.types.loadable_target_origin import LoadableTargetOrigin
from dagster._utils.env import environ
from dagster_shared.serdes.serdes import get_storage_fields
from dagster_shared.serdes.utils import hash_str

from dagster_tests.api_tests.utils import get_bar_repo_code_location


def test_streaming_external_repositories_api_grpc(instance):
    with get_bar_repo_code_location(instance) as code_location:
        repository_snaps = sync_get_streaming_external_repositories_data_grpc(
            code_location.client, code_location
        )

        assert len(repository_snaps) == 1

        repository_snap = repository_snaps["bar_repo"]

        assert isinstance(repository_snap, RepositorySnap)
        assert repository_snap.name == "bar_repo"
        assert repository_snap.metadata == {
            "string": dg.TextMetadataValue("foo"),
            "integer": dg.IntMetadataValue(123),
        }

        async_repository_snaps = asyncio.run(
            gen_streaming_external_repositories_data_grpc(code_location.client, code_location)
        )

        assert async_repository_snaps == repository_snaps


def test_streaming_external_repositories_error(instance):
    with get_bar_repo_code_location(instance) as code_location:
        code_location.repository_names = {"does_not_exist"}
        assert code_location.repository_names == {"does_not_exist"}

        with pytest.raises(
            DagsterUserCodeProcessError,
            match='Could not find a repository called "does_not_exist"',
        ):
            sync_get_streaming_external_repositories_data_grpc(code_location.client, code_location)

        with pytest.raises(
            DagsterUserCodeProcessError,
            match='Could not find a repository called "does_not_exist"',
        ):
            asyncio.run(
                gen_streaming_external_repositories_data_grpc(code_location.client, code_location)
            )


@dg.op
def do_something():
    return 1


@job
def giant_job():
    # Job big enough to be larger than the max size limit for a gRPC message in its
    # external repository
    for _i in range(20000):
        do_something()


@dg.repository  # pyright: ignore[reportArgumentType]
def giant_repo():
    return {
        "jobs": {
            "giant": giant_job,
        },
    }


@contextmanager
def get_giant_repo_grpc_code_location(instance):
    with ManagedGrpcPythonEnvCodeLocationOrigin(
        loadable_target_origin=LoadableTargetOrigin(
            executable_path=sys.executable,
            attribute="giant_repo",
            module_name="dagster_tests.api_tests.test_api_snapshot_repository",
        ),
        location_name="giant_repo_location",
    ).create_single_location(instance) as location:
        yield location


@pytest.mark.skip("https://github.com/dagster-io/dagster/issues/6940")
def test_giant_external_repository_streaming_grpc():
    with dg.instance_for_test() as instance:
        with get_giant_repo_grpc_code_location(instance) as code_location:
            # Using streaming allows the giant repo to load
            repository_snaps = sync_get_streaming_external_repositories_data_grpc(
                code_location.client, code_location
            )

            assert len(repository_snaps) == 1

            repository_snap = repository_snaps["giant_repo"]

            assert isinstance(repository_snap, RepositorySnap)
            assert repository_snap.name == "giant_repo"


@pytest.mark.parametrize("env", [{}, {DISABLE_FAST_EXTRACT_ENV_VAR: "true"}])
def test_defer_snapshots(instance: DagsterInstance, env):
    with get_bar_repo_code_location(instance) as code_location, environ(env):
        repo_origin = RemoteRepositoryOrigin(
            code_location.origin,
            "bar_repo",
        )

        ser_repo_data = code_location.client.external_repository(
            repo_origin,
            defer_snapshots=True,
        )

        _state = {}

        def _ref_to_data(ref: JobRefSnap):
            _state["cnt"] = _state.get("cnt", 0) + 1
            reply = code_location.client.external_job(
                repo_origin,
                ref.name,
            )
            assert reply.serialized_job_data, reply.serialized_error
            assert (
                hash_str(
                    extract_serialized_job_snap_from_serialized_job_data_snap(
                        reply.serialized_job_data
                    )
                )
                == ref.snapshot_id
            ), ref.name

            job_data_snap = dg.deserialize_value(reply.serialized_job_data, JobDataSnap)
            return job_data_snap

        repository_snap = dg.deserialize_value(ser_repo_data, RepositorySnap)
        assert repository_snap.job_refs and len(repository_snap.job_refs) == 8
        assert repository_snap.job_datas is None

        repo = RemoteRepository(
            repository_snap,
            RepositoryHandle.from_location(repository_name="bar_repo", code_location=code_location),
            auto_materialize_use_sensors=True,
            ref_to_data_fn=_ref_to_data,
        )
        jobs = repo.get_all_jobs()
        assert len(jobs) == 8
        assert _state.get("cnt", 0) == 0

        job = jobs[0]

        # basic accessors should not cause a fetch
        _ = job.computed_job_snapshot_id
        assert _state.get("cnt", 0) == 0

        _ = job.name
        assert _state.get("cnt", 0) == 0

        _ = job.active_presets
        assert _state.get("cnt", 0) == 0

        _ = job.job_snapshot
        assert _state.get("cnt", 0) == 1

        # access should be memoized
        _ = job.job_snapshot
        assert _state.get("cnt", 0) == 1

        # refetching job should share fetched data
        expected = 1  # from job[0] access
        for job in repo.get_all_jobs():
            _ = job.job_snapshot
            assert _state.get("cnt", 0) == expected
            expected += 1

        # Test that the external job source is available on the relevant job ref snap.
        external_job_ref = next(
            ref for ref in repository_snap.job_refs if ref.name == "job_with_external_tag"
        )
        assert external_job_ref.get_preview_tags().get(EXTERNAL_JOB_SOURCE_TAG_KEY) == "airflow"
        assert "foo" not in external_job_ref.get_preview_tags()


def test_job_data_snap_layout():
    # defend against assumptions made in

    # must remain last position
    assert get_storage_fields(JobDataSnap)[-1] == "pipeline_snapshot"
