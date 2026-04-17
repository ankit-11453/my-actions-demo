*** Settings ***
Resource    ../resources/api_keywords.resource
Suite Setup    Create API Session

*** Test Cases ***
Health Check Should Be Up
    ${response}=    Get Health Status
    Verify Status Code    ${response}    200

Create User Successfully
    ${response}=    Create User With Valid Data    Rahul    rahul@test.com
    Verify Status Code    ${response}    201
    Verify Response Has User Id    ${response}

Create User Validation Failure
    ${response}=    Create User With Invalid Data    Rahul
    Should BeTrue    ${response.status_code} == 400 or ${response.status_code} == 422

Get Existing User
    ${create_response}=    Create User With Valid Data    Meera    meera@test.com
    ${user_id}=    Set Variable    ${create_response.json()}[id]
    ${get_response}=    Get User By Id    ${user_id}
    Verify Status Code    ${get_response}    200