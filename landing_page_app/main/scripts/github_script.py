import logging
from landing_page_app.main.services.github_service import GithubService
from landing_page_app.main.config.constants import (
    MINISTRY_OF_JUSTICE,
    MOJ_ANALYTICAL_SERVICES,
    MOJ_TEST_ORG,
    MINIMUM_ORG_SEATS,
    MAX_ALLOWED_ORG_PENDING_INVITES,
    MOJ_ORGS,
)

logger = logging.getLogger(__name__)


class GithubScript:
    def __init__(self, github_service: GithubService):
        self.github_service = github_service

    def add_returning_user_to_github_org(self, username: str, organisations: list):
        if username == "" or username is None or len(organisations) == 0:
            logger.debug(
                "add_returning_user_to_github_org: incorrect function argument"
            )
        else:
            user = self.github_service.get_user(username.lower())
            if user is not None:
                for organisation in organisations:
                    if organisation.lower() in MOJ_ORGS:
                        # TODO: change MOJ_TEST_ORG to organisation
                        self.github_service.invite_user_to_org_using_nameduser(
                            user, MOJ_TEST_ORG
                        )
                        logger.debug(
                            f"{user.login.lower()} has been invited to {organisation.lower()} with the role 'member'."
                        )

    def add_new_user_to_github_org(self, email_address: str, organisations: list):
        if email_address == "" or email_address is None or len(organisations) == 0:
            logger.debug("add_new_user_to_github_org: incorrect function argument")
        else:
            for organisation in organisations:
                if organisation.lower() in MOJ_ORGS:
                    # TODO: change MOJ_TEST_ORG to organisation
                    self.github_service.invite_user_to_org_using_email_address(
                        email_address.lower(), MOJ_TEST_ORG
                    )
                    logger.debug(
                        f"{email_address.lower()} has been invited to {organisation.lower()} with the role 'member'."
                    )

    def get_selected_organisations(self, moj_org: bool, as_org: bool) -> list:
        organisations = []
        if moj_org:
            organisations.append(MINISTRY_OF_JUSTICE)
        if as_org:
            organisations.append(MOJ_ANALYTICAL_SERVICES)
        return organisations

    def validate_user_rejoining_org(self, organisations: list[str], username: str = ""):
        for organisation in organisations:
            if self.is_user_in_audit_log(username, organisation) is False:
                return False
        return True

    def is_user_in_audit_log(self, username: str = "", organisation: str = ""):
        found_user = False
        # TODO: change MOJ_TEST_ORG to organisation
        removed_users = self.github_service.get_removed_users_from_audit_log(
            MOJ_TEST_ORG
        )
        username = username.lower()
        if username in removed_users:
            found_user = True
        return found_user

    def is_github_seat_protection_enabled(self):
        protection_enabled = False
        for organisation in MOJ_ORGS:
            available_seats = self.github_service.get_org_available_seats(organisation)
            pending_invites = self.github_service.get_org_pending_invites(organisation)
            if (
                available_seats <= MINIMUM_ORG_SEATS
                or pending_invites >= MAX_ALLOWED_ORG_PENDING_INVITES
            ):
                protection_enabled = True
                break
        return protection_enabled
