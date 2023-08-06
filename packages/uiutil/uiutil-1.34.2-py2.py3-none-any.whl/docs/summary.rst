Advantages of Uiutil
====================

* Frames and Widgets are added to the current frame automatically.
  No need to pass the frame/window/parent to the frame or widget.

* Easier positioning

    * No more widget.grid() calls.
    * Grid parameters are supplied directly to widgets
    * Positioning with ``START``, ``NEXT``, ``FIRST``, ``LAST``
    * No need to supply a row or column value if it's
      the same as the previous widget.

* Variables are provided for free.

   * No need to declare them.
   * No need to reference them.
   * Use ``widget.value`` instead of ``var.get()``
   * Use ``widget.value = <value>`` instead of ``var.set()``

* Associate objects and display values.
  (Widgets can return more than just IntVat, StringVar and BoolVar)
* Easier field validation
* Easier Scroll frames
* SwitchBox widget: multiple checkboxes
* RadioBox widget: multiple radio buttons
* Dynamic Tooltips on widgets
* Images on Buttons and Labels
* Image mapping - multiple targets on an image Label
