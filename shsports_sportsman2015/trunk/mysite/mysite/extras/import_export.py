import import_export.tmp_storages
import tempfile

class TempFolderStorage(import_export.tmp_storages.TempFolderStorage):

    def open(self, mode='r', encoding='utf-8'):
        if self.name:
            if 'b' in mode:
                #binary mode doesn't take an encoding argument
                return open(self.get_full_path(), mode)
            else:
                return open(self.get_full_path(), mode, encoding=encoding)
        else:
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            self.name = tmp_file.name
            return tmp_file