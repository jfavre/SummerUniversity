# script-version: 2.0
import paraview
paraview.compatibility.major = 6
paraview.compatibility.minor = 0

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

ImageResolution = [1024,1024]

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.Set(
  ViewSize = ImageResolution,
  CenterOfRotation = [0.5, 0.5, 0.0],
  CameraPosition =   [0.5, 0.5, 2.5],
  CameraFocalPoint = [0.5, 0.5, 0.0],
  CameraFocalDisk = 1.0,
  CameraParallelScale = 0.6326744773387929,
  OrientationAxesVisibility = 0,
  )

reader = TrivialProducer(registrationName='grid')

contour1 = Contour(registrationName='Contour1', Input=reader)
contour1.Set(
  ContourBy = ['POINTS', 'temperature'],
  ComputeNormals = 0,
  Isosurfaces = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
  PointMergeMethod = 'Uniform Binning',
  )

processIds1 = ProcessIds(registrationName='ProcessIds1', Input=contour1)
processIds1Display = Show(processIds1)

ColorBy(processIds1Display , ['POINTS', 'PointProcessIds'])

readerDisplay = Show(reader, renderView1, 'UniformGridRepresentation')

# trace defaults for the display properties.
readerDisplay.Set(
  Representation = 'Outline',
  ColorArrayName = ['POINTS', ''],
  )
pointProcessIdsLUT = GetColorTransferFunction('PointProcessIds')
pointProcessIdsLUTColorBar = GetScalarBar(pointProcessIdsLUT, renderView1)
pointProcessIdsLUTColorBar.Set(
    WindowLocation='Upper Right Corner',
    Title='PointProcessIds',
)

# set color bar visibility
pointProcessIdsLUTColorBar.Visibility = 1
processIds1Display.SetScalarBarVisibility(renderView1, True)

pNG1 = CreateExtractor('PNG', renderView1, registrationName='PNG1')
pNG1.Trigger = 'TimeStep'
pNG1.Trigger.Frequency = 10000
pNG1.Writer.FileName = 'Temperature-Catalyst.{timestep:05d}{camera}.png'
pNG1.Writer.ImageResolution = ImageResolution
pNG1.Writer.Format = 'PNG'

vTP1 = CreateExtractor('VTPD', reader, registrationName='VTPD1')
vTP1.Trigger = 'TimeStep'
vTP1.Trigger.Frequency = 40000
vTP1.Writer.FileName = 'dataset_{timestep:06d}.vtpd'

# Catalyst options
from paraview import catalyst
options = catalyst.Options()
options.GlobalTrigger = 'Time Step'
options.CatalystLiveTrigger = 'Time Step'
options.ExtractsOutputDirectory = 'datasets'
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    from paraview.simple import SaveExtractsUsingCatalystOptions
    # Code for non in-situ environments; if executing in post-processing
    # i.e. non-Catalyst mode, let's generate extracts using Catalyst options
    SaveExtractsUsingCatalystOptions(options)
