def planck(ncolors=256):
    from matplotlib.colors import LinearSegmentedColormap as cm
    """
        Returns a color map similar to the one used for the "Planck CMB Map".
        Parameters
        ----------
        ncolors : int, *optional*
            Number of color segments (default: 256).
        Returns
        -------
        cmap : matplotlib.colors.LinearSegmentedColormap instance
            Linear segmented color map.
    """
    segmentdata = {"red":   [(0.0, 0.00, 0.00), (0.1, 0.00, 0.00),
                             (0.2, 0.00, 0.00), (0.3, 0.00, 0.00),
                             (0.4, 0.00, 0.00), (0.5, 1.00, 1.00),
                             (0.6, 1.00, 1.00), (0.7, 1.00, 1.00),
                             (0.8, 0.83, 0.83), (0.9, 0.67, 0.67),
                             (1.0, 0.50, 0.50)],
                   "green": [(0.0, 0.00, 0.00), (0.1, 0.00, 0.00),
                             (0.2, 0.00, 0.00), (0.3, 0.30, 0.30),
                             (0.4, 0.70, 0.70), (0.5, 1.00, 1.00),
                             (0.6, 0.70, 0.70), (0.7, 0.30, 0.30),
                             (0.8, 0.00, 0.00), (0.9, 0.00, 0.00),
                             (1.0, 0.00, 0.00)],
                   "blue":  [(0.0, 0.50, 0.50), (0.1, 0.67, 0.67),
                             (0.2, 0.83, 0.83), (0.3, 1.00, 1.00),
                             (0.4, 1.00, 1.00), (0.5, 1.00, 1.00),
                             (0.6, 0.00, 0.00), (0.7, 0.00, 0.00),
                             (0.8, 0.00, 0.00), (0.9, 0.00, 0.00),
                             (1.0, 0.00, 0.00)]}

    return cm("Planck-like", segmentdata, N=int(ncolors), gamma=1.0)
