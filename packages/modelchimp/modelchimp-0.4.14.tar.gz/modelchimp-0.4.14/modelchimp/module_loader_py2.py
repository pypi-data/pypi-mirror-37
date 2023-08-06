import sys
import imp

class Finder(object):

    def __init__(self, module_name, patcher, patchee):
        self.module_name = module_name
        self.patcher = patcher
        self.patchee_list = patchee

    def find_module(self, fullname, path=None):
        if fullname == self.module_name:
            return self
        return

    def load_module(self, fullname):
        module = self._import_module(fullname)

        for patchee in self.patchee_list:
            self._patch_object(patchee, module)

        return module

    def _import_module(self, fullname):
        fullname_split = fullname.split(".")
        parent = ".".join(fullname_split[:-1])

        if fullname in sys.modules:
            return sys.modules[fullname]

        parent = sys.modules[parent]
        module_path = imp.find_module(fullname_split[-1], parent.__path__)
        return imp.load_module(fullname, *module_path)


    def _patch_object(self, patchee, module):
        try:
            patchee_path = patchee.split('.')
            patchee_child = module

            # Access the parent and child objects
            for obj in patchee_path:
                patchee_parent = patchee_child
                patchee_child = getattr(patchee_child, obj)

            # Path the function
            patchee_child = self.patcher(patchee_child)
            setattr(patchee_parent, patchee_path[-1], patchee_child)
        except Exception as e:
            print(e)
