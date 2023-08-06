# coding=utf-8
"""Utility functions for RPM CLI tests."""
from pulp_smash import cli


def count_langpacks(cfg, repo_id):
    """Tell how many langpack content units are in the given repository.

    :param cfg: Information about
        the Pulp deployment being targeted.
    :param repo_id: A repository ID.
    :returns: The number of langpacks in the named repository, as an integer.
    """
    # This function could be refactored to take a third "keyword" argument. But
    # what do we do about the "rpm" word in the command below?
    keyword = 'Package Langpacks:'
    completed_proc = cli.Client(cfg).run(
        'pulp-admin rpm repo list --repo-id {} --fields content_unit_counts'
        .format(repo_id).split()
    )
    lines = [
        line for line in completed_proc.stdout.splitlines() if keyword in line
    ]
    # A "Package Langpacks: n" line is printed only if at least one unit of
    # that kind is present.
    assert len(lines) in (0, 1)
    if lines:
        return int(lines[0].split(keyword)[1].strip())
    return 0
