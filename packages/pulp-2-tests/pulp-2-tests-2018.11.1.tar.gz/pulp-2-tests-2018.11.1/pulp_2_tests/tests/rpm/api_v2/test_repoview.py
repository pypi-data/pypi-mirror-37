# coding=utf-8
"""Tests that exercise Pulp's repoview feature.

For more information, see:

* `Pulp #189 <https://pulp.plan.io/issues/189>`_: "Repoview-like functionality
  for browsing repositories via the web interface"
* Yum Plugins → Yum Distributor → `Optional Configuration Parameters
  <http://docs.pulpproject.org/plugins/pulp_rpm/tech-reference/yum-plugins.html#optional-configuration-parameters>`_
"""
import unittest
from urllib.parse import urljoin

from packaging.version import Version
from pulp_smash import api, config, selectors, utils
from pulp_smash.pulp2.constants import REPOSITORY_PATH
from pulp_smash.pulp2.utils import publish_repo, upload_import_unit

from pulp_2_tests.constants import RPM_UNSIGNED_URL
from pulp_2_tests.tests.rpm.utils import set_up_module as setUpModule  # pylint:disable=unused-import
from pulp_2_tests.tests.rpm.api_v2.utils import gen_distributor, gen_repo


class RepoviewTestCase(unittest.TestCase):
    """Publish a repository with the repoview feature on and off.

    Do the following:

    1. Create an RPM repository, and add some content to it.
    2. Publish the repository. Get ``/pulp/repos/{rel_url}/``, and verify that
       no redirects occur.
    3. Publish the repository with the ``repoview`` and ``generate_sqlite``
       options set to true. Get ``/pulp/repos/{rel_url}/``, and verify that a
       redirect to ``/pulp/repos/{rel_url}/repoview/index.html`` occurs.
    4. Repeat step 2.
    """

    def test_all(self):
        """Publish a repository with the repoview feature on and off."""
        cfg = config.get_config()
        if cfg.pulp_version < Version('2.9'):
            self.skipTest('https://pulp.plan.io/issues/189')
        if utils.fips_is_supported(cfg) and utils.fips_is_enabled(cfg):
            self.skipTest('https://pulp.plan.io/issues/3775')

        # Create a repo, and add content
        client = api.Client(cfg)
        body = gen_repo()
        body['distributors'] = [gen_distributor()]
        repo = client.post(REPOSITORY_PATH, body).json()
        self.addCleanup(client.delete, repo['_href'])
        rpm = utils.http_get(RPM_UNSIGNED_URL)
        upload_import_unit(cfg, rpm, {'unit_type_id': 'rpm'}, repo)

        # Get info about the repo distributor
        repo = client.get(repo['_href'], params={'details': True}).json()
        pub_path = urljoin(
            '/pulp/repos/',
            repo['distributors'][0]['config']['relative_url']
        )

        # Publish the repo
        publish_repo(cfg, repo)
        response = client.get(pub_path)
        with self.subTest(comment='first publish'):
            self.assertEqual(len(response.history), 0, response.history)

        # Publish the repo a second time
        publish_repo(cfg, repo, {
            'id': repo['distributors'][0]['id'],
            'override_config': {'generate_sqlite': True, 'repoview': True},
        })
        response = client.get(pub_path)
        with self.subTest(comment='second publish'):
            self.assertEqual(len(response.history), 1, response.history)
            self.assertEqual(
                response.request.url,
                urljoin(response.history[0].request.url, 'repoview/index.html')
            )

        # Publish the repo a third time
        if not selectors.bug_is_fixed(2349, cfg.pulp_version):
            self.skipTest('https://pulp.plan.io/issues/2349')
        publish_repo(cfg, repo)
        response = client.get(pub_path)
        with self.subTest(comment='third publish'):
            self.assertEqual(len(response.history), 0, response.history)
