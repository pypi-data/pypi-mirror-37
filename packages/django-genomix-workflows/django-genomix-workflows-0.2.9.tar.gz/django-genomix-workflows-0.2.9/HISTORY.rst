.. :changelog:

History
-------

0.1.0 (2018-01-12)
++++++++++++++++++

* First release on PyPI.

0.2.0 (2018-06-27)
++++++++++++++++++

* Changed models completely.
* Add graph interpretations for workflows.
* Add signal to automatically create task instances after workflow instance initiation.
* Add signals to update related task status after task updates.
* Add methods for single workflow/task instances to get current status, graph, JSON graph, and other useful helpers.
* Add managers for combined workflow and task methods.
* Add single and combined graph diagram, current status, and topographical sort to Django Admin.
* Complete the switch to Django 2.0
* Update requirements and dependencies.

0.2.1 (2018-07-02)
++++++++++++++++++

* Add raw id in Admin for workflow instance parent field

0.2.2 (2018-07-03)
++++++++++++++++++

* Add raw id in Admin for Task instance

0.2.3 (2018-07-06)
++++++++++++++++++

* Fix an issue with next and previous task instances

0.2.4 (2018-07-08)
++++++++++++++++++

* Improve combined Next and Previous calculations

0.2.5 (2018-07-09)
++++++++++++++++++

* Fix current state for a single workflow without running or pending tasks

0.2.6 (2018-08-07)
++++++++++++++++++

* Add Skip action feature
+ Increase coverage

0.2.7 (2018-08-13)
++++++++++++++++++

`Full Changelog <https://github.com/chopdgd/django-genomix-worfklows/compare/v0.2.6...v0.2.7>`_

* Updated 3rd party requirements. Some requirements had changed so it was causing failures

0.2.8 (2018-08-30)
++++++++++++++++++

* Add version to Tasks

0.2.9 (2018-10-29)
++++++++++++++++++

* Updated 3rd party requirements.
