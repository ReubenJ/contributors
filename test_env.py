"""This is the test module for the env module."""

import os
import unittest
from unittest.mock import patch

import env


class TestEnv(unittest.TestCase):
    """
    Test case for the env module.
    """

    def setUp(self):
        env_keys = [
            "DRY_RUN",
            "END_DATE",
            "GH_APP_ID",
            "GH_ENTERPRISE_URL",
            "GH_APP_INSTALLATION_ID",
            "GH_APP_PRIVATE_KEY",
            "GITHUB_APP_ENTERPRISE_ONLY",
            "GH_TOKEN",
            "ORGANIZATION",
            "REPOSITORY",
            "START_DATE",
        ]
        for key in env_keys:
            if key in os.environ:
                del os.environ[key]

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_APP_ID": "",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "token",
            "GH_ENTERPRISE_URL": "",
            "START_DATE": "2022-01-01",
            "END_DATE": "2022-12-31",
            "SPONSOR_INFO": "False",
            "LINK_TO_PROFILE": "True",
        },
        clear=True,
    )
    def test_get_env_vars(self):
        """
        Test the get_env_vars function when all environment variables are set correctly.
        """

        (
            organization,
            repository_list,
            gh_app_id,
            gh_app_installation_id,
            gh_app_private_key,
            gh_app_enterprise_only,
            token,
            ghe,
            start_date,
            end_date,
            sponsor_info,
            link_to_profile,
        ) = env.get_env_vars()

        self.assertEqual(organization, "org")
        self.assertEqual(repository_list, ["repo", "repo2"])
        self.assertIsNone(gh_app_id)
        self.assertIsNone(gh_app_installation_id)
        self.assertEqual(gh_app_private_key, b"")
        self.assertFalse(gh_app_enterprise_only)
        self.assertEqual(token, "token")
        self.assertEqual(ghe, "")
        self.assertEqual(start_date, "2022-01-01")
        self.assertEqual(end_date, "2022-12-31")
        self.assertFalse(sponsor_info)
        self.assertTrue(link_to_profile)

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_APP_ID": "",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "",
            "GH_ENTERPRISE_URL": "",
            "START_DATE": "2022-01-01",
            "END_DATE": "2022-12-31",
            "SPONSOR_INFO": "False",
            "LINK_TO_PROFILE": "True",
        },
        clear=True,
    )
    def test_get_env_vars_missing_values(self):
        """
        Test the get_env_vars function when none of the environment variables are set.
        Expect a ValueError to be raised.
        """

        with self.assertRaises(ValueError) as cm:
            env.get_env_vars()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), "GH_TOKEN environment variable not set")

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_APP_ID": "",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "token",
            "GH_ENTERPRISE_URL": "",
            "START_DATE": "2022/01/01",
            "END_DATE": "2022-12-31",
            "SPONSOR_INFO": "False",
            "LINK_TO_PROFILE": "True",
        },
        clear=True,
    )
    def test_get_env_vars_invalid_start_date(self):
        """
        Test the get_env_vars function when invalid start date given.
        Expect a ValueError to be raised.
        """

        with self.assertRaises(ValueError) as cm:
            env.get_env_vars()
        the_exception = cm.exception
        self.assertEqual(
            str(the_exception),
            "START_DATE environment variable not in the format YYYY-MM-DD",
        )

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_APP_ID": "",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "token",
            "GH_ENTERPRISE_URL": "",
            "START_DATE": "",
            "END_DATE": "",
            "SPONSOR_INFO": "False",
            "LINK_TO_PROFILE": "True",
        },
        clear=True,
    )
    def test_get_env_vars_no_dates(self):
        """
        Test the get_env_vars function when all environment variables are set correctly
        and start_date and end_date are not set.
        """

        (
            organization,
            repository_list,
            gh_app_id,
            gh_app_installation_id,
            gh_app_private_key,
            gh_app_enterprise_only,
            token,
            ghe,
            start_date,
            end_date,
            sponsor_info,
            link_to_profile,
        ) = env.get_env_vars()

        self.assertEqual(organization, "org")
        self.assertEqual(repository_list, ["repo", "repo2"])
        self.assertIsNone(gh_app_id)
        self.assertIsNone(gh_app_installation_id)
        self.assertEqual(gh_app_private_key, b"")
        self.assertFalse(gh_app_enterprise_only)
        self.assertEqual(token, "token")
        self.assertEqual(ghe, "")
        self.assertEqual(start_date, "")
        self.assertEqual(end_date, "")
        self.assertFalse(sponsor_info)
        self.assertTrue(link_to_profile)

    @patch.dict(os.environ, {})
    def test_get_env_vars_missing_org_or_repo(self):
        """Test that an error is raised if required environment variables are not set"""
        with self.assertRaises(ValueError) as cm:
            env.get_env_vars()
        the_exception = cm.exception
        self.assertEqual(
            str(the_exception),
            "ORGANIZATION and REPOSITORY environment variables were not set. Please set one",
        )

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "my_organization",
            "GH_APP_ID": "12345",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "",
        },
        clear=True,
    )
    def test_get_env_vars_auth_with_github_app_installation_missing_inputs(self):
        """Test that an error is raised there are missing inputs for the gh app"""
        with self.assertRaises(ValueError) as context_manager:
            env.get_env_vars()
        the_exception = context_manager.exception
        self.assertEqual(
            str(the_exception),
            "GH_APP_ID set and GH_APP_INSTALLATION_ID or GH_APP_PRIVATE_KEY variable not set",
        )


if __name__ == "__main__":
    unittest.main()
