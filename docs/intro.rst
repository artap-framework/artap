Introduction
============

The development of the Artap was motivated by our experiences with modeling for
real applications. These applications exhibited several common features:

	* The real, industrial design problems and processes are complex tasks characterized by mutual interaction of several coupled physical fields. They are often three-dimensional and nonlinear. The computation time varies from tens of seconds to many hours. Moreover, the solution of these tasks is often based on the judgement and experience of the design experts. It is difficult to model every design aspect mathematically, in a closed, deterministic way. Beside this, it is difficult to find correctly all constraints. Calculation of some variants can fail.
	* Some geometrical dimensions are known with uncertainty.
	* Material parameters and characteristics are known only with a given tolerances. 
	* It is often difficult to prescribe correct boundary conditions.
	* There may exist various phenomena, which are difficult to describe in the deterministic manner.


The software Artap should be the software package which will connect tools for 
physical fields analysis, optimization, robust design and control synthesis. 
The Artap should

    * ensure an open platform for developing new optimization algorithms,
    * should contain its own or integrated tools for model order reduction,    
    * should offer automatic calibration (identification) of models.