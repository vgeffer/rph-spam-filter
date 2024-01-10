# rph-spam-filter
This repository contains an implementation of semestral assignment from b4b33rph - spam filter.
More info about implementation requirements, data format and provided datasets can be found [here](https://cw.fel.cvut.cz/wiki/courses/b4b33rph/cviceni/spam/start) (in Czech language).
With my testing the filter achieves around 80 - 85% accuracy with provided datasets.

### Running 
Run the file `quality.py` from the root directory of the repo. This file contains code to evaluate accuracy and performance of the filter on given dataset.
It does not require any dependencies to run. Tested working on Python 3.10+. May not work on Windows (uses /tmp directory for datasets).

### Using as a module
I don't really know why would you do that, but ok. 
Just import `MyFilter` from `filter.filter`
If you want aditional functions related to measuring accuracy of the filter, import module `quality`.
For miscelaneous helper funtions import `filter.utils`.
