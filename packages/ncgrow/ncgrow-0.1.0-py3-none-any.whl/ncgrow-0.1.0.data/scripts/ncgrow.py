#!python
# -*- coding: utf-8 -*-
"""
Purpose: To grow/extend masked fields so they extend into the mask. Developed
    mainly to extend ocean data with a land-sea mask either after regridding or
    for visualization. The script computes weights and indices iteratively and
    then applies them to the selected input fields.

Note: The script tests the mask to see if it has changed, e.g sea-ice, and might
    re-compute weights, if mask changes very often this can increase the runtime.

Author: Brian Højen-Sørensen, brs@fcoo.dk

Version: 1.0 Initial version
Version: 1.1 Option to define land-mask from variable
Version: 1.2 Added support for additional dimensions
Version: 1.3 Granulated control for different variables
Version: 1.4 Output mask can be enforced
Version: 1.5 Added default (optional) smoothing
Version: 1.5.1 Code restructuring and bugfixes
Version: 1.5.2 Re-ordered loops for better performance
Version: 1.5.3 Added checks for packed files and inconsistent dimensions
Version: 1.6 Added niter_chunck for memory limiting
Version: 1.6.1 More correct handling of packed files
Version: 1.6.2 Ignore unmasked variables

TODO:
1: A lot of code is very similar and could be put in functions to simplify
   overall code
2: check for latitude and longitude dimensions for growing, hardcoded as 
   last two dimensions for now (which is reasonable).
3: Generalize for higher dimensional variables
4: Add support for degenerate dimensions (ignore them)
"""
# Standard library imports
from __future__ import print_function
import sys
import shutil
import os
import argparse
import time as tm

# External library imports
import netCDF4
import numpy as np

# Get my own name
scriptname = os.path.basename(__file__)

def ncgrow():
    """Grow/extend and/or fill masked fields"""

    # Get command line arguments
    parser = argparse.ArgumentParser(
        description ="Grow/extend and/or fill masked fields.")
    
    parser.add_argument(dest="infile", type=str, help="path to source file.")
    
    parser.add_argument(dest="outfile", type=str,
                        help="filename of the output file.")

    parser.add_argument("-v", "--variables", nargs='?', dest="variables",
                        type=str, metavar="..",
                        help="list of variables to extend, e.g. -v temp,elev.")

    parser.add_argument("-d", "--dims", action='append', nargs='?',
                        dest="dims",metavar="..",type=str,
                        help="Dimension subset, e.g. -d level,1,10,2")
    
    parser.add_argument("-m", "--maskvar", dest="maskvar",metavar="..",
                        nargs='?', action="append",type=str,
                        help="Variable name for land-sea mask that will be the \
                        enforced.")

    parser.add_argument("--maskfile", dest="maskfile",metavar='filename',
                        action="store",type=str,
                        help="External file containing mask variable(s), \
                              i.e. maskvar. Will be used before \
                              infile in case maskvar is present in both.")

    parser.add_argument("--smooth", metavar="..", nargs='?',
                        dest="smooth", action='append', type=str, 
                        help="Smooth grown cells to avoid unphysical values.\
                              Can also be specified per variable, e.g. \
                              --smooth True,temp, --smooth False,ice.\
                              default is True.")

    parser.add_argument("--fill", metavar="..", nargs='?',
                        dest="fill", action='append', type=str,
                        help="Default value to apply to any \
                              cells that are not missing_value or Fillvalue in \
                              maskvar. Will be ignored if --maskvar is not \
                              set. Optionally one can select 'max' 'min', \
                              'mean' of variable or None. Can also be \
                              specified per variable, e.g. --fill mean, \
                              temp, --fill 0,ice.")

    parser.add_argument("-i", "--iterations", dest="niter", metavar="..",
                        nargs='?', type=str, action='append',
                        help="Number of iterations to use, corresponds to one \
                              land cell per iteration. optionally with variable \
                              name appended, e.g. -i 2,temp,elev. Multiple \
                              defintions possible for granulated control.")

    parser.add_argument("--niter_chunks", dest="niter_chunks", metavar="..",
                        nargs='?', type=str, action='append',
                        help="Maximum number of iterations to hold in memory. \
                              Will reduce performance, but enable larger \
                              dataset and number of iterations. Optionally \
                              with variable name appended. Multiple \
                              defintions possible for granulated control. \
                              Default is 5.")

    parser.add_argument("-c", "--converge", dest="converge", metavar="..",
                        nargs='?', type=str, action='append',
                        help="Converge towards a given value 'V' with a factor \
                              f = [0-1] (default = 1). If not set no \
                              convergence is applied. e.g. -c 0,0.25,ice. Multiple \
                              defintions possible for granulated control.")

    parser.add_argument("-O", "--overwrite", dest="overwrite", default=False,
                        action="store_true", help="Overwrite output file if it \
                        exist (or append to input file).")

    parser.add_argument("-V", "--verbose", dest="verbose", default=False,
                        action="store_true", help="Increase runtime information.")

    parser.add_argument('--version', action='version', version='%(prog)s 1.6.2')

    args         = parser.parse_args()

    variables    = args.variables
    dims         = args.dims
    infile       = args.infile
    outfile      = args.outfile
    niter        = args.niter
    chunk        = args.niter_chunks
    maskvar      = args.maskvar
    maskfile     = args.maskfile
    fill         = args.fill
    smooth       = args.smooth
    converge     = args.converge
    overwrite    = args.overwrite
    verbose      = args.verbose

    # Does the input file actually exist
    if not os.path.isfile(infile):
        sys.exit(scriptname+': input file: '+infile+': no such file.')

    # Does the mask file actually exist
    if maskfile is not None:
        if not os.path.isfile(maskfile):
            sys.exit(scriptname+': mask file: '+maskfile+': no such file.')

    # Check if we are trying to overwrite any files (unless overwrite = True)
    if not overwrite:
        if os.path.isfile(outfile):
            sys.exit('{}: {} exists. Choose different name or use -O / --overwrite'.format(scriptname, outfile))

    # Copy input file to output file
    if infile != outfile: # Copy to <outfile>
        shutil.copyfile(infile, outfile)

    # Open destination file
    nc = netCDF4.Dataset(outfile, mode='a')

    # Check variables or choose all masked variables if None is specified
    if variables:
        variables = variables.split(',')
        for var in variables:
            if var not in nc.variables:
                sys.exit('{}: variable {} does not exist in sourcefile'.format(scriptname, var))
            if var in nc.dimensions:
                sys.exit('{}: variable {} is a dimension variable and should not be selected'.format(scriptname, var))
            if not is_masked(nc.variables[var]):
                sys.exit('{}: variable {} is not masked and should not be selected'.format(scriptname, var))
    else:
        variables = [v for v in nc.variables if not v in nc.dimensions and is_masked(nc.variables[v])]

    # Check dimensions or loop over all if none is specified (empty dict)
    dimensions= {}
    if dims:
        for dim in dims:
            dimensions[dim.split(',')[0]] = [int(i) for i in dim.split(',')[1:]]
        for dim in dimensions:
            if dim not in nc.dimensions:
                sys.exit('{}: dimension {} does not exist in sourcefile'.format(scriptname, dim[0]))

    # Construct iteration dictionary
    niter_global = 1
    if niter is not None:
        for ni in niter:
            if len(ni.split(',')) == 1:
                niter_global = int(ni.split(',')[0])
    niters = {}
    for var in variables:
        niters[var] = niter_global
        if niter is not None:
            for ni in niter:
                if var in ni:
                    niters[var] = int(ni.split(',')[0])

    # Construct chunk dictionary
    chunk_global = 5
    if chunk is not None:
        for c in chunk:
            if len(c.split(',')) == 1:
                chunk_global = int(c.split(',')[0])
    chunks = {}
    for var in variables:
        chunks[var] = chunk_global
        if chunk is not None:
            for c in chunk:
                if var in c:
                    chunks[var] = int(c.split(',')[0])
    
    # Construct fill dictionary
    fillvals_global = None
    if fill is None:
        fill = ['']
    else:
        for fv in fill:
            if len(fv.split(',')) == 1:
                fillvals_global = fv.split(',')[0]
    fillvals = {}
    for var in variables:
        fillvals[var] = fillvals_global
        for fv in fill:
            if var in fv:
                fillvals[var] = fv.split(',')[0]

    # Construct smoothing dictionary
    smooth_global=True
    if smooth is None:
        smooth = [str(smooth_global)]
    else:
        for s in smooth:
            if len(s.split(',')) == 1:
                smooth_global = (not s.split(',')[0] in ['false','False'])
    smoothvalues = {}
    for var in variables:
        smoothvalues[var] = smooth_global
        for s in smooth:
            if var in s:
                smoothvalues[var] = (not s.split(',')[0] in ['false','False'])

    # Construct mask dictionary
    maskvar_global = ''
    if maskvar is None:
        maskvar = [maskvar_global]
    else:
        for m in maskvar:
            if len(m.split(',')) == 1:
                maskvar_global = m.split(',')[0]
    maskvars = {}
    for var in variables:
        maskvars[var] = maskvar_global
        for m in maskvar:
            if var in m.split(',')[1:]:
                maskvars[var] = m.split(',')[0]
 
    # Construct converge dictionary
    converge_global = [None,None]
    if converge is None:
        converge = [converge_global]
    else:
        for c in converge:
            if len(c.split(',')) == 1:
                converge_global = [float(c.split(',')[0]),1.0]
            elif len(c.split(',')) == 2:
                try:
                    converge_global = [float(c.split(',')[0]),float(c.split(',')[1])]
                except ValueError:
                    converge_global = [float(c.split(',')[0]),1.0]
    convergevars = {}
    for var in variables:
        convergevars[var] = converge_global
        for c in converge:
            if var in c:
                try:
                    convergevars[var] = [float(c.split(',')[0]),float(c.split(',')[1])]
                except ValueError:
                    convergevars[var] = [float(c.split(',')[0]),1.0]

    # Open maskfile if neccesary
    if maskfile is None:
        ncm = netCDF4.Dataset(infile, mode='r')
    else:
        ncm = netCDF4.Dataset(maskfile, mode='r')

    # Extend fields
    for var in variables:
        t = tm.time()
        # Skip if we do not grow
        if niters[var] == 0:
            continue
        v = nc.variables[var]
        ndim = len(v.shape)

        # Only consider variables with at least 2 dimensions
        if ndim < 2:
            continue
        
        # initialize
        vmask = None
        lmask = None
        ncells = 0

        # Check if variable is packed and see if fill and converge values are possible
        if convergevars[var][0] is not None:
            check_packed_value(v, convergevars[var][0])
        if fillvals[var] is not None or fillvals[var] in ['min','mean','max']:
            check_packed_value(v, fillvals[var])

        if verbose:
            print('{} - Processing'.format(var), end='\r')
            sys.stdout.flush()

        # Look for mask(s) in file(s)
        if maskvars[var]:
            # Choose correct mask file
            if maskvars[var] in ncm.variables:
                    lsmout = ncm.variables[maskvars[var]]
            elif maskvars[var] in nc.variables:
                    lsmout = nc.variables[maskvars[var]]
            else:
                sys.exit('{}: maskvar {} does not exist in sourcefile or maskfile'.format(scriptname, maskvars[var]))
        else:
            lsmout = None

        # Simple case for 2D fields
        if ndim == 2: 
            if lsmout:
                if len(lsmout.shape) == 2 and lsmout.shape[:] == v.shape[:]:
                    lmask = lsmout[:].mask
                else:
                   sys.exit('{}: {} : dimensions of land-sea mask seems wrong: dims = {}'.format(scriptname, var, lsmout.shape[:]))

            # Compute weights
            vmask = v[:].mask
            ia, ib, ni, wi = grow_weights(vmask, niter=niters[var])
            # Grow
            v[:] = grow(v[:], ia, ib, ni, wi, niter=niters[var], 
                locked_mask=lmask, smooth=smoothvalues[var],
                converge=convergevars[var][0],converge_speed=convergevars[var][1])
            
            # Sum cells grown
            ncells += np.count_nonzero(ni)
 
            # Apply default value where needed
            if lsmout and fillvals[var] is not None:
                v[:] = fill_mask(v[:], fillvals[var], lmask)
        # 3D fields
        elif ndim == 3:
            # Get dimension range
            irange = dim_range(v, dimensions, 0)
            # Loop over chunks
            c = 0
            crange = chunk_range(niters[var], chunks[var])
            for ic in crange:
                c += 1
                # Loop over first dimension
                for i in irange:
                    if lsmout:
                        if len(lsmout.shape) == 3 and lsmout.shape[:] == v.shape[:]:
                            lmask = lsmout[i].mask
                        elif len(lsmout.shape) == 2 and lsmout.shape[:] == v.shape[1:]:
                            lmask = lsmout[:].mask
                        else:
                            sys.exit('{}: {} : dimensions of land-sea mask seems wrong: dims = {}'.format(scriptname, var, lsmout.shape[:]))

                    imask = v[i].mask
                    if not np.array_equal(vmask, imask):
                        vmask = imask
                        ia, ib, ni, wi = grow_weights(vmask, niter=ic)
                    # Grow
                    v[i] = grow(v[i], ia, ib, ni, wi, niter=ic,
                        locked_mask=lmask, smooth=smoothvalues[var],
                        converge=convergevars[var][0],converge_speed=convergevars[var][1])

                    # Sum cells grown
                    ncells += np.count_nonzero(ni)

                    # Last chunk
                    if c == len(crange):
                        # Apply default value where needed
                        if lsmout and fillvals[var] is not None:
                            v[i] = fill_mask(v[i],fillvals[var],lmask)
        # 4D fields
        elif ndim == 4:
            # Get dimension ranges
            irange = dim_range(v, dimensions, 0)
            jrange = dim_range(v, dimensions, 1)
            # Loop over second dimension
            for j in jrange:
                # Loop over chunks
                c = 0
                crange = chunk_range(niters[var], chunks[var])
                for ic in crange:
                    c += 1
                    # Loop over first dimension
                    for i in irange:
                        if lsmout:
                            if len(lsmout.shape) == 4 and lsmout.shape[:] == v.shape[:]:
                                lmask = lsmout[i,j].mask
                            elif len(lsmout.shape) == 3 and lsmout.shape[0] == v.shape[0] and lsmout.shape[1:] == v.shape[2:]:
                                lmask = lsmout[i].mask
                            elif len(lsmout.shape) == 2 and lsmout.shape[:] == v.shape[2:]:
                                lmask = lsmout[:].mask
                            else:
                                sys.exit('{}: {} : dimensions of land-sea mask seems wrong: dims = {}'.format(scriptname, var, lsmout.shape[:]))
    
                        imask = v[i,j].mask
                        if not np.array_equal(vmask, imask):
                            vmask = imask
                            ia, ib, ni, wi = grow_weights(vmask, niter=ic)
    
                        # Grow
                        v[i,j] = grow(v[i,j], ia, ib, ni, wi, niter=ic,
                            locked_mask=lmask, smooth=smoothvalues[var],
                            converge=convergevars[var][0],converge_speed=convergevars[var][1])
    
                        # Sum cells grown
                        ncells += np.count_nonzero(ni)

                        # Last chunk
                        if c == len(crange):     
                            # Apply default value where needed
                            if lsmout and fillvals[var] is not None:
                                v[i,j] = fill_mask(v[i,j],fillvals[var],lmask)
        else:
            sys.exit('{}: Too many dimensions ({}) for variable {}. Only 2D, 3D, and 4D is supported'.format(scriptname, ndim, var))
    
        if verbose:
            print('{} - {} cells in {:.2f} seconds'.format(var,ncells,tm.time()-t))

    # Append history information and close output file
    old_hist = nc.history
    nowstr = tm.strftime('%Y-%m-%d %H:%M:%S (GM)', tm.gmtime())
    hist = "%s ncgrow.py %s\n" %(nowstr, ' '.join(sys.argv[1:]))
    nc.history = hist + old_hist
    nc.close()
    ncm.close()

def grow(vals, ia, ib, ni, wi, niter=1, locked_mask=None, smooth=True, converge=None, converge_speed=1):
    """"Apply weights for growing"""
    # Define initial mask
    m = vals.mask

    # Loop over growth iterations
    for i in range(niter):
        n = np.where(ni[i], True, False)

        # Set masked values to 0
        vals = np.where(m, 0, vals)

        # Add mean value from neighbors in growth zone
        vals[n] +=(vals[ib[n,0], ia[n,0]] + vals[ib[n,1], ia[n,0]] + vals[ib[n,2], ia[n,0]]
                +  vals[ib[n,0], ia[n,1]] + vals[ib[n,1], ia[n,1]] + vals[ib[n,2], ia[n,1]]
                +  vals[ib[n,0], ia[n,2]] + vals[ib[n,1], ia[n,2]] + vals[ib[n,2], ia[n,2]]) / wi[i,n]

        # Update mask
        m = np.where(n, False, m)

        # Enforce locked mask
        if locked_mask is not None: 
            m = np.where(locked_mask, True, m)

        # Smooth new values
        if smooth:
            vals[n] = masked_smooth(vals, m)[n]

        # Converge new values
        if converge is not None:
            vals[n] = (1-0.5*converge_speed)*vals[n] + 0.5*converge_speed*converge

    # Apply mask to array
    vals = np.ma.masked_where(m, vals)

    return vals

def grow_weights(mask, niter=1):
    """Compute iterative weights for growing"""
    # Initialize work arrays
    nlat = mask.shape[0]
    nlon = mask.shape[1]
    ni = np.zeros((niter,nlat,nlon))
    wi = np.zeros((niter,nlat,nlon))

    # Create arrays of indices
    ia,ib = np.meshgrid(np.arange(0,nlon,1), np.arange(0,nlat,1))

    ia = np.dstack((ia - 1, ia, ia + 1))
    ib = np.dstack((ib - 1, ib, ib + 1))
    ia = np.where(ia < 0, 0, ia)
    ib = np.where(ib < 0, 0, ib)
    ia = np.where(ia > nlon-1, nlon-1, ia)
    ib = np.where(ib > nlat-1, nlat-1, ib)
    
    for i in range(niter):
        # Initialize work arrays
        valw = np.where(mask, 0.0, 1.0)

        # Calculate weight
        wi[i] = ( valw[ib[:,:,0], ia[:,:,0]] + valw[ib[:,:,1], ia[:,:,0]] + valw[ib[:,:,2], ia[:,:,0]] 
                + valw[ib[:,:,0], ia[:,:,1]] + valw[ib[:,:,1], ia[:,:,1]] + valw[ib[:,:,2], ia[:,:,1]] 
                + valw[ib[:,:,0], ia[:,:,2]] + valw[ib[:,:,1], ia[:,:,2]] + valw[ib[:,:,2], ia[:,:,2]] )

        # Compute mask change
        n = np.where(wi[i] < 1, False, True) 
        ni[i] = np.where(n, mask, False)

        # Update mask
        mask = ~n
   
    return ia, ib, ni, wi

def masked_smooth(vals, mask):
    """Smooth field"""
    v = vals.copy()
    m = ~mask
    r = v*m  # set all 'masked' points to 0. so they aren't used in the smoothing
    a = 0 + r[2:,1:-1] + r[:-2,1:-1] + r[1:-1,2:] + r[1:-1,:-2]
    b = 0 + m[2:,1:-1] + m[:-2,1:-1] + m[1:-1,2:] + m[1:-1,:-2]  # a divisor that accounts for masked points
    b[b==0] = 1.  # for avoiding divide by 0 error (region is masked so value doesn't matter)
    v[1:-1,1:-1] = a/b

    return v

def fill_mask(vals, fill, mask):
    """Fill unmasked values"""
    # Compute fillvalue
    if fill == 'mean':
        fv = np.ma.mean(vals)
    elif fill == 'min':
        fv = np.ma.min(vals)
    elif fill == 'max':
        fv = np.ma.max(vals)
    else:
        fv = float(fill)

    # Apply mask
    fvmask = np.where(vals.mask, ~mask, vals.mask)
    vals = np.where(fvmask,fv, vals)
    vals = np.ma.masked_where(mask, vals)
    return vals

def dim_range(var, dimensions, i):
    """Return dimension range"""
    dim = var.dimensions[i]
    if dim in dimensions:
        drange = range(dimensions[dim][0],dimensions[dim][1]+1,dimensions[dim][2])
    else:
        drange = range(var.shape[i])
    return drange

def check_packed_value(var, val):
    """Check if value can be represented"""
    # Check if value is packed
    if 'add_offset' in var.ncattrs() or 'scale_factor' in var.ncattrs():
        if not 'add_offset' in var.ncattrs():
            add_offset = 0.0
        else:
            add_offset = var.add_offset
        if not 'scale_factor' in var.ncattrs():
            scale_factor = 1.0
        else:
            scale_factor = var.scale_factor
        
        val = float(val)
        a = (val-add_offset)/scale_factor
        b = round(a)*scale_factor+add_offset
        vmax=np.iinfo(var.dtype).max*scale_factor+add_offset
        vmin=np.iinfo(var.dtype).min*scale_factor+add_offset
        if vmax < vmin:
            vmin, vmax = vmax,vmin
        if vmin <= val <= vmax:
            if b != val:
                print('Warning: fill {} cannot be represented exactly in packed variable. Nearest value = {:.5f}'.format(val, b))
        else:
            sys.exit('{}: fill {} cannot be represented in packed variable. range = [{:.5f}, {:.5f}]'.format(scriptname, val, vmin, vmax))

def chunk_range(size, chunk_size):
    """Return list of chunks"""
    if chunk_size is None:
        return [size]
    crange = [chunk_size]*(size//chunk_size) \
           + [size-chunk_size*(size//chunk_size)]
    crange = [x for x in crange if x != 0]
    return crange

def mem_limiter(mem, domain_size):
    """Compute max chunk_size"""
    # Current memory profile
    #NOTE inconsistent across systems
    m0 = 26500.0
    m1 = 0.21
    m2 = 0.0315
    (nx, ny) = domain_size
    used_mem = m0+m1*nx*ny+m2*nx*ny
    chunk_size = (1e3*mem-m0-m1*nx*ny)/(m2*nx*ny)
    return max(1, int(chunk_size))

def is_masked(variable):
    """Test if a variable is masked"""
    ndim = len(variable.shape)
    if ndim <= 2:
        return np.ma.is_masked(variable[:])
    if ndim == 3:
        return np.ma.is_masked(variable[0,:])
    if ndim == 4:
        return np.ma.is_masked(variable[0,0,:])
    else:
        sys.exit('{}: Too many dimensions ({}) for variable {}. Only 2D, 3D, and 4D is supported'.format(scriptname, ndim, variable))

if __name__ == "__main__":
    """Execute main function"""
    ncgrow()
