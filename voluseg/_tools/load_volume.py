def load_volume(fullname_ext):
    '''load volume based on input name and extension'''

    import h5py
    import nibabel
    import numpy as np
    try:
        from skimage.external import tifffile
    except:
        import tifffile
    try:
        import PIL
        import pyklb
    except:
        pass

    try:
        ext = '.'+fullname_ext.split('.', 1)[1]

        if ('.tif' in ext) or ('.tiff' in ext):
            try:
                volume = tifffile.imread(fullname_ext)
            except:
                img = PIL.Image.open(fullname_ext)
                volume = []
                for i in range(img.n_frames):
                    img.seek(i)
                    volume.append(np.array(img).T)
                volume = np.array(volume)
        elif ('.h5' in ext) or ('.hdf5' in ext):
            with h5py.File(fullname_ext, 'r') as file_handle:
                volume = file_handle[list(file_handle.keys())[0]][()]
        elif ('.klb' in ext):
            volume = pyklb.readfull(fullname_ext)
            volume = volume.transpose(0, 2, 1)
        elif ('.nii' in ext) or ('.nii.gz' in ext):
            volume = nibabel.load(fullname_ext).get_data()
        else:
            raise Exception('unknown extension.')

        return volume

    except:
        return None
