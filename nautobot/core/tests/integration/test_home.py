from django.test.utils import override_settings
from selenium.common.exceptions import NoSuchElementException

from nautobot.circuits.models import Circuit, Provider
from nautobot.dcim.models import PowerFeed, PowerPanel, Site
from nautobot.tenancy.models import Tenant
from nautobot.utilities.testing.integration import SeleniumTestCase


class HomeTestCase(SeleniumTestCase):
    """Integration tests against the home page."""

    fixtures = ["user-data.json"]  # bob/bob
    layout = {
        "Organization": {
            "Sites": {"model": Site, "permission": "dcim.view_site"},
            "Tenant": {"model": Tenant, "permission": "tenancy.view_tenant"},
        },
        "Power": {
            "Power Feeds": {"model": PowerFeed, "permission": "dcim.view_powerfeed"},
            "Power Panel": {"model": PowerPanel, "permission": "dcim.view_powerpanel"},
        },
        "Circuits": {
            "Providers": {"model": Provider, "permission": "circuits.view_provider"},
            "Circuits": {"model": Circuit, "permission": "circuits.view_circuit"},
        },
    }

    def setUp(self):
        super().setUp()
        self.login(self.user.username, self.password)

    def tearDown(self):
        self.logout()
        super().tearDown()

    def get_panel_permissions(self, panel_details):
        permissions = []
        for panel in panel_details.values():
            permissions.append(panel["permission"])
        return permissions

    def test_login(self):
        """
        Perform a UI login.
        """
        # Wait for the page to render and make sure we got a body.
        self.load_page(self.live_server_url)

    def test_homepage_render(self):
        """
        Render homepage with app defined objects.
        """
        # Set test user to admin
        self.user.is_superuser = True
        self.user.save()

        self.load_page(self.live_server_url)

        columns_html = self.selenium.find_elements_by_class_name("homepage_column")
        for panel_name, panel_details in self.layout.items():
            columns_html[0].find_element_by_xpath(f".//strong[text()='{panel_name}']")
            for item_name, _ in panel_details.items():
                columns_html[0].find_element_by_xpath(f".//a[contains(text(), '{item_name}')]")

    def test_homepage_render_counters(self):
        """
        Ensure object counters are correct.
        """
        # Set test user to admin
        self.user.is_superuser = True
        self.user.save()

        self.load_page(self.live_server_url)

        columns_html = self.selenium.find_elements_by_class_name("homepage_column")
        for panel_name, panel_details in self.layout.items():
            columns_html[0].find_element_by_xpath(f".//strong[text()='{panel_name}']")
            for item_name, item_details in panel_details.items():
                item_html = columns_html[0].find_element_by_xpath(f".//a[contains(text(), '{item_name}')]")
                if item_details.get("model"):
                    counter = item_details["model"].objects.count()
                    counter_html = int(item_html.find_element_by_xpath("./../../span").get_property("innerHTML"))
                    self.assertEqual(counter, counter_html)

    @override_settings(HIDE_RESTRICTED_UI=False)
    def test_homepage_render_no_permissions(self):
        """
        Render homepage with no permissions.
        """
        self.load_page(self.live_server_url)

        columns_html = self.selenium.find_elements_by_class_name("homepage_column")
        for panel_name, panel_details in self.layout.items():
            columns_html[0].find_element_by_xpath(f".//strong[text()='{panel_name}']")
            for item_name, _ in panel_details.items():
                item_html = columns_html[0].find_element_by_xpath(f".//h4[contains(text(), '{item_name}')]")
                self.assertTrue(
                    "mdi mdi-lock" in item_html.find_element_by_xpath("./../span").get_property("innerHTML")
                )

    @override_settings(HIDE_RESTRICTED_UI=False)
    def test_homepage_render_limit_permissions(self):
        """
        Render homepage with limited permissions.
        """
        self.add_permissions("dcim.view_site")
        self.add_permissions("circuits.view_circuit")
        user_permissions = self.user.get_all_permissions()

        self.load_page(self.live_server_url)

        columns_html = self.selenium.find_elements_by_class_name("homepage_column")
        for panel_name, panel_details in self.layout.items():
            columns_html[0].find_element_by_xpath(f".//*[text()='{panel_name}']")
            for item_name, item_details in panel_details.items():
                if item_details["permission"] in user_permissions:
                    item_html = columns_html[0].find_element_by_xpath(f".//a[contains(text(), '{item_name}')]")
                    if item_details.get("model"):
                        counter = item_details["model"].objects.count()
                        counter_html = int(item_html.find_element_by_xpath("./../../span").get_property("innerHTML"))
                        self.assertEqual(counter, counter_html)
                else:
                    item_html = columns_html[0].find_element_by_xpath(f".//h4[contains(text(), '{item_name}')]")
                    self.assertTrue(
                        "mdi mdi-lock" in item_html.find_element_by_xpath("./../span").get_property("innerHTML")
                    )

    @override_settings(HIDE_RESTRICTED_UI=True)
    def test_homepage_render_limit_permissions_with_restricted_ui(self):
        """
        Render homepage with limited permissions and restricted UI.
        """
        self.add_permissions("dcim.view_site")
        self.add_permissions("circuits.view_circuit")
        user_permissions = self.user.get_all_permissions()

        self.load_page(self.live_server_url)

        columns_html = self.selenium.find_elements_by_class_name("homepage_column")
        for panel_name, panel_details in self.layout.items():
            if any(perm in self.get_panel_permissions(panel_details) for perm in user_permissions):
                columns_html[0].find_element_by_xpath(f".//strong[text()='{panel_name}']")
                for item_name, item_details in panel_details.items():
                    if item_details["permission"] in user_permissions:
                        columns_html[0].find_element_by_xpath(f".//a[contains(text(), '{item_name}')]")
                    else:
                        with self.assertRaises(NoSuchElementException):
                            columns_html[0].find_element_by_xpath(f".//h4[contains(text(), '{item_name}')]")
            else:
                with self.assertRaises(NoSuchElementException):
                    columns_html[0].find_element_by_xpath(f".//*[contains(text(), '{panel_name}')]")
