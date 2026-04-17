*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}    http://127.0.0.1:8000

*** Keywords ***
Create API Session
    Create Session    userapi    ${BASE_URL}

Get Health Status
    ${response}=    GET On Session    userapi    /health    expected_status=200
    RETURN    ${response}

Create User With Valid Data
    [Arguments]    ${name}    ${email}
    &{body}=    Create Dictionary    name=${name}    email=${email}
    ${response}=    POST On Session    userapi    /users    json=${body}    expected_status=201
    RETURN    ${response}

Create User With Invalid Data
    [Arguments]    ${name}
    &{body}=    Create Dictionary    name=${name}
    ${response}=    POST On Session    userapi    /users    json=${body}    expected_status=anything
    RETURN    ${response}

Get User By Id
    [Arguments]    ${user_id}
    ${response}=    GET On Session    userapi    /users/${user_id}    expected_status=anything
    RETURN    ${response}

Verify Status Code
    [Arguments]    ${response}    ${expected_code}
    Should Be Equal As Integers    ${response.status_code}    ${expected_code}

Verify Response Has User Id
    [Arguments]    ${response}
    Dictionary Should Contain Key    ${response.json()}    id