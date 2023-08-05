class Conversions(object):
    """
    int2,int8,int10,int16,str2,str8,str10,str16,
    array_int2,array_int8,array_int10,array_int16,
    array_str2,array_str8,array_str10,array_str16,
    string,bytes,file,
    str_to_bytes not encode
    bytes_to_str not decode
    """
    def __init__(self, value, prefix='', encoding='utf-8'):
        self.value = value
        self.prefix = prefix
        self.encoding = encoding

    def get_file(self):
        return ''

    def get_array(self, prefix='', array_type=''):
        if array_type == 'int':
            return [1, 2, 3]
        elif array_type == 'str':
            return ['1', '2', '3']
