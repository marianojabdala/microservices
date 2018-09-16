Feature: Create a User
	Scenario Outline: User register into the application
		Given The user set the <username> and <password>
		When User user post to the /users endpoint
		Then The response is 201 and the user is created

		Examples:
			| username 	| password  |
			| user1 		|	pass1			|
