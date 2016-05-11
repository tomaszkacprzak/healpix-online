import sys, os, glob, warnings, logging, argparse, yaml
import healpy as hp
import pylab as pl
import numpy as np
from skimage.io import imread, imsave
from astropy.io import fits

warnings.simplefilter("ignore"); warnings.simplefilter(action = "ignore", category = FutureWarning)
logger = logging.getLogger("apert_mass")
if len(logger.handlers)==0:
    log_formatter = logging.Formatter("%(asctime)s %(levelname).3s %(filename).10s   %(message)s", datefmt="%y-%m-%d %H:%M:%S")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    logger.setLevel(logging.INFO)

def make_homepage(config):

    with open('html_template.html') as fo:
        template=fo.read()

    index_insert = template.find('$INSERT_MAP_CODE_HERE$')
    html_start = template[:index_insert]
    html_end = template[index_insert+23:]

    list_codes = ''
    for id_tag, map_info in enumerate(config['healpix_maps']):

        dirname_hips = os.path.join(os.path.basename(map_info['filename']) + 'HiPS')

        # // var hipsDir1 = hipsDir.concat('/kappaE');

        code_str1 = """var hipsDir%d = hipsDir.concat('/%s');\n""" % (id_tag, dirname_hips)
        code_str2 = """var survey%d = aladin.createImageSurvey('%s', '%s', hipsDir%d, 'equatorial', 3, {imgFormat: 'png'});\n""" % (id_tag, map_info['tag'], map_info['tag'], id_tag)
        list_codes += code_str1+code_str2
        # var hipsDir1 = hipsDir.concat('/kappaE');
        # var hipsDir2 = hipsDir.concat('/kappaB');
        # var survey1 = aladin.createImageSurvey('KappaE', 'KappaE', hipsDir1, 'equatorial', 3, {imgFormat: 'png'})
        # var survey2 = aladin.createImageSurvey('KappaB', 'KappaB', hipsDir2, 'equatorial', 3, {imgFormat: 'png'})

    final_html = html_start + list_codes + html_end

    filename_html_final = os.path.join(config['results_dirname'], 'index.html')
    with open(filename_html_final, 'w') as fo:
        fo.write(final_html)
    logger.info('wrote %s' % filename_html_final)

def make_homepage_double(config):

    with open('html_template_double.html') as fo:
        template=fo.read()

    index_insert = template.find('$INSERT_MAP_CODE_HERE$')
    html_start = template[:index_insert]
    html_end = template[index_insert+23:]

    list_codes = ''
    for id_tag, map_info in enumerate(config['healpix_maps']):

        dirname_hips = os.path.join(os.path.basename(map_info['filename']) + 'HiPS')

        # // var hipsDir1 = hipsDir.concat('/kappaE');

        code_str1 = """var hipsDir%d = hipsDir.concat('/%s');\n""" % (id_tag, dirname_hips)
        code_str2 = """var survey%d = aladin.createImageSurvey('%s', '%s', hipsDir%d, 'equatorial', 3, {imgFormat: 'png'});\n""" % (id_tag, map_info['tag'], map_info['tag'], id_tag)
        list_codes += code_str1+code_str2
        # var hipsDir1 = hipsDir.concat('/kappaE');
        # var hipsDir2 = hipsDir.concat('/kappaB');
        # var survey1 = aladin.createImageSurvey('KappaE', 'KappaE', hipsDir1, 'equatorial', 3, {imgFormat: 'png'})
        # var survey2 = aladin.createImageSurvey('KappaB', 'KappaB', hipsDir2, 'equatorial', 3, {imgFormat: 'png'})

    template2 = html_start + list_codes + html_end

    index_insert = template2.find('$INSERT_MAP_CODE_HERE_2$')
    html_start = template2[:index_insert]
    html_end = template2[index_insert+25:]

    list_codes = ''
    for id_tag, map_info in enumerate(config['healpix_maps']):

        dirname_hips = os.path.join(os.path.basename(map_info['filename']) + 'HiPS')

        # // var hipsDir1 = hipsDir.concat('/kappaE');

        code_str1 = """var hipsDir%d = hipsDir.concat('/%s');\n""" % (id_tag, dirname_hips)
        code_str2 = """var survey%d = aladin.createImageSurvey('%s', '%s', hipsDir%d, 'equatorial', 3, {imgFormat: 'png'});\n""" % (id_tag, map_info['tag'], map_info['tag'], id_tag)
        list_codes += code_str1+code_str2
        # var hipsDir1 = hipsDir.concat('/kappaE');
        # var hipsDir2 = hipsDir.concat('/kappaB');
        # var survey1 = aladin.createImageSurvey('KappaE', 'KappaE', hipsDir1, 'equatorial', 3, {imgFormat: 'png'})
        # var survey2 = aladin.createImageSurvey('KappaB', 'KappaB', hipsDir2, 'equatorial', 3, {imgFormat: 'png'})

    final_html = html_start + list_codes + html_end


    filename_html_final = os.path.join(config['results_dirname'], 'index_double.html')
    with open(filename_html_final, 'w') as fo:
        fo.write(final_html)
    logger.info('wrote %s' % filename_html_final)

def make_single_map(map_info, results_dirname, filename_mask=None):
# make_single_map(dirname_output=config['results_dirname'], filename_healpix = map_info['filename_normed'], tag = map_info['tag'], cmap_name = map_info['cmap'])

    filename_healpix = map_info['filename_normed']
    dirname_output = results_dirname
    tag = map_info['tag']
    cmap_name = map_info['cmap']

    if cmap_name=='planck-like':
        import cmap_planck
        cmap = cmap_planck.planck()
    else:
        cmap = pl.cm.get_cmap(cmap_name)

    dirname_hips = os.path.join(dirname_output, os.path.basename(filename_healpix) + 'HiPS')

    filename_aladin_out = "aladin_cmd_out.txt"
    logger.info('getting limits')
    cmd = """java  -Xmx16000m  -jar  AladinBeta.jar  -hipsgen  in=%s out=%s > %s """ % (filename_healpix, dirname_hips, filename_aladin_out)
    logger.info(cmd)
    os.system(cmd)

    with open(filename_aladin_out) as fo:
        aladin_out = fo.read()

    id_start=aladin_out.find('Pixel dynamic range=')
    id_end  =aladin_out.find('cut=[')
    range_str=aladin_out[id_start:id_end]
    id_start =range_str.find('[')
    id_end =range_str.find(']')
    range_str=range_str[id_start+1:id_end]
    pix_min =  float(range_str.split('..')[0])
    pix_max =  float(range_str.split('..')[1])

    logger.info('running hipsgen with right limits')
    cmd = """java  -Xmx16000m  -jar  AladinBeta.jar  -hipsgen  in=%s out=%s pixelCut="%2.5f %2.5f" > %s """ % (filename_healpix, dirname_hips, pix_min, pix_max, filename_aladin_out)
    logger.info(cmd)
    os.system(cmd)

    def add_color(filename_fits):

        img_bw=fits.getdata(filename_fits)
        img_color = cmap(img_bw)
        filename_color = filename_fits.replace('.fits', '.png').replace('.pngHiPS', '.fitsHiPS')
        imsave(filename_color, np.flipud(img_color))
        logger.debug('saved %s' % filename_color)

    logger.info('adding colours')
    add_color( os.path.join(dirname_hips, 'Norder3', 'Allsky.fits') )
    filelist = glob.glob( os.path.join(dirname_hips, 'Norder3', 'Dir0', '*fits')  )
    for fn in filelist:
        add_color(fn)

def save_normalised_map(results_dirname, filename_healpix, clim=[1,1], filename_mask=None):

        def normalise(x):
            import scipy.stats
            clip_res = scipy.stats.sigmaclip(x, low=clim[0], high=clim[1])
            min_val = clip_res.clipped.min()
            max_val = clip_res.clipped.max()
            y = x - min_val
            z = y / (max_val-min_val)
            z[z<0]=0
            z[z>1]=1
            return z

        healpix_map = hp.read_map(filename_healpix, verbose=False)
        logger.info('read %s' % filename_healpix)
        if filename_mask!=None:
            hpmask = hp.read_map(filename_mask, verbose=False)
            logger.info('read %s' % filename_mask)
            select = hpmask>0.99
            logger.info('applied mask')

        logger.info('read %s' % filename_healpix)
        healpix_map[select] = normalise(healpix_map[select])
        healpix_map[~select]=healpix_map[select].min()
        # pl.hist(healpix_map[select], bins=200);
        # pl.yscale('log')
        # pl.title(filename_healpix);
        # pl.show()
        # import pdb; pdb.set_trace()

        filename_normed = os.path.join(results_dirname, os.path.basename(filename_healpix))
        hp.write_map(filename_normed, healpix_map, coord='C', fits_IDL=False)
        return filename_normed

def make_all_maps(config):



    if os.path.isdir(config['results_dirname']):
        logger.info('using existing dir %s' % config['results_dirname'])
    else:
        os.mkdir(config['results_dirname'])
        logger.info('making new dir %s' % config['results_dirname'])

    for map_info in config['healpix_maps']:

        if 'filename_mask' in map_info:
            filename_mask = map_info['filename_mask']
        else:
            filename_mask = None

        map_info['filename_normed'] = save_normalised_map(config['results_dirname'], map_info['filename'], clim=map_info['clim'], filename_mask=filename_mask)
        map_info['dirname_hips'] = os.path.join(config['results_dirname'], os.path.basename(map_info['filename_normed']) + 'HiPS')

        if os.path.isdir(map_info['dirname_hips']):
            logger.info('map %s exists in %s' % (map_info['filename_normed'], map_info['dirname_hips']))
        else:
            logger.info('making map %s' % map_info['tag'])
            # make_single_map(dirname_output=config['results_dirname'], filename_healpix = map_info['filename_normed'], tag = map_info['tag'], cmap_name = map_info['cmap'])
            make_single_map(map_info, results_dirname=config['results_dirname'],  filename_mask=filename_mask)


def main():

    description = 'make-healpix-online, see config.yaml for description of input'
    parser = argparse.ArgumentParser(description=description, add_help=True)
    parser.add_argument('-v', '--verbosity', type=int, action='store', default=2, choices=(0, 1, 2, 3 ), help='integer verbosity level: min=0, max=3 [default=2]')
    parser.add_argument('-c', '--config', type=str, default='config.yaml' , action='store', help='filename of file containing config')
    args = parser.parse_args()
    logging_levels = { 0: logging.CRITICAL, 1: logging.WARNING, 2: logging.INFO, 3: logging.DEBUG }
    logging_level = logging_levels[args.verbosity]
    logger.setLevel(logging_level)
    config = yaml.load(open(args.config)); logger.info('opened %s' % (args.config))

    make_all_maps(config)
    make_homepage(config)
    make_homepage_double(config)

main()
