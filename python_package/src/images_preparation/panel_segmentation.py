import cv2
import os
import numpy as np
from scipy import ndimage
from skimage.measure import label, regionprops
from images_preparation.utils import save_images, COMICS_PAGES_DIR, PANELS_DIR

IMAGE_TYPE = "_##_panel_"


def cut_pages(
    input_directory: str = COMICS_PAGES_DIR, output_directory: str = PANELS_DIR
):
    pages = os.listdir(input_directory)
    for page in pages:
        panels = process_page(f"{input_directory}/{page}")
        save_images(panels, output_directory, page[:-4], IMAGE_TYPE)


def process_page(image_path: str) -> list[np.ndarray]:
    src_img = cv2.imread(image_path)
    edges_img = apply_canny_edge_detection(src_img)
    regions = extract_regions(edges_img)
    panels_bbox = refine_regions_into_panels(regions, src_img.shape)
    panels = cut_panels_from_source(src_img, panels_bbox)

    return panels


def apply_canny_edge_detection(src_img: np.ndarray) -> np.ndarray:
    # Transform to grayscale
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    # Applying Canny edge detection
    edges = cv2.Canny(gray_img, 50, 150, apertureSize=3)

    # TODO see if dilation (edge thickening) is need (maybe condition on image size ?)
    # thick_edges = cv2.dilate(edges)

    return edges


def extract_regions(edges_img: np.ndarray) -> list:
    # Filling hole part surounded by white
    segmentation = ndimage.binary_fill_holes(edges_img).astype(np.uint8)
    # Labelling each white patch
    labels = label(segmentation)
    # return a list of labeled images properties
    return regionprops(labels)


def is_bboxes_overlaping(a: tuple, b: tuple) -> bool:
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def merge_bboxes(a: tuple, b: tuple) -> tuple:
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def refine_regions_into_panels(regions: list, img_shape: tuple) -> list[tuple]:
    panels_bbox = []
    for region in regions:
        for i, panel in enumerate(panels_bbox):
            if is_bboxes_overlaping(region.bbox, panel):
                panels_bbox[i] = merge_bboxes(panel, region.bbox)
                break
        else:
            panels_bbox.append(region.bbox)

    return remove_small_panels(panels_bbox, img_shape)


def remove_small_panels(panels_bbox: list[tuple], img_shape: tuple) -> list[tuple]:
    for i, panel in reversed(list(enumerate(panels_bbox))):
        img_area = (panel[2] - panel[0]) * (panel[3] - panel[1])
        if img_area < 0.01 * img_shape[0] * img_shape[1]:
            del panels_bbox[i]
    return panels_bbox


def cut_panels_from_source(
    src_img: np.ndarray, panels_bbox: list[tuple]
) -> list[np.ndarray]:
    panels = []
    for bbox in panels_bbox:
        panel = src_img[bbox[0] : bbox[2], bbox[1] : bbox[3]]
        panels.append(panel)

    return panels
