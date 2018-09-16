Feature: Service is up and running
	Scenario: The user service is healthy
		When Hit the /_health endpoint
		Then I can get the json body
