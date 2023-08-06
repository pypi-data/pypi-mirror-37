# ncgrow

To grow/extend masked fields so they extend into the mask. Developed mainly to extend ocean data with a land-sea mask either after regridding or for visualization. The script computes weights and indices iteratively and then applies them 

## Installation

ncgrow can be installed after downloading this repository by running:

```
python3 setup.py install [--user]
```

It can also be installed directly from the Python Packaging Index (PyPI) by running:

```
pip3 install ncgrow
```

## Development

### Packaging

Create distribution:

```
python3 setup.py sdist bdist_wheel
```

After that the package can be uploaded to PyPI.

## Usage ##
The ncgrow script has the following usage.
 ```
 usage: ncgrow.py [-h] [-v [..]] [-d [..]] [-m [..]] [--maskfile filename]
                 [--smooth [..]] [--fill [..]] [-i [..]] [--niter_chunks [..]]
                 [-c [..]] [-O] [-V] [--version]
                 infile outfile

Grow/extend and/or fill masked fields.

positional arguments:
  infile                path to source file.
  outfile               filename of the output file.

optional arguments:
  -h, --help            show this help message and exit
  -v [..], --variables [..]
                        list of variables to extend, e.g. -v temp,elev.
  -d [..], --dims [..]  Dimension subset, e.g. -d level,1,10,2
  -m [..], --maskvar [..]
                        Variable name for land-sea mask that will be the
                        enforced.
  --maskfile filename   External file containing mask variable(s), i.e.
                        maskvar. Will be used before infile in case maskvar is
                        present in both.
  --smooth [..]         Smooth grown cells to avoid unphysical values. Can
                        also be specified per variable, e.g. --smooth
                        True,temp, --smooth False,ice. default is True.
  --fill [..]           Default value to apply to any cells that are not
                        missing_value or Fillvalue in maskvar. Will be ignored
                        if --maskvar is not set. Optionally one can select
                        'max' 'min', 'mean' of variable or None. Can also be
                        specified per variable, e.g. --fill mean, temp, --fill
                        0,ice.
  -i [..], --iterations [..]
                        Number of iterations to use, corresponds to one land
                        cell per iteration. optionally with variable name
                        appended, e.g. -i 2,temp,elev. Multiple defintions
                        possible for granulated control.
  --niter_chunks [..]   Maximum number of iterations to hold in memory. Will
                        reduce performance, but enable larger dataset and
                        number of iterations. Optionally with variable name
                        appended. Multiple defintions possible for granulated
                        control. Default is 5.
  -c [..], --converge [..]
                        Converge towards a given value 'V' with a factor f =
                        [0-1] (default = 1). If not set no convergence is
                        applied. e.g. -c 0,0.25,ice. Multiple defintions
                        possible for granulated control.
  -O, --overwrite       Overwrite output file if it exist (or append to input
                        file).
  -V, --verbose         Increase runtime information.
  --version             show program's version number and exit

 ```