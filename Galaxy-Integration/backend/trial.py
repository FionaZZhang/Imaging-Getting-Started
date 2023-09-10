from bioblend.galaxy import GalaxyInstance
import time

galaxy_url = "https://usegalaxy.org.au/"
galaxy_api_key = "38ae4d7d23fc78506d217aee88282462"
gi = GalaxyInstance(url=galaxy_url, key=galaxy_api_key)

input_image_path = '../../input.tif'
history_name = 'HistogramNormalisationInput'

history = gi.histories.create_history(name=history_name)

input_dataset = gi.tools.upload_file(input_image_path, history['id'])
input_id = input_dataset['outputs'][0]['id']
input_dataset = gi.datasets.show_dataset(input_dataset['outputs'][0]['id'])

print("input_dataset")
while input_dataset['state'] != 'ok':
    time.sleep(5)
    input_dataset = gi.datasets.show_dataset(input_dataset['dataset_id'])
    print(input_dataset['state'])

workflow = gi.workflows.show_workflow('b7acc99e5fb755e8')
datamap = {
    '0': {
        'src': 'hda',
        'id': input_id,
    }
}
hist = gi.workflows.invoke_workflow(workflow['id'], inputs=datamap, history_id=history['id'])
hist = gi.histories.show_history(hist['history_id'])

print('hist')
while hist['state'] != 'ok':
    time.sleep(10)  # Wait for 10 seconds before checking again
    hist = gi.histories.show_history(hist['id'])
    print(hist['state'])

datasetinfo = gi.datasets.show_dataset(hist['state_ids']['ok'][-1])
gi.datasets.download_dataset(dataset_id=datasetinfo['id'], file_path="outputs/histogram_equilization.tiff", use_default_filename=False)





def hdab_counts(input_image_path, output_folder):

    # Read the input image
    full_image = AICSImage(input_image_path)
    full_image = full_image.get_image_dask_data("YXS", T=0, C=0, Z=0)
    YSize, XSize, CSize = full_image.shape
    splitInto = 8
    xTileSize = int(XSize / splitInto)
    yTileSize = int(YSize / splitInto)

    results = []

    for x in range(0, splitInto):
        for y in range(0, splitInto):
            roi_y0 = y * yTileSize
            roi_x0 = x * xTileSize
            roi_y1 = roi_y0 + yTileSize
            roi_x1 = roi_x0 + xTileSize
            im = full_image[roi_y0:roi_y1, roi_x0:roi_x1]

            total_cells, pos_cells = processImage(im)

            results.append((x, y, total_cells, pos_cells))

    result_str = ""
    for tile_x, tile_y, total_cells, pos_cells in results:
        result_str += f"Tile {tile_x * splitInto + tile_y}: Total Cells = {total_cells}, Positive Cells = {pos_cells}\n"

    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Write the result string to a text file in the output folder
    output_file_path = os.path.join(output_folder, "hdab_counts.txt")
    with open(output_file_path, "w") as output_file:
        output_file.write(result_str)

    response_data = {
        'output_path': output_file_path
    }

    return response_data

def processImage(im):
    # create psuedo fluoro
    im2 = skimage.color.rgb2gray(im)
    im2 = skimage.util.invert(im2)

    # define model
    model = StarDist2D.from_pretrained('2D_versatile_fluo')

    # predict on big region
    try:
        labels, _ = model.predict_instances_big(im2, axes='YX', block_size=2048, min_overlap=128, context=128,
                                            show_progress=True)

        # colour deconvolve
        im3 = skimage.color.rgb2hed(im)
        dab = im3[:, :, 2]
        blue = im3[:, :, 0]

        # measure intensities on colours
        res = skimage.measure.regionprops(labels, intensity_image=dab)
        blueres = skimage.measure.regionprops(labels, intensity_image=blue)

        # filter for blue signal
        x = [d for d, b in zip(res, blueres) if d.area > 200 and b.intensity_mean > 0.020]
        totalCells = len(x)

        p = [d for d, b in zip(res, blueres) if d.area > 200 and d.intensity_mean > 0.02 and b.intensity_mean > 0.020]
        posCells = len(p)
    except:
        #if stardist fails
        print("STARDIST FAILURE CHECK THIS FILE")
        totalCells = 0
        posCells = 0

    return totalCells, posCells