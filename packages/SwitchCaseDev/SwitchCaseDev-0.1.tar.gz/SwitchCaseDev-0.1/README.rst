``SwitchCaseDev``
==============

``SwitchCaseDev`` is a command in python command which is similar to switch-case in java and python.
It is also a implementation of a simple Switch-Case in Python.

Basic Usage:
===============

``switch()``:
Basic Syntax:
.. code :: python
switch(case_list,default_value)

    where,
        case_list -> a dictionary item , it contains the dictionary of all the case in which switch will be applied
        default_value -> it is the default value which will excute if any of the given case is not applied.

``case()``:
Basic Syntax:
.. code :: python
case(value)
    
    where,
        value -> the case the need to be applied.


Example :
.. code-block::python
import Switch_Case
exg=Switch_Case.switch(case_list={"a":2,"b":4},default_value=0)
print(exg.case("a"))

Output:
2

Note: All name I tried are unavailable so I switch the name to SwitchCaseDev.