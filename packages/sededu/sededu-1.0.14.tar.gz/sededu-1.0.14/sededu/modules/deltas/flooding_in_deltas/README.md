# Flooding in deltas educational module

This flooding risk module is intended to help educators demonstrate some basic physics of why rivers flood. A computer code with a fully interactive graphical user interface module (GUI) is interacted with alongside worksheets designed for students of varying ages.

This readme file provides an overview of the installation and setup process, as well as a brief description of the module worksheets available.

This repository is also linked into the [SedEdu suite of education modules](https://github.com/amoodie/sededu), and can be accessed there as well.

A Matlab version of this module exists [here](https://github.com/amoodie/research_outreach/tree/master/flooding_risk).

![demo image](./private/gui_demo.png "Demo of GUI")<!-- .element height="50%" width="50%" -->

## Installation and running the module

Visit the section of the text below for more information on installing and executing the `flooding_in_deltas` program on your computer. 

### Requirements
This module depends on Python3, and the libraries `numpy` and `matplotlib`. 

#### Anaconda installation
It is recommended that you install Anaconda, which is an open source distribution of Python. It comes with many basic scientific libraries, some of which are used in the module. Anaconda can be downloaded at https://www.anaconda.com/download/ for Windows, macOS, and Linux. Please follow the instruction provided in the website as to how to install and setup Python on your computer.

#### Custom Python installation
If you want a more flexible and lightweight Python distribution, you can use whatever your favorite package manager is distributing (e.g., `homebrew` or `apt`), check the [Windows downloads here](https://www.python.org/downloads/windows/), or compile [from source](https://www.python.org/downloads/source/).

Whatever method you choose, you will need to install the dependencies. installation by `pip` is easiest, and probably supported if you used anything but compiling from source.

### Download the source code

#### grab the zip
You can download this entire repository as a `.zip` by clicking the "Clone or download button on this page", or by [clicking here](https://github.com/amoodie/flooding_in_deltas/archive/master.zip) to get a `.zip` folder. Unzip the folder in your preferred location.

#### git 
If you have installed `git` and are comfortable working with it, you can simply clone the repository to your preferred location.

```
git clone https://github.com/amoodie/flooding_in_deltas.git
```

### Run the module
Run the module by command line, with
```
python3 <path-to-the-repo-folder>/src/backwater_flooding.py
```



## Module worksheet information

Worksheets are being written to accompany the GUI module. The aim of the worksheets is to help guide a discussion about flooding on deltas or rivers, as may be discussed in Earth Science courses. The modules currently available are targeted at specific age groups:

* High School Earth Science -- 9th to 12th graders

**Educators:** please let me know if you used this module, and if there are any ways you can see for us to help facilitate this sort of module in the future. Your feedback is very much appreciated. Email to Andrew Moodie, amoodie@rice.edu.



## Disclaimer

The module was created by Andrew J. Moodie as part of an National Science Foundation funded research project assessing the sustainability of anthropogenically influenced deltas.
The research is supported by Grant No. 1427262 and an NSF Graduate Research Fellowship to A.J.M. under Grant No. 1450681.
Any opinion, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation.
For more information, please visit [http://www.coastalsustainability.rice.edu/outreach/](http://www.coastalsustainability.rice.edu/outreach/).

