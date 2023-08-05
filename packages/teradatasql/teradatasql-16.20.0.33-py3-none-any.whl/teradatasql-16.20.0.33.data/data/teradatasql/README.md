## Teradata SQL Driver for Python

This package enables Python applications to connect to the Teradata Database.

This package implements the [PEP-249 Python Database API Specification 2.0](https://www.python.org/dev/peps/pep-0249/).

This package requires 64-bit Python 3.4 or later, and runs on Windows, macOS, and Linux. 32-bit Python is not supported.

For community support, please visit the [Connectivity Forum](http://community.teradata.com/t5/Connectivity/bd-p/DevXConnectivityBoard).

For Teradata customer support, please visit [Teradata Access](https://access.teradata.com/).

Copyright 2018 Teradata. All Rights Reserved.

### Table of Contents

* [Features](#Features)
* [Limitations](#Limitations)
* [Installation](#Installation)
* [License](#License)
* [Documentation](#Documentation)
* [Sample Programs](#SamplePrograms)
* [Using the Teradata SQL Driver for Python](#Using)
* [Connection Parameters](#ConnectionParameters)
* [Data Types](#DataTypes)
* [Null Values](#NullValues)
* [Module Constructors](#ModuleConstructors)
* [Module Globals](#ModuleGlobals)
* [Module Exceptions](#ModuleExceptions)
* [Connection Methods](#ConnectionMethods)
* [Cursor Attributes](#CursorAttributes)
* [Cursor Methods](#CursorMethods)
* [Type Objects](#TypeObjects)
* [Escape Syntax](#EscapeSyntax)

<a name="Features"></a>

### Features

The *Teradata SQL Driver for Python* is a young product that offers a basic feature set. We are working diligently to add features to the Teradata SQL Driver for Python, and our goal is feature parity with the Teradata JDBC Driver.

At the present time, the Teradata SQL Driver for Python offers the following features.

* Supported for use with Teradata Database 14.10 and later releases. Informally tested to work with Teradata Database 12.0 and later releases.
* Encrypted logon using the `TD2`, `LDAP`, `KRB5` (Kerberos), or `TDNEGO` logon mechanisms.
* Data encryption enabled via the `encryptdata` connection parameter.
* Unicode character data transferred via the UTF8 session character set.
* 1 MB rows supported with Teradata Database 16.0 and later.
* Multi-statement requests that return multiple result sets.
* Most JDBC escape syntax.
* Parameterized SQL requests with question-mark parameter markers.
* Parameterized batch SQL requests with multiple rows of data bound to question-mark parameter markers.
* ElicitFile protocol support for DDL commands that create external UDFs or stored procedures and upload a file from client to database.

<a name="Limitations"></a>

### Limitations

* The Teradata Database's default transaction mode (ANSI or TERA) is always used. The `tmode` connection parameter is not supported yet.
* The UTF8 session character set is always used. The `charset` connection parameter is not supported.
* The following complex data types are not supported yet: `XML`, `JSON`, `DATASET STORAGE FORMAT AVRO`, and `DATASET STORAGE FORMAT CSV`.
* The `CREATE PROCEDURE` and `REPLACE PROCEDURE` commands are not supported yet. These commands use a different wire protocol from other DDL commands.
* COP Discovery is not supported yet. You must specify the hostname or IP address of a specific Teradata Database node to connect to.
* No support yet for data encryption that is governed by central administration. To enable data encryption, you must specify a `true` value for the `encryptdata` connection parameter.
* Laddered Concurrent Connect is not supported yet.
* The JWT logon mechanism is not supported yet.
* No support yet for Recoverable Network Protocol and Redrive.
* Auto-commit for ANSI transaction mode is not offered yet. You must explicitly execute a `commit` command when using ANSI transaction mode.
* FastLoad is not available yet.
* FastExport is not available yet.
* Monitor partition support is not available yet.

<a name="Installation"></a>

### Installation

Use pip to install the Teradata SQL Driver for Python.

Platform       | Command
-------------- | ---
macOS or Linux | `pip install teradatasql`
Windows        | `py -3 -m pip install teradatasql`

When upgrading to a new version of the Teradata SQL Driver for Python, you may need to use pip install's `--no-cache-dir` option to force the download of the new version.

Platform       | Command
-------------- | ---
macOS or Linux | `pip install --no-cache-dir -U teradatasql`
Windows        | `py -3 -m pip install --no-cache-dir -U teradatasql`

<a name="License"></a>

### License

Use of the Teradata SQL Driver for Python is governed by the *License Agreement for the Teradata SQL Driver for Python*.

When the Teradata SQL Driver for Python is installed, the `LICENSE` and `THIRDPARTYLICENSE` files are placed in the `teradatasql` directory under your Python installation directory.

<a name="Documentation"></a>

### Documentation

When the Teradata SQL Driver for Python is installed, the `README.md` file is placed in the `teradatasql` directory under your Python installation directory. This permits you to view the documentation offline, when you are not connected to the Internet.

The `README.md` file is a plain text file containing the documentation for the Teradata SQL Driver for Python. While the file can be viewed with any text file viewer or editor, your viewing experience will be best with an editor that understands Markdown format.

<a name="SamplePrograms"></a>

### Sample Programs

Sample programs are provided to demonstrate how to use the Teradata SQL Driver for Python. When the Teradata SQL Driver for Python is installed, the sample programs are placed in the `teradatasql/samples` directory under your Python installation directory.

The sample programs are coded with a fake Teradata Database hostname `whomooz`, username `guest`, and password `please`. Substitute your actual Teradata Database hostname and credentials before running a sample program.

Program                     | Purpose
--------------------------- | ---
DriverDatabaseVersion.py    | Displays the Teradata SQL Driver version and Teradata Database version
ElicitFile.py               | Demonstrates C source file upload to create a User-Defined Function (UDF)
HelpSession.py              | Displays session information
LoadCSVFile.py              | Demonstrates how to load data from a CSV file into a table
MetadataFromPrepare.py      | Demonstrates how to prepare a SQL request and obtain SQL statement metadata
TJEncryptPassword.py        | Creates encrypted password files

<a name="Using"></a>

### Using the Teradata SQL Driver for Python

Your Python script must import the `teradatasql` package in order to use the Teradata SQL Driver for Python.

    import teradatasql

After importing the `teradatasql` package, your Python script calls the `teradatasql.connect` function to open a connection to the Teradata Database.

You may specify connection parameters as a JSON string, as `kwargs`, or using a combination of the two approaches. The `teradatasql.connect` function's first argument is a JSON string. The `teradatasql.connect` function's second and subsequent arguments are optional `kwargs`.

Connection parameters specified only as `kwargs`:

    con = teradatasql.connect(None, host='whomooz', user='guest', password='please')

Connection parameters specified only as a JSON string:

    con = teradatasql.connect('{"host":"whomooz","user":"guest","password":"please"}')

Connection parameters specified using a combination:

    con = teradatasql.connect('{"host":"whomooz"}', user='guest', password='please')

<a name="ConnectionParameters"></a>

### Connection Parameters

The following table lists the connection parameters currently offered by the Teradata SQL Driver for Python.

Our goal is consistency for the connection parameters offered by the Teradata SQL Driver for Python and the Teradata JDBC Driver, with respect to connection parameter names and functionality. For comparison, Teradata JDBC Driver connection parameters are [documented here](http://developer.teradata.com/doc/connectivity/jdbc/reference/current/jdbcug_chapter_2.html#BGBHDDGB).

Parameter          | Default     | Type           | Description
------------------ | ----------- | -------------- | ---
`account`          |             | string         | Specifies the Teradata Database account. Equivalent to the Teradata JDBC Driver `ACCOUNT` connection parameter.
`column_name`      | `"false"`   | quoted boolean | Controls the behavior of cursor `.description` sequence `name` items. Equivalent to the Teradata JDBC Driver `COLUMN_NAME` connection parameter. False specifies that a cursor `.description` sequence `name` item provides the AS-clause name if available, or the column name if available, or the column title. True specifies that a cursor `.description` sequence `name` item provides the column name if available, but has no effect when StatementInfo parcel support is unavailable.
`dbs_port`         | `"1025"`    | quoted integer | Specifies Teradata Database port number. Equivalent to the Teradata JDBC Driver `DBS_PORT` connection parameter.
`encryptdata`      | `"false"`   | quoted boolean | Controls encryption of data exchanged between the Teradata Database and the Teradata SQL Driver for Python. Equivalent to the Teradata JDBC Driver `ENCRYPTDATA` connection parameter.
`fake_result_sets` | `"false"`   | quoted boolean | Controls whether a fake result set containing statement metadata precedes each real result set.
`host`             |             | string         | Specifies the Teradata Database hostname. Note that COP Discovery is not implemented yet.
`lob_support`      | `"true"`    | quoted boolean | Controls LOB support. Equivalent to the Teradata JDBC Driver `LOB_SUPPORT` connection parameter.
`log`              | `"0"`       | quoted integer | Controls debug logging. Somewhat equivalent to the Teradata JDBC Driver `LOG` connection parameter. This parameter's behavior is subject to change in the future. This parameter's value is currently defined as an integer in which the 1-bit governs function and method tracing, the 2-bit governs debug logging, and the 4-bit governs transmit and receive message hex dumps.
`logdata`          |             | string         | Specifies extra data for the chosen logon authentication method. Equivalent to the Teradata JDBC Driver `LOGDATA` connection parameter.
`logmech`          | `"TD2"`     | string         | Specifies the logon authentication method. Equivalent to the Teradata JDBC Driver `LOGMECH` connection parameter. Possible values are `TD2` (the default), `LDAP`, `KRB5` for Kerberos, or `TDNEGO`. Note that JWT authentication is not supported yet.
`max_message_body` | `"2097000"` | quoted integer | Not fully implemented yet and intended for future usage. Equivalent to the Teradata JDBC Driver `MAX_MESSAGE_BODY` connection parameter.
`partition`        | `"DBC/SQL"` | string         | Specifies the Teradata Database Partition. Equivalent to the Teradata JDBC Driver `PARTITION` connection parameter.
`password`         |             | string         | Specifies the Teradata Database password. Equivalent to the Teradata JDBC Driver `PASSWORD` connection parameter.
`sip_support`      | `"true"`    | quoted boolean | Controls whether StatementInfo parcel is used. Equivalent to the Teradata JDBC Driver `SIP_SUPPORT` connection parameter.
`teradata_values`  | `"true"`    | quoted boolean | Controls whether `str` or a more specific Python data type is used for certain Result set column value types. Refer to the table below for details.
`user`             |             | string         | Specifies the Teradata Database username. Equivalent to the Teradata JDBC Driver `USER` connection parameter.

<a name="DataTypes"></a>

### Data Types

The table below lists the Teradata Database data types supported by the Teradata SQL Driver for Python, and indicates the corresponding Python data type returned in result set rows.

Teradata Database data type        | Result set Python data type       | With `teradata_values` as `"false"`
---------------------------------- | --------------------------------- | ---
`BIGINT`                           | `int`                             |
`BLOB`                             | `bytes`                           |
`BYTE`                             | `bytes`                           |
`BYTEINT`                          | `int`                             |
`CHAR`                             | `str`                             |
`CLOB`                             | `str`                             |
`DATE`                             | `datetime.date`                   | `str`
`DECIMAL`                          | `decimal.Decimal`                 | `str`
`FLOAT`                            | `float`                           |
`INTEGER`                          | `int`                             |
`INTERVAL YEAR`                    | `str`                             |
`INTERVAL YEAR TO MONTH`           | `str`                             |
`INTERVAL MONTH`                   | `str`                             |
`INTERVAL DAY`                     | `str`                             |
`INTERVAL DAY TO HOUR`             | `str`                             |
`INTERVAL DAY TO MINUTE`           | `str`                             |
`INTERVAL DAY TO SECOND`           | `str`                             |
`INTERVAL HOUR`                    | `str`                             |
`INTERVAL HOUR TO MINUTE`          | `str`                             |
`INTERVAL HOUR TO SECOND`          | `str`                             |
`INTERVAL MINUTE`                  | `str`                             |
`INTERVAL MINUTE TO SECOND`        | `str`                             |
`INTERVAL SECOND`                  | `str`                             |
`NUMBER`                           | `decimal.Decimal`                 | `str`
`PERIOD(DATE)`                     | `str`                             |
`PERIOD(TIME)`                     | `str`                             |
`PERIOD(TIME WITH TIME ZONE)`      | `str`                             |
`PERIOD(TIMESTAMP)`                | `str`                             |
`PERIOD(TIMESTAMP WITH TIME ZONE)` | `str`                             |
`SMALLINT`                         | `int`                             |
`TIME`                             | `datetime.time`                   | `str`
`TIME WITH TIME ZONE`              | `datetime.time` with `tzinfo`     | `str`
`TIMESTAMP`                        | `datetime.datetime`               | `str`
`TIMESTAMP WITH TIME ZONE`         | `datetime.datetime` with `tzinfo` | `str`
`VARBYTE`                          | `bytes`                           |
`VARCHAR`                          | `str`                             |

The table below lists the parameterized SQL bind-value Python data types supported by the Teradata SQL Driver for Python, and indicates the corresponding Teradata Database data type transmitted to the server.

Bind-value Python data type       | Teradata Database data type
--------------------------------- | ---
`bytes`                           | `VARBYTE`
`datetime.date`                   | `DATE`
`datetime.datetime`               | `TIMESTAMP`
`datetime.datetime` with `tzinfo` | `TIMESTAMP WITH TIME ZONE`
`datetime.time`                   | `TIME`
`datetime.time` with `tzinfo`     | `TIME WITH TIME ZONE`
`datetime.timedelta`              | `VARCHAR` format compatible with `INTERVAL DAY TO SECOND`
`decimal.Decimal`                 | `NUMBER`
`float`                           | `FLOAT`
`int`                             | `BIGINT`
`str`                             | `VARCHAR`

Transforms are used for SQL `ARRAY` data values, and they can be transferred to and from the database as `VARCHAR` values.

Transforms are used for structured UDT data values, and they can be transferred to and from the database as `VARCHAR` values.

<a name="NullValues"></a>

### Null Values

SQL `NULL` values received from the Teradata Database are returned in result set rows as Python `None` values.

A Python `None` value bound to a question-mark parameter marker is transmitted to the Teradata Database as a `NULL` `VARCHAR` value.

<a name="ModuleConstructors"></a>

### Module Constructors

`teradatasql.connect(` *JSONConnectionString* `,` *Parameters...* `)`

Creates a connection to the database and returns a Connection object.

The first parameter is a JSON string or `None`. The second and subsequent arguments are optional `kwargs`. Specify connection parameters as a JSON string, as `kwargs`, or  a combination of the two.

---

`teradatasql.Date(` *Year* `,` *Month* `,` *Day* `)`

Creates and returns a `datetime.date` value.

---

`teradatasql.DateFromTicks(` *Seconds* `)`

Creates and returns a `datetime.date` value corresponding to the specified number of seconds after 1970-01-01 00:00:00.

---

`teradatasql.Time(` *Hour* `,` *Minute* `,` *Second* `)`

Creates and returns a `datetime.time` value.

---

`teradatasql.TimeFromTicks(` *Seconds* `)`

Creates and returns a `datetime.time` value corresponding to the specified number of seconds after 1970-01-01 00:00:00.

---

`teradatasql.Timestamp(` *Year* `,` *Month* `,` *Day* `,` *Hour* `,` *Minute* `,` *Second* `)`

Creates and returns a `datetime.datetime` value.

---

`teradatasql.TimestampFromTicks(` *Seconds* `)`

Creates and returns a `datetime.datetime` value corresponding to the specified number of seconds after 1970-01-01 00:00:00.

<a name="ModuleGlobals"></a>

### Module Globals

`teradatasql.apilevel`

String constant `"2.0"` indicating that the Teradata SQL Driver for Python implements the [PEP-249 Python Database API Specification 2.0](https://www.python.org/dev/peps/pep-0249/).

---

`teradatasql.threadsafety`

Integer constant `2` indicating that threads may share this module, and threads may share connections, but threads must not share cursors.

---

`teradatasql.paramstyle`

String constant `"qmark"` indicating that prepared SQL requests use question-mark parameter markers.

<a name="ModuleExceptions"></a>

### Module Exceptions

`teradatasql.Error` is the base class for other exceptions.
* `teradatasql.InterfaceError` is raised for errors related to the driver. Not supported yet.
* `teradatasql.DatabaseError` is raised for errors related to the database.
  * `teradatasql.DataError` is raised for data value errors such as division by zero. Not supported yet.
  * `teradatasql.IntegrityError` is raised for referential integrity violations. Not supported yet.
  * `teradatasql.OperationalError` is raised for errors related to the database's operation.
  * `teradatasql.ProgrammingError` is raised for SQL object existence errors and SQL syntax errors. Not supported yet.

<a name="ConnectionMethods"></a>

### Connection Methods

`.close()`

Closes the Connection.

---

`.commit()`

Commits the current transaction. Not implemented yet.

---

`.cursor()`

Creates and returns a new Cursor object for the Connection.

---

`.rollback()`

Rolls back the current transaction. Not implemented yet.

<a name="CursorAttributes"></a>

### Cursor Attributes

`.arraysize`

Read/write attribute specifying the number of rows to fetch at a time with the `.fetchmany()` method. Defaults to `1` meaning fetch a single row at a time.

---

`.connection`

Read-only attribute indicating the Cursor's parent Connection object.

---

`.description`

Read-only attribute consisting of a sequence of seven-item sequences that each describe a result set column, available after a SQL request is executed.
* `.description[`*Column*`][0]` provides the column name.
* `.description[`*Column*`][1]` provides the column type code as an object comparable to one of the Type Objects listed below.
* `.description[`*Column*`][2]` provides the column display size in characters. Not implemented yet.
* `.description[`*Column*`][3]` provides the column size in bytes.
* `.description[`*Column*`][4]` provides the column precision if applicable, or `None` otherwise.
* `.description[`*Column*`][5]` provides the column scale if applicable, or `None` otherwise.
* `.description[`*Column*`][6]` provides the column nullability as `True` or `False`.

---

`.rowcount`

Read-only attribute indicating the number of rows returned from, or affected by, the current SQL statement.

<a name="CursorMethods"></a>

### Cursor Methods

`.callproc(` *ProcedureName* `,` *OptionalSequenceOfParameterValues* `)`

Calls the stored procedure specified by *ProcedureName*.
If a sequence of parameter values is provided as the second argument, the values will be bound to question-mark parameter markers in the SQL request. Specifying parameter values as a mapping is not supported.
Returns a result set consisting of the parameter output values, if any, followed by any dynamic result sets.

---

`.close()`

Closes the Cursor.

---

`.execute(` *SQLRequest* `,` *OptionalSequenceOfParameterValues* `)`

Executes the SQL request.
If a sequence of parameter values is provided as the second argument, the values will be bound to question-mark parameter markers in the SQL request. Specifying parameter values as a mapping is not supported.

---

`.executemany(` *SQLRequest* `,` *SequenceOfSequencesOfParameterValues* `)`

Executes the SQL request as an iterated SQL request for the batch of parameter values.
The batch of parameter values must be specified as a sequence of sequences. Specifying parameter values as a mapping is not supported.

---

`.fetchall()`

Fetches all remaining rows of the current result set.
Returns a sequence of sequences of column values.

---

`.fetchmany(` *OptionalRowCount* `)`

Fetches the next series of rows of the current result set.
The argument specifies the number of rows to fetch. If no argument is provided, then the Cursor's `.arraysize` attribute will determine the number of rows to fetch.
Returns a sequence of sequences of column values, or an empty sequence to indicate that all rows have been fetched.

---

`.fetchone()`

Fetches the next row of the current result set.
Returns a sequence of column values, or `None` to indicate that all rows have been fetched.

---

`.nextset()`

Advances to the next result set.
Returns `True` if another result set is available, or `None` to indicate that all result sets have been fetched.

---

`.setinputsizes(` *SequenceOfTypesOrSizes* `)`

Has no effect.

---

`.setoutputsize(` *Size* `,` *OptionalColumnIndex* `)`

Has no effect.

<a name="TypeObjects"></a>

### Type Objects

`teradatasql.BINARY`

Identifies a SQL `BLOB`, `BYTE`, or `VARBYTE` column as a binary data type when compared with the Cursor's description attribute. 

`.description[`*Column*`][1] == teradatasql.BINARY`

---

`teradatasql.DATETIME`

Identifies a SQL `DATE`, `TIME`, `TIME WITH TIME ZONE`, `TIMESTAMP`, or `TIMESTAMP WITH TIME ZONE` column as a date/time data type when compared with the Cursor's description attribute. 

`.description[`*Column*`][1] == teradatasql.DATETIME`

---

`teradatasql.NUMBER`

Identifies a SQL `BIGINT`, `BYTEINT`, `DECIMAL`, `FLOAT`, `INTEGER`, `NUMBER`, or `SMALLINT` column as a numeric data type when compared with the Cursor's description attribute.

`.description[`*Column*`][1] == teradatasql.NUMBER`

---

`teradatasql.STRING`

Identifies a SQL `CHAR`, `CLOB`, `INTERVAL`, `PERIOD`, or `VARCHAR` column as a character data type when compared with the Cursor's description attribute.

`.description[`*Column*`][1] == teradatasql.STRING`

<a name="EscapeSyntax"></a>

### Escape Syntax

The Teradata SQL Driver for Python accepts most of the JDBC escape clauses offered by the Teradata JDBC Driver.

#### Date and Time Literals

Date and time literal escape clauses are replaced by the corresponding SQL literal before the SQL request text is transmitted to the database.

Literal Type | Format
------------ | ------
Date         | `{d '`*yyyy-mm-dd*`'}`
Time         | `{t '`*hh:mm:ss*`'}`
Timestamp    | `{ts '`*yyyy-mm-dd hh:mm:ss*`'}`
Timestamp    | `{ts '`*yyyy-mm-dd hh:mm:ss.f*`'}`

For timestamp literal escape clauses, the decimal point and fractional digits may be omitted, or 1 to 6 fractional digits *f* may be specified after a decimal point.

#### Scalar Functions

Scalar function escape clauses are replaced by the corresponding SQL expression before the SQL request text is transmitted to the database.

Numeric Function                       | Returns
-------------------------------------- | ---
`{fn ABS(`*number*`)}`                 | Absolute value of *number*
`{fn ACOS(`*float*`)}`                 | Arccosine, in radians, of *float*
`{fn ASIN(`*float*`)}`                 | Arcsine, in radians, of *float*
`{fn ATAN(`*float*`)}`                 | Arctangent, in radians, of *float*
`{fn ATAN2(`*y*`,`*x*`)}`              | Arctangent, in radians, of *y* / *x*
`{fn CEILING(`*number*`)}`             | Smallest integer greater than or equal to *number*
`{fn COS(`*float*`)}`                  | Cosine of *float* radians
`{fn COT(`*float*`)}`                  | Cotangent of *float* radians
`{fn DEGREES(`*number*`)}`             | Degrees in *number* radians
`{fn EXP(`*float*`)}`                  | *e* raised to the power of *float*
`{fn FLOOR(`*number*`)}`               | Largest integer less than or equal to *number*
`{fn LOG(`*float*`)}`                  | Natural (base *e*) logarithm of *float*
`{fn LOG10(`*float*`)}`                | Base 10 logarithm of *float*
`{fn MOD(`*integer1*`,`*integer2*`)}`  | Remainder for *integer1* / *integer2*
`{fn PI()}`                            | The constant pi, approximately equal to 3.14159...
`{fn POWER(`*number*`,`*integer*`)}`   | *number* raised to *integer* power
`{fn RADIANS(`*number*`)}`             | Radians in *number* degrees
`{fn RAND(`*seed*`)}`                  | A random float value such that 0 ≤ value < 1, and *seed* is ignored
`{fn ROUND(`*number*`,`*places*`)}`    | *number* rounded to *places*
`{fn SIGN(`*number*`)}`                | -1 if *number* is negative; 0 if *number* is 0; 1 if *number* is positive
`{fn SIN(`*float*`)}`                  | Sine of *float* radians
`{fn SQRT(`*float*`)}`                 | Square root of *float*
`{fn TAN(`*float*`)}`                  | Tangent of *float* radians
`{fn TRUNCATE(`*number*`,`*places*`)}` | *number* truncated to *places*

String Function                                                | Returns
-------------------------------------------------------------- | ---
`{fn ASCII(`*string*`)}`                                       | ASCII code of the first character in *string*
`{fn CHAR(`*code*`)}`                                          | Character with ASCII *code*
`{fn CHAR_LENGTH(`*string*`)}`                                 | Length in characters of *string*
`{fn CHARACTER_LENGTH(`*string*`)}`                            | Length in characters of *string*
`{fn CONCAT(`*string1*`,`*string2*`)}`                         | String formed by concatenating *string1* and *string2*
`{fn DIFFERENCE(`*string1*`,`*string2*`)}`                     | A number from 0 to 4 that indicates the phonetic similarity of *string1* and *string2* based on their Soundex codes, such that a larger return value indicates greater phonetic similarity; 0 indicates no similarity, 4 indicates strong similarity
`{fn INSERT(`*string1*`,`*position*`,`*length*`,`*string2*`)}` | String formed by replacing the *length*-character segment of *string1* at *position* with *string2*, available beginning with Teradata Database 15.0
`{fn LCASE(`*string*`)}`                                       | String formed by replacing all uppercase characters in *string* with their lowercase equivalents
`{fn LEFT(`*string*`,`*count*`)}`                              | Leftmost *count* characters of *string*
`{fn LENGTH(`*string*`)}`                                      | Length in characters of *string*
`{fn LOCATE(`*string1*`,`*string2*`)}`                         | Position in *string2* of the first occurrence of *string1*, or 0 if *string2* does not contain *string1*
`{fn LTRIM(`*string*`)}`                                       | String formed by removing leading spaces from *string*
`{fn OCTET_LENGTH(`*string*`)}`                                | Length in octets (bytes) of *string*
`{fn POSITION(`*string1*` IN `*string2*`)}`                    | Position in *string2* of the first occurrence of *string1*, or 0 if *string2* does not contain *string1*
`{fn REPEAT(`*string*`,`*count*`)}`                            | String formed by repeating *string* *count* times, available beginning with Teradata Database 15.0
`{fn REPLACE(`*string1*`,`*string2*`,`*string3*`)}`            | String formed by replacing all occurrences of *string2* in *string1* with *string3*
`{fn RIGHT(`*string*`,`*count*`)}`                             | Rightmost *count* characters of *string*, available beginning with Teradata Database 15.0
`{fn RTRIM(`*string*`)}`                                       | String formed by removing trailing spaces from *string*
`{fn SOUNDEX(`*string*`)}`                                     | Soundex code for *string*
`{fn SPACE(`*count*`)}`                                        | String consisting of *count* spaces
`{fn SUBSTRING(`*string*`,`*position*`,`*length*`)}`           | The *length*-character segment of *string* at *position*
`{fn UCASE(`*string*`)}`                                       | String formed by replacing all lowercase characters in *string* with their uppercase equivalents

System Function                         | Returns
--------------------------------------- | ---
`{fn DATABASE()}`                       | Current default database name
`{fn IFNULL(`*expression*`,`*value*`)}` | *expression* if *expression* is not NULL, or *value* if *expression* is NULL
`{fn USER()}`                           | Logon user name, which may differ from the current authorized user name after `SET QUERY_BAND` sets a proxy user

Time/Date Function                                                 | Returns
------------------------------------------------------------------ | ---
`{fn CURDATE()}`                                                   | Current date
`{fn CURRENT_DATE()}`                                              | Current date
`{fn CURRENT_TIME()}`                                              | Current time
`{fn CURRENT_TIMESTAMP()}`                                         | Current date and time
`{fn CURTIME()}`                                                   | Current time
`{fn DAYOFMONTH(`*date*`)}`                                        | Integer from 1 to 31 indicating the day of month in *date*
`{fn EXTRACT(YEAR FROM `*value*`)}`                                | The year component of the date and/or time *value*
`{fn EXTRACT(MONTH FROM `*value*`)}`                               | The month component of the date and/or time *value*
`{fn EXTRACT(DAY FROM `*value*`)}`                                 | The day component of the date and/or time *value*
`{fn EXTRACT(HOUR FROM `*value*`)}`                                | The hour component of the date and/or time *value*
`{fn EXTRACT(MINUTE FROM `*value*`)}`                              | The minute component of the date and/or time *value*
`{fn EXTRACT(SECOND FROM `*value*`)}`                              | The second component of the date and/or time *value*
`{fn HOUR(`*time*`)}`                                              | Integer from 0 to 23 indicating the hour of *time*
`{fn MINUTE(`*time*`)}`                                            | Integer from 0 to 59 indicating the minute of *time*
`{fn MONTH(`*date*`)}`                                             | Integer from 1 to 12 indicating the month of *date*
`{fn NOW()}`                                                       | Current date and time
`{fn SECOND(`*time*`)}`                                            | Integer from 0 to 59 indicating the second of *time*
`{fn TIMESTAMPADD(SQL_TSI_YEAR,`*count*`,`*timestamp*`)}`          | Timestamp formed by adding *count* years to *timestamp*
`{fn TIMESTAMPADD(SQL_TSI_MONTH,`*count*`,`*timestamp*`)}`         | Timestamp formed by adding *count* months to *timestamp*
`{fn TIMESTAMPADD(SQL_TSI_DAY,`*count*`,`*timestamp*`)}`           | Timestamp formed by adding *count* days to *timestamp*
`{fn TIMESTAMPADD(SQL_TSI_HOUR,`*count*`,`*timestamp*`)}`          | Timestamp formed by adding *count* hours to *timestamp*
`{fn TIMESTAMPADD(SQL_TSI_MINUTE,`*count*`,`*timestamp*`)}`        | Timestamp formed by adding *count* minutes to *timestamp*
`{fn TIMESTAMPADD(SQL_TSI_SECOND,`*count*`,`*timestamp*`)}`        | Timestamp formed by adding *count* seconds to *timestamp*
`{fn TIMESTAMPDIFF(SQL_TSI_YEAR,`*timestamp1*`,`*timestamp2*`)}`   | Number of years by which *timestamp2* exceeds *timestamp1*
`{fn TIMESTAMPDIFF(SQL_TSI_MONTH,`*timestamp1*`,`*timestamp2*`)}`  | Number of months by which *timestamp2* exceeds *timestamp1*
`{fn TIMESTAMPDIFF(SQL_TSI_DAY,`*timestamp1*`,`*timestamp2*`)}`    | Number of days by which *timestamp2* exceeds *timestamp1*
`{fn TIMESTAMPDIFF(SQL_TSI_HOUR,`*timestamp1*`,`*timestamp2*`)}`   | Number of hours by which *timestamp2* exceeds *timestamp1*
`{fn TIMESTAMPDIFF(SQL_TSI_MINUTE,`*timestamp1*`,`*timestamp2*`)}` | Number of minutes by which *timestamp2* exceeds *timestamp1*
`{fn TIMESTAMPDIFF(SQL_TSI_SECOND,`*timestamp1*`,`*timestamp2*`)}` | Number of seconds by which *timestamp2* exceeds *timestamp1*
`{fn YEAR(`*date*`)}`                                              | The year of *date*

#### Conversion Functions

Conversion function escape clauses are replaced by the corresponding SQL expression before the SQL request text is transmitted to the database.

Conversion Function                                             | Returns
--------------------------------------------------------------- | ---
`{fn CONVERT(`*value*`, SQL_BIGINT)}`                           | *value* converted to SQL `BIGINT`
`{fn CONVERT(`*value*`, SQL_BINARY(`*size*`))}`                 | *value* converted to SQL `BYTE(`*size*`)`
`{fn CONVERT(`*value*`, SQL_CHAR(`*size*`))}`                   | *value* converted to SQL `CHAR(`*size*`)`
`{fn CONVERT(`*value*`, SQL_DATE)}`                             | *value* converted to SQL `DATE`
`{fn CONVERT(`*value*`, SQL_DECIMAL(`*precision*`,`*scale*`))}` | *value* converted to SQL `DECIMAL(`*precision*`,`*scale*`)`
`{fn CONVERT(`*value*`, SQL_DOUBLE)}`                           | *value* converted to SQL `DOUBLE PRECISION`, a synonym for `FLOAT`
`{fn CONVERT(`*value*`, SQL_FLOAT)}`                            | *value* converted to SQL `FLOAT`
`{fn CONVERT(`*value*`, SQL_INTEGER)}`                          | *value* converted to SQL `INTEGER`
`{fn CONVERT(`*value*`, SQL_LONGVARBINARY)}`                    | *value* converted to SQL `VARBYTE(64000)`
`{fn CONVERT(`*value*`, SQL_LONGVARCHAR)}`                      | *value* converted to SQL `LONG VARCHAR`
`{fn CONVERT(`*value*`, SQL_NUMERIC)}`                          | *value* converted to SQL `NUMBER`
`{fn CONVERT(`*value*`, SQL_SMALLINT)}`                         | *value* converted to SQL `SMALLINT`
`{fn CONVERT(`*value*`, SQL_TIME(`*scale*`))}`                  | *value* converted to SQL `TIME(`*scale*`)`
`{fn CONVERT(`*value*`, SQL_TIMESTAMP(`*scale*`))}`             | *value* converted to SQL `TIMESTAMP(`*scale*`)`
`{fn CONVERT(`*value*`, SQL_TINYINT)}`                          | *value* converted to SQL `BYTEINT`
`{fn CONVERT(`*value*`, SQL_VARBINARY(`*size*`))}`              | *value* converted to SQL `VARBYTE(`*size*`)`
`{fn CONVERT(`*value*`, SQL_VARCHAR(`*size*`))}`                | *value* converted to SQL `VARCHAR(`*size*`)`

#### LIKE Predicate Escape Character

Within a `LIKE` predicate's *pattern* argument, the characters `%` (percent) and `_` (underscore) serve as wildcards.
To interpret a particular wildcard character literally in a `LIKE` predicate's *pattern* argument, the wildcard character must be preceded by an escape character, and the escape character must be indicated in the `LIKE` predicate's `ESCAPE` clause.

`LIKE` predicate escape character escape clauses are replaced by the corresponding SQL clause before the SQL request text is transmitted to the database.

`{escape '`*EscapeCharacter*`'}`

The escape clause must be specified immediately after the `LIKE` predicate that it applies to.

#### Outer Joins

Outer join escape clauses are replaced by the corresponding SQL clause before the SQL request text is transmitted to the database.

`{oj `*TableName*` `*OptionalCorrelationName*` LEFT OUTER JOIN `*TableName*` `*OptionalCorrelationName*` ON `*JoinCondition*`}`

`{oj `*TableName*` `*OptionalCorrelationName*` RIGHT OUTER JOIN `*TableName*` `*OptionalCorrelationName*` ON `*JoinCondition*`}`

`{oj `*TableName*` `*OptionalCorrelationName*` FULL OUTER JOIN `*TableName*` `*OptionalCorrelationName*` ON `*JoinCondition*`}`

#### Stored Procedure Calls

Stored procedure call escape clauses are replaced by the corresponding SQL clause before the SQL request text is transmitted to the database.

`{call `*ProcedureName*`}`

`{call `*ProcedureName*`(`*CommaSeparatedParameterValues...*`)}`

#### Native SQL

When a SQL request contains the native SQL escape clause, all escape clauses are replaced in the SQL request text, and the modified SQL request text is returned to the application as a result set containing a single row and a single VARCHAR column. The SQL request text is not transmitted to the database, and the SQL request is not executed. The native SQL escape clause mimics the functionality of the JDBC API `Connection.nativeSQL` method.

`{fn teradata_nativesql}`

#### Connection Functions

The following table lists connection function escape clauses that are intended for use with the native SQL escape clause `{fn teradata_nativesql}`.

These functions provide information about the connection, or control the behavior of the connection.
Functions that provide information return locally-cached information and avoid a round-trip to the database.
Connection function escape clauses are replaced by the returned information before the SQL request text is transmitted to the database.

Connection Function                           | Returns
--------------------------------------------- | ---
`{fn teradata_amp_count}`                     | Number of AMPs of the Teradata Database system
`{fn teradata_database_version}`              | Version number of the Teradata Database
`{fn teradata_driver_version}`                | Version number of the Teradata SQL Driver for Python
`{fn teradata_getloglevel}`                   | Current log level
`{fn teradata_logon_sequence_number}`         | Session's Logon Sequence Number, if available
`{fn teradata_provide(config_response)}`      | Config Response parcel contents in JSON format
`{fn teradata_provide(connection_id)}`        | Connection's unique identifier within the process
`{fn teradata_provide(default_connection)}`   | `false` indicating this is not a stored procedure default connection
`{fn teradata_provide(host_id)}`              | Session's host ID
`{fn teradata_provide(java_charset_name)}`    | `UTF8`
`{fn teradata_provide(lob_support)}`          | `true` or `false` indicating this connection's LOB support
`{fn teradata_provide(local_address)}`        | Local address of the connection's TCP socket
`{fn teradata_provide(local_port)}`           | Local port of the connection's TCP socket
`{fn teradata_provide(original_hostname)}`    | Original specified Teradata Database hostname
`{fn teradata_provide(redrive_active)}`       | `true` or `false` indicating whether this connection has Redrive active
`{fn teradata_provide(remote_address)}`       | Hostname (if available) and IP address of the connected Teradata Database node
`{fn teradata_provide(remote_port)}`          | TCP port number of the Teradata Database
`{fn teradata_provide(rnp_active)}`           | `true` or `false` indicating whether this connection has Recoverable Network Protocol active
`{fn teradata_provide(session_charset_code)}` | Session character set code `191`
`{fn teradata_provide(session_charset_name)}` | Session character set name `UTF8`
`{fn teradata_provide(sip_support)}`          | `true` or `false` indicating this connection's StatementInfo parcel support
`{fn teradata_provide(transaction_mode)}`     | Session's transaction mode, `ANSI` or `TERA`
`{fn teradata_session_number}`                | Session number
`{fn teradata_setloglevel(`*LogLevel*`)}`     | Empty string, and changes the connection's *LogLevel*

#### Request-Scope Functions

The following table lists request-scope function escape clauses that are intended for use with the Cursor `.execute` or `.executemany` methods.

These functions control the behavior of the corresponding Cursor, and are limited in scope to the particular SQL request in which they are specified.
Request-scope function escape clauses are removed before the SQL request text is transmitted to the database.

Request-Scope Function                                 | Effect
------------------------------------------------------ | ---
`{fn teradata_failfast}`                               | Reject ("fail fast") this SQL request rather than delay by a workload management rule or throttle
`{fn teradata_fake_result_sets}`                       | A fake result set containing statement metadata precedes each real result set
`{fn teradata_lobselect(`*Option*`)}`                  | Executes the SQL request with LOB select *Option* `S` (spool-scoped LOB locators), `T` (transaction-scoped LOB locators), or the default `I` (inline materialized LOB values)
`{fn teradata_provide(request_scope_lob_support_off)}` | Turns off LOB support for this SQL request
`{fn teradata_provide(request_scope_refresh_rsmd)}`    | Executes the SQL request with the default request processing option `B` (both)
`{fn teradata_provide(request_scope_sip_support_off)}` | Turns off StatementInfo parcel support for this SQL request
`{fn teradata_rpo(`*RequestProcessingOption*`)}`       | Executes the SQL request with *RequestProcessingOption* `S` (prepare), `E` (execute), or the default `B` (both)
`{fn teradata_untrusted}`                              | Marks the SQL request as untrusted; not implemented yet
