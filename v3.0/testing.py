from utility import install_XML_importer
import inspect
install_XML_importer()
import objects as obj

item = obj.Item(uuid=0, name='test', weight=7, special_text='testing', price=1)

print(inspect.signature(obj.Item))
print(item.__dict__)
