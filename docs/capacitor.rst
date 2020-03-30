.. index::
   single: Single objective problem with Comsol Multiphysics

Capacitor - Optimization problem with Comsol Multiphysics
=========================================================

This example demonstrates the usage of Artap together with the commercial software: Comsol Multiphysics.
The problem seems to be somewhat artificial. The reason is to demonstrate the procedure
on a simple example. Suppose we design a plane capacitor and we require capacity :math:`C = 5` pF.
Our design variables are the width of dielectricum :math:`a` and the hight of dielectricum :math:`b`.


Prepare model in Comsol Multiphysics
------------------------------------

The first thing is preparing the model in Comsol Multiphysics. We have to create parameters with the same name
both in the Comsol Multiphysics and consequently in Artap:

.. image:: figures/comsol_parameters.png
   :width: 400px   
   :align: center


|

Then, it is necessary to add a sequence to the Study:

.. image:: figures/comsol_sequence.png
   :width: 400px   
   :align: center

|
The next step is to calculate the required value
which is in our case: the stored energy in the capacitor.
This can be done using derived values.
|

.. image:: figures/comsol_derived_values.png
   :width: 700px   
   :align: center

After running the simulation, the Table is created. The table must be saved in the file.
Artap will use this file.

.. image:: figures/comsol_table.png
   :width: 400px   
   :align: center

At this moment, we have a model, which is prepared to use together with Artap.
We recommend clearing the solution, before you save your model.


Create Artap problem file
-------------------------

The **Problem** class is composed in the standard way. At first, make sure that parameters have the same name in the **Problem class** and in Comsol model.

.. code-block:: python

    # Parameters must be defined in the Comsol model
    self.parameters = [{'name': 'a', 'initial_value': 10, 'bounds': [0.1, 100]},  # parameters a, b must be positive
                        {'name': 'b', 'initial_value': 10, 'bounds': [0.1, 100]}]


It is necessary to specify the name of the  model file, and the file is produced by Comsol Multiphysics.
   
.. code-block:: python
    
    self.costs = [{'name': 'F1', 'criteria': 'minimize'}]
    self.output_files = ["energy.txt"]

    # Executor serves for calling the Comsol Multiphisics
    self.executor = LocalComsolExecutor(self,
                                        problem_file="./capacitor.mph",   # File with the model
                                        output_files=self.output_files)   # file with results produced by Comsol


------------------------------------------------------------
Automatically generated docummentation from the example file
------------------------------------------------------------

.. automodule:: artap.examples.capacitor
    :members:


