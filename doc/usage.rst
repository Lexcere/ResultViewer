=====
Usage
=====

CLI
===

results <commands> [options]

commands:

- show, s         show statistic about results
- viewer, v       open GUI
- report , r      generate report

options:

-

GUI
===

Read
----

Read TestResult from the Reading folder is possible via the following menu/icon:

.. image:: images/Read.png
  :alt: Alternative text

Menu: File/Read

----

Because of speed performance, only N last generated files will be readed. is possible to set this value from
the number input widget

.. image:: images/NumberOfTest.png
  :alt: Alternative text

----

The reading folder can be reset to the default folder using the following menu/icon:
Menu File/Reset folder

.. image:: images/ResetFolder.png
  :alt: Alternative text

View
----

To view the TXT or HTML version of TestResult/s selected. Right click on the list of result, click the
preferred option from the context menu.

.. image:: images/contextMenu.png
  :alt: Alternative text

From the context menu is also possible to:

- Replace in one or multiple TestResult, one specific field with a choosen value.
- Open the folder of selected TestResult.
- Save selected TestResult.
- Delete selected TestResult.

Filtering
---------

Is possible to filter the visualized result using the toolbar filter widget.
Select the column you want to filter, type the string to filter and click [ENTER] to refresh the list.

.. image:: images/filter_toolbar.png
  :alt: Alternative text

Reset filter is possible via menu **Filter/Reset all**.

Is possible to check/uncheck the case sensitive via menu **Filter/Case sensitive**.

From the Filter menu is possible to set quick filters.

Save
----

To save the selected TestResult to the Saving folder use the following command:

.. image:: images/Save.png
  :alt: Alternative text

Menu: File/Save
Context menu: Save

If TestResult is linked with one or more MDF file/s, the MDF/s is/are saved as well in the saving folder.

Report
------

Read Test Result
~~~~~~~~~~~~~~~~

The report is generated using the test result displayed on the ResultViewer list.

- Update SVN Folder containing test result
- Read folder (Menu File/Read)
    .. ATTENTION::
        Request at least 1000 test cases and check that the number of test is below 1000
- Check there are no error messages in the dedicate box
- Correct all problems
- Commit SVN Folder after modifications

Create HTML
~~~~~~~~~~~

Display the Test Result of which you want to generate the report.
Start the generation process via menu Report/Generate (HTML). Report is generated in same folder
choose to display the Test Result.

Add on
""""""

Add on files can be used to add content to the final report without worrying about style.

.. ATTENTION::
    Content of Add on will be automatically added to the report only if they are present in the same
    folder where the report is generated.

Following table will give a short description of each add on:
Info | Add to the Summary page the information about the maturity and project of the SW under test. | AC22
Deviation | Allow CSM + AC to give a status for each deviation raised during the validation of SW. | CSM + AC