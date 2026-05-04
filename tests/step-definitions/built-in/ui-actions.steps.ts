import { Given, When, Then } from '@wdio/cucumber-framework';
import { $ } from '@wdio/globals';
import uiActions from '../../support/uiActions';
// ===============================
// GLOBAL ACTIONS STEP DEFINITIONS
// ===============================
// This file contains only action steps (Given/When) that perform operations
// For assertions and verifications, see global-assertions.steps.ts

// ===============================
// CLICK ACTIONS
// ===============================
When(/^I click on "([^"]*)" (button|link|element|radio button)$/, async (elementName: string, elementType: string) => {
    console.log(`Clicking on ${elementName} ${elementType}`);
    await uiActions.clickOn(elementName, elementType);
});

When(/^I double click on "([^"]*)" (button|link|element|radio button)$/, async (elementName: string, elementType: string) => {
    console.log(`Double clicking on ${elementName} ${elementType}`);
    await uiActions.doubleClickOn(elementName, elementType);
});

When(/^I right click on "([^"]*)" (button|link|element|radio button)$/, async (elementName: string, elementType: string) => {
    console.log(`Right clicking on ${elementName} ${elementType}`);
    await uiActions.rightClickOn(elementName, elementType);
});

// ===============================
// DROPDOWN AND SELECTION ACTIONS
// ===============================
When(/^I select "([^"]*)" from "([^"]*)" dropdown$/, async (option: string, elementName: string) => {
    console.log(`Selecting "${option}" from ${elementName} dropdown`);
    await uiActions.selectFromDropdown(elementName, option);
});

When(/^I select "([^"]*)" option from "([^"]*)" dropdown$/, async (option: string, elementName: string) => {
    console.log(`Selecting ${option} option from ${elementName} dropdown`);
    await uiActions.selectFromDropdown(elementName, option);
});

// ===============================
// HOVER AND FOCUS ACTIONS
// ===============================
When(/^I hover over "([^"]*)" (button|link|element|radio button)$/, async (elementName: string, elementType: string) => {
    console.log(`Hovering over ${elementName} ${elementType}`);
    await uiActions.hoverOn(elementName, elementType);
});

When(/^I focus on "([^"]*)" (field|input|element)$/, async (elementName: string, elementType: string) => {
    console.log(`Focusing on ${elementName} ${elementType}`);
    await uiActions.focusOn(elementName, elementType);
});

// ===============================
// SCROLL ACTIONS
// ===============================
When(/^I scroll to "([^"]*)" (element|section)$/, async (elementName: string, elementType: string) => {
    console.log(`Scrolling to ${elementName} ${elementType}`);
    await uiActions.scrollTo(elementName, elementType);
});

When(/^I scroll to "([^"]*)" and click$/, async (elementName: string) => {
    console.log(`Scrolling to ${elementName} and clicking`);
    await uiActions.scrollToAndClick(elementName);
});

When(/^I scroll to "([^"]*)" and double click$/, async (elementName: string) => {
    console.log(`Scrolling to ${elementName} and double clicking`);
    await uiActions.scrollToAndDoubleClick(elementName);
});

When(/^I scroll to "([^"]*)" and right click$/, async (elementName: string) => {
    console.log(`Scrolling to ${elementName} and right clicking`);
    await uiActions.scrollToAndRightClick(elementName);
});

When(/^I scroll (left|right|up|down) to "([^"]*)" and click on "([^"]*)"$/, async (direction: string, targetElement: string, clickElement: string) => {
    console.log(`Scrolling ${direction} to ${targetElement} and clicking on ${clickElement}`);
    await uiActions.scrollDirectionToAndClick(direction, targetElement, clickElement);
});

When(/^I scroll (left|right|up|down) by (\d+) pixels$/, async (direction: string, pixels: string) => {
    console.log(`Scrolling ${direction} by ${pixels} pixels`);
    await uiActions.scrollByPixels(direction, pixels);
});

// ===============================
// TOUCH AND GESTURE ACTIONS (Mobile)
// ===============================
When(/^I press and hold "([^"]*)" (element|button)$/, async (elementName: string, elementType: string) => {
    console.log(`Pressing and holding ${elementName} ${elementType}`);
    await uiActions.pressAndHold(elementName, elementType);
});

When(/^I release the hold on "([^"]*)" (element|button)$/, async (elementName: string, elementType: string) => {
    console.log(`Releasing hold on ${elementName} ${elementType}`);
    await uiActions.releaseHold(elementName, elementType);
});

When(/^I long press on "([^"]*)" (element|button)$/, async (elementName: string, elementType: string) => {
    console.log(`Long pressing on ${elementName} ${elementType}`);
    await uiActions.longPress(elementName, elementType);
});

When(/^I swipe from "([^"]*)" to "([^"]*)"$/, async (fromElement: string, toElement: string) => {
    console.log(`Swiping from ${fromElement} to ${toElement}`);
    await uiActions.swipeFromTo(fromElement, toElement);
});

When(/^I swipe (left|right|up|down) on "([^"]*)"$/, async (direction: string, elementName: string) => {
    console.log(`Swiping ${direction} on ${elementName}`);
    await uiActions.swipeDirection(direction, elementName);
});

When(/^I pinch in on "([^"]*)"$/, async (elementName: string) => {
    console.log(`Pinching in on ${elementName}`);
    await uiActions.pinchIn(elementName);
});

When(/^I pinch out on "([^"]*)"$/, async (elementName: string) => {
    console.log(`Pinching out on ${elementName}`);
    await uiActions.pinchOut(elementName);
});

When(/^I zoom in on "([^"]*)"$/, async (elementName: string) => {
    console.log(`Zooming in on ${elementName}`);
    await uiActions.zoomIn(elementName);
});

When(/^I zoom out on "([^"]*)"$/, async (elementName: string) => {
    console.log(`Zooming out on ${elementName}`);
    await uiActions.zoomOut(elementName);
});
// ===============================
// TEXT INPUT ACTIONS
// ===============================
When(/^I (type|enter) "([^"]*)" into "([^"]*)" (field|input|textbox)$/, async (action: string, text: string, elementName: string, elementType: string) => {
    console.log(`Typing/Entering "${text}" into ${elementName} ${elementType}`);
    await uiActions.typeText(text, elementName, elementType);
});

When(/^I clear "([^"]*)" (field|input|textbox)$/, async (elementName: string, elementType: string) => {
    console.log(`Clearing ${elementName} ${elementType}`);
    await uiActions.clearField(elementName, elementType);
});

When(/^I select all text in "([^"]*)" (field|input|textbox)$/, async (elementName: string, elementType: string) => {
    console.log(`Selecting all text in ${elementName} ${elementType}`);
    await uiActions.selectAllText(elementName, elementType);
});

// ===============================
// CHECKBOX AND RADIO ACTIONS
// ===============================
When(/^I check "([^"]*)" checkbox$/, async (elementName: string) => {
    console.log(`Checking ${elementName} checkbox`);
    await uiActions.checkCheckbox(elementName);
});

When(/^I uncheck "([^"]*)" checkbox$/, async (elementName: string) => {
    console.log(`Unchecking ${elementName} checkbox`);
    await uiActions.uncheckCheckbox(elementName);
});

When(/^I select "([^"]*)" radio button$/, async (elementName: string) => {
    console.log(`Selecting ${elementName} radio button`);
    await uiActions.selectRadioButton(elementName);
});



// ===============================
// NAVIGATION ACTIONS
// ===============================
Given(/^I navigate to "([^"]*)"$/, async (url: string) => {
    console.log(`Navigating to "${url}"`);
    await uiActions.navigateTo(url);
});

When(/^I go back$/, async () => {
    console.log('Going back in browser');
    await uiActions.goBack();
});

When(/^I go forward$/, async () => {
    console.log('Going forward in browser');
    await uiActions.goForward();
});

When(/^I refresh the page$/, async () => {
    console.log('Refreshing the page');
    await uiActions.refreshPage();
});

When(/^I reload the page$/, async () => {
    console.log('Reloading the page');
    await uiActions.reloadPage();
});

When(/^I switch to tab (\d+)$/, async (tabIndex: string) => {
    console.log(`Switching to tab ${tabIndex}`);
    await uiActions.switchToTab(tabIndex);
});

When(/^I open new tab$/, async () => {
    console.log('Opening new tab');
    await uiActions.openNewTab();
});

When(/^I close current tab$/, async () => {
    console.log('Closing current tab');
    await uiActions.closeCurrentTab();
});



// ===============================
// WAIT ACTIONS
// ===============================
When(/^I wait for "([^"]*)" (button|link|element|radio button) to be visible$/, async (elementName: string, elementType: string) => {
    console.log(`Waiting for ${elementName} ${elementType}  to be visible`);
    await uiActions.waitSeconds(5); // Short wait to ensure any animations have started
    await uiActions.waitForVisible(elementName, elementType);
});

When(/^I wait for "([^"]*)" (button|link|element|radio button) to disappear$/, async (elementName: string, elementType: string) => {
    console.log(`Waiting for ${elementName} ${elementType} to disappear`);
    await uiActions.waitForDisappear(elementName, elementType);
});

When(/^I wait for "([^"]*)" (button|link|element|radio button) to be enabled$/, async (elementName: string, elementType: string) => {
    console.log(`Waiting for ${elementName} ${elementType} to be enabled`);
    await uiActions.waitForEnabled(elementName, elementType);
});

When(/^I wait for "([^"]*)" (button|link|element|radio button) to be clickable$/, async (elementName: string, elementType: string) => {
    console.log(`Waiting for ${elementName} ${elementType} to be clickable`);
    await uiActions.waitForClickable(elementName, elementType  );
});

When(/^I wait (\d+) seconds$/, async (seconds: string) => {
    console.log(`Waiting ${seconds} seconds`);
    await uiActions.waitSeconds(seconds);
});

When('I wait for page to load', async () => {
    console.log('Waiting for page to load');
    await uiActions.waitForPageLoad();
});

// ===============================
// FILE UPLOAD ACTIONS
// ===============================
When(/^I upload file "([^"]*)" to "([^"]*)"$/, async (filePath: string, elementName: string) => {
    console.log(`Uploading file "${filePath}" to ${elementName}`);
    await uiActions.uploadFile(filePath, elementName);
});

When(/^I select file "([^"]*)" from file picker$/, async (filePath: string) => {
    console.log(`Selecting file "${filePath}" from file picker`);
    await uiActions.selectFileFromPicker(filePath);
});



// ===============================
// ALERT AND MODAL ACTIONS
// ===============================
When(/^I accept the alert$/, async () => {
    console.log('Accepting the alert');
    await uiActions.acceptAlert();
});

When(/^I dismiss the alert$/, async () => {
    console.log('Dismissing the alert');
    await uiActions.dismissAlert();
});

When(/^I type "([^"]*)" in alert prompt$/, async (text: string) => {
    console.log(`Typing "${text}" in alert prompt`);
    await uiActions.typeInAlert(text);
});

When(/^I close the modal$/, async () => {
    console.log('Closing the modal');
    await uiActions.closeModal();
});

When(/^I click outside the modal$/, async () => {
    console.log('Clicking outside the modal');
    await uiActions.clickOutsideModal();
});



// ===============================
// MOBILE-SPECIFIC ACTIONS
// ===============================
When(/^I rotate device to (landscape|portrait)$/, async (orientation: string) => {
    console.log(`Rotating device to ${orientation}`);
    await uiActions.rotateDevice(orientation);
});

When(/^I shake the device$/, async () => {
    console.log('Shaking the device');
    await uiActions.shakeDevice();
});

When(/^I lock the device$/, async () => {
    console.log('Locking the device');
    await uiActions.lockDevice();
});

When(/^I unlock the device$/, async () => {
    console.log('Unlocking the device');
    await uiActions.unlockDevice();
});

When(/^I put app in background for (\d+) seconds$/, async (seconds: string) => {
    console.log(`Putting app in background for ${seconds} seconds`);
    await uiActions.putAppInBackground(seconds);
});

When(/^I bring app to foreground$/, async () => {
    console.log('Bringing app to foreground');
    await uiActions.bringAppToForeground();
});

When(/^I take a screenshot$/, async () => {
    console.log('Taking a screenshot');
    await uiActions.takeScreenshot();
});

When(/^I hide keyboard$/, async () => {
    console.log('Hiding keyboard');
    await uiActions.hideKeyboard();
});

When(/^I show keyboard$/, async () => {
    console.log('Showing keyboard');
    await uiActions.showKeyboard();
});

// ===============================
// FORM ACTIONS
// ===============================
When(/^I submit the form$/, async () => {
    console.log('Submitting the form');
    await uiActions.submitForm();
});

When(/^I reset the form$/, async () => {
    console.log('Resetting the form');
    await uiActions.resetForm();
});

When(/^I fill form with:$/, async (dataTable: any) => {
    console.log('Filling form with data table:', dataTable.raw());
    await uiActions.fillFormWithData(dataTable);
});



// ===============================
// KEYBOARD ACTIONS
// ===============================
When(/^I press (Enter|Tab|Escape|Space|Backspace|Delete) key$/, async (key: string) => {
    console.log(`Pressing ${key} key`);
    await uiActions.pressKey(key);
});

When(/^I press key combination "([^"]*)"$/, async (keys: string) => {
    console.log(`Pressing key combination "${keys}"`);
    await uiActions.pressKeyCombination(keys);
});



// ===============================
// DRAG AND DROP ACTIONS
// ===============================
When(/^I drag "([^"]*)" to "([^"]*)"$/, async (sourceElement: string, targetElement: string) => {
    console.log(`Dragging ${sourceElement} to ${targetElement}`);
    await uiActions.dragToElement(sourceElement, targetElement);
});

When(/^I drag "([^"]*)" by offset \((\d+),(\d+)\)$/, async (elementName: string, x: string, y: string) => {
    console.log(`Dragging ${elementName} by offset (${x},${y})`);
    await uiActions.dragByOffset(elementName, x, y);
});

