import mysql.connector
from varname import nameof

def execute(query, result=False, debug=True):
	try:
		cursor.execute(query)
		db.commit()
	except mysql.connector.Error as error:
		if debug:
			print(f"\n\nmySQEasyDB mySQL Error: {error}\n\n")
	
	if result:
		print(f"Query Output:\n\n {cursor.fetchall()}")

debug = True

# ----------------------------------------MAKE CONNECTION---------------------------------------- #

def connect(host=None, user=None, password=None, database=None):
	if not all(isinstance(i, str) for i in [host, user, password, database]): # Handle Argument Errors
		print("\n\n")
		for argumentname, argumentdata in zip([nameof(host), nameof(user), nameof(password), nameof(database)], [host, user, password, database]):
			if not isinstance(argumentdata, str):
				print(f"mySQEasyDB Syntax Error (2001, Connection Error): {argumentname} needs to be a string.")

	if debug:
		print(f"\n\nMaking connection to {user}@{host} in {database}..")

	try:
		global db
		db = mysql.connector.connect(
		host=host,
		user=user,
		password=password,
		database=database,
		)
		global cursor
		cursor = db.cursor(prepared=True)
		global selectionCursor
		selectionCursor = db.cursor(buffered=True)
	except mysql.connector.Error as error:
		if debug:
			print(f"\n\nmySQEasyDB mySQL Error: {error}\n\nEnsure you have entered the correct database information and your database is running.\n\n")
		exit()
	else:
		if debug:
			print(f"Successfully connected to {db.database}!\n\n")

# ----------------------------------------CREATE TABLE---------------------------------------- #

def newTable(name=None, columns=[], columnTypes={}, columnLengths={}, defaultValues=False, null=True, autoIncrement={}, collation={}, attributes={}, index={}):

	def handleErrors():
		if not name:
			print("mySQEasyDB Syntax Error (2001, Table Error): Your table needs a name.\n\n")
			exit()
		if not isinstance(name, str):
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): Your table name needs to be a string.\n\n")
		
		if not columns:
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): Your table needs at least one column.\n\n")
		if not isinstance(columns, list):
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): Your table name needs to be a list containing at least one string.\n\n")
		for column in columns:
			if not column or not isinstance(column, str):
				print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): Your table needs at least one column that is a string.\n\n")
		
		if not columnTypes:
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): You need to define your column types.\n\n")
		if not isinstance(columnTypes, dict):
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): You need to define your column types, they need to be strings.\n\n")
		for columnType in columnTypes:
			if not columnType or not isinstance(columnType, str):
				print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): A string column type is required.\n\n")
		
		if not columnLengths:
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): You need to define your column lengths.\n\n")
		if not isinstance(columnLengths, dict):
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): You need to define your column lengths, they need to be strings.\n\n")
		for columnLength in columnLengths:
			if not columnLength or not isinstance(columnLength, str):
				print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{name if name else ''}' Table): A string column length is required.\n\n")
	handleErrors()
	

	

	colSQL = str()
	colSQL = "("
	for col in columns:
		
		columnIndex = columns.index(col)

		try: # Column Length Valid
			if not columnLengths:
				COLUMN_LENGTH = str()
			elif columnLengths[col]:
				COLUMN_LENGTH = f"({columnLengths[col]})"
		except (KeyError, TypeError): # Column Length Not Specified
			COLUMN_LENGTH = str()

		try: # Default Valid
			if not defaultValues:
				DEFAULT = str()
			elif defaultValues[col] == "CURRENT_TIMESTAMP":
				DEFAULT = " DEFAULT CURRENT_TIMESTAMP"
			else:
				DEFAULT = f" DEFAULT {defaultValues[col]}"
		except (KeyError, TypeError): # Default Not Specified
			DEFAULT = str()

		try:
			if null == True or null[col] == True:
				NOT_NULL = str()
			elif not null or not null[col]:
				NOT_NULL = " NOT_NULL"
		except (KeyError, TypeError):
			NOT_NULL = str()

		try:
			if not autoIncrement or not autoIncrement[col]:
				AUTO_INCREMENT = str()
			elif autoIncrement == True or autoIncrement[col] == True:
				AUTO_INCREMENT = " AUTO_INCREMENT PRIMARY KEY"
		except (KeyError, TypeError):
			AUTO_INCREMENT = str()

		try:
			if not collation or not collation[col]:
				COLLATE = str()
			else:
				COLLATE = f" COLLATE {collation[col]}"
		except (KeyError, TypeError):
			COLLATE = str()

		try:
			if not attributes or not attributes[col]:
				COLLATE = str()
			else:
				COLLATE = f" {attributes[col]}"
		except (KeyError, TypeError):
			COLLATE = str()

		try:
			if not index or not index[col]:
				INDEX = str()#
			else:
				INDEX = f" {index[col]}"
		except (KeyError, TypeError):
			INDEX = str()

		colSQL = f"{colSQL}{col} {columnTypes[col]}{COLUMN_LENGTH}{DEFAULT}{NOT_NULL}{AUTO_INCREMENT}{COLLATE}{INDEX}{',' if columnIndex != len(columns)-1 else ''}"
	colSQL = colSQL + ")"
	
	query = f"CREATE TABLE {name} {colSQL}"
	print(f"Attempting query: {query}")

	try: 
		global cursor
		cursor.execute(query)
		db.commit()
	except mysql.connector.Error as error:
		if debug:
			print(f"mySQEasyDB mySQL Error: {error}\n\nEnsure you have entered values in the correct format and that your table does not already exist.")
			exit()
	else:
		if debug:
			print(f"Query Sucessfull!\n\nSuccessfully created table: {name}\n\n")

# ----------------------------------------ADD COLUMN---------------------------------------- #

def addColumn(tableName=None, name=None, columns=[], columnTypes={}, columnLengths={}, after=None, before=None, defaultValues=False, null=True, autoIncrement={}, collation={}, attributes={}, index={}):
	def handleErrors():
		if not tableName:
			print("mySQEasyDB Syntax Error (2001, Table Error): You need to specify a table name.\n\n")
			exit()
		if not isinstance(tableName, str):
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): Your table name needs to be a string.\n\n")
		
		if not columns:
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): Your table needs at least one column.\n\n")
		if not isinstance(columns, list):
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): Your table name needs to be a list containing at least one string.\n\n")
		for column in columns:
			if not column or not isinstance(column, str):
				print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): Your table needs at least one column that is a string.\n\n")
		
		if not columnTypes:
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): You need to define your column types.\n\n")
		if not isinstance(columnTypes, dict):
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): You need to define your column types, they need to be strings.\n\n")
		for columnType in columnTypes:
			if not columnType or not isinstance(columnType, str):
				print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): A string column type is required.\n\n")
		
		if not columnLengths:
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): You need to define your column lengths.\n\n")
		if not isinstance(columnLengths, dict):
			print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): You need to define your column lengths, they need to be strings.\n\n")
		for columnLength in columnLengths:
			if not columnLength or not isinstance(columnLength, str):
				print(f"mySQEasyDB Syntax Error (2001, Table Error, In The '{tableName if tableName else ''}' Table): A string column length is required.\n\n")
	handleErrors()

	colSQL = str()
	for col in columns:
		
		columnIndex = columns.index(col)

		try: # Column Length Valid
			if not columnLengths:
				COLUMN_LENGTH = str()
			elif columnLengths[col]:
				COLUMN_LENGTH = f"({columnLengths[col]})"
		except (KeyError, TypeError): # Column Length Not Specified
			COLUMN_LENGTH = str()

		try: # Default Valid
			if not defaultValues:
				DEFAULT = str()
			elif defaultValues[col] == "CURRENT_TIMESTAMP":
				DEFAULT = " DEFAULT CURRENT_TIMESTAMP"
			else:
				DEFAULT = f" DEFAULT {defaultValues[col]}"
		except (KeyError, TypeError): # Default Not Specified
			DEFAULT = str()

		try:
			if null == True or null[col] == True:
				NOT_NULL = str()
			elif not null[col]:
				NOT_NULL = " NOT_NULL"
		except (KeyError, TypeError):
			NOT_NULL = str()

		try:
			if not autoIncrement or not autoIncrement[col]:
				AUTO_INCREMENT = str()
			elif autoIncrement == True or autoIncrement[col] == True:
				AUTO_INCREMENT = " AUTO_INCREMENT PRIMARY KEY"
		except (KeyError, TypeError):
			AUTO_INCREMENT = str()

		try:
			if not collation or not collation[col]:
				COLLATE = str()
			else:
				COLLATE = f" COLLATE {collation[col]}"
		except (KeyError, TypeError):
			COLLATE = str()

		try:
			if not attributes or not attributes[col]:
				COLLATE = str()
			else:
				COLLATE = f" {attributes[col]}"
		except (KeyError, TypeError):
			COLLATE = str()

		try:
			if not index or not index[col]:
				INDEX = str()
			else:
				INDEX = f" {index[col]}"
		except (KeyError, TypeError):
			INDEX = str()

		try:
			if not after or not after[col]:
				AFTER = str()
			else:
				AFTER = f" AFTER {after[col]}"
		except (KeyError, TypeError):
			AFTER = str()

		try:
			if not before or not before[col]:
				BEFORE = str()
			else:
				BEFORE = f" BEFORE {before[col]}"
		except (KeyError, TypeError):
			BEFORE = str()

		colSQL = f"{colSQL}ADD {col} {columnTypes[col]}{COLUMN_LENGTH}{DEFAULT}{NOT_NULL}{AUTO_INCREMENT}{COLLATE}{INDEX}{BEFORE}{AFTER}{',' if columnIndex != len(columns)-1 else ''}"
	
	query = f"ALTER TABLE {tableName} {colSQL}"
	print(f"Attempting query: {query}")

	try: 
		global cursor
		cursor.execute(query)
		db.commit()
	except mysql.connector.Error as error:
		if debug:
			print(f"mySQEasyDB mySQL Error: {error}\n\nEnsure you have entered values in the correct format and that your table does not already exist.")
			exit()
	else:
		if debug:
			print(f"Query Sucessfull!\n\nSuccessfully added columns to table: {tableName}\n\n")

def deleteTable(tableName=None):
	def handleErrors():
		if not tableName:
			print(f"mySQEasyDB Syntax Error (2001, Table Error): You need to define a table name in order to delete it.\n\n")
		if not isinstance(tableName, str):
			print(f"mySQEasyDB Syntax Error (2001, Table Error): Your table name needs to be a string in order to delete it.\n\n")

	handleErrors()

	query = f"DROP TABLE {tableName}"
	print(f"Attempting query: {query}")

	try: 
		global cursor
		cursor.execute(query)
		db.commit()
	except mysql.connector.Error as error:
		if debug:
			print(f"mySQEasyDB mySQL Error: {error}\n\nEnsure you have entered values in the correct format.")
			exit()
	else:
		if debug:
			print(f"Query Sucessfull!\n\nSuccessfully deleted table: {tableName}\n\n")

def deleteColumn(tableName=None, columnName=None):
	def handleErrors():
		if not tableName:
			print(f"mySQEasyDB Syntax Error (2001, Table Error): You need to define a table name in order to delete it.\n\n")
		if not isinstance(tableName, str):
			print(f"mySQEasyDB Syntax Error (2001, Table Error): Your table name needs to be a string in order to delete it.\n\n")
		
		if not columnName:
			print(f"mySQEasyDB Syntax Error (2001, Table Error): You need to define a column name in order to delete it.\n\n")
		if not isinstance(columnName, str):
			print(f"mySQEasyDB Syntax Error (2001, Table Error): Your column name needs to be a string in order to delete it.\n\n")

	handleErrors()

	query = f"ALTER TABLE {tableName} DROP COLUMN {columnName}"

	try: 
		global cursor
		cursor.execute(query)
		db.commit()
	except mysql.connector.Error as error:
		if debug:
			print(f"mySQEasyDB mySQL Error: {error}\n\nEnsure you have entered values in the correct format.")
			exit()
	else:
		if debug:
			print(f"Query Sucessfull!\n\nSuccessfully deleted {columnName} from table: {tableName}\n\n")

def select(select={}, uniqueOnly=False, tableName=None, condition=None):
	def handleErrors():
		if not select:
			print(f"mySQEasyDB Syntax Error (2001, Select Error): You need to define what you are selecting in order to delete it.\n\n")

		if not tableName:
			print(f"mySQEasyDB Syntax Error (2001, Select Error): You need to define a table name in order to delete it.\n\n")
		if not isinstance(tableName, str):
			print(f"mySQEasyDB Syntax Error (2001, Select Error): Your table name needs to be a string in order to delete it.\n\n")

		if not isinstance(uniqueOnly, bool):
			print(f"mySQEasyDB Syntax Error (2001, Select Error): The unique only property needs to be a boolean type.\n\n")
	handleErrors()

	query = f"SELECT {'DISTINCT' if uniqueOnly else ''} {select} FROM {tableName} {'WHERE ' + condition if condition else ''}"
	print(f"Attempting query: {query}")

	try: 
		global cursor
		selectionCursor.execute(query)
		db.commit()
	except mysql.connector.Error as error:
		if debug:
			print(f"mySQEasyDB mySQL Error: {error}\n\nEnsure you have entered values in the correct format.")
			exit()
	else:
		if debug:
			print(f"Query Sucessfull!\n\nOutput:\n\n{selectionCursor.fetchall()}\n\n")

def insert(tableName=None, columns=[], values={}):
	def handleErrors():
		if not tableName:
			print(f"mySQEasyDB Syntax Error (2001, Insert Error): You need to define a table to insert into.\n\n")
		if not isinstance(tableName, str):
			print(f"mySQEasyDB Syntax Error (2001, Insert Error): Your table name needs to be a string type.\n\n")
	handleErrors()

	colSQL = str()
	valSQL = str()
	valPrepared = str()

	for col in columns:
		columnIndex = columns.index(col)

		colSQL = f"{colSQL}{col}{',' if columnIndex != len(columns)-1 else ''}"
		valSQL = f"{valSQL}%s{',' if columnIndex != len(columns)-1 else ''}"
		valPrepared = tuple(values.values())

	query = f"INSERT INTO {tableName} ({colSQL}) VALUES {valPrepared}"
	print(f"Attempting query: {query}")
	query = f"INSERT INTO {tableName} ({colSQL}) VALUES ({valSQL})"

	try: 
		global cursor
		cursor.execute(query, valPrepared)
		db.commit()
	except mysql.connector.Error as error:
		if debug:
			print(f"mySQEasyDB mySQL Error: {error}\n\nEnsure you have entered values in the correct format.")
			exit()
	else:
		if debug:
			print(f"Query Sucessfull!\n\nSuccessfully inserted values into table: {tableName}.\n\n")

def update(tableName=None, columns=[], values={}, condition=None):
	def handleErrors():
		if not tableName:
			print(f"mySQEasyDB Syntax Error (2001, Update Error): You need to define a table to update.\n\n")
		if not isinstance(tableName, str):
			print(f"mySQEasyDB Syntax Error (2001, Update Error): Your table name needs to be a string type.\n\n")
		
		if not columns:
			print(f"mySQEasyDB Syntax Error (2001, Update Error): You need to define at least one column to update.\n\n")
		if not values:
			print(f"mySQEasyDB Syntax Error (2001, Update Error): You need to define at least one value to update.\n\n")
		if not isinstance(columns, list):
			print(f"mySQEasyDB Syntax Error (2001, Update Error): Your columns need to be a list type.\n\n")
		if not isinstance(values, dict):
			print(f"mySQEasyDB Syntax Error (2001, Update Error): Your values need to be a dictionary type.\n\n")

	handleErrors()

	updateSQL = str()

	for col in columns:
		columnIndex = columns.index(col)
		updateSQL = f"{updateSQL}{col} = %s{',' if columnIndex != len(columns)-1 else ''}"
		updatePrepared = tuple(values.values())

	query = f"UPDATE {tableName} SET {updateSQL} {'WHERE ' + condition if condition else ''}"
	print(f"Attempting query: {query}")

	try: 
		global cursor
		cursor.execute(query, updatePrepared)
		db.commit()
	except mysql.connector.Error as error:
		if debug:
			print(f"mySQEasyDB mySQL Error: {error}\n\nEnsure you have entered values in the correct format.")
			exit()
	else:
		if debug:
			print(f"Query Sucessfull!\n\nSuccessfully updated values in table: {tableName}.\n\n")

def deleteRow(tableName=None, condition=None):
	def handleErrors():
		if not tableName:
			print(f"mySQEasyDB Syntax Error (2001, Insert Error): You need to define a table to insert into.\n\n")
		if not isinstance(tableName, str):
			print(f"mySQEasyDB Syntax Error (2001, Insert Error): Your table name needs to be a string type.\n\n")
	handleErrors()

	query = f"DELETE FROM {tableName} {'WHERE ' + condition if condition else ''}"
	print(f"Attempting query: {query}")

	try: 
		global cursor
		cursor.execute(query)
		db.commit()
	except mysql.connector.Error as error:
		if debug:
			print(f"mySQEasyDB mySQL Error: {error}\n\nEnsure you have entered values in the correct format.")
			exit()
	else:
		if debug:
			print(f"Query Sucessfull!\n\nSuccessfully deleted specified rows from table: {tableName}.\n\n")