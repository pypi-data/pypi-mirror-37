Introduction
=============

SSBJ(SuperSonic Business Jet)-KADMOS(Knowledge- and graph-based Agile Design for Multidisciplinary Optimization System) is a small repository containing tools defined by NASA for the analysis of an SSBJ. The tools have been defined by NASA, were developed in Python by ONERA and have been KADMOSized by TU Delft.

SSBJ test case definition: http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19980234657.pdf
SSBJ OpenMDAO (Python) implementation: https://github.com/OneraHub/SSBJ-OpenMDAO


Repository Structure
====================

The repository is structured as follows:

- dist/

	 contains copies of all major distributions of SSBJ-KADMOS

- ssbj-kadmos/

     - tools
	  
		 contains the KADMOS compatible SSBJ analysis tools
	 
     - utils

         contains utility functions

     - config.py

         configuration file for the tools and the used data schema

- license.md

     contains the license

- readme.md

     contains this document


Credits
=======

Original Python implementation for OpenMDAO integration developed by Sylvain Dubreuil and Remi Lafage of ONERA, the French Aerospace Lab. The files were adjusted for optimal use in KADMOS by Imco van Gent (TU Delft) as per this repository.

Changelog
=========

## 0.1.3 (21/10/2018)

- Added analytic partials determination to all disciplines (except outputfunctions). Implementation based on openlego.

## 0.1.2 (15/08/2018)

- Renamed to "ssbjkadmos" to avoid issues with hyphen on package imports.

## 0.1.1 (15/08/2018)

- Updated files based on OpenLEGO runs and CMDOWS 0.9 developments.
- Added start files and results of different CMDOWS files.
- Renamed main folder (from "ssbjkadmos" to "ssbj-kadmos") to match distribution name.

## 0.1.0 (01/08/2018)

- First public release
