from lib5c.tools.parents import lim_parser, primerfile_parser


def add_visualize_dispersion_tool(parser):
    visualize_dispersion_parser = parser.add_parser(
        'visualize-dispersion',
        prog='lib5c plot visualize-dispersion',
        help='visualize dispersion estimates',
        parents=[primerfile_parser, lim_parser]
    )
    visualize_dispersion_parser.add_argument(
        'observed',
        type=str,
        help='''Glob-expandable file pattern matching observed countsfiles for
        at least two replicates (quoted to prevent shell expansion).''')
    visualize_dispersion_parser.add_argument(
        'expected',
        type=str,
        help='''File containing expected counts.''')
    visualize_dispersion_parser.add_argument(
        'outfile',
        type=str,
        help='''Filename to draw plot to.''')
    visualize_dispersion_parser.add_argument(
        '-m', '--model',
        type=str,
        choices=['lognorm', 'norm', 'nbinom'],
        default='lognorm',
        help='''The model used to estimate the pixel-wise dispersion/variance.
        Default is 'lognorm'.''')
    visualize_dispersion_parser.add_argument(
        '--x_unit',
        type=str,
        choices=['dist', 'exp'],
        default='dist',
        help='''The x-units of the plot. Default is 'dist'.''')
    visualize_dispersion_parser.add_argument(
        '--y_unit',
        type=str,
        choices=['disp', 'var'],
        default='disp',
        help='''The y-units of the plot. Default is 'disp'.''')
    visualize_dispersion_parser.add_argument(
        '--unlogx',
        action='store_true',
        help='''Pass to unlog the x-axis (default is to log it).''')
    visualize_dispersion_parser.add_argument(
        '--unlogy',
        action='store_true',
        help='''Pass to unlog the y-axis (default is to log it).''')
    visualize_dispersion_parser.add_argument(
        '-S', '--scatter',
        action='store_true',
        help='''Pass to plot a simple scatterplot (default is a hexbin
        plot).''')
    visualize_dispersion_parser.add_argument(
        '-v', '--variance',
        help='''Pass a countsfile of variance estimate to overlay the estimates
        over the data.''')
    visualize_dispersion_parser.add_argument(
        '-V', '--vst',
        action='store_true',
        help='''Pass this flag with -v/--variance to interpret the entries in
        the countsfile as stabilized variances (already on the scale of
        dispersion).''')
    visualize_dispersion_parser.set_defaults(func=visualize_dispersion_tool)


def visualize_dispersion_tool(parser, args):
    import glob
    import numpy as np
    from lib5c.tools.helpers import resolve_primerfile
    from lib5c.parsers.primers import load_primermap
    from lib5c.parsers.counts import load_counts
    from lib5c.util.counts import flatten_counts_to_list
    from lib5c.algorithms.variance_legacy.dispersion import dispersion_to_variance, \
        variance_to_dispersion
    from lib5c.algorithms.variance import estimate_pixel_wise_variance
    from lib5c.plotters.scatter import scatter
    from lib5c.plotters.curve_fits import plot_fit

    # resolve primerfile
    primerfile = resolve_primerfile(args.observed, args.primerfile)

    # expand infiles
    expanded_infiles = glob.glob(args.observed)

    # load counts
    print('loading counts')
    primermap = load_primermap(primerfile)
    obs_counts_superdict = {
        expanded_infile: load_counts(expanded_infile, primermap)
        for expanded_infile in expanded_infiles}
    exp_counts = load_counts(args.expected, primermap)

    # resolve xlim and ylim
    xlim = map(float, args.xlim.strip('()').split(',')) \
        if args.xlim is not None else None
    ylim = map(float, args.ylim.strip('()').split(',')) \
        if args.ylim is not None else None

    # flatten everything, including distance values
    print('preparing to plot')
    exp, dist, mean_mle, disp_mle, var_mle, idx, idx_od, matrix, region_order =\
        estimate_pixel_wise_variance(obs_counts_superdict, exp_counts,
                                     model=args.model)

    x = dist if args.x_unit == 'dist' else exp
    y = disp_mle if args.y_unit == 'disp' else var_mle

    # load variance if passed
    if args.variance is not None:
        var_counts = load_counts(args.variance, primermap)
        var = flatten_counts_to_list(var_counts, region_order=region_order,
                                     discard_nan=False)
        var = var[idx]
        if args.y_unit == 'disp' and not args.vst:
            if args.model == 'lognorm':
                y_hat = np.log(1 + var/exp**2)
            elif args.model == 'nbinom':
                y_hat = variance_to_dispersion(var, exp, min_disp=1e-7)
            else:
                y_hat = var
        elif args.y_unit == 'var' and args.vst:
            # vst block - var is actually disp
            if args.model == 'lognorm':
                mean = np.log(exp) - var / 2
                var[idx] = (np.exp(var) - 1) * np.exp(2 * mean + var)
            elif args.model == 'nbinom':
                y_hat = dispersion_to_variance(var, exp)
            else:
                y_hat = var
        else:
            y_hat = var

        plot_fit(x, y, y_hat, logx=not args.unlogx, logy=not args.unlogy,
                 hexbin=not args.scatter, xlabel=args.x_unit,
                 ylabel=args.y_unit, xlim=xlim, ylim=ylim, outfile=args.outfile)
    else:
        scatter(x, y, logx=not args.unlogx, logy=not args.unlogy,
                hexbin=not args.scatter, xlabel=args.x_unit,
                ylabel=args.y_unit, xlim=xlim, ylim=ylim, outfile=args.outfile)
