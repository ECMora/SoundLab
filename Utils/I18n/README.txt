Here is how an internationalized application is created.

1. Create the application using QObject.tr() or QApplication.translate() for
all user-visible strings.
2. Modify the application to read in the locale-specific .qm (Qt message) files
at start-up if they are available.
3. Create a .pro file that lists the application’s .ui (Qt Designer) files, its .py
and .pyw source files, and the .ts (translation source) file that it will use.
4. Run pylupdate4 to create the .ts file.
5. Ask the translator to translate the .ts file’s strings using Qt Linguist.
6. Run lrelease to convert the updated .ts file (that contains the translations)
to a .qm file.

And here is how such an application is maintained.

1. Update the application, making sure that all user-visible strings use
QObject.tr() or QApplication.translate().
2. Update the .pro file if necessary—for example, adding any new .ui or .py
files that have been added to the application.
3. Run pylupdate4 to update the .ts file with any new strings.
4. Ask the translator to translate any new strings in the .ts file.
5. Run lrelease to convert the .ts file to a .qm file.