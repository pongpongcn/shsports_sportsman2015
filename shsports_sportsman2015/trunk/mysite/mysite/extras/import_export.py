import import_export.tmp_storages
import tempfile
import chardet

class TempFolderStorage(import_export.tmp_storages.TempFolderStorage):

    def open(self, mode='r'):
        if self.name:
            if 'b' in mode:
                #binary mode doesn't take an encoding argument
                return open(self.get_full_path(), mode)
            else:
                #detect file encoding, prevent failure.
                with open(self.get_full_path(), 'rb') as f:
                    rawdata = f.read()
                    detectResult = chardet.detect(rawdata)
                    if detectResult['encoding'] == "GB2312":
                        #Extend range
                        encoding = "GB18030"
                    else:
                        encoding = detectResult['encoding']
                return open(self.get_full_path(), mode, encoding=encoding)
        else:
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            self.name = tmp_file.name
            return tmp_file