class ObjectDimension(object):
    
    
    ENVELOPE = '001'
    PACKAGE = '002'
    CYLINDER = '003'

    _TYPES_ALLOWED = [ENVELOPE, PACKAGE, CYLINDER]
    
    def __init__(self,
                 type_object,
                 height=2,
                 width=11,
                 length=16,
                 diameter=2):


        self._validate_types(type_object)
        self._validate_values(type_object, height, width, length, diameter)

        self.tipo_objeto = type_object
        self.dimensao_altura = int(height)
        self.dimensao_largura = int(width)
        self.dimensao_comprimento = int(length)
        self.dimensao_diametro = int(diameter)

    def _validate_types(self, type_v):
        if self._TYPES_ALLOWED.index(type_v) > -1:
            return True
        else:
            raise ValueError('Type not allowed')

    def _validate_values(self,
                         type_object,
                         height=2,
                         width=11,
                         length=16,
                         diameter=2):

        if type_object == self.PACKAGE:
            if height < 2 or width < 11 or length < 16:
                raise Exception(
                    'Width, height and length are mandatory for object package types')
        elif type_object == self.CYLINDER:
            if length < 16 and diameter < 2:
                raise Exception(
                    'length and diameter are mandatory for object package types')

        return
