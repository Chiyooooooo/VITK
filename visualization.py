import vtk
from vtk.util import numpy_support
import itk
import logging

def itk_to_vtk_image(itk_image):
    logging.info("Converting ITK image to VTK image")
    numpy_array = itk.GetArrayFromImage(itk_image)
    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(numpy_array.shape[::-1])
    vtk_image.SetSpacing(itk_image.GetSpacing())
    vtk_image.SetOrigin(itk_image.GetOrigin())
    
    flatten_array = numpy_array.ravel()
    vtk_array = numpy_support.numpy_to_vtk(num_array=flatten_array, deep=True, array_type=vtk.VTK_FLOAT)
    
    vtk_image.GetPointData().SetScalars(vtk_array)
    return vtk_image

def visualize_tumor_changes(difference_image):
    logging.info("Starting tumor change visualization")
    vtk_image = itk_to_vtk_image(difference_image)
    
    volume = vtk.vtkVolume()
    volume_mapper = vtk.vtkSmartVolumeMapper()
    volume_mapper.SetInputData(vtk_image)
    
    volume_property = vtk.vtkVolumeProperty()
    
    color_func = vtk.vtkColorTransferFunction()
    color_func.AddRGBPoint(0, 0.0, 0.0, 0.0)  # Black for no difference
    color_func.AddRGBPoint(1, 0.0, 0.0, 1.0)  # Blue for differences
    
    opacity_func = vtk.vtkPiecewiseFunction()
    opacity_func.AddPoint(0, 0.0)  # Fully transparent for no difference
    opacity_func.AddPoint(1, 1.0)  # Fully opaque for differences
    
    volume_property.SetColor(color_func)
    volume_property.SetScalarOpacity(opacity_func)
    volume_property.ShadeOn()
    
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)
    
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    
    renderer.AddVolume(volume)
    renderer.SetBackground(0.1, 0.1, 0.1)  # Dark gray background
    renderer.ResetCamera()
    
    render_window.Render()
    render_window_interactor.Start()
    logging.info("Tumor change visualization completed")
