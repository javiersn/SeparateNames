SeparateNames
=
Simple tool for separating full name strings, according to latin style naming, into three basic sub-components: name (or *first name*), first surname (or *fathers family name*), and second surname or (*mothers family name*).

Project is currently in version 0.1 (considered Beta). 

Getting Started
-
### Prerequisites
You must have installed:
* Python 3.6 or higher
* Pandas 
* Unidecode

Download all project files and folders, and use according to the following methods:

### Usage
You may use SeparateNames in three different ways:
#### 1. As a Command Line Tool
By downloading all project folders and files, and from your terminal, located at the project folder, executing:

`python ./SeparateNames.py [-on|-os] ['Name 1'] ['Name 2'] ...`

Since full names are frequently written in two different forms:
* Name first (i.e. Luis Lopez Perez)
* Surname first (i.e. Lopez Perez Luis)

A optional switches *-on* is used to force a 'Name First' form, and or *-os* is used to force a 'Surname First' form. If neither is specified, the script will use logic to determine the most likely form for each provided full  name.

It is also possible to provide a list of names through *stdin*, by the following command:

`cat names.txt | python ./SeparateNames.py [-on|-os] ['Name 1'] ['Name 2'] ...`

Where names.txt is a file containing a new line separated listing of full names.

Upon executing the above commands successfully, it will print out a listing of dictionaries in the following form:

`{name: 'Luis', first_surname: 'Lopez', seconf_surname: 'Perez'}` 

#### 2. As an Imported Function
In its most simple form, you may import SeparateNames.py into your own project and use it as follows:

```
from SeparateNames import split_name 

name = 'Lopez Perez Luis'
print(split_name(name))
```

Which prints out a python dictionary in the form `{name: 'Luis', first_surname: 'Lopez', seconf_surname: 'Perez'}`

If the script fails to split a name, it will return None.

#### 3. As Imported Classes
You may also import the script as a module, typically using `import SeparateNames`, in which case you will gain full access to the *NameSplitter* and *NameToken* classes.

Please read the DocString documentation for more details. 

Important Notice on DataSets and Dictionaries
-
The script uses name and surname dictionaries in order to identify and separate name. These dictionaries were obtained from publicly available datasets provided by the *U.S. Social Security (SSA)* and the *U.S. and the U.S. Census Bureau (USCENSUS)*. These datasets are not included in the License, and are subject to the policies, licenses and/or terms and conditions of their respective agencies. Please do review the terms and conditions in their respective websites:

  https://www.ssa.gov/oact/babynames/limits.html
  
  https://www.census.gov/data/developers/data-sets/surnames.html
