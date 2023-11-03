import logging
import re
from landing_page_app.main.services.github_service import GithubService
from landing_page_app.main.config.constants import (
    MINISTRY_OF_JUSTICE,
    MOJ_ANALYTICAL_SERVICES,
    MOJ_TEST_ORG,
    MOJ_ORG_ALLOWED_EMAIL_DOMAINS,
    AS_ORG_ALLOWED_EMAIL_DOMAINS,
    MINIMUM_ORG_SEATS,
    MAX_ALLOWED_ORG_PENDING_INVITES,
    MOJ_ORGS,
)

logger = logging.getLogger(__name__)


class GithubScript:
    def __init__(self, github_service: GithubService):
        self.github_service = github_service

    def _check_email_address(self, email_address: str):
        valid = False
        if email_address is not None and email_address != "":
            regex = re.compile("[@]")
            if regex.search(email_address) is not None:
                valid = True
        return valid

    def _is_email_address_pre_approved(self, organisation: str, email_address: str):
        pre_approved = False
        if (
            self._check_email_address(email_address)
            and organisation != ""
            and organisation is not None
        ):
            email_domain = email_address[email_address.index("@") + 1:]
            if organisation.lower() == MOJ_ANALYTICAL_SERVICES:
                if email_domain in AS_ORG_ALLOWED_EMAIL_DOMAINS:
                    pre_approved = True
            elif organisation.lower() == MINISTRY_OF_JUSTICE:
                if email_domain in MOJ_ORG_ALLOWED_EMAIL_DOMAINS:
                    pre_approved = True
        return pre_approved

    def add_new_user_to_github_org(
        self, username: str, email_address: str, organisations: list
    ):
        non_approved_requests = []
        if (
            username == ""
            or username is None
            or email_address == ""
            or email_address is None
            or len(organisations) == 0
        ):
            logger.debug("add_new_user_to_github_org: incorrect function argument")
        else:
            user = self.github_service.get_user(username.lower())
            for organisation in organisations:
                if organisation.lower() in MOJ_ORGS:
                    if self._is_email_address_pre_approved(
                        organisation, email_address.lower()
                    ):
                        # TODO: change MOJ_TEST_ORG to organisation
                        if user is not None:
                            self.github_service.add_new_user_to_org(email_address.lower(), MOJ_TEST_ORG)
                            logger.debug(
                                f"{user.login.lower()} has been invited to {organisation.lower()} with the role 'member'."
                            )
                    else:
                        non_approved_requests.append(
                            {
                                "username": username.lower(),
                                "email_address": email_address.lower(),
                                "organisation": organisation.lower(),
                            }
                        )
        return non_approved_requests

    def get_selected_organisations(self, moj_org: bool, as_org: bool) -> list:
        organisations = []
        if moj_org:
            organisations.append(MINISTRY_OF_JUSTICE)
        if as_org:
            organisations.append(MOJ_ANALYTICAL_SERVICES)
        return organisations

    def is_user_in_audit_log(self, username: str = "", organisation: str = ""):
        found_user = False
        # TODO: change MOJ_TEST_ORG to organisation
        removed_users = self.github_service.get_removed_users_from_audit_log(MOJ_TEST_ORG)
        username = username.lower()
        if username in removed_users:
            found_user = True
        return found_user

    def is_github_seat_protection_enabled(self):
        protection_enabled = False
        for organisation in MOJ_ORGS:
            available_seats = self.github_service.get_org_available_seats(organisation)
            pending_invites = self.github_service.get_org_pending_invites(organisation)
            if available_seats <= MINIMUM_ORG_SEATS or pending_invites >= MAX_ALLOWED_ORG_PENDING_INVITES:
                protection_enabled = True
                break
        return protection_enabled
