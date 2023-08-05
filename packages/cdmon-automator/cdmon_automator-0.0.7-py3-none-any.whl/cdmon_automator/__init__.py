import chromedriver_binary
from decouple import config
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait, Select

TIMEOUT = config("TIMEOUT", cast=int, default=10)

# redirect_type can be one of the following:
REDIRECT_TYPE_OPTS = {
    "@": "1",     # The entire domain
    "*": "2",     # Undefined subdomains
    "custom": "3" # Custom subdomain
}

class document_complete(object):
    def __call__(self, driver):
        script = 'return document.readyState'
        try:
            return driver.execute_script(script) == 'complete'
        except WebDriverException:
            return False

class CDMON():
    def __init__(self):
        options = Options()
        if not config("DEBUG", cast=bool, default=False):
            options.add_argument("--headless")

        if config("NETDEBUG", cast=bool, default=False):
            import http.client
            http.client.HTTPConnection.debuglevel = 1

        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            chrome_options=options
        )
        self.driver.implicitly_wait(TIMEOUT)
        self.driver.set_page_load_timeout(TIMEOUT)
        self.driver.set_window_size(1920, 2160)

    def login(self):
        self.driver.get("https://admin.cdmon.com/es/acceso")
        self._disable_alerts()

        user_field = self.driver.find_element_by_name("dades[usuario]")
        user_field.clear()
        user_field.send_keys(config("USERNAME"))

        password_field = self.driver.find_element_by_name("dades[contrasenya]")
        password_field.clear()
        password_field.send_keys(config("PASSWORD"))

        login_button = self.driver.find_element_by_xpath("//button[@title='Entrar']")
        login_button.click()

    def work_on(self, domain_name):
        self.domain_name = domain_name

    def create_record(self, record_type, values):
        self._go_to_domain()
        self._go_to_dns_entries()

        create_button = self.driver.find_element_by_id("btnNewDns")
        create_button.click()

        record_type_dropdown = Select(self.driver.find_element_by_id("tipus"))
        record_type_dropdown.select_by_value(record_type.lower())

        sw = record_type.upper()

        if sw == "TXT" or sw == "SPF":
            self._setup_txt_spf_a_aaaa_cname_ns_srv(values)
            self._fill_txt_spf(values)

        elif sw == "A" or sw == "AAAA" or sw == "CNAME" or sw == "NS":
            self._setup_txt_spf_a_aaaa_cname_ns_srv(values)
            self._fill_a_aaaa_cname_ns(values)

        elif sw == "SRV":
            self._setup_txt_spf_a_aaaa_cname_ns_srv(values)
            self._fill_srv(values)

        elif sw == "MX":
            self._setup_mx(values)
            self._fill_mx(values)

        save_button = self.driver.find_element_by_xpath("//div/button[@title='Guardar registro']")
        save_button.click()

        self._handle_save_record()

    def change_record(self, record_type, record_name, values):
        self._go_to_domain()
        self._go_to_dns_entries()

        row = self._find_record_row(record_type, record_name)

        edit_link = row.find_element_by_link_text("Editar registro")
        edit_link.click()

        sw = record_type.upper()

        if sw == "TXT" or sw == "SPF":
            self._fill_txt_spf(values)

        elif sw == "A" or sw == "AAAA" or sw == "CNAME" or sw == "NS":
            self._fill_a_aaaa_cname_ns(values)

        elif sw == "SRV":
            self._fill_srv(values)

        elif sw == "MX":
            self._fill_mx(values)

        save_button = self.driver.find_element_by_xpath("//div/button[@title='Guardar registro']")
        save_button.click()

        self._handle_save_record()

    def delete_record(self, record_type, record_name):
        self._go_to_domain()
        self._go_to_dns_entries()

        row = self._find_record_row(record_type, record_name)

        delete_link = row.find_element_by_css_selector(".action-delete")
        delete_link.click()

        self._handle_delete_record()

    def terminate(self):
        self.driver.quit()

    """
    PRIVATE METHODS
    """
    def _disable_alerts(self):
        WebDriverWait(self.driver, TIMEOUT).until(document_complete())
        self.driver.execute_script("window.onbeforeunload = function() {};")
        self.driver.execute_script("window.alert = function() {};")
        self.driver.execute_script("window.confirm = function() {};")

    def _find_record_row(self, record_type, record_name):
        expected_row = None
        self.driver.implicitly_wait(0)

        rows = self.driver.find_elements_by_css_selector(".tipus-%s" % record_type.upper())
        for row in rows:
            try:
                res = row.find_element_by_xpath(".//td[contains(text(), '%s')]" % record_name)
                if res:
                    expected_row = row
            except:
                pass

        self.driver.implicitly_wait(TIMEOUT)

        if not expected_row:
            raise Exception("I can't find the requested record")

        return expected_row

    def _go_to_domain(self):
        self._disable_alerts()

        domains_link = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.LINK_TEXT, "Listado dominios")
            )
        )
        domains_link.click()

        self._disable_alerts()

        domain_link = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.LINK_TEXT, self.domain_name)
            )
        )
        domain_link.click()

        self._disable_alerts()

    def _go_to_dns_entries(self):
        self._disable_alerts()

        dns_entries_link = self.driver.find_element_by_link_text("Gestionar registros")
        dns_entries_link.click()

        self._disable_alerts()

    def _handle_save_record(self):
        self.driver.implicitly_wait(1)

        try:
            self.driver.find_element_by_xpath("//body/section[contains(@id, 'panel-alert')]//p[contains(text(), 'error')]")
            self.driver.save_screenshot("error.png")
            raise Exception("Something went wrong!")
        except NoSuchElementException as ex:
            pass

        self.driver.implicitly_wait(TIMEOUT)

        accept_button = self.driver.find_element_by_xpath("//body/section[contains(@id, 'panel-alert')]//button[@title='Aceptar']")
        accept_button.click()

    def _handle_delete_record(self):
        self.driver.implicitly_wait(1)

        try:
            self.driver.find_element_by_xpath("//body/section[contains(@id, 'panel-alert')]//p[contains(text(), 'error')]")
            self.driver.save_screenshot("error.png")
            raise Exception("Something went wrong!")
        except NoSuchElementException as ex:
            pass

        self.driver.implicitly_wait(TIMEOUT)

        accept_button = self.driver.find_element_by_xpath("//body/section[contains(@id, 'panel-confirm')]//button[@title='Aceptar']")
        accept_button.click()

    """
    FORM HELPERS

    _setup_* methods are onlyused during the creation of a new record, because
    the "edit record" dialog doesn't have all the fields that the "create
    record" dialog has.
    """
    def _setup_txt_spf_a_aaaa_cname_ns_srv(self, values):
        redirect_type_dropdown = Select(self.driver.find_element_by_id("redir"))
        redirect_type_dropdown.select_by_value(
            REDIRECT_TYPE_OPTS.get(
                values.get("redirect_type").lower()
            )
        )

        redirect_host_field = self.driver.find_element_by_id("redirHost")
        redirect_host_field.clear()
        redirect_host_field.send_keys(values.get("subdomain"))

    def _fill_txt_spf(self, values):
        value_field = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "valor")
            )
        )
        value_field.clear()
        value_field.send_keys(values.get("value"))

    def _fill_a_aaaa_cname_ns(self, values):
        value_field = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "desti")
            )
        )
        value_field.clear()
        value_field.send_keys(values.get("destination"))

    def _fill_srv(self, values):
        value_field = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "desti")
            )
        )
        value_field.clear()
        value_field.send_keys(values.get("destination"))

        priority_field = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "prioritat")
            )
        )
        priority_field.clear()
        priority_field.send_keys(values.get("priority"))

        weight_field = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "peso")
            )
        )
        weight_field.clear()
        weight_field.send_keys(values.get("weight"))

        port_field = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "puerto")
            )
        )
        port_field.clear()
        port_field.send_keys(values.get("port"))

    def _setup_mx(self, values):
        redirect_host_field = self.driver.find_element_by_id("host")
        redirect_host_field.clear()
        redirect_host_field.send_keys(values.get("subdomain"))

    def _fill_mx(self, values):
        value_field = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "desti")
            )
        )
        value_field.clear()
        value_field.send_keys(values.get("destination"))

        priority_field = WebDriverWait(self.driver, TIMEOUT).until(
            expected_conditions.element_to_be_clickable(
                (By.ID, "prioritat")
            )
        )
        priority_field.clear()
        priority_field.send_keys(values.get("priority"))