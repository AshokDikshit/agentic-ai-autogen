import { Then, defineParameterType } from '@wdio/cucumber-framework';
import uiAssertions from '../../support/uiAssertions';

// ===============================
// CUSTOM PARAMETER TYPES
// ===============================
// Define custom parameter type for element types
// This allows centralized management of element types
// Alternative approach: Use direct regex patterns in step definitions
// Since {elementType} might not work in all Cucumber implementations
defineParameterType({
    name: 'elementType',
    regexp: /button|link|element|field|input|textbox|section/,
    transformer: (s: string) => s
});

// ===============================
// GLOBAL ASSERTIONS STEP DEFINITIONS
// ===============================
// This file contains only assertion steps (Then) that verify conditions
// For actions and operations, see global-actions.steps.ts

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label|radio button) should be visible$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be visible`);
    await uiAssertions.verifyElementVisible(element, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label|radio button) should not be visible$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should not be visible`);
    await uiAssertions.verifyElementNotVisible(element, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label|radio button) should be displayed$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be displayed`);
    await uiAssertions.verifyElementDisplayed(element, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label|radio button) should be hidden$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be hidden`);
    await uiAssertions.verifyElementHidden(element, elementType);
});

// Element State Assertions
Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label|radio button) should be enabled$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be enabled`);
    await uiAssertions.verifyElementEnabled(element, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label|radio button) should be disabled$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be disabled`);
    await uiAssertions.verifyElementDisabled(element, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label|radio button) should be selected$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be selected`);
    await uiAssertions.verifyElementSelected(element, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label|radio button) should not be selected$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should not be selected`);
    await uiAssertions.verifyElementNotSelected(element, elementType);
});

Then(/^"([^"]*)" (checkbox|element) should be checked$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be checked`);
    await uiAssertions.verifyCheckboxChecked(element);
});

Then(/^"([^"]*)" (checkbox|element) should be unchecked$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be unchecked`);
    await uiAssertions.verifyCheckboxUnchecked(element);
});

// Text and Content Assertions
Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should contain text "([^"]*)"$/, async (element: string, elementType: string, text: string) => {
    console.log(`Verifying ${element} ${elementType} should contain text "${text}"`);
    await uiAssertions.verifyElementContainsText(element, text, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should not contain text "([^"]*)"$/, async (element: string, elementType: string, text: string) => {
    console.log(`Verifying ${element} ${elementType} should not contain text "${text}"`);
    // Implementation needed
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should have exact text "([^"]*)"$/, async (element: string, elementType: string, text: string) => {
    console.log(`Verifying ${element} ${elementType} should have exact text "${text}"`);
    await uiAssertions.verifyElementExactText(element, text, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should be empty$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be empty`);
    await uiAssertions.verifyFieldEmpty(element, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should have value "([^"]*)"$/, async (element: string, elementType: string, value: string) => {
    console.log(`Verifying ${element} ${elementType} should have value "${value}"`);
    await uiAssertions.verifyElementValue(element, value, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should have placeholder "([^"]*)"$/, async (element: string, elementType: string, placeholder: string) => {
    console.log(`Verifying ${element} ${elementType} should have placeholder "${placeholder}"`);
    await uiAssertions.verifyElementPlaceholder(element, placeholder, elementType);
});

// Attribute and Property Assertions
Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should have attribute "([^"]*)" with value "([^"]*)"$/, async (element: string, elementType: string, attribute: string, value: string) => {
    console.log(`Verifying ${element} ${elementType} should have attribute "${attribute}" with value "${value}"`);
    await uiAssertions.verifyElementAttribute(element, attribute, value, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should have class "([^"]*)"$/, async (element: string, elementType: string, className: string) => {
    console.log(`Verifying ${element} ${elementType} should have class "${className}"`);
    await uiAssertions.verifyElementHasClass(element, className, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should not have class "([^"]*)"$/, async (element: string, elementType: string, className: string) => {
    console.log(`Verifying ${element} ${elementType} should not have class "${className}"`);
    await uiAssertions.verifyElementNotHasClass(element, className, elementType);
});

// Count and List Assertions
Then(/^there should be (\d+) "([^"]*)" elements$/, async (count: string, element: string) => {
    console.log(`Verifying there should be ${count} ${element} elements`);
    await uiAssertions.verifyElementCount(element, parseInt(count));
});

Then(/^there should be at least (\d+) "([^"]*)" elements$/, async (count: string, element: string) => {
    console.log(`Verifying there should be at least ${count} ${element} elements`);
    await uiAssertions.verifyElementCountAtLeast(element, parseInt(count));
});

Then(/^there should be at most (\d+) "([^"]*)" elements$/, async (count: string, element: string) => {
    console.log(`Verifying there should be at most ${count} ${element} elements`);
    await uiAssertions.verifyElementCountAtMost(element, parseInt(count));
});

Then(/^"([^"]*)" list should contain "([^"]*)"$/, async (element: string, item: string) => {
    console.log(`Verifying ${element} list should contain "${item}"`);
    await uiAssertions.verifyListContains(element, item);
});

Then(/^"([^"]*)" list should not contain "([^"]*)"$/, async (element: string, item: string) => {
    console.log(`Verifying ${element} list should not contain "${item}"`);
    await uiAssertions.verifyListNotContains(element, item);
});

// Page and Navigation Assertions
Then(/^the page title should be "([^"]*)"$/, async (title: string) => {
    console.log(`Verifying the page title should be "${title}"`);
    await uiAssertions.verifyPageTitle(title);
});

Then(/^the current URL should contain "([^"]*)"$/, async (urlPart: string) => {
    console.log(`Verifying the current URL should contain "${urlPart}"`);
    await uiAssertions.verifyUrlContains(urlPart);
});

Then(/^the current URL should be "([^"]*)"$/, async (url: string) => {
    console.log(`Verifying the current URL should be "${url}"`);
    await uiAssertions.verifyUrl(url);
});

// Alert and Modal Assertions
Then(/^an alert should be present$/, async () => {
    console.log('Verifying an alert should be present');
    await uiAssertions.verifyAlertPresent();
});

Then(/^no alert should be present$/, async () => {
    console.log('Verifying no alert should be present');
    await uiAssertions.verifyNoAlertPresent();
});

Then(/^the alert text should be "([^"]*)"$/, async (text: string) => {
    console.log(`Verifying the alert text should be "${text}"`);
    await uiAssertions.verifyAlertText(text);
});

Then(/^a modal should be open$/, async () => {
    console.log('Verifying a modal should be open');
    await uiAssertions.verifyModalOpen();
});

Then(/^no modal should be open$/, async () => {
    console.log('Verifying no modal should be open');
    await uiAssertions.verifyNoModalOpen();
});

// Form Validation Assertions
Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should show validation error "([^"]*)"$/, async (element: string, elementType: string, error: string) => {
    console.log(`Verifying ${element} ${elementType} should show validation error "${error}"`);

    await uiAssertions.verifyValidationError(element, error, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should not show any validation error$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should not show any validation error`);

    await uiAssertions.verifyNoValidationError(element, elementType);
});

Then(/^the form should be valid$/, async () => {
    console.log('Verifying the form should be valid');
    await uiAssertions.verifyFormValid();
});

Then(/^the form should be invalid$/, async () => {
    console.log('Verifying the form should be invalid');
    await uiAssertions.verifyFormInvalid();
});

// Loading and State Assertions
Then(/^the page should be loaded$/, async () => {
    console.log('Verifying the page should be loaded');
    await uiAssertions.verifyPageLoaded();
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should be loading$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should be loading`);

    await uiAssertions.verifyElementLoading(element, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should not be loading$/, async (element: string, elementType: string) => {
    console.log(`Verifying ${element} ${elementType} should not be loading`);
    await uiAssertions.verifyElementNotLoading(element, elementType);
});

// Mobile-specific Assertions
Then(/^the device orientation should be (landscape|portrait)$/, async (orientation: string) => {
    console.log(`Verifying the device orientation should be ${orientation}`);
    await uiAssertions.verifyDeviceOrientation(orientation);
});

Then(/^the keyboard should be visible$/, async () => {
    console.log('Verifying the keyboard should be visible');
    await uiAssertions.verifyKeyboardVisible();
});

Then(/^the keyboard should be hidden$/, async () => {
    console.log('Verifying the keyboard should be hidden');
    await uiAssertions.verifyKeyboardHidden();
});

// Wait-based Assertions
Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should appear within (\d+) seconds$/, async (element: string, elementType: string, timeout: string) => {
    console.log(`Verifying ${element} ${elementType} should appear within ${timeout} seconds`);
    await uiAssertions.verifyElementAppearsWithin(element, parseInt(timeout), elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should disappear within (\d+) seconds$/, async (element: string, elementType: string, timeout: string) => {
    console.log(`Verifying ${element} ${elementType} should disappear within ${timeout} seconds`);
    await uiAssertions.verifyElementDisappearsWithin(element, parseInt(timeout), elementType);
});

// Style and Visual Assertions
Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should have background color "([^"]*)"$/, async (element: string, elementType: string, color: string) => {
    console.log(`Verifying ${element} ${elementType} should have background color "${color}"`);
    await uiAssertions.verifyElementBackgroundColor(element, color, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should have text color "([^"]*)"$/, async (element: string, elementType: string, color: string) => {
    console.log(`Verifying ${element} ${elementType} should have text color "${color}"`);
    await uiAssertions.verifyElementTextColor(element, color, elementType);
});

Then(/^"([^"]*)" (button|link|element|field|input|textbox|section|heading|label) should be positioned at coordinates \((\d+),(\d+)\)$/, async (element: string, elementType: string, x: string, y: string) => {
    console.log(`Verifying ${element} ${elementType} should be positioned at coordinates (${x},${y})`);
    await uiAssertions.verifyElementPosition(element, parseInt(x), parseInt(y), elementType);
});