import { Given, When, Then } from '@wdio/cucumber-framework';
import { expect } from '@wdio/globals';
import uiActions from '../../support/uiActions';
import uiAssertions from '../../support/uiAssertions';

// ===============================
// REGISTRATION SPECIFIC STEP DEFINITIONS
// ===============================
// This file contains step definitions specific to registration flow
// that are not covered by existing global step definitions

// ===============================
// NAVIGATION AND PAGE STATE STEPS
// ===============================
Given(/^I am on the homepage$/, async () => {
    console.log('Verifying user is on the homepage');
    // Implementation: Verify homepage elements are visible
    await uiAssertions.verifyElementVisible('Homepage Logo', 'element');
});

Given(/^I am on the registration page$/, async () => {
    console.log('Navigating to registration page');
    await uiActions.navigateTo('https://retailwebsite.com/register');
    await uiAssertions.verifyElementVisible('Create Account', 'heading');
});

Then(/^I should be redirected to the registration page$/, async () => {
    console.log('Verifying redirection to registration page');
    await uiAssertions.verifyUrlContains('/register');
    await uiAssertions.verifyElementVisible('Create Account', 'heading');
});

Then(/^I should be redirected to the email verification page$/, async () => {
    console.log('Verifying redirection to email verification page');
    await uiAssertions.verifyUrlContains('/verify-email');
    await uiAssertions.verifyElementVisible('Email Verification', 'heading');
});

Then(/^I should be redirected to the login page$/, async () => {
    console.log('Verifying redirection to login page');
    await uiAssertions.verifyUrlContains('/login');
    await uiAssertions.verifyElementVisible('Login', 'heading');
});

Then(/^I should be redirected to the dashboard$/, async () => {
    console.log('Verifying redirection to dashboard');
    await uiAssertions.verifyUrlContains('/dashboard');
    await uiAssertions.verifyElementVisible('Welcome to Dashboard', 'element');
});

// ===============================
// OAUTH AND SOCIAL LOGIN STEPS
// ===============================
Then(/^I should be redirected to (Google|Facebook) OAuth provider$/, async (provider: string) => {
    console.log(`Verifying redirection to ${provider} OAuth provider`);
    if (provider === 'Google') {
        await uiAssertions.verifyUrlContains('accounts.google.com');
    } else if (provider === 'Facebook') {
        await uiAssertions.verifyUrlContains('facebook.com');
    }
});

When(/^I complete (Google|Facebook) OAuth authorization$/, async (provider: string) => {
    console.log(`Completing ${provider} OAuth authorization`);
    // Implementation: Handle OAuth flow
    // This would typically involve interacting with OAuth provider's interface
    // For testing purposes, this might be mocked or use test credentials
    if (provider === 'Google') {
        await uiActions.typeText('test.user@gmail.com', 'Email', 'field');
        await uiActions.typeText('TestPassword123', 'Password', 'field');
        await uiActions.clickOn('Sign in', 'button');
        await uiActions.clickOn('Allow', 'button');
    } else if (provider === 'Facebook') {
        await uiActions.typeText('test.user@facebook.com', 'Email', 'field');
        await uiActions.typeText('TestPassword123', 'Password', 'field');
        await uiActions.clickOn('Log In', 'button');
        await uiActions.clickOn('Continue', 'button');
    }
});

Then(/^my account should be created automatically$/, async () => {
    console.log('Verifying account creation through OAuth');
    // Implementation: Verify account creation success indicators
    await uiAssertions.verifyElementVisible('Account Created', 'element');
});

// ===============================
// EMAIL VERIFICATION STEPS
// ===============================
Given(/^I have successfully registered with email "([^"]*)"$/, async (email: string) => {
    console.log(`Setting up successful registration with email: ${email}`);
    // Implementation: Complete registration process
    await uiActions.navigateTo('https://retailwebsite.com/register');
    await uiActions.typeText('John', 'First Name', 'field');
    await uiActions.typeText('Smith', 'Last Name', 'field');
    await uiActions.typeText(email, 'Email Address', 'field');
    await uiActions.typeText('Test@1234', 'Password', 'field');
    await uiActions.typeText('Test@1234', 'Confirm Password', 'field');
    await uiActions.typeText('+44 7912345678', 'Mobile Number', 'field');
    await uiActions.checkCheckbox('Terms & Conditions');
    await uiActions.clickOn('Create Account', 'button');
    await uiAssertions.verifyElementVisible('Account created successfully', 'element');
});

When(/^I check my email inbox$/, async () => {
    console.log('Checking email inbox for verification email');
    // Implementation: Access email service or mock email checking
    // This might involve API calls to email service or database checks
    await uiActions.navigateTo('https://mailservice.com/inbox');
});

Then(/^I should receive a verification email within (\d+) minutes$/, async (minutes: string) => {
    console.log(`Verifying verification email received within ${minutes} minutes`);
    // Implementation: Check for email arrival within specified time
    await uiActions.waitSeconds('120'); // Wait up to 2 minutes
    await uiAssertions.verifyElementVisible('Verification Email', 'element');
});

Then(/^the email should contain "([^"]*)" text$/, async (text: string) => {
    console.log(`Verifying email contains text: ${text}`);
    await uiAssertions.verifyElementContainsText('Email Content', text, 'element');
});

Then(/^the email should contain "([^"]*)" button$/, async (buttonText: string) => {
    console.log(`Verifying email contains button: ${buttonText}`);
    await uiAssertions.verifyElementVisible(buttonText, 'button');
});

When(/^I click the "([^"]*)" link in email$/, async (linkText: string) => {
    console.log(`Clicking ${linkText} link in email`);
    await uiActions.clickOn(linkText, 'link');
});

// ===============================
// FORM VALIDATION STEPS
// ===============================
Then(/^no session timeout error should be displayed$/, async () => {
    console.log('Verifying no session timeout error is displayed');
    // Implementation: Check that no timeout error messages are visible
    await uiAssertions.verifyElementNotVisible('Session Timeout', 'element');
    await uiAssertions.verifyElementNotVisible('Session Expired', 'element');
});
