import itk
import vtk
import logging
from align import load_scan, register_images
from segmentation import segment_tumor, calculate_tumor_difference
from visualization import visualize_tumor_changes

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logging.info("Starting the tumor evolution study")

    scan1_path = 'Data/case6_gre1.nrrd'
    scan2_path = 'Data/case6_gre2.nrrd'

    scan1 = load_scan(scan1_path)
    scan2 = load_scan(scan2_path)

    registered_scan2 = register_images(scan1, scan2)

    segmented_tumor1 = segment_tumor(scan1)
    segmented_tumor2 = segment_tumor(registered_scan2)

    tumor_difference = calculate_tumor_difference(segmented_tumor1, segmented_tumor2)

    visualize_tumor_changes(tumor_difference)

    logging.info("Tumor evolution study completed")

if __name__ == "__main__":
    main()
