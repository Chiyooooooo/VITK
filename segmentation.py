import itk
import logging

def segment_tumor(image):
    logging.info("Starting tumor segmentation")
    otsu_filter = itk.OtsuThresholdImageFilter.New(Input=image)
    otsu_filter.Update()
    threshold_value = otsu_filter.GetThreshold()
    logging.info(f"Otsu threshold value: {threshold_value}")

    binary_threshold = itk.BinaryThresholdImageFilter.New(Input=image)
    binary_threshold.SetLowerThreshold(threshold_value)
    binary_threshold.SetUpperThreshold(itk.NumericTraits[itk.F].max())
    binary_threshold.SetInsideValue(1)
    binary_threshold.SetOutsideValue(0)
    binary_threshold.Update()

    segmented_image = binary_threshold.GetOutput()
    
    # clean up 
    median_filter = itk.MedianImageFilter.New(Input=segmented_image)
    median_filter.SetRadius(5)
    median_filter.Update()
    
    logging.info("Tumor segmentation completed")
    return median_filter.GetOutput()

def calculate_tumor_difference(segmented1, segmented2):
    logging.info("Calculating tumor difference")
    subtract_filter = itk.SubtractImageFilter.New(Input1=segmented1, Input2=segmented2)
    subtract_filter.Update()
    difference = subtract_filter.GetOutput()

    difference_array = itk.GetArrayFromImage(difference)
    num_diff_pixels = (difference_array != 0).sum()
    total_pixels = difference_array.size
    percentage_diff = (num_diff_pixels / total_pixels) * 100
    
    logging.info(f"Difference in pixels: {num_diff_pixels}")
    logging.info(f"Percentage difference: {percentage_diff:.2f}%")

    return difference
