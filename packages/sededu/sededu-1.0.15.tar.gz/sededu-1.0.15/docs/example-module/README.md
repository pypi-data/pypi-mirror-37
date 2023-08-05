# Example Module for SedEdu

The goal of this module is to give module developers a potential workflow for designing their modules and a sense of what is possible. 
This `README.md` is __not__ a template for a module README; you can find a [template README](https://github.com/amoodie/template-module_sededu/blob/master/README.md) in the `template-module`.
In fact, the companion repository `template-module` is a great place to look for additional examples of a blank `about.json` and empty folder structure.



## Folder and file organization

This section discusses a potential folder structure for your module.
It describes some of the logic behind this structure, but it by no means required to follow this setup.

The folder structure of this example module is to separate the logical portions of the module, and is configured to work with SedEdu and includes GitHub repository folders and files. 
Note that the contents of `.git` are not listed in the tree for brevity.

```
example-module/
├── .git
│   └── not-listed-here
├── docs
│   ├── theory.md
│   └── worksheet.md
├── private
│   ├── base_slider.png
│   ├── custom_slider.png
│   ├── example-module_demo.png
│   └── without_sliders.png
├── src
│   ├── example-module.py
│   └── utils.py
├── about.json
├── .gitignore
├── LICENSE.txt
└── README.md
```

The module root is the `example-module` folder, and this root contains 4 folders and 4 files. 
The first folder is the `.git` folder, which manages the `git` history of the repository -- we won't go over that technology or its importance here, you can ignore it for this tutorial.

The second folder is `docs` and it contains 2 files. 
This folder would be where we would put all the activities related to the module (worksheets, explanations, answer keys, etc.).

Third, there is a folder called `private` which is used to store files and folders that should not be interacted with directly by the user.
In this example module, the images used in the README are stored in this folder.
If you had static images that were used in your module you could put them here.
You could also put data here (in a subfolder called `data`).

Finally we have the `src` folder, which contains our module's codebase. 
This is where the main executable `example-module.py` and a support module `utils.py` live.

In the root repository then we have a `README.md` (the file you are reading!), a `LICENSE.txt`, a file called `about.json`, and a `.gitignore`.
The `README` should provide an overview of using the module, and information about authors, supporting documents (publications?), funding sources, etc.
The `LICENSE.txt` contains the modules licensing information, see [Module Licensing](https://github.com/amoodie/sededu/blob/release/docs/contributing_module.md#module-licensing) for more information (we recommend the [MIT license](https://choosealicense.com/licenses/mit/)).
The `about.json` file just contains some simple information which gets displayed/used within SedEdu; see [Contributing a Module](https://github.com/amoodie/sededu/blob/release/docs/contributing_module.md) and [Writing about.json](https://github.com/amoodie/sededu/blob/release/docs/writing_aboutjson.md) for more information about this file's contents.
The `.gitignore` file is a GitHub related file that tells your local repository which files to sync with the remote GitHub repository (you don't need to worry about this right now)

Below the _minimum required files for your module to be incorporated into SedEdu_ are listed. A separate article exists with complete information on [contributing a module to SedEdu](https://github.com/amoodie/sededu/blob/release/docs/contributing_module.md).

* `README.md` -- here is a template
* `LICENSE.txt` -- see [below](#licensing), and [Module Licensing](https://github.com/amoodie/sededu/blob/release/docs/contributing_module.md#module-licensing)
* `about.json` -- see [writing `about.json`](https://github.com/amoodie/sededu/blob/release/docs/writing_aboutjson.md)
* executable python script

The following section describes in detail the last listed required file: the executable python script `example-module.py`.



## The Module

The main module code resides in `src/example-module.py`. 
This is the executable code that will launch your module when called from SedEdu.
A complete walk-through of this file is below, but the basic workflow is to:
1. set initial parameters
1. define functions to run the module and update the plots (i.e., the backend)
1. run the model once
1. set up the figure
1. set up and connect the interactive widgets

Please note that what follows is __not__ meant to be an exhaustive description of what you can do with a module.
There is no reason that your module should be limited to one main figure, or only slider widgets, or even using `matplotlib` as the main back end.
You are encouraged to be way more creative in designing your module!

This is also not supposed to be a tutorial on Python, `matplotlib`, etc.; please refer to documentation and tutorials in those tools for more information.

The module we will develop here is not really a model, but just a simple evaluation of the sine function over a predefined interval.
We'll introduce some sliders to manipulate the amplitude and period of the sine and link those to updating the  when they are moved.
Finally, we'll add a button to reset the module to its initial condition.
The module GUI is below.

![demo image](./private/example-module_demo.png "demo of the module")


### Setting initial parameters

First we import the packages/libraries needed:

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget
import utils
```

`matplotlib`'s `pyplot` and `widgets` will provide the bulk of the interface elements we use in this simple module.
You should do all your package/module imports at the start of the script here. 
SedEdu modules already depends on `scipy` (and `numpy`), `matplotlib`, `pygame`, and `shapely`, as well as all the standard packages; feel free to import and use anything in these packages in your module.
If you need another package, you will need to make a strong case for including it in SedEdu as a requirement; open an issue on [sededu/issues](https://github.com/amoodie/sededu/issues) to discuss this with other developers/maintainers.

`utils` is just another python file I have written for myself to use within this module; the file is located in `src/utils.py` so it can be imported only from the local directory.
In this way, you can split function or object logic across files as your module becomes more complex.
Of course, this is not necessary, it just helps keep your code clean and readable. 
It is common to have a `utils.py` module that provides a place to stick simple utility-like functions (e.g., formatting a number properly, or ugly if-then statements). 

Next, we declare the parameter set used in our model.
This could include anything from model coefficients to plotting vectors, and should include the limits you will use on any sliders that manipulate parts of the model.

```python
pi = np.pi
t = np.linspace(-3*pi, 6*pi, 1000)

ampInit = 1
amp = ampInit
ampMax = 5
ampMin = 0

perInit = 2 #2*pi
per = perInit
perMax = 10
perMin = 0.1
```

In this case, we set up the "x" coordinates of our plot as the period of the sine function `t`. 
The next two blocks initiate the amplitude and period variables (`amp` and `per`) and the bounds on the sliders (`ampMin`, `perMax`, etc.) that we'll use later when we make the sliders.


### Defining functions

Next we define some functions, in this module we'll only define two, since out model is very simple.
In most any module you design the minimum requirement would be an `update` function that is run on some `event`.
This `event` could be (as in our case) a change in slider position, or a button press, or a mouse click, or many other possible event triggers. 

Our `update` function will simply grab the current value of the sliders (i.e., get the amplitude and period of the sine function), recalculate the sine function, and update the plot to reflect the new sine function.

```python
def update(event):

    # read values from the sliders/statics
    theamp = slide_amp.val # using "the" here keeps main namespace clean
    theper = slide_per.val

    # compute new y values
    they = theamp * np.sin( ((2*pi)/(theper*pi)) * t )

    # update the plot
    sin_line.set_ydata(they)

    # replace in main namespace
    amp = theamp
    per = theper
    y = they

    # redraw the canvas
    fig.canvas.draw_idle()
```

We have not created the sliders yet, so this may be a little confusing, but we are going to create two sliders called `slide_amp` and `slide_per` that each have an attribute `val` that contains the value of the slider object. 
We use these values to compute the new y coordinates. 
Inside the function, we use variables prefixed with "the" to ensure we are using the new values and not muddying the namespace with that outside the function.
This shouldn't be strictly necessary, but if you have some weird bugs in updating from sliders it might be fixed by prefixing with "the".

We also define a `reset` function here, which will be connected to an event of clicking a "Reset" button.
The `reset` function is fairly simple, we simply set the sliders back to their initial state, and then evaluate the model with the new (reset) values.
This, in turn, updates the plot.

```python
def reset(event):
    
    # reset button
    slide_amp.reset()
    slide_per.reset()
    update(event)
```


### Run the model once first

In our really simple model, this step consists of only one line of code, to calculate the y coordinates of the sine function with initial amplitude and period values:

```python
y = amp * np.sin( ((2*pi)/(per*pi)) * t )
```

Now, in our model it is not really necessary to do this after the function declarations, we could do it up with our parameters declarations (e.g., right after `t`, `amp`, and `per` have each been declared.
It is preferred to lay our your module in this way because as your model becomes more elaborate, you may have multiple other function calls in your model execution.
For example, `y = ...` above could become:

```python
y3 = function_a(amp, per)
y2 = function_b(y3, another_var)
y = function_c(y2, y3, another_another_var)
```

where `function_a`, `function_b`, and `function_c` are arbitrarily complex functions.
By laying the module logic out with the first model evaluation only after the function declarations, we reduce code redundancy. 
We can simply call `function_a`, `function_b`, and `function_c` for our first initialization of the model, instead of rewriting the entirety of their logic at the top of the script (with the parameter declarations) and then again in function declarations and/or in the `update` function.


### Setting up a main figure

Our main figure in this module will display the sine function we are evaluating in our model.
Commented code describing the setup of this figure is below:

```python
plt.rcParams['toolbar'] = 'None'                                    # turn off the matplotlib toolbar in the figure
plt.rcParams['figure.figsize'] = 11, 7                              # size of the figure in inches
fig, ax = plt.subplots()                                            # gives us a figure object and axes object to manipulate and plot things into
fig.canvas.set_window_title('SedEdu -- example module')             # title of the figure window
plt.subplots_adjust(left=0.075, bottom=0.1, top=0.95, right=0.5)    # where do we want the limits of the axes object
ax.set_xlabel("t")                                                  # the axis xlabel
ax.set_ylabel("y")                                                  # the axis ylabel
plt.xlim(min(t), max(t))                                            # the axis x limits
plt.ylim(-ampMax*1.25, ampMax*1.25)                                 # the axis y limits
ax.xaxis.set_major_locator(plt.MultipleLocator(base=pi))            # locate tick marks every pi
ax.xaxis.set_major_formatter( plt.FuncFormatter( \ 
                        lambda v, x: str(int(v/pi)) + '$\pi$') )    # label them with X$\pi$ 
```

The figure and axes syntax is reasonably simple if you have used Matlab before (the namesake of `matplotlib`), and you can find _extensive_ documentation for `matplotlib.pyplot` on the [official site](https://matplotlib.org/api/pyplot_summary.html).

Adding artists (that's what points, lines, polygons, etc. are called in `matplotlib`) is simple too, and follows a Matlab-like syntax.
In our axes, we'll add an "x" and "y" line to denote the origin, and then add our sine function evaluation.

```python
x_line = plt.plot([min(t), max(t)], [0, 0], ls=':', lw=1, color='gray')
y_line = plt.plot([0, 0], [-ampMax*1.5, ampMax*1.5], ls=':', lw=1, color='gray')
sin_line, = plt.plot(t, y, lw=1.5, color='blue')
```

__NOTE:__ that to be able to manipulate an artist after creating it, you need to retain a handle to the artist (i.e., a left-hand assignment).
A comma after the left-hand assignment prevents the artist object from going into a list. 
If you instantiate multiple artists with a single `plot` command, you can receive them back in a list or unpack them with comma separated variable names.

This example module only has one main figure, though there is no reason you could not have more in your module.
You would simply need to retain a unique handle to manipulate the `matplotlib` axes and children artists with. 


### Setting up and connecting widgets

This finishes off the basis of our module. If we were to run our code now (call `plt.show()`, we would produce a figure window that has our lines in the axes, on the left side of the window.

![non-interactive](./private/without_sliders.png "the module without sliders")
 
But our module has no interactive component and is pretty darn boring.
We'll add two sliders that modulate the amplitude and period of the sine function.
`matplotlib` widgets get created into axes which determine their dimensions and position, so we first instantiate axes where we want the slider to be and then plot the slider. 
We will specify the axes coordinates in relative terms `(0, 0)` is lower left coordinate and `(1, 1)` is the upper right; `[x, y, w, h]` where `xy` are the coordinates of the lower left corner of the axes and `wh` is the width and height of the axes. 
To make the relative plotting work though, we need to `transform` in our call to create the widgets in the next step (`transform=ax.transAxes`). 

```python
widget_color = 'lightgoldenrodyellow'

ax_amp = plt.axes([0.55, 0.85, 0.4, 0.05], facecolor=widget_color)
slide_amp = utils.MinMaxSlider(ax_amp, 'amplitude', ampMin, ampMax, 
    valinit=ampInit, valstep=0.1, valfmt='%g', transform=ax.transAxes)

ax_per = plt.axes([0.55, 0.725, 0.4, 0.05], facecolor=widget_color)
slide_per = utils.MinMaxSlider(ax_per, 'period', perMin, perMax, 
    valinit=perInit, valstep=0.1, valfmt='%g'+'$\pi$', transform=ax.transAxes)
```

__NOTE:__ in this example, we use a custom slider widget from `utils` called `MinMaxSlider`.
This is a custom class (object) created by Andrew Moodie which simply adds/modifies a few labels of the base `matplotlib.widgets.Slider` class. 
In this custom class, the label is below the slider, the minimum value and maximum value are on the left and right ends of the slider respectively, and the selected value is in the center body of the slider.

![custom slider](./private/custom_slider.png "custom slider")

The custom slider code can be found in `src/utils.py` of this repository if you wish to use it in your own module. 
The custom slider could be switched out for the base slider with, for example:

```python
slide_per = widget.Slider(ax_per, 'period', perMin, perMax, 
    valinit=perInit, valstep=0.01, valfmt='%g', transform=ax.transAxes)
```

which places the label on the left end and the value on the right end.

![base slider](./private/base_slider.png "base slider")

Now we add the reset button. 
Similar to the sliders, the button dimensions and location are determined by the axis object they are plotted into.

```python
btn_reset_ax = plt.axes([0.825, 0.5, 0.1, 0.04])
btn_reset = widget.Button(btn_reset_ax, 'Reset', color=widget_color, hovercolor='0.975')
```

This completes the frontend of our module.
We now have to connect activity of the widgets to functions.
Sliders have a method to "do something" `on_changed` which we will connect to, and buttons have a method `on_clicked`.

```python
slide_amp.on_changed(update)
slide_per.on_changed(update)
btn_reset.on_clicked(reset)
```

Note that we do not include parentheses in the reference to `update`.
This is because on_changed and on_clicked take functions as arguments, _not values_.
If for some reason you need to pass a value to `update` other than what is in the global namespace, you can pass with a `lambda`:

```python
slide_per.on_changed(lambda e, x: update(e, x))
```

where `e` is the event trigger and `x` is whatever other value you need.


And finally, we reveal the constructed figure:

```python
plt.show()
```



## Activities and Worksheets

Now that we have a working module, we need to write activities to complete alongside the module.
For our simple module, it would be good to have a document describing some "theory" behind a sine function and an activity to explore the functionality our module offers.
Some __incomplete example__ activities like this are [in the `docs` folder](https://github.com/amoodie/example-module_sededu/tree/master/docs).



## Integrating into SedEdu
To integrate this activity into SedEdu at this point is quite simple. 
In summary, we need to 

* create an `about.json` file to describe the module
* add a license
* push our project to our own repository on GitHub
* fork SedEdu
* add our module as a submodule
* pull request to SedEdu

This process is _very_ easy, but requires a thorough explanation for those new to the `git` workflow.
Therefore, there is an entire article describing [how to contribute a module to SedEdu](https://github.com/amoodie/sededu/blob/release/docs/contributing_module.md).



## Licensing

You will need to add a license to your module and GitHub repository before it will be incorporated into SedEdu.
At the very least, your module needs to be licensed to allow the module to be incorporated into larger software projects (e.g., SedEdu).

We recommend the [MIT license](https://choosealicense.com/licenses/mit/) first, and then the [GNU GPLv3 license](https://choosealicense.com/licenses/gpl-3.0/).
Simply create a file called `LICENSE.txt` and copy-paste the contents of the license into that file.

For more help choosing a license see [GitHub on licenses](https://help.github.com/articles/licensing-a-repository/) or [choosealicense.com](https://choosealicense.com/)
