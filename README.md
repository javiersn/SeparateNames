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

A optional switches **-on** is used to force a 'Name First' form, and or **-os** is used to force a 'Surname First' form. If neither is specified, the script will use logic to determine the most likely form for each provided full  name.

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
You may also import the script as a module, typically using `import SeparateNames`, in which case you will gain full access to the **NameSplitter** and **NameToken** classes.

Please read the DocString documentation for more details. 

Licensing
-
This project is developed and provided under MIT License:

Copyright 2018 by github.com/javiersn

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.