import itk
import logging

def load_scan(file_path):
    logging.info(f"Loading scan from {file_path}")
    image = itk.imread(file_path, itk.F)
    return image

def register_images(fixed_image, moving_image):
    logging.info("Starting image registration")
    Dimension = 3

    FixedImageType = itk.Image[itk.F, Dimension]
    MovingImageType = itk.Image[itk.F, Dimension]

    TransformType = itk.VersorRigid3DTransform[itk.D]

    OptimizerType = itk.RegularStepGradientDescentOptimizerv4[itk.D]
    optimizer = OptimizerType.New()
    optimizer.SetLearningRate(1)
    optimizer.SetMinimumStepLength(0.001)
    optimizer.SetRelaxationFactor(0.5)
    optimizer.SetNumberOfIterations(200)

    MetricType = itk.MattesMutualInformationImageToImageMetricv4[FixedImageType, MovingImageType]
    metric = MetricType.New()
    metric.SetNumberOfHistogramBins(50)
    metric.SetUseMovingImageGradientFilter(False)
    metric.SetUseFixedImageGradientFilter(False)

    RegistrationType = itk.ImageRegistrationMethodv4[FixedImageType, MovingImageType]
    registration = RegistrationType.New()

    initialTransform = TransformType.New()
    initialTransform.SetIdentity()

    initializer = itk.CenteredTransformInitializer[TransformType, FixedImageType, MovingImageType].New()
    initializer.SetTransform(initialTransform)
    initializer.SetFixedImage(fixed_image)
    initializer.SetMovingImage(moving_image)
    initializer.MomentsOn()
    initializer.InitializeTransform()

    registration.SetFixedImage(fixed_image)
    registration.SetMovingImage(moving_image)
    registration.SetMetric(metric)
    registration.SetOptimizer(optimizer)
    registration.SetInitialTransform(initialTransform)

    # Multi-resolution setup
    registration.SetNumberOfLevels(3)
    registration.SetSmoothingSigmasPerLevel([4, 2, 1])
    registration.SetShrinkFactorsPerLevel([4, 2, 1])

    registration.Update()

    resampler = itk.ResampleImageFilter.New(Input=moving_image)
    resampler.SetTransform(registration.GetTransform())
    resampler.SetUseReferenceImage(True)
    resampler.SetReferenceImage(fixed_image)
    resampler.SetDefaultPixelValue(0)
    resampler.Update()

    registered_image = resampler.GetOutput()
    
    logging.info("Image registration completed")
    return registered_image
