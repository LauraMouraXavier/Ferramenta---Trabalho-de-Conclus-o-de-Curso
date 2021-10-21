"""
Model exported as python.
Name : Produtividade_cod
Group : TCC
With QGIS : 31401
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterEnum
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterField
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFileDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsExpression
import processing


class Produtividade_cod(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterEnum('Culturaa', 'Cultura', options=['Milho','Trigo','Girassol'], allowMultiple=False, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab02', 'Insira a B02 (Azul)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab03', 'Insira a B03 (Verde)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab04', 'Insira a B04 (Vermelho)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab05', 'Insira a B05 (RE 1)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab06', 'Insira a B06 (RE 2)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab07', 'Insira a B07 (RE 3)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab08', 'Insira a B08 (IVP)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab08a', 'Insira a B08A (RE 4)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab011', 'Insira a B11 (SWIR1)', defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterLayer('insiraab012', 'Insira a B12 (SWIR2)', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('insiraocontornodarea', 'Contorno da Área', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorLayer('validao', 'Insira uma camada de pontos para validação', optional=True, types=[QgsProcessing.TypeVectorPoint], defaultValue=None))
        self.addParameter(QgsProcessingParameterField('campoparavalidao', 'Indique a coluna de produtividade medida', optional=True, type=QgsProcessingParameterField.Numeric, parentLayerParameterName='validao', allowMultiple=False, defaultValue=''))
        self.addParameter(QgsProcessingParameterRasterDestination('SuperfcieDeProdutividade', 'Superfície de Produtividade', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFileDestination('EstatsticaDaProdutividade', 'Estatística da Produtividade', fileFilter='Arquivos HTML (*.html *.HTML)', createByDefault=True, defaultValue=''))
        self.addParameter(QgsProcessingParameterFeatureSink('ErroDePreviso', 'Erro de Previsão', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(83, model_feedback)
        results = {}
        outputs = {}

        # R - B05
        alg_params = {
            'INPUT': parameters['insiraab05'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB05'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # R - B07
        alg_params = {
            'INPUT': parameters['insiraab07'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB07'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # P - B07
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB07']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB07'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # R - B06
        alg_params = {
            'INPUT': parameters['insiraab06'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB06'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # R - B02
        alg_params = {
            'INPUT': parameters['insiraab02'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB02'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # R - B04
        alg_params = {
            'INPUT': parameters['insiraab04'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB04'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # P - B04
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB04']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB04'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # R - B11
        alg_params = {
            'INPUT': parameters['insiraab011'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB11'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # NormB04
        alg_params = {
            'INPUT': outputs['RB04']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb04'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # R - B12
        alg_params = {
            'INPUT': parameters['insiraab012'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB12'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # NormB05
        alg_params = {
            'INPUT': outputs['RB05']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb05'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # NormB12
        alg_params = {
            'INPUT': outputs['RB12']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb12'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # NormB07
        alg_params = {
            'INPUT': outputs['RB07']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb07'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # R - B08A
        alg_params = {
            'INPUT': parameters['insiraab08a'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB08a'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # P - B05
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB05']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB05'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # R - B08
        alg_params = {
            'INPUT': parameters['insiraab08'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB08'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # NormB02
        alg_params = {
            'INPUT': outputs['RB02']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb02'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # NormB06
        alg_params = {
            'INPUT': outputs['RB06']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb06'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # P - B06
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB06']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB06'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # P - B12
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB12']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB12'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # R - B03
        alg_params = {
            'INPUT': parameters['insiraab03'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 0,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['RB03'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # NormB08A
        alg_params = {
            'INPUT': outputs['RB08a']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb08a'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # P - B02
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB02']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB02'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # NormB08
        alg_params = {
            'INPUT': outputs['RB08']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb08'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # P - B11
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB11']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB11'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # P - B03
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB03']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB03'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # P - B08A
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB08a']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB08a'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # NormB11
        alg_params = {
            'INPUT': outputs['RB11']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb11'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # NormB03
        alg_params = {
            'INPUT': outputs['RB03']['OUTPUT'],
            'RANGE_MAX': 1,
            'RANGE_MIN': -1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Normb03'] = processing.run('saga:rasternormalisation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # P - B08
        alg_params = {
            'FIELD_NAME': 'VALUE',
            'INPUT_RASTER': outputs['RB08']['OUTPUT'],
            'RASTER_BAND': 1,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['PB08'] = processing.run('native:pixelstopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Unir B02+B03
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['PB02']['OUTPUT'],
            'JOIN': outputs['PB03']['OUTPUT'],
            'JOIN_FIELDS': None,
            'METHOD': 0,
            'PREDICATE': 2,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirB02b03'] = processing.run('qgis:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Unir B02+03+B04
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UnirB02b03']['OUTPUT'],
            'JOIN': outputs['PB04']['OUTPUT'],
            'JOIN_FIELDS': None,
            'METHOD': 0,
            'PREDICATE': 2,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirB0203b04'] = processing.run('qgis:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Unir B02+03+B04+B05
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UnirB0203b04']['OUTPUT'],
            'JOIN': outputs['PB05']['OUTPUT'],
            'JOIN_FIELDS': None,
            'METHOD': 0,
            'PREDICATE': 2,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirB0203b04b05'] = processing.run('qgis:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Unir B02+03+B04+B05+B06
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UnirB0203b04b05']['OUTPUT'],
            'JOIN': outputs['PB06']['OUTPUT'],
            'JOIN_FIELDS': None,
            'METHOD': 0,
            'PREDICATE': 2,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirB0203b04b05b06'] = processing.run('qgis:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Unir B02+03+B04+B05+B06+B07
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UnirB0203b04b05b06']['OUTPUT'],
            'JOIN': outputs['PB07']['OUTPUT'],
            'JOIN_FIELDS': None,
            'METHOD': 0,
            'PREDICATE': 2,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirB0203b04b05b06b07'] = processing.run('qgis:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Unir B02+03+B04+B05+B06+B07+B08
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UnirB0203b04b05b06b07']['OUTPUT'],
            'JOIN': outputs['PB08']['OUTPUT'],
            'JOIN_FIELDS': None,
            'METHOD': 0,
            'PREDICATE': 2,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirB0203b04b05b06b07b08'] = processing.run('qgis:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Unir B02+03+B04+B05+B06+B07+B08+B08A
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UnirB0203b04b05b06b07b08']['OUTPUT'],
            'JOIN': outputs['PB08a']['OUTPUT'],
            'JOIN_FIELDS': None,
            'METHOD': 0,
            'PREDICATE': 2,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirB0203b04b05b06b07b08b08a'] = processing.run('qgis:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Unir B02+03+B04+B05+B06+B07+B08+B08A+B11
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UnirB0203b04b05b06b07b08b08a']['OUTPUT'],
            'JOIN': outputs['PB11']['OUTPUT'],
            'JOIN_FIELDS': None,
            'METHOD': 0,
            'PREDICATE': 2,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirB0203b04b05b06b07b08b08ab11'] = processing.run('qgis:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Unir B02+03+B04+B05+B06+B07+B08+B08A+B11+B12
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'INPUT': outputs['UnirB0203b04b05b06b07b08b08ab11']['OUTPUT'],
            'JOIN': outputs['PB12']['OUTPUT'],
            'JOIN_FIELDS': None,
            'METHOD': 0,
            'PREDICATE': 2,
            'PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnirB0203b04b05b06b07b08b08ab11b12'] = processing.run('qgis:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
        if feedback.isCanceled():
            return {}

        # C - NDVI
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'ndvi',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': '( \"VALUE_7\" - \"VALUE_3\" )/( \"VALUE_7\" + \"VALUE_3\" )',
            'INPUT': outputs['UnirB0203b04b05b06b07b08b08ab11b12']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CNdvi'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # C - GNDVI
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'gndvi',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': '( \"VALUE_7\" - \"VALUE_2\" )/( \"VALUE_7\" + \"VALUE_2\" )',
            'INPUT': outputs['CNdvi']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CGndvi'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # C - VARI
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'vari',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': '( \"VALUE_2\" - \"VALUE_3\" )/( \"VALUE_2\" + \"VALUE_3\" - \"VALUE\" )',
            'INPUT': outputs['CGndvi']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CVari'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
        if feedback.isCanceled():
            return {}

        # E - campos
        alg_params = {
            'FIELDS_MAPPING': [{'expression': '\"VALUE\"','length': 20,'name': 'B02','precision': 8,'type': 6},{'expression': '\"VALUE_2\"','length': 20,'name': 'B03','precision': 8,'type': 6},{'expression': '\"VALUE_3\"','length': 20,'name': 'B04','precision': 8,'type': 6},{'expression': '\"VALUE_4\"','length': 20,'name': 'B05','precision': 8,'type': 6},{'expression': '\"VALUE_5\"','length': 20,'name': 'B06','precision': 8,'type': 6},{'expression': '\"VALUE_6\"','length': 20,'name': 'B07','precision': 8,'type': 6},{'expression': '\"VALUE_7\"','length': 20,'name': 'B08','precision': 8,'type': 6},{'expression': '\"VALUE_8\"','length': 20,'name': 'B8A','precision': 8,'type': 6},{'expression': '\"VALUE_9\"','length': 20,'name': 'B11','precision': 8,'type': 6},{'expression': '\"VALUE_10\"','length': 20,'name': 'B12','precision': 8,'type': 6},{'expression': '\"ndvi\"','length': 10,'name': 'ndvi','precision': 5,'type': 6},{'expression': '\"gndvi\"','length': 10,'name': 'gndvi','precision': 5,'type': 6},{'expression': '\"vari\"','length': 10,'name': 'vari','precision': 5,'type': 6}],
            'INPUT': outputs['CVari']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ECampos'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(43)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo - Cultura
        alg_params = {
            'FIELD_LENGTH': 15,
            'FIELD_NAME': 'cultura',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 2,
            'FORMULA': 'CASE \nWHEN @Culturaa = \'0\' THEN \'milho\'\nWHEN @Culturaa = \'1\' THEN \'trigo\'\nWHEN @Culturaa = \'2\' THEN \'girassol\' END',
            'INPUT': outputs['ECampos']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampoCultura'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        # Eno1
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno1',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.269696*\"B02\"+0.12389*\"B03\"+0.21787*\"B04\"+7.821163*\"B05\"+0.292960*\"B06\"-0.171659*\"B07\"-0.369680*\"B08\"-0.30183*\"B08A\"+0.23069*\"B11\"+0.332267*\"B12\"-4.23696*\"ndvi\"+4.58038*\"gndvi\"-0.23204*\"vari\"-6.38630) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,3.50879*\"B02\"+3.27560*\"B03\"+3.59707*\"B04\"+4.35135*\"B05\"+2.56718*\"B06\"+6.14078*\"B07\"+3.47414*\"B08\"+2.52739*\"B08A\"+1.45889*\"B11\"+1.59149*\"B12\"-2.18953*\"ndvi\"-3.21957*\"gndvi\"+3.39240*\"vari\"+0.88977)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-5.17466*\"B02\"-24.75716*\"B03\"-12.04560*\"B04\"+46.48136*\"B05\"-32.22727*\"B06\"+49.38880*\"B07\"+44.863977*\"B08\"+46.78115*\"B08A\"+3.90765*\"B11\"-5.36316*\"B12\"+30.63061*\"ndvi\"+42.06062*\"gndvi\"+23.95966*\"vari\"+0.18784)\r\nEND',
            'INPUT': outputs['CalculadoraDeCampoCultura']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno1'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}

        # Eno2
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno2',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.10443*\"B02\"+0.84054*\"B03\"+0.474688*\"B04\"+0.41413*\"B05\"+0.31192*\"B06\"-8.41076*\"B07\"+0.449367*\"B08\"-0.124615*\"B08A\"+0.136218*\"B11\"+0.233943*\"B12\"-0.24576*\"ndvi\"-0.35152*\"gndvi\"+2.33751*\"vari\"-21.20167) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-4.76092*\"B02\"-3.4832*\"B03\"-5.68393*\"B04\"+7.05650*\"B05\"-2.38549*\"B06\"+1.16403*\"B07\"+5.93333*\"B08\"+5.10777*\"B08A\"-1.60215*\"B11\"-3.16655*\"B12\"+6.23305*\"ndvi\"+5.83260*\"gndvi\"+2.42643*\"vari\"+1.10574)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.12740*\"B02\"-2.67116*\"B03\"-1.06481*\"B04\"+6.31513*\"B05\"-4.04208*\"B06\"+7.62422*\"B07\"+6.32515*\"B08\"+6.81297*\"B08A\"+0.47597*\"B11\"+0.12951*\"B12\"+3.53748*\"ndvi\"+5.24302*\"gndvi\"+2.17915*\"vari\"+0.89087) \r\nEND',
            'INPUT': outputs['Eno1']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno2'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # Eno3
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno3',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.18564*\"B02\"+0.18232*\"B03\"+0.336434*\"B04\"-0.17644*\"B05\"-0.335302*\"B06\"+0.13870*\"B07\"-0.15579*\"B08\"-0.34664*\"B08A\"+0.477602*\"B11\"+0.22226*\"B12\"+6.43927*\"ndvi\"-0.10057*\"gndvi\"+0.18326*\"vari\"+16.51137) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,2.59543*\"B02\"+2.16249*\"B03\"+2.52140*\"B04\"+2.18040*\"B05\"+1.84032*\"B06\"+3.40354*\"B07\"+1.41390*\"B08\"+1.25627*\"B08A\"+1.82217*\"B11\"+1.47976*\"B12\"-2.22937*\"ndvi\"-2.31248*\"gndvi\"+1.08015*\"vari\"+0.93324)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-5.34829*\"B02\"-14.41599*\"B03\"-8.60469*\"B04\"+25.95697*\"B05\"-17.33504*\"B06\"+27.41662*\"B07\"+25.85279*\"B08\"+26.49298*\"B08A\"+2.16554*\"B11\"-3.16769*\"B12\"+19.10077*\"ndvi\"+23.31156*\"gndvi\"+15.89832*\"vari\"+0.57882) \r\nEND',
            'INPUT': outputs['Eno2']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno3'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}

        # Eno4
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno4',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,7.21130*\"B02\"+5.65043*\"B03\"+9.68735*\"B04\"+2.28421*\"B05\"+0.131217*\"B06\"-1.85523*\"B07\"-7.03917*\"B08\"-4.87689*\"B08A\"+9.24442*\"B11\"+9.541003*\"B12\"-4.36293*\"ndvi\"-0.89624*\"gndvi\"-8.62369*\"vari\"-2.29924) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-6.73177*\"B02\"-5.35936*\"B03\"-6.30219*\"B04\"+9.45637*\"B05\"-5.66157*\"B06\"+1.08524*\"B07\"+7.45705*\"B08\"+6.76853*\"B08A\"-4.86015*\"B11\"-5.04263*\"B12\"+7.58578*\"ndvi\"+8.00850*\"gndvi\"+5.17721*\"vari\"+1.08353)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.89465*\"B02\"-9.87844*\"B03\"-3.52624*\"B04\"+21.43860*\"B05\"-13.34123*\"B06\"+23.55040*\"B07\"+20.39985*\"B08\"+22.53675*\"B08A\"+3.67951*\"B11\"-1.15485*\"B12\"+13.43308*\"ndvi\"+18.56269*\"gndvi\"+9.53777*\"vari\"+0.62897) \r\nEND',
            'INPUT': outputs['Eno3']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno4'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(48)
        if feedback.isCanceled():
            return {}

        # Eno5
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno5',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.38312*\"B02\"+6.07141*\"B03\"+0.178897*\"B04\"-0.13748*\"B05\"+0.428081*\"B06\"-8.31758*\"B07\"-0.11538*\"B08\"-0.53671*\"B08A\"-0.15776*\"B11\"-0.01003*\"B12\"-3.20499*\"ndvi\"+2.85798*\"gndvi\"+0.12972*\"vari\"-22.13402) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-1.97423*\"B02\"+2.00533*\"B03\"+2.45164*\"B04\"+4.39861*\"B05\"+0.86095*\"B06\"+4.39719*\"B07\"+3.16191*\"B08\"+2.63134*\"B08A\"-0.14573*\"B11\"+1.39320*\"B12\"-1.14606*\"ndvi\"-1.658273*\"gndvi\"+3.10651*\"vari\"+0.90780)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-2.23844*\"B02\"-5.37664*\"B03\"-2.55812*\"B04\"+8.79424*\"B05\"-7.66559*\"B06\"+7.99665*\"B07\"+7.40629*\"B08\"+8.26272*\"B08A\"+0.89538*\"B11\"-1.50264*\"B12\"+6.58383*\"ndvi\"+8.42799*\"gndvi\"+6.01985*\"vari\"+0.81878) \r\nEND',
            'INPUT': outputs['Eno4']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno5'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(49)
        if feedback.isCanceled():
            return {}

        # Eno6
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno6',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.29034*\"B02\"+0.41055*\"B03\"-0.43533*\"B04\"-0.49892*\"B05\"+8.22423*\"B06\"-0.01121*\"B07\"+0.01317*\"B08\"-0.37088*\"B08A\"-0.02590*\"B11\"+0.012603*\"B12\"+3.61893*\"ndvi\"-0.06971*\"gndvi\"+0.285776*\"vari\"-15.87173) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,0.19142*\"B02\"+0.32116*\"B03\"+0.71710*\"B04\"+0.10504*\"B05\"+0.95326*\"B06\"-0.75433*\"B07\"-0.79826*\"B08\"-0.97479*\"B08A\"+1.81792*\"B11\"+2.33615*\"B12\"-0.52236*\"ndvi\"-0.46863*\"gndvi\"-1.16678*\"vari\"+0.98404)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-4.48430*\"B02\"-22.65196*\"B03\"-11.78930*\"B04\"+57.37191*\"B05\"-28.58504*\"B06\"+62.34578*\"B07\"+58.78663*\"B08\"+61.09623*\"B08A\"+8.09439*\"B11\"-5.24842*\"B12\"+34.80750*\"ndvi\"+45.41039*\"gndvi\"+25.071739*\"vari\"+0.22270) \r\nEND',
            'INPUT': outputs['Eno5']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno6'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(50)
        if feedback.isCanceled():
            return {}

        # Eno7
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno7',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-4.99235*\"B02\"+0.571226*\"B03\"+0.50723*\"B04\"+0.50673*\"B05\"+0.620933*\"B06\"-0.99977*\"B07\"-0.29881*\"B08\"+0.23568*\"B08A\"-8.62160*\"B11\"-0.78755*\"B12\"+9.97673*\"ndvi\"+5.78526*\"gndvi\"-0.32717*\"vari\"-43.66526) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,0.32220*\"B02\"-0.39759*\"B03\"+0.82667*\"B04\"+4.61448*\"B05\"-0.72148*\"B06\"+2.49658*\"B07\"+3.31024*\"B08\"-3.07326*\"B08A\"-1.12394*\"B11\"-0.37760*\"B12\"-0.30099*\"ndvi\"-0.06682*\"gndvi\"+3.20875*\"vari\"+0.92954)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-9.89686*\"B02\"-37.83653*\"B03\"-19.69073*\"B04\"+68.21941*\"B05\"-48.21099*\"B06\"+72.32647*\"B07\"+64.03276*\"B08\"+68.93998*\"B08A\"+7.83187*\"B11\"-6.80026*\"B12\"+46.53327*\"ndvi\"+63.55857*\"gndvi\"+38.57586*\"vari\"-0.23940) \r\nEND',
            'INPUT': outputs['Eno6']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno7'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(51)
        if feedback.isCanceled():
            return {}

        # Eno8
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno8',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.46415*\"B02\"+0.32472*\"B03\"+0.25826*\"B04\"+0.10528*\"B05\"+0.19197*\"B06\"+0.119004*\"B07\"-0.10851*\"B08\"-8.40655*\"B08A\"+0.33378*\"B11\"+0.175980*\"B12\"-0.134118*\"ndvi\"-0.14015*\"gndvi\"+0.10625*\"vari\"-11.09114) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,0.98578*\"B02\"+0.66142*\"B03\"+1.09678*\"B04\"-1.46631*\"B05\"+0.86095*\"B06\"-1.56311*\"B07\"-1.07397*\"B08\"-1.34292*\"B08A\"+0.81679*\"B11\"+0.72276*\"B12\"-0.80923*\"ndvi\"-1.17459*\"gndvi\"-1.91132*\"vari\"+1.02692)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-7.16942*\"B02\"-26.54006*\"B03\"-13.66558*\"B04\"+48.054435*\"B05\"-33.43423*\"B06\"+51.07081*\"B07\"+46.38037*\"B08\"+49.07949*\"B08A\"+5.12060*\"B11\"-5.64924*\"B12\"+33.52957*\"ndvi\"+44.27275*\"gndvi\"+26.41715*\"vari\"+0.15099) \r\nEND',
            'INPUT': outputs['Eno7']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno8'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(52)
        if feedback.isCanceled():
            return {}

        # Eno9
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno9',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-1.69094*\"B02\"+0.45465*\"B03\"-0.35471*\"B04\"-8.38138*\"B05\"+0.014664*\"B06\"-0.908246*\"B07\"-0.60038*\"B08\"+0.38922*\"B08A\"-0.019509*\"B11\"+6.082953*\"B12\"+0.18470*\"ndvi\"-7.45741*\"gndvi\"+7.40332*\"vari\"+18.05207) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,13.82520*\"B02\"+12.38905*\"B03\"+17.69891*\"B04\"-9.30192*\"B05\"+14.61691*\"B06\"+1.78021*\"B07\"-10.90302*\"B08\"-9.56307*\"B08A\"+15.25606*\"B11\"+17.90823*\"B12\"-17.06504*\"ndvi\"-16.03924*\"gndvi\"-8.87573*\"vari\"+0.71887)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-6.00481*\"B02\"-23.37804*\"B03\"-12.20460*\"B04\"+40.59528*\"B05\"-29.88012*\"B06\"+42.81524*\"B07\"+37.71415*\"B08\"+41.33647*\"B08A\"+3.80490*\"B11\"-5.13238*\"B12\"+28.68611*\"ndvi\"+38.26272*\"gndvi\"+23.10513*\"vari\"+0.25255) \r\nEND',
            'INPUT': outputs['Eno8']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno9'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(53)
        if feedback.isCanceled():
            return {}

        # Eno10
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno10',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.612848*\"B02\"+3.74518*\"B03\"-0.347391*\"B04\"-0.365818*\"B05\"-0.18754*\"B06\"-0.28979*\"B07\"-0.15768*\"B08\"+0.982759*\"B08A\"-1.35528*\"B11\"+0.41373*\"B12\"+0.27571*\"ndvi\"-1.87745*\"gndvi\"-8.93078*\"vari\"-3.40273) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,26.49656*\"B02\"+25.98294*\"B03\"+31.57700*\"B04\"+7.69198*\"B05\"+25.73948*\"B06\"+9.96233*\"B07\"-3.34309*\"B08\"-3.62540*\"B08A\"+25.41609*\"B11\"+31.55474*\"B12\"-27.82545*\"ndvi\"-25.73760*\"gndvi\"-7.83820*\"vari\"+0.59673)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,2.91764*\"B02\"-4.00238*\"B03\"-0.27557*\"B04\"+19.20746*\"B05\"-6.34003*\"B06\"+21.07955*\"B07\"+20.26041*\"B08\"+20.65802*\"B08A\"+4.290778*\"B11\"-0.41311*\"B12\"+7.86351*\"ndvi\"+12.46983*\"gndvi\"+3.54263*\"vari\"+0.77342) \r\nEND',
            'INPUT': outputs['Eno9']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno10'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(54)
        if feedback.isCanceled():
            return {}

        # Eno11
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno11',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.89312*\"B02\"-5.82249*\"B03\"-0.38664*\"B04\"-0.115218*\"B05\"-0.23114*\"B06\"+3.98988*\"B07\"-0.38667*\"B08\"-1.50168*\"B08A\"+3.57661*\"B11\"-8.09858*\"B12\"+0.194881*\"ndvi\"-3.53877*\"gndvi\"+0.28662*\"vari\"-21.31023) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,11.31270*\"B02\"+10.01976*\"B03\"+15.29340*\"B04\"-3.19608*\"B05\"+12.22978*\"B06\"+5.00238*\"B07\"-5.38838*\"B08\"-5.02979*\"B08A\"+11.16262*\"B11\"+13.80487*\"B12\"-13.70746*\"ndvi\"-12.51250*\"gndvi\"-4.22216*\"vari\"+0.69042)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,2.08310*\"B02\"-4.04433*\"B03\"+0.80010*\"B04\"+7.99873*\"B05\"-7.33255*\"B06\"+8.56566*\"B07\"+6.079165*\"B08\"+7.71841*\"B08A\"+1.94945*\"B11\"+1.01741*\"B12\"+2.92966*\"ndvi\"+7.52287*\"gndvi\"+1.21830*\"vari\"+0.78029) \r\nEND',
            'INPUT': outputs['Eno10']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno11'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(55)
        if feedback.isCanceled():
            return {}

        # Eno12
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno12',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.36929*\"B02\"+0.34069*\"B03\"+4.53101*\"B04\"-0.13864*\"B05\"+5.46364*\"B06\"+0.14107*\"B07\"+0.12897*\"B08\"+0.214382*\"B08A\"-0.17139*\"B11\"+3.891412*\"B12\"-6.66987*\"ndvi\"-0.26188*\"gndvi\"+0.28582*\"vari\"-12.93236) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,2.08746*\"B02\"+1.79935*\"B03\"+3.46971*\"B04\"+6.51999*\"B05\"+1.01098*\"B06\"+5.71868*\"B07\"+4.46957*\"B08\"+4.55249*\"B08A\"-0.90719*\"B11\"+0.75778*\"B12\"-1.86371*\"ndvi\"-1.51698*\"gndvi\"+4.30809*\"vari\"+0.86872)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-3.76212*\"B02\"-16.76257*\"B03\"-8.35923*\"B04\"+35.34316*\"B05\"-21.05538*\"B06\"+37.49082*\"B07\"+34.92868*\"B08\"+36.51904*\"B08A\"+4.94940*\"B11\"-3.64313*\"B12\"+22.73779*\"ndvi\"+30.25144*\"gndvi\"+17.38772*\"vari\"+0.44665) \r\nEND',
            'INPUT': outputs['Eno11']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno12'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(56)
        if feedback.isCanceled():
            return {}

        # Eno13
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno13',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.36699*\"B02\"+0.35739*\"B03\"+5.37728*\"B04\"-0.20198*\"B05\"+0.11923*\"B06\"+0.23604*\"B07\"+9.53078*\"B08\"+0.93828*\"B08A\"-0.94600*\"B11\"-6.96843*\"B12\"-8.98925*\"ndvi\"-0.30948*\"gndvi\"+0.29147*\"vari\"-12.50210) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,3.99194*\"B02\"+3.99356*\"B03\"+0.77214*\"B04\"-4.43556*\"B05\"+1.29338*\"B06\"-0.29248*\"B07\"-1.54148*\"B08\"-1.43477*\"B08A\"+0.64256*\"B11\"-0.75528*\"B12\"-1.59849*\"ndvi\"-4.14597*\"gndvi\"-3.01404*\"vari\"+1.08305)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,5.15622*\"B02\"+9.62662*\"B03\"+7.03864*\"B04\"-14.14579*\"B05\"+12.87474*\"B06\"-14.76200*\"B07\"-14.75168*\"B08\"-15.64240*\"B08A\"+1.190362*\"B11\"+4.45722*\"B12\"-12.20546*\"ndvi\"-14.19497*\"gndvi\"-10.84262*\"vari\"+1.25674) \r\nEND',
            'INPUT': outputs['Eno12']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno13'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(57)
        if feedback.isCanceled():
            return {}

        # Eno14
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno14',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.339200*\"B02\"+0.010040*\"B03\"-0.01183*\"B04\"-0.025490*\"B05\"+0.011912*\"B06\"-0.011097*\"B07\"-0.011417*\"B08\"+0.014458*\"B08A\"-0.02736*\"B11\"+0.012024*\"B12\"+0.9470668*\"ndvi\"+3.14612*\"gndvi\"-0.80330*\"vari\"+53.73523) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,0.93787*\"B02\"+0.87012*\"B03\"+1.10643*\"B04\"+2.01866*\"B05\"+0.28870*\"B06\"+2.95747*\"B07\"+0.77943*\"B08\"+1.35966*\"B08A\"+0.11499*\"B11\"+0.30079*\"B12\"-0.60638*\"ndvi\"-1.12345*\"gndvi\"+2.21424*\"vari\"+0.95121)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-1.82732*\"B02\"-16.39686*\"B03\"-6.26179*\"B04\"+28.54613*\"B05\"-22.03747*\"B06\"+30.72779*\"B07\"+26.05184*\"B08\"+28.29853*\"B08A\"+4.95714*\"B11\"-1.72902*\"B12\"+18.66438*\"ndvi\"+27.50417*\"gndvi\"+14.74616*\"vari\"+0.40932) \r\nEND',
            'INPUT': outputs['Eno13']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno14'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(58)
        if feedback.isCanceled():
            return {}

        # Eno15
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno15',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.65391*\"B02\"+0.206191*\"B03\"-6.84147*\"B04\"-4.45088*\"B05\"-0.116351*\"B06\"-0.109562*\"B07\"-0.19747*\"B08\"+3.51546*\"B08A\"-0.1763304*\"B11\"-8.02962*\"B12\"+0.110591*\"ndvi\"-4.76206*\"gndvi\"-1.82373*\"vari\"-8.20892) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,4.64037*\"B02\"+5.24493*\"B03\"+0.67113*\"B04\"-6.55676*\"B05\"-1.33386*\"B06\"-4.34939*\"B07\"-2.17232*\"B08\"-2.71880*\"B08A\"-1.60832*\"B11\"-3.02215*\"B12\"-2.51541*\"ndvi\"-4.56461*\"gndvi\"-3.64281*\"vari\"+1.09331)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-2.62367*\"B02\"-15.31914*\"B03\"-6.65964*\"B04\"+20.80114*\"B05\"-20.43421*\"B06\"+22.53254*\"B07\"+18.03046*\"B08\"+20.16291*\"B08A\"+1.96466*\"B11\"-2.12335*\"B12\"+14.92985*\"ndvi\"+21.73591*\"gndvi\"+13.20459*\"vari\"+0.49045) \r\nEND',
            'INPUT': outputs['Eno14']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno15'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(59)
        if feedback.isCanceled():
            return {}

        # Eno16
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Eno16',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,0.188779*\"B02\"+0.186108*\"B03\"+0.600681*\"B04\"+0.22666*\"B05\"+0.103207*\"B06\"-0.242056*\"B07\"-0.354037*\"B08\"-0.43394*\"B08A\"+0.173119*\"B11\"+0.20241*\"B12\"+0.15748*\"ndvi\"+9.358786*\"gndvi\"+7.616870*\"vari\"-2.00425) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-4.29389*\"B02\"-4.13094*\"B03\"-3.55841*\"B04\"+7.59859*\"B05\"-3.11930*\"B06\"-0.39337*\"B07\"+5.36306*\"B08\"+4.64955*\"B08A\"-2.78407*\"B11\"-1.26942*\"B12\"+4.39520*\"ndvi\"+5.70901*\"gndvi\"+2.63515*\"vari\"+1.04643)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.51684*\"B02\"+0.93635*\"B03\"+0.45522*\"B04\"-4.66011*\"B05\"+0.85310*\"B06\"-5.26656*\"B07\"-4.26076*\"B08\"-4.86447*\"B08A\"-1.97470*\"B11\"-1.54917*\"B12\"-2.04833*\"ndvi\"-2.98645*\"gndvi\"-2.08050*\"vari\"+1.06002) \r\nEND',
            'INPUT': outputs['Eno15']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Eno16'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(60)
        if feedback.isCanceled():
            return {}

        # Ono1
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono1',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.18511*\"Eno1\"-0.16521*\"Eno2\"-0.49099*\"Eno3\"-7.84523*\"Eno4\"+0.23793*\"Eno5\"-0.33120*\"Eno6\"-0.425661*\"Eno7\"-9.16568*\"Eno8\"-0.101647*\"Eno9\"-0.314178*\"Eno10\"-0.790454*\"Eno11\"-3.05089*\"Eno12\"-1.89407*\"Eno13\"+4.89382*\"Eno14\"-0.407276*\"Eno15\"-0.13045*\"Eno16\"+0.759656) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.28250*\"Eno1\"-0.96902*\"Eno2\"-0.26550*\"Eno3\"-0.88187*\"Eno4\"-0.59423*\"Eno5\"-1.03846*\"Eno6\"-0.90409*\"Eno7\"-0.92984*\"Eno8\"-0.99195*\"Eno9\"-1.38168*\"Eno10\"-1.52445*\"Eno11\"-1.17399*\"Eno12\"-1.34479*\"Eno13\"-0.15480*\"Eno14\"-1.23360*\"Eno15\"-1.77827*\"Eno16\"+0.92228)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,0.33379*\"Eno1\"+0.08139*\"Eno2\"-0.57616*\"Eno3\"+0.08825*\"Eno4\"-0.04623*\"Eno5\"-0.44194*\"Eno6\"-0.55576*\"Eno7\"-0.09685*\"Eno8\"-0.09493*\"Eno9\"-0.06036*\"Eno10\"-0.01913*\"Eno11\"+0.37397*\"Eno12\"-0.21498*\"Eno13\"+0.37319*\"Eno14\"+0.01090*\"Eno15\"-7.72139*\"Eno16\"+0.02016) \r\nEND',
            'INPUT': outputs['Eno16']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono1'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(61)
        if feedback.isCanceled():
            return {}

        # Ono2
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono2',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.32045*\"Eno1\"-3.29241*\"Eno2\"-1.83172*\"Eno3\"-7.08936*\"Eno4\"-0.30976*\"Eno5\"-2.40597*\"Eno6\"-1.84074*\"Eno7\"-6.09815*\"Eno8\"-4.57826*\"Eno9\"-3.76290*\"Eno10\"-1.393967*\"Eno11\"-0.01056*\"Eno12\"-3.96276*\"Eno13\"-0.26755*\"Eno14\"-0.33294*\"Eno15\"-1.893807*\"Eno16\"-0.35158) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,0.13846*\"Eno1\"-0.17548*\"Eno2\"-0.31757*\"Eno3\"-0.20104*\"Eno4\"-0.09774*\"Eno5\"-0.46762*\"Eno6\"-0.11506*\"Eno7\"-0.67154*\"Eno8\"-0.43849*\"Eno9\"-0.40249*\"Eno10\"+0.03614*\"Eno11\"+0.22916*\"Eno12\"+0.02609*\"Eno13\"-0.40103*\"Eno14\"-0.72280*\"Eno15\"-0.19181*\"Eno16\"+0.53418)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.35040*\"Eno1\"-0.16220*\"Eno2\"-0.026779*\"Eno3\"-0.26388*\"Eno4\"-0.17928*\"Eno5\"-0.57439*\"Eno6\"-0.46290*\"Eno7\"-0.35493*\"Eno8\"-0.28859*\"Eno9\"-0.34511*\"Eno10\"-0.26879*\"Eno11\"-0.314567*\"Eno12\"-0.17323*\"Eno13\"-0.24746*\"Eno14\"-0.16843*\"Eno15\"-0.10968*\"Eno16\"+0.77371) \r\nEND',
            'INPUT': outputs['Ono1']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono2'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(62)
        if feedback.isCanceled():
            return {}

        # Ono3
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono3',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.11405*\"Eno1\"+1.58913*\"Eno2\"-1.21588*\"Eno3\"+0.39325*\"Eno4\"-0.223231*\"Eno5\"-0.202943*\"Eno6\"-9.969562*\"Eno7\"-0.57901*\"Eno8\"-0.252544*\"Eno9\"-9.51139*\"Eno10\"-3.47616*\"Eno11\"-2.79047*\"Eno12\"-6.72373*\"Eno13\"-6.00492*\"Eno14\"-0.11377*\"Eno15\"-6.73537*\"Eno16\"+0.81772) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-1.46773*\"Eno1\"-4.79867*\"Eno2\"-1.82592*\"Eno3\"-3.24700*\"Eno4\"-1.10610*\"Eno5\"-0.29878*\"Eno6\"-0.60584*\"Eno7\"-1.43851*\"Eno8\"-0.29715*\"Eno9\"-8.82314*\"Eno10\"-0.61799*\"Eno11\"-0.27729*\"Eno12\"-2.16039*\"Eno13\"-0.65112*\"Eno14\"-2.89526*\"Eno15\"-5.17304*\"Eno16\"+0.67840)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.80237*\"Eno1\"-0.31240*\"Eno2\"-0.55680*\"Eno3\"-0.47618*\"Eno4\"-0.70856*\"Eno5\"-0.478913*\"Eno6\"-0.01150*\"Eno7\"-0.01025*\"Eno8\"-0.940406*\"Eno9\"-6.43471*\"Eno10\"-3.11557*\"Eno11\"-0.578081*\"Eno12\"-0.20762*\"Eno13\"-0.635679*\"Eno14\"-0.80402*\"Eno15\"-0.37412*\"Eno16\"-0.13562) \r\nEND',
            'INPUT': outputs['Ono2']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono3'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(63)
        if feedback.isCanceled():
            return {}

        # Ono4
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono4',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.409066*\"Eno1\"-1.75249*\"Eno2\"-0.308810*\"Eno3\"-2.09240*\"Eno4\"-0.636804*\"Eno5\"-0.50588*\"Eno6\"-0.783493*\"Eno7\"-1.68995*\"Eno8\"-0.990775*\"Eno9\"-1.11955*\"Eno10\"-0.61544*\"Eno11\"-0.70422*\"Eno12\"-0.764725*\"Eno13\"-0.05531*\"Eno14\"-0.49259*\"Eno15\"-0.89407*\"Eno16\"-0.32485) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.00386*\"Eno1\"-0.24597*\"Eno2\"+0.29446*\"Eno3\"-0.13430*\"Eno4\"-0.42831*\"Eno5\"-1.29045*\"Eno6\"-0.12667*\"Eno7\"-1.61415*\"Eno8\"-5.46717*\"Eno9\"-3.72881*\"Eno10\"-2.55944*\"Eno11\"+0.32637*\"Eno12\"-1.42504*\"Eno13\"-0.29109*\"Eno14\"-1.71546*\"Eno15\"-0.00084*\"Eno16\"+0.67151)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.26443*\"Eno1\"-0.13993*\"Eno2\"-0.11198*\"Eno3\"-0.17828*\"Eno4\"-0.17031*\"Eno5\"-0.21709*\"Eno6\"-0.30544*\"Eno7\"-0.29154*\"Eno8\"-0.24838*\"Eno9\"-0.12682*\"Eno10\"-5.09599*\"Eno11\"-0.20148*\"Eno12\"-0.12464*\"Eno13\"-0.199605*\"Eno14\"-0.20938*\"Eno15\"-0.14725*\"Eno16\"+0.40009) \r\nEND',
            'INPUT': outputs['Ono3']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono4'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(64)
        if feedback.isCanceled():
            return {}

        # Ono5
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono5',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-4.49188*\"Eno1\"-7.10979*\"Eno2\"-3.27706*\"Eno3\"-8.48472*\"Eno4\"-0.28032*\"Eno5\"-3.40968*\"Eno6\"-6.04895*\"Eno7\"-6.947003*\"Eno8\"-6.65184*\"Eno9\"-7.14276*\"Eno10\"-4.38060*\"Eno11\"-4.78844*\"Eno12\"-6.56323*\"Eno13\"-1.15723*\"Eno14\"-6.18750*\"Eno15\"-6.27798*\"Eno16\"-0.179077) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.04815*\"Eno1\"-1.12690*\"Eno2\"-0.92091*\"Eno3\"-0.70821*\"Eno4\"-0.29816*\"Eno5\"-0.65367*\"Eno6\"-0.37502*\"Eno7\"-0.74244*\"Eno8\"+0.10285*\"Eno9\"-0.77795*\"Eno10\"-1.20252*\"Eno11\"-0.99272*\"Eno12\"-1.12741*\"Eno13\"-0.57433*\"Eno14\"-2.01205*\"Eno15\"-1.14897*\"Eno16\"+0.15139)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,0.02843*\"Eno1\"-3.06768*\"Eno2\"-0.19441*\"Eno3\"+0.06474*\"Eno4\"-6.45014*\"Eno5\"-0.00418*\"Eno6\"-0.56017*\"Eno7\"-0.17838*\"Eno8\"+0.03168*\"Eno9\"-0.34801*\"Eno10\"-0.16440*\"Eno11\"-0.24601*\"Eno12\"-0.16985*\"Eno13\"-0.37522*\"Eno14\"-2.57839*\"Eno15\"-9.43047*\"Eno16\"+0.15568) \r\nEND',
            'INPUT': outputs['Ono4']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono5'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(65)
        if feedback.isCanceled():
            return {}

        # Ono6
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono6',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.90206*\"Eno1\"-3.09819*\"Eno2\"-1.94909*\"Eno3\"-7.42499*\"Eno4\"-2.21522*\"Eno5\"-1.93814*\"Eno6\"-2.33633*\"Eno7\"-5.62737*\"Eno8\"-4.21203*\"Eno9\"-3.32839*\"Eno10\"-1.25086*\"Eno11\"-0.23752*\"Eno12\"-4.25266*\"Eno13\"-0.143389*\"Eno14\"-0.442057*\"Eno15\"-0.442057*\"Eno16\"-0.82504) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.70433*\"Eno1\"-5.20484*\"Eno2\"-1.02727*\"Eno3\"-4.99801*\"Eno4\"-0.77795*\"Eno5\"-0.83751*\"Eno6\"-0.12677*\"Eno7\"-2.11307*\"Eno8\"-9.19175*\"Eno9\"-0.45902*\"Eno10\"-0.18089*\"Eno11\"+0.97342*\"Eno12\"-3.33846*\"Eno13\"-0.97472*\"Eno14\"-3.67814*\"Eno15\"-6.13258*\"Eno16\"+0.69145)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.01143*\"Eno1\"-0.37532*\"Eno2\"-0.93102*\"Eno3\"-0.64897*\"Eno4\"-0.01134*\"Eno5\"-0.56862*\"Eno6\"-0.01799*\"Eno7\"-0.015611*\"Eno8\"-0.01465*\"Eno9\"+0.13129*\"Eno10\"+4.84411*\"Eno11\"-0.79826*\"Eno12\"-0.19007*\"Eno13\"-0.92095*\"Eno14\"-0.01257*\"Eno15\"-0.47730*\"Eno16\"-0.35949) \r\nEND',
            'INPUT': outputs['Ono5']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono6'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(66)
        if feedback.isCanceled():
            return {}

        # Ono7
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono7',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.608636*\"Eno1\"-0.16878*\"Eno2\"-1.886906*\"Eno3\"-5.290764*\"Eno4\"-2.41388*\"Eno5\"-2.54537*\"Eno6\"-3.572304*\"Eno7\"-1.644171*\"Eno8\"-0.58765*\"Eno9\"-1.88662*\"Eno10\"-1.522493*\"Eno11\"-2.14080*\"Eno12\"+0.190196*\"Eno13\"-0.828921*\"Eno14\"-4.01214*\"Eno15\"-0.46859*\"Eno16\"-0.51213)\r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.03423*\"Eno1\"-0.26303*\"Eno2\"+0.03944*\"Eno3\"-0.56205*\"Eno4\"-0.43698*\"Eno5\"-0.45704*\"Eno6\"-0.15974*\"Eno7\"+0.14845*\"Eno8\"-0.64817*\"Eno9\"-0.32725*\"Eno10\"+0.02982*\"Eno11\"-0.56960*\"Eno12\"-0.03010*\"Eno13\"-0.07961*\"Eno14\"-0.24855*\"Eno15\"-0.31781*\"Eno16\"+0.85695)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.31530*\"Eno1\"-0.16874*\"Eno2\"-0.13704*\"Eno3\"-0.21605*\"Eno4\"-0.20942*\"Eno5\"-0.26371*\"Eno6\"-0.36638*\"Eno7\"-0.35040*\"Eno8\"-0.29849*\"Eno9\"-0.155790*\"Eno10\"-6.55342*\"Eno11\"-0.248342*\"Eno12\"-0.14511*\"Eno13\"-0.24525*\"Eno14\"-0.25472*\"Eno15\"-0.19192*\"Eno16\"+0.39533) \r\nEND',
            'INPUT': outputs['Ono6']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono7'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(67)
        if feedback.isCanceled():
            return {}

        # Ono8
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono8',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-4.92427*\"Eno1\"-4.02299*\"Eno2\"-2.19345*\"Eno3\"-1.70447*\"Eno4\"-2.30321*\"Eno5\"-3.045072*\"Eno6\"-1.39276*\"Eno7\"-1.297637*\"Eno8\"-0.011551*\"Eno9\"-3.71237*\"Eno10\"-2.25324*\"Eno11\"+0.41079*\"Eno12\"-0.74877*\"Eno13\"-0.46744*\"Eno14\"-5.71283*\"Eno15\"-3.75109*\"Eno16\"+7.85151) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-3.21833*\"Eno1\"-2.31883*\"Eno2\"-3.95429*\"Eno3\"-2.79149*\"Eno4\"-3.61977*\"Eno5\"-2.62705*\"Eno6\"-3.80986*\"Eno7\"-0.42717*\"Eno8\"-3.63426*\"Eno9\"-3.51885*\"Eno10\"-8.09025*\"Eno11\"-7.51060*\"Eno12\"-2.89403*\"Eno13\"-2.98612*\"Eno14\"-6.82117*\"Eno15\"-4.57502*\"Eno16\"+0.58973)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.920449*\"Eno1\"-0.38429*\"Eno2\"-0.62446*\"Eno3\"-0.504702*\"Eno4\"-0.73311*\"Eno5\"-0.50183*\"Eno6\"-0.012845*\"Eno7\"-0.011237*\"Eno8\"-0.01053*\"Eno9\"-7.24528*\"Eno10\"-3.77545*\"Eno11\"-0.66616*\"Eno12\"-0.192064*\"Eno13\"-0.71007*\"Eno14\"-0.87068*\"Eno15\"-0.401238*\"Eno16\"-0.32304) \r\nEND',
            'INPUT': outputs['Ono7']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono8'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(68)
        if feedback.isCanceled():
            return {}

        # Ono9
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono9',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-3.27605*\"Eno1\"-5.11541*\"Eno2\"-2.22503*\"Eno3\"-6.45689*\"Eno4\"-0.367465*\"Eno5\"-2.58237*\"Eno6\"-4.298911*\"Eno7\"-5.27994*\"Eno8\"-4.79214*\"Eno9\"-5.07782*\"Eno10\"-3.25345*\"Eno11\"-3.545587*\"Eno12\"-4.93532*\"Eno13\"-0.789495*\"Eno14\"-4.82235*\"Eno15\"-4.243184*\"Eno16\"-0.479815) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.16940*\"Eno1\"-3.65476*\"Eno2\"-0.17077*\"Eno3\"-5.25883*\"Eno4\"-0.12286*\"Eno5\"-8.87476*\"Eno6\"-6.17789*\"Eno7\"-8.75756*\"Eno8\"-6.26508*\"Eno9\"-1.21518*\"Eno10\"-0.10075*\"Eno11\"-0.11575*\"Eno12\"-9.49581*\"Eno13\"-0.11364*\"Eno14\"-0.10540*\"Eno15\"-5.48064*\"Eno16\"+0.53807)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.31033*\"Eno1\"-0.97292*\"Eno2\"-0.28475*\"Eno3\"-0.17059*\"Eno4\"-0.32867*\"Eno5\"-0.13411*\"Eno6\"-0.50342*\"Eno7\"-0.43940*\"Eno8\"-0.41997*\"Eno9\"+6.92115*\"Eno10\"+2.02041*\"Eno11\"-0.21166*\"Eno12\"-3.62026*\"Eno13\"-0.25060*\"Eno14\"-0.35438*\"Eno15\"-0.12314*\"Eno16\"-0.21404) \r\nEND',
            'INPUT': outputs['Ono8']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono9'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(69)
        if feedback.isCanceled():
            return {}

        # Ono10
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono10',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-5.46019*\"Eno1\"-7.08600*\"Eno2\"-4.52914*\"Eno3\"-0.21880*\"Eno4\"-0.19332*\"Eno5\"-7.18479*\"Eno6\"-0.10016*\"Eno7\"-0.15935*\"Eno8\"-0.103289*\"Eno9\"-8.06120*\"Eno10\"-4.99217*\"Eno11\"-6.93515*\"Eno12\"-8.52398*\"Eno13\"-4.509443*\"Eno14\"-0.125393*\"Eno15\"-6.39928*\"Eno16\"+-0.00513) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.63527*\"Eno1\"-0.80531*\"Eno2\"-1.18752*\"Eno3\"-0.20495*\"Eno4\"-0.95975*\"Eno5\"-0.57680*\"Eno6\"-0.26622*\"Eno7\"-0.73298*\"Eno8\"-0.28205*\"Eno9\"-0.42755*\"Eno10\"-0.43598*\"Eno11\"-0.78450*\"Eno12\"-0.69446*\"Eno13\"-0.26737*\"Eno14\"-0.11786*\"Eno15\"-0.54800*\"Eno16\"+0.41063)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.22387*\"Eno1\"+0.593016*\"Eno2\"-0.41559*\"Eno3\"-0.15366*\"Eno4\"+0.43745*\"Eno5\"+0.13423*\"Eno6\"-0.20825*\"Eno7\"+0.28524*\"Eno8\"-0.57205*\"Eno9\"+0.226981*\"Eno10\"-0.06591*\"Eno11\"+0.07267*\"Eno12\"-0.15157*\"Eno13\"+0.02093*\"Eno14\"+0.51491*\"Eno15\"-4.26742*\"Eno16\"+0.35789) \r\nEND',
            'INPUT': outputs['Ono9']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono10'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(70)
        if feedback.isCanceled():
            return {}

        # Ono11
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono11',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.45501*\"Eno1\"-1.65276*\"Eno2\"-0.94319*\"Eno3\"-3.37009*\"Eno4\"-0.354441*\"Eno5\"-1.12616*\"Eno6\"-1.14119*\"Eno7\"-2.81559*\"Eno8\"-2.02588*\"Eno9\"-1.51279*\"Eno10\"-0.977588*\"Eno11\"-0.019706*\"Eno12\"-2.37841*\"Eno13\"-0.046918*\"Eno14\"-0.31982*\"Eno15\"-1.163819*\"Eno16\"-0.005501) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.71580*\"Eno1\"-0.01573*\"Eno2\"-0.12019*\"Eno3\"-0.02414*\"Eno4\"-0.34260*\"Eno5\"-8.69690*\"Eno6\"-2.31685*\"Eno7\"-4.80445*\"Eno8\"-0.26470*\"Eno9\"-0.50870*\"Eno10\"-0.10714*\"Eno11\"+0.33053*\"Eno12\"-4.76536*\"Eno13\"-0.33606*\"Eno14\"-3.22127*\"Eno15\"-0.01865*\"Eno16\"+0.44351)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.11095*\"Eno1\"-5.44773*\"Eno2\"-4.88888*\"Eno3\"-7.31693*\"Eno4\"-5.62679*\"Eno5\"-8.61085*\"Eno6\"-0.123427*\"Eno7\"-0.120237*\"Eno8\"-0.10379*\"Eno9\"-5.61745*\"Eno10\"-2.47400*\"Eno11\"-8.11072*\"Eno12\"-2.34271*\"Eno13\"-8.51690*\"Eno14\"-8.25638*\"Eno15\"-4.55468*\"Eno16\"+0.59366) \r\nEND',
            'INPUT': outputs['Ono10']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono11'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(71)
        if feedback.isCanceled():
            return {}

        # Ono12
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono12',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-1.11646*\"Eno1\"-0.87525*\"Eno2\"-0.13675*\"Eno3\"-2.162555*\"Eno4\"-1.12536*\"Eno5\"-1.34817*\"Eno6\"-0.56122*\"Eno7\"-2.03976*\"Eno8\"-1.50678*\"Eno9\"-1.24081*\"Eno10\"-0.431349*\"Eno11\"-0.66450*\"Eno12\"-1.15263*\"Eno13\"-0.39562*\"Eno14\"-0.91792*\"Eno15\"-1.17686*\"Eno16\"-0.006785) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,1.16192*\"Eno1\"-1.21164*\"Eno2\"+2.08704*\"Eno3\"-0.18201*\"Eno4\"+1.24329*\"Eno5\"-3.99161*\"Eno6\"+0.67127*\"Eno7\"-1.56735*\"Eno8\"-0.11710*\"Eno9\"-0.21334*\"Eno10\"-4.25619*\"Eno11\"+0.827033*\"Eno12\"-1.60574*\"Eno13\"+0.19957*\"Eno14\"-0.66121*\"Eno15\"-1.31680*\"Eno16\"+0.87652)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.19143*\"Eno1\"-0.94153*\"Eno2\"-0.83165*\"Eno3\"-0.12456*\"Eno4\"-0.11884*\"Eno5\"-0.15509*\"Eno6\"-0.21861*\"Eno7\"-0.20652*\"Eno8\"-0.17579*\"Eno9\"-9.36998*\"Eno10\"-4.21416*\"Eno11\"-0.14540*\"Eno12\"-7.83809*\"Eno13\"-0.14867*\"Eno14\"-0.14845*\"Eno15\"-9.72957*\"Eno16\"+0.22325) \r\nEND',
            'INPUT': outputs['Ono11']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono12'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(72)
        if feedback.isCanceled():
            return {}

        # Ono13
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono13',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.349238*\"Eno1\"+0.61415*\"Eno2\"+1.66714*\"Eno3\"-0.196753*\"Eno4\"-0.273266*\"Eno5\"-0.24447*\"Eno6\"-0.17147*\"Eno7\"-0.55706*\"Eno8\"-0.611435*\"Eno9\"-6.26314*\"Eno10\"-0.448532*\"Eno11\"-0.28258*\"Eno12\"-0.47441*\"Eno13\"+2.80599*\"Eno14\"-9.00727*\"Eno15\"-0.18903*\"Eno16\"+0.382660) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.63864*\"Eno1\"-1.8476*\"Eno2\"-1.30277*\"Eno3\"-1.89317*\"Eno4\"-1.69013*\"Eno5\"-2.00480*\"Eno6\"-2.31209*\"Eno7\"-0.95898*\"Eno8\"-1.70724*\"Eno9\"-2.35449*\"Eno10\"-3.23614*\"Eno11\"-2.95076*\"Eno12\"-1.97873*\"Eno13\"-0.52398*\"Eno14\"-3.47669*\"Eno15\"-3.64284*\"Eno16\"+0.43866)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-1.58192*\"Eno1\"+1.07198*\"Eno2\"-0.75418*\"Eno3\"-2.27408*\"Eno4\"-0.30727*\"Eno5\"-3.89020*\"Eno6\"-3.41260*\"Eno7\"-2.74227*\"Eno8\"-1.62349*\"Eno9\"-2.23699*\"Eno10\"-0.96272*\"Eno11\"-1.22929*\"Eno12\"-0.58953*\"Eno13\"-1.80235*\"Eno14\"-1.03445*\"Eno15\"-0.175890*\"Eno16\"-0.04766) \r\nEND',
            'INPUT': outputs['Ono12']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono13'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(73)
        if feedback.isCanceled():
            return {}

        # Ono14
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono14',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-0.31081*\"Eno1\"+0.27072*\"Eno2\"+0.542068*\"Eno3\"-3.30318*\"Eno4\"-0.749168*\"Eno5\"-0.80341*\"Eno6\"-0.543253*\"Eno7\"-0.30778*\"Eno8\"+4.51686*\"Eno9\"-0.29968*\"Eno10\"-0.68020*\"Eno11\"-0.53371*\"Eno12\"-0.47466*\"Eno13\"+3.90502*\"Eno14\"+9.845962*\"Eno15\"-0.566500*\"Eno16\"+0.86768) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,0.31348*\"Eno1\"+0.21928*\"Eno2\"-0.26527*\"Eno3\"-0.83233*\"Eno4\"+0.03273*\"Eno5\"-0.27607*\"Eno6\"-0.15817*\"Eno7\"-0.13404*\"Eno8\"-0.03155*\"Eno9\"-3.24728*\"Eno10\"-0.49453*\"Eno11\"-0.35838*\"Eno12\"+0.462321*\"Eno13\"+0.31694*\"Eno14\"-0.27633*\"Eno15\"-1.40193*\"Eno16\"+0.18179)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.13174*\"Eno1\"-3.19271*\"Eno2\"-5.67492*\"Eno3\"-8.4235*\"Eno4\"-4.64447*\"Eno5\"-0.10841*\"Eno6\"-0.15046*\"Eno7\"-0.14498*\"Eno8\"-0.121534*\"Eno9\"-5.86061*\"Eno10\"-2.32491*\"Eno11\"-0.10268*\"Eno12\"-0.74088*\"Eno13\"-9.88055*\"Eno14\"-6.96216*\"Eno15\"-0.33228*\"Eno16\"+0.32206) \r\nEND',
            'INPUT': outputs['Ono13']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono14'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(74)
        if feedback.isCanceled():
            return {}

        # Ono15
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono15',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  max(0,-1.04668*\"Eno1\"-5.27993*\"Eno2\"-2.81656*\"Eno3\"-0.11348*\"Eno4\"-0.48526*\"Eno5\"-4.30825*\"Eno6\"-3.28450*\"Eno7\"-9.19285*\"Eno8\"-6.40089*\"Eno9\"-5.20483*\"Eno10\"-2.44396*\"Eno11\"-0.54405*\"Eno12\"-6.12485*\"Eno13\"-0.14362*\"Eno14\"-1.15321*\"Eno15\"-3.57629*\"Eno16\"-0.010657) \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-1.36127*\"Eno1\"-1.95154*\"Eno2\"-0.47146*\"Eno3\"-2.38849*\"Eno4\"-1.32758*\"Eno5\"-2.95307*\"Eno6\"-1.44247*\"Eno7\"-0.41955*\"Eno8\"-1.61188*\"Eno9\"-3.19536*\"Eno10\"-3.00659*\"Eno11\"-2.19156*\"Eno12\"-1.63267*\"Eno13\"-0.55435*\"Eno14\"-2.80495*\"Eno15\"-3.73747*\"Eno16\"+0.57589)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.15716*\"Eno1\"-7.50454*\"Eno2\"-6.43613*\"Eno3\"-0.104965*\"Eno4\"-8.62582*\"Eno5\"-0.126792*\"Eno6\"-0.17913*\"Eno7\"-0.17137*\"Eno8\"-0.14619*\"Eno9\"-7.92413*\"Eno10\"-3.79685*\"Eno11\"-0.11959*\"Eno12\"-0.49552*\"Eno13\"-0.11811*\"Eno14\"-0.10991*\"Eno15\"-0.25606*\"Eno16\"+0.20797) \r\nEND',
            'INPUT': outputs['Ono14']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono15'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(75)
        if feedback.isCanceled():
            return {}

        # Ono16
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'Ono16',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  1 \r\nWHEN  \"cultura\" = \'trigo\' THEN max(0,-0.089882*\"Eno1\"-1.42121*\"Eno2\"-0.93207*\"Eno3\"-2.62311*\"Eno4\"-0.22482*\"Eno5\"-0.64452*\"Eno6\"-1.23573*\"Eno7\"-2.13349*\"Eno8\"-1.89524*\"Eno9\"-1.42926*\"Eno10\"-0.58477*\"Eno11\"+0.04768*\"Eno12\"-1.45048*\"Eno13\"-0.00368*\"Eno14\"-0.21134*\"Eno15\"-0.75053*\"Eno16\"-0.11995)\r\nWHEN \"cultura\" = \'girassol\' THEN max(0,-0.22667*\"Eno1\"-0.12571*\"Eno2\"-9.76523*\"Eno3\"-0.150513*\"Eno4\"-0.145825*\"Eno5\"-0.18507*\"Eno6\"-0.25849*\"Eno7\"-0.245953*\"Eno8\"-0.21352*\"Eno9\"+0.113959*\"Eno10\"-4.76430*\"Eno11\"-0.173552*\"Eno12\"-0.10163*\"Eno13\"-0.17890*\"Eno14\"-0.18101*\"Eno15\"-0.13752*\"Eno16\"+0.13716) \r\nEND',
            'INPUT': outputs['Ono15']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Ono16'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(76)
        if feedback.isCanceled():
            return {}

        # Sno1
        alg_params = {
            'FIELD_LENGTH': 15,
            'FIELD_NAME': 'Sno1',
            'FIELD_PRECISION': 5,
            'FIELD_TYPE': 0,
            'FORMULA': 'CASE \r\nWHEN \"cultura\"  = \'milho\' THEN  \r\n-8.22132*\"Ono1\"-10.52073*\"Ono2\"-9.43594*\"Ono3\"-3.55434*\"Ono4\"-29.99544*\"Ono5\"-10.91237*\"Ono6\"-49.86741*\"Ono7\"+24.51519*\"Ono8\"-17.04138*\"Ono9\"-6.95815*\"Ono10\"-5.62455*\"Ono11\"-12.31283*\"Ono12\"-4.86970*\"Ono13\"-6.95156*\"Ono14\"-16.74193*\"Ono15\"-3.73404*\"Ono16\"+6141.15634\r\nWHEN  \"cultura\" = \'trigo\' THEN  4.16991*\"Ono1\"-1.81007*\"Ono2\"-3.61399*\"Ono3\"+2.56221*\"Ono4\"+1.05100*\"Ono5\"-23.04195*\"Ono6\"-1.63380*\"Ono7\"+15.73015*\"Ono8\"-47.84620*\"Ono9\"+1.963887*\"Ono10\"-2.03446*\"Ono11\"-13.47990*\"Ono12\"+11.04877*\"Ono13\"+0.170664*\"Ono14\"+0.554892*\"Ono15\"-2.40182*\"Ono16\"+5.72251\r\nWHEN \"cultura\" = \'girassol\' THEN \r\n2.44705*\"Ono1\"+347.8534*\"Ono2\"+32.34529*\"Ono3\"+35.923690*\"Ono4\"+3.65388*\"Ono5\"-499.94417*\"Ono6\"+75.42071*\"Ono7\"+44.88567*\"Ono8\"-231.93658*\"Ono9\"-8.060901*\"Ono10\"+16.637892*\"Ono11\"+33.43717*\"Ono12\"-47.00082*\"Ono13\"+44.51176*\"Ono14\"+36.67993*\"Ono15\"+55.27329*\"Ono16\"+2.48312\r\nEND',
            'INPUT': outputs['Ono16']['OUTPUT'],
            'NEW_FIELD': True,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Sno1'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(77)
        if feedback.isCanceled():
            return {}

        # Rasterizar
        alg_params = {
            'BURN': 0,
            'DATA_TYPE': 5,
            'EXTENT': parameters['insiraocontornodarea'],
            'EXTRA': '',
            'FIELD': 'Sno1',
            'HEIGHT': QgsExpression('( @insiraocontornodarea_maxy -  @insiraocontornodarea_miny )/10').evaluate(),
            'INIT': None,
            'INPUT': outputs['Sno1']['OUTPUT'],
            'INVERT': False,
            'NODATA': 0,
            'OPTIONS': '',
            'UNITS': 0,
            'WIDTH': QgsExpression('( @insiraocontornodarea_maxx - @insiraocontornodarea_minx )/10').evaluate(),
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Rasterizar'] = processing.run('gdal:rasterize', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(78)
        if feedback.isCanceled():
            return {}

        # Reamostragem
        alg_params = {
            'INPUT': outputs['Rasterizar']['OUTPUT'],
            'KEEP_TYPE': True,
            'SCALE_DOWN': 3,
            'SCALE_UP': 5,
            'TARGET_TEMPLATE': None,
            'TARGET_USER_FITS': 0,
            'TARGET_USER_SIZE': 10,
            'TARGET_USER_XMIN TARGET_USER_XMAX TARGET_USER_YMIN TARGET_USER_YMAX': parameters['insiraocontornodarea'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Reamostragem'] = processing.run('saga:resampling', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(79)
        if feedback.isCanceled():
            return {}

        # Rec_mask
        alg_params = {
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'DATA_TYPE': 0,
            'EXTRA': '',
            'INPUT': outputs['Reamostragem']['OUTPUT'],
            'KEEP_RESOLUTION': False,
            'MASK': parameters['insiraocontornodarea'],
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'SET_RESOLUTION': False,
            'SOURCE_CRS': 'ProjectCrs',
            'TARGET_CRS': None,
            'X_RESOLUTION': None,
            'Y_RESOLUTION': None,
            'OUTPUT': parameters['SuperfcieDeProdutividade']
        }
        outputs['Rec_mask'] = processing.run('gdal:cliprasterbymasklayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['SuperfcieDeProdutividade'] = outputs['Rec_mask']['OUTPUT']

        feedback.setCurrentStep(80)
        if feedback.isCanceled():
            return {}

        # Add raster values to points
        alg_params = {
            'GRIDS': outputs['Rec_mask']['OUTPUT'],
            'RESAMPLING': 0,
            'SHAPES': parameters['validao'],
            'RESULT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AddRasterValuesToPoints'] = processing.run('saga:addrastervaluestopoints', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(81)
        if feedback.isCanceled():
            return {}

        # C - erro
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'erro',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 0,
            'FORMULA': '\"prod\" - \"OUTPUT\" ',
            'INPUT': outputs['AddRasterValuesToPoints']['RESULT'],
            'NEW_FIELD': True,
            'OUTPUT': parameters['ErroDePreviso']
        }
        outputs['CErro'] = processing.run('qgis:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['ErroDePreviso'] = outputs['CErro']['OUTPUT']

        feedback.setCurrentStep(82)
        if feedback.isCanceled():
            return {}

        # Estatísticas da camada raster
        alg_params = {
            'BAND': 1,
            'INPUT': outputs['Rec_mask']['OUTPUT'],
            'OUTPUT_HTML_FILE': parameters['EstatsticaDaProdutividade']
        }
        outputs['EstatsticasDaCamadaRaster'] = processing.run('native:rasterlayerstatistics', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['EstatsticaDaProdutividade'] = outputs['EstatsticasDaCamadaRaster']['OUTPUT_HTML_FILE']
        return results

    def name(self):
        return 'Produtividade_cod'

    def displayName(self):
        return 'Produtividade_cod'

    def group(self):
        return 'TCC'

    def groupId(self):
        return 'TCC'

    def shortHelpString(self):
        return """<html><body><h2>Descrição do algoritmo</h2>
<p>Ferramenta para previsão de produtividade de culturas a partir de imagens multiespectrais Sentinel-2 utilizando modelo de Redes Neurais Artificiais - RNA

Bandas utilizadas: B02, B03, B04, B05, B06, B07, B08, B08A, B11 e B12

Culturas: milho, trigo e girassol

Observações: todos os dados de entrada devem estar no mesmo SRC (preferencialmente projetadas/métricas)
</p>
<h2>parâmetros de entrada</h2>
<h3>Cultura</h3>
<p>Seleciona a cultura para previsão (milho, trigo, girassol)</p>
<h3>Insira a B02 (Azul)</h3>
<p>Inserir a banda B02 - Azul do satélite Sentinel 2</p>
<h3>Insira a B03 (Verde)</h3>
<p>Inserir a banda B03 - Verde do satélite Sentinel 2</p>
<h3>Insira a B04 (Vermelho)</h3>
<p>Inserir a banda B04 - Vermelho do satélite Sentinel 2</p>
<h3>Insira a B05 (RE 1)</h3>
<p>Inserir a banda B05 - Vermelho Limítrofe 1 do satélite Sentinel 2</p>
<h3>Insira a B06 (RE 2)</h3>
<p>Inserir a banda B06 - Vermelho Limítrofe 2 do satélite Sentinel 2</p>
<h3>Insira a B07 (RE 3)</h3>
<p>Inserir a banda B07 - Vermelho Limítrofe 3 do satélite Sentinel 2</p>
<h3>Insira a B08 (IVP)</h3>
<p>Inserir a banda B08 - Infra Vermelho Próximo - IVP do satélite Sentinel 2</p>
<h3>Insira a B08A (RE 4)</h3>
<p>Inserir a banda B08A - Vermelho Limítrofe 4 do satélite Sentinel 2</p>
<h3>Insira a B11 (SWIR1)</h3>
<p>Inserir a banda B11 - SWIR 1 do satélite Sentinel 2</p>
<h3>Insira a B12 (SWIR2)</h3>
<p>Inserir a banda B12 - SWIR 2 do satélite Sentinel 2</p>
<h3>Contorno da Área</h3>
<p>Camada do tipo polígono que delimita a área de interesse</p>
<h3>Insira uma camada de pontos para validação</h3>
<p>Opcional - Camada do tipo ponto com campO correspondente ao valor de produtividade mensurada para validação da previsão
Observação: o campo com a produtividade mensurada deve chamar "prod"</p>
<h3>Indique a coluna de produtividade medida</h3>
<p>Opcional - Campo da camada que corresponde ao valor de produtividade mensurada</p>
<h3>Superfície de Produtividade</h3>
<p>Superfície de produtividade em formato raster</p>
<h3>Estatística da Produtividade</h3>
<p>Estatísticas básicas da camada de produtividade em formato de arquivo de texto</p>
<h3>Erro de Previsão</h3>
<p>Camada com campos de Produtividade Medida, Produtividade Calculada e Erro de Previsão</p>
<h2>Saídas</h2>
<h3>Superfície de Produtividade</h3>
<p>Superfície de produtividade em formato raster</p>
<h3>Estatística da Produtividade</h3>
<p>Estatísticas básicas da camada de produtividade em formato de arquivo de texto</p>
<h3>Erro de Previsão</h3>
<p>Camada com campos de Produtividade Medida, Produtividade Calculada e Erro de Previsão</p>
<br><p align="right">Autor do algoritmo: Xavier, L.C.M. 
Martins, G.D.
(2021)</p><p align="right">Autor da ajuda: Xavier, L.C.M. 
Martins, G.D.
(2021)</p><p align="right">Versão do Algoritmo: 1.0</p></body></html>"""

    def helpUrl(self):
        return '"""Colocar link para o trabalho no repositório"""'

    def createInstance(self):
        return Produtividade_cod()
