## LFE-FRESH
2D and 3D G-code planning code for an open-sourced long fiber embedded hydrogel 3D print head

(* Mechanical assembly and usage of the printer will be made available once the manuscript is published)

# Steps to process a preliminary (motion control only without extrusion control) G-code file for 2D fiber embedding:
Requirement: a preliminary G-code file (.gcode) produced by DXF2GCODE (https://sourceforge.net/projects/dxf2gcode/), e.g., motion_only.gcode

Modify the preliminary G-code:

Add the following line immediately before the first motion command:
```
;startFlag
```
Add the following line immediately after the last motion command:
```
;endFlag
```
Download add_extrusion.py to a designated folder and move the preliminary G-code file there.

Using the command line, navigate to the folder and execute the following line to process the G-code with default settings:
```
python add_extrusion.py -f [G-code file name]
```
For example, 
```
python add_extrusion.py -f motion_only.gcode
```
Help information on optional arguments can be retrieved using:
```
python add_extrusion.py -h
```
The output G-code will be stored in the same folder, prefixed with ‘updated_’, e.g., updated_motion_only.gcode

# Steps to generate and visualize a preliminary (motion control only without extrusion control) G-code file for the 3D conical helix fiber embedding (Fig. 6N in the manuscript):
Download conical_helix.py to a designated folder.

Using the command line, navigate to the folder and execute the following line:
```
python conical_helix.py
```
The resulting preliminary G-code will be saved as conical_helix.gcode and an image of the generated pattern will be created and saved in the same folder.

# Steps to process the preliminary G-code file for 3D conical helix fiber embedding (conical_helix.gcode):
Requirement: conical_helix.gcode generated by conical_helix.py

Download add_extrusion_3D.py to a designated folder and move conical_helix.gcode there.

Using the command line, navigate to the folder and execute the following line to process G-code with default settings:
```
python add_extrusion_3D.py -f conical_helix.gcode
```

Help information on optional arguments can be retrieved using:
```
python add_extrusion_3D.py -h
```
The output G-code will be stored in the same folder and named updated_conical_helix.gcode.

# Steps to generate and visualize a preliminary (motion control only without extrusion control) G-code file for the 3D ventricle sleeve fiber embedding (Fig. 6R in the manuscript):
Download ventricle.py to a designated folder

Using the command line, navigate to the folder and execute the following line:
```
python ventricle.py
```
The resulting preliminary G-code will be saved as ventricle.gcode and an image of the generated pattern will be created and saved in the same folder

The preliminary G-code file for 3D ventricle sleeve fiber embedding can be processed using add_extrusion_3D.py as shown earlier and the updated G-code file will be stored as updated_ventricle.gcode:
	python add_extrusion_3D.py -f ventricle.gcode
