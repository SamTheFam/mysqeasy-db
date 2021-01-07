'''

-----NOTES-----

- To test this example please enter your database info the the 'dbinfo.py' file.
- If you want to test specific functions, feel free to hash out other ones to disable their functionality.
- Select results can be found in the output terminal.

'''

# Import the library as the variable 'db'.
import mysqeasydb as db
# We recommend putting your database info in another file (import database info).
import dbinfo

# If you want success messages to appear, I would turn this off when deploying your program.
debug = True

# Make connection to the database.
db.connect(
	host=dbinfo.host,
	user=dbinfo.user,
	password=dbinfo.password,
	database=dbinfo.database
	)

# Create a new 'users' table in the database.
db.newTable(
	name="users",
	columns=["id", "username", "email", "forename", "surname", "age" ,"password"],
	columnTypes={
	"id": "INT",
	"username":"VARCHAR",
	"email":"VARCHAR",
	"forename":"VARCHAR",
	"surname":"VARCHAR",
	"age":"TINYINT",
	"password":"TEXT",
	},
	columnLengths={
	"username":"25",
	"email":"50",
	"forename":"25",
	"surname":"25",
	"age":"3",
	},
	defaultValues={},
	null=False,
	autoIncrement={"id":True,}
)

# Create a new 'telephone' column in a table - You can add more than one column if you wish to.
db.addColumn(
	tableName="users",
	columns=["telephone",],
	columnTypes={
	"telephone":"BIGINT",
	},
	columnLengths={
	"telephone":"11"
	},
	after={"telephone":"email"},
	defaultValues={},
	null=False,
)

# Insert a new user into the table.
db.insert(tableName="users",
 		columns=["username", "email", "forename", "surname", "age" ,"password",],
 		values={
		"username": "Johnny1234",
		"email":"johnny5@hotmail.com",
		"forename":"Johnny",
		"surname":"Smith",
		"age":"24",
		"password":"12345ilovecats"}, # It's mandatory to hash passwords, this is for demonstration purposes.
		# Also please don't use passwords as weak as these!
	)

# Insert another user into the table.
db.insert(tableName="users",
 		columns=["username", "email", "forename", "surname", "age" ,"password"],
 		values={
		"username": "jjamesSuperstar4",
		"email":"jamesroberts@gmail.com",
		"forename":"James",
		"surname":"Roberts",
		"age":"34",
		"password":"ILoveLvis"},
	)

# Select a user from the users table where a user's username is 'Johnny1234'.
db.select(select="*", tableName="users", condition="username = 'Johnny1234'")

# Select all emails in the table.
db.select(select="email", tableName="users", condition=None)

# Update a user from the users table where their id is 2 to have a new password.
db.update(tableName="users",
		columns=["password"],
		values={"password":"4mazingN3wP@ssword"},
		condition="id=2"
	)

# Delete the age column from the users table.
db.deleteColumn(tableName="users", columnName="age",)

# Delete a user where their id is equal to 1.
db.deleteRow(tableName="users", condition="id=1")

# Delete the users table.
db.deleteTable("users")

# You can also run custom queries if you're more advanced or we broke something :)
# Selection won't work with the execute() function, but you can still make raw queries if need be.
query = "CREATE TABLE messagefromowlstoolbox (messages TEXT);"
db.execute(query)
query = "INSERT INTO messagefromowlstoolbox (messages) VALUES ('Thank you so much for downloading mySQEasyDB!');"
db.execute(query)