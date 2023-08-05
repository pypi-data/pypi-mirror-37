from matplotlib import pyplot as plt

from autolens import conf
from autolens.plotting import plotter_tools

def plot_grid(grid, xmin=None, xmax=None, ymin=None, ymax=None,
              figsize=(12, 8), pointsize=3, xyticksize=16,
              title='Grid', titlesize=16, xlabelsize=16, ylabelsize=16,
              output_path=None, output_format='show', output_filename='grid'):

    plt.figure(figsize=figsize)
    plt.scatter(y=grid[:, 0], x=grid[:, 1], s=pointsize, marker='.')
    plotter_tools.set_title(title=title, titlesize=titlesize)
    plt.ylabel('y (arcsec)', fontsize=xlabelsize)
    plt.xlabel('x (arcsec)', fontsize=ylabelsize)
    plt.tick_params(labelsize=xyticksize)
    if xmin is not None and xmax is not None and ymin is not None and ymax is not None:
        plt.axis([xmin, xmax, ymin, ymax])
    plotter_tools.output_array(None, False, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot=False)

def plot_image(image, mask=None, positions=None, grid=None, as_subplot=False,
               units='arcsec', kpc_per_arcsec=None,
               xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
               figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
               title='Observed Image', titlesize=16, xlabelsize=16, ylabelsize=16,
               output_path=None, output_format='show', output_filename='observed_image'):

    if positions is not None:
        positions = list(map(lambda pos: image.grid_arc_seconds_to_grid_pixels(grid_arc_seconds=pos), positions))

    plotter_tools.plot_array(image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh, linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(image.shape, units, kpc_per_arcsec, image.xticks, image.yticks, xlabelsize,
                                          ylabelsize, xyticksize)

    # TODO : if you use set_colorbar and plt.scatter the scatter plot doesnt show...default to removing colorbar now

    if mask is None:
        plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.plot_mask(mask)
    plotter_tools.plot_points(positions)
    plotter_tools.plot_grid(grid)
    plotter_tools.output_array(image, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)

def plot_noise_map(noise_map, mask=None, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Noise-Map', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='noise_map'):


    plotter_tools.plot_array(noise_map, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh, linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(noise_map.shape, units, kpc_per_arcsec, noise_map.xticks, noise_map.yticks,
                                          xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.plot_mask(mask)
    plotter_tools.output_array(noise_map, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)

def plot_psf(psf, as_subplot=False,
             units='arcsec', kpc_per_arcsec=None,
             xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
             figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
             title='PSF', titlesize=16, xlabelsize=16, ylabelsize=16,
             output_path=None, output_format='show', output_filename='psf'):

    plotter_tools.plot_array(psf, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh, linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(psf.shape, units, kpc_per_arcsec, psf.xticks, psf.yticks,
                                          xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(psf, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)

def plot_signal_to_noise_map(signal_to_noise_map, mask=None, as_subplot=False,
                             units='arcsec', kpc_per_arcsec=None,
                             xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                             figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                             title='Noise-Map', titlesize=16, xlabelsize=16, ylabelsize=16,
                             output_path=None, output_format='show', output_filename='signal_to_noise_map'):


    plotter_tools.plot_array(signal_to_noise_map, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(signal_to_noise_map.shape, units, kpc_per_arcsec,
                                          signal_to_noise_map.xticks, signal_to_noise_map.yticks,
                                          xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.plot_mask(mask)
    plotter_tools.output_array(signal_to_noise_map, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)

def plot_intensities(intensities, as_subplot=False,
                     units='arcsec', kpc_per_arcsec=None,
                     xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                     figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                     title='Intensities', titlesize=16, xlabelsize=16, ylabelsize=16,
                     output_path=None, output_format='show', output_filename='intensities'):

    plotter_tools.plot_array(intensities, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(intensities.shape, units, kpc_per_arcsec, intensities.xticks,
                                          intensities.yticks,
                                          xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(intensities, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)


def plot_surface_density(surface_density, as_subplot=False,
                         units='arcsec', kpc_per_arcsec=None,
                         xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                         figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                         title='Surface Density', titlesize=16, xlabelsize=16, ylabelsize=16,
                         output_path=None, output_format='show', output_filename='surface_density'):
    plotter_tools.plot_array(surface_density, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(surface_density.shape, units, kpc_per_arcsec, surface_density.xticks,
                                          surface_density.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(surface_density, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)


def plot_potential(potential, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Potential', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='potential'):
    plotter_tools.plot_array(potential, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(potential.shape, units, kpc_per_arcsec, potential.xticks, potential.yticks,
                                          xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(potential, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)


def plot_deflections_y(deflections_y, as_subplot=False,
                       units='arcsec', kpc_per_arcsec=None,
                       xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                       figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                       title='Deflections (y)', titlesize=16, xlabelsize=16, ylabelsize=16,
                       output_path=None, output_format='show', output_filename='deflections_y'):
    plotter_tools.plot_array(deflections_y, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(deflections_y.shape, units, kpc_per_arcsec, deflections_y.xticks,
                                          deflections_y.yticks,
                                          xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(deflections_y, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)


def plot_deflections_x(deflections_x, as_subplot=False,
                       units='arcsec', kpc_per_arcsec=None,
                       xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                       figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                       title='Deflections (x)', titlesize=16, xlabelsize=16, ylabelsize=16,
                       output_path=None, output_format='show', output_filename='deflections_x'):

    plotter_tools.plot_array(deflections_x, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(deflections_x.shape, units, kpc_per_arcsec, deflections_x.xticks,
                                          deflections_x.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(deflections_x, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)


def plot_image_plane_image(image_plane_image, mask=None, positions=None, grid=None, as_subplot=False,
                           units='arcsec', kpc_per_arcsec=None,
                           xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                           figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                           title='Image-Plane Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                           output_path=None, output_format='show', output_filename='plane_image_plane_image'):

    if positions is not None:
        positions = list(map(lambda pos: image_plane_image.grid_arc_seconds_to_grid_pixels(grid_arc_seconds=pos),
                             positions))

    plotter_tools.plot_array(image_plane_image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min,
                             linthresh, linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(image_plane_image.shape, units, kpc_per_arcsec, image_plane_image.xticks,
                                          image_plane_image.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.plot_points(positions)
    plotter_tools.plot_mask(mask)
    plotter_tools.plot_grid(grid)
    plotter_tools.output_array(image_plane_image, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)

def plot_plane_image(plane_image, positions=None, plot_grid=False, as_subplot=False,
                     units='arcsec', kpc_per_arcsec=None,
                     xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                     figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                     title='Plane Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                     output_path=None, output_format='show', output_filename='plane_image'):

    if positions is not None:
        positions = list(map(lambda pos: plane_image.grid_arc_seconds_to_grid_pixels(grid_arc_seconds=pos),
                             positions))

    plotter_tools.plot_array(plane_image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min,
                             linthresh, linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(plane_image.shape, units, kpc_per_arcsec, plane_image.xticks, plane_image.yticks,
                                          xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.plot_points(positions)
    if plot_grid:
        plotter_tools.plot_grid(plane_image.grid)
    plotter_tools.output_array(plane_image, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)

def plot_model_image(model_image, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Model Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='model_image'):

    plotter_tools.plot_array(model_image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(model_image.shape, units, kpc_per_arcsec, model_image.xticks, 
                                          model_image.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(model_image, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)

def plot_residuals(residuals, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Residuals', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='residuals'):

    plotter_tools.plot_array(residuals, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(residuals.shape, units, kpc_per_arcsec, residuals.xticks, residuals.yticks,
                                          xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(residuals, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)
    
def plot_chi_squareds(chi_squareds, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Chi-Squareds', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='chi_squareds'):

    plotter_tools.plot_array(chi_squareds, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(chi_squareds.shape, units, kpc_per_arcsec, chi_squareds.xticks, 
                                          chi_squareds.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(chi_squareds, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)

def plot_contributions(contributions, as_subplot=False,
                     units='arcsec', kpc_per_arcsec=None,
                     xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                     figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                     title='Scaled Model Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                     output_path=None, output_format='show', output_filename='contributions'):

    plotter_tools.plot_array(contributions, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(contributions.shape, units, kpc_per_arcsec, contributions.xticks,
                                          contributions.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(contributions, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)

def plot_scaled_model_image(scaled_model_image, as_subplot=False,
                     units='arcsec', kpc_per_arcsec=None,
                     xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                     figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                     title='Scaled Model Image', titlesize=16, xlabelsize=16, ylabelsize=16,
                     output_path=None, output_format='show', output_filename='scaled_model_image'):

    plotter_tools.plot_array(scaled_model_image, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(scaled_model_image.shape, units, kpc_per_arcsec, scaled_model_image.xticks,
                                          scaled_model_image.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(scaled_model_image, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)


def plot_scaled_residuals(scaled_residuals, as_subplot=False,
                   units='arcsec', kpc_per_arcsec=None,
                   xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                   figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                   title='Scaled Residuals', titlesize=16, xlabelsize=16, ylabelsize=16,
                   output_path=None, output_format='show', output_filename='scaled_residuals'):

    plotter_tools.plot_array(scaled_residuals, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(scaled_residuals.shape, units, kpc_per_arcsec, scaled_residuals.xticks, 
                                          scaled_residuals.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(scaled_residuals, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)


def plot_scaled_chi_squareds(scaled_chi_squareds, as_subplot=False,
                      units='arcsec', kpc_per_arcsec=None,
                      xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                      figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                      title='Scaled Chi-Squareds', titlesize=16, xlabelsize=16, ylabelsize=16,
                      output_path=None, output_format='show', output_filename='scaled_chi_squareds'):

    plotter_tools.plot_array(scaled_chi_squareds, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(scaled_chi_squareds.shape, units, kpc_per_arcsec, scaled_chi_squareds.xticks,
                                          scaled_chi_squareds.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(scaled_chi_squareds, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)
    
def plot_scaled_noise_map(scaled_noise_map, as_subplot=False,
                      units='arcsec', kpc_per_arcsec=None,
                      xyticksize=16, norm='linear', norm_min=None, norm_max=None, linthresh=0.05, linscale=0.01,
                      figsize=(7, 7), aspect='equal', cmap='jet', cb_ticksize=16,
                      title='Scaled Noise Map', titlesize=16, xlabelsize=16, ylabelsize=16,
                      output_path=None, output_format='show', output_filename='scaled_noise_map'):

    plotter_tools.plot_array(scaled_noise_map, as_subplot, figsize, aspect, cmap, norm, norm_max, norm_min, linthresh,
                             linscale)
    plotter_tools.set_title(title, titlesize)
    plotter_tools.set_xy_labels_and_ticks(scaled_noise_map.shape, units, kpc_per_arcsec, scaled_noise_map.xticks,
                                          scaled_noise_map.yticks, xlabelsize, ylabelsize, xyticksize)
    plotter_tools.set_colorbar(cb_ticksize)
    plotter_tools.output_array(scaled_noise_map, as_subplot, output_path, output_filename, output_format)
    plotter_tools.plot_close(as_subplot)