######################################################################
# Copyright 2016, 2021 John J. Rofrano.
######################################################################
"""
Web Steps

Step definitions for interacting with the Product UI using Selenium
"""

import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = "product_"


######################################################################
# BASIC NAVIGATION
######################################################################
@when('I visit the "Home Page"')
def step_visit_home(context):
    context.driver.get(context.base_url)


@then('I should see "{message}" in the title')
def step_see_title(context, message):
    assert message in context.driver.title


@then('I should not see "{text}"')
def step_should_not_see(context, text):
    body = context.driver.find_element(By.TAG_NAME, "body")
    assert text not in body.text


######################################################################
# FORM INPUTS
######################################################################
@when('I set the "{field}" to "{value}"')
def step_set_field(context, field, value):
    field_id = ID_PREFIX + field.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, field_id)
    element.clear()
    element.send_keys(value)


@when('I select "{value}" in the "{field}" dropdown')
@when('I select "{value}" from the "{field}" dropdown')
def step_select_dropdown(context, value, field):
    field_id = ID_PREFIX + field.lower().replace(" ", "_")
    select = Select(context.driver.find_element(By.ID, field_id))
    select.select_by_visible_text(value)


######################################################################
# VERIFY FORM VALUES
######################################################################
@then('I should see "{text}" in the "{field}" field')
@when('I should see "{text}" in the "{field}" field')
def step_see_field_value(context, text, field):
    field_id = ID_PREFIX + field.lower().replace(" ", "_")
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.text_to_be_present_in_element_value((By.ID, field_id), text)
    )


@then('I should see "{value}" in the "{field}" dropdown')
@when('I should see "{value}" in the "{field}" dropdown')
def step_verify_dropdown(context, value, field):
    field_id = ID_PREFIX + field.lower().replace(" ", "_")
    select = Select(context.driver.find_element(By.ID, field_id))
    assert select.first_selected_option.text == value


@then('the "{field}" field should be empty')
def step_field_empty(context, field):
    field_id = ID_PREFIX + field.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, field_id)
    assert element.get_attribute("value") == ""


######################################################################
# COPY & PASTE
######################################################################
@when('I copy the "{field}" field')
def step_copy_field(context, field):
    field_id = ID_PREFIX + field.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, field_id)
    context.clipboard = element.get_attribute("value")
    logging.info("Clipboard = %s", context.clipboard)


@when('I paste the "{field}" field')
def step_paste_field(context, field):
    field_id = ID_PREFIX + field.lower().replace(" ", "_")
    element = context.driver.find_element(By.ID, field_id)
    element.clear()
    element.send_keys(context.clipboard)


######################################################################
# BUTTON ACTIONS
######################################################################
@when('I press the "{button}" button')
def step_press_button(context, button):
    button_id = button.lower() + "-btn"
    context.driver.find_element(By.ID, button_id).click()


######################################################################
# RESULTS & MESSAGES
######################################################################
@then('I should see "{text}" in the results')
@when('I should see "{text}" in the results')
def step_see_results(context, text):
    results = context.driver.find_element(By.ID, "search_results")
    assert text in results.text


@then('I should see the message "{message}"')
def step_see_message(context, message):
    flash = context.driver.find_element(By.ID, "flash_message")
    assert message in flash.text
