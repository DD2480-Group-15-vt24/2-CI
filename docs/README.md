# Features

## Notifications

### Implementation
The CI server sets the commit status on the repository using the GitHub REST API. Based on the results from the Black format check, the commit status is set to either  **pending**, **failure** or **success**. 

### Test
The notification feature is tested using **pytest** and **unittest.mock**. The test checks if the notification function sends a valid and correctly formatted request to the GitHub REST API. The test also checks if the function returns correctly based on the request's response. The function returns True if the status code of the response is 201, False otherwise. 