import hashlib
import os

from django.contrib.staticfiles.management.commands import collectstatic


class Command(collectstatic.Command):

    def delete_file(self, path, prefixed_path, source_storage):  # noqa
        """
        Checks if the target file should be deleted if it already exists
        """
        if hasattr(self.storage, 'preload_metadata') and not self.storage.preload_metadata:
            self.log('Forcing storage to preload metadata')
            self.storage.preload_metadata = True

        self.log(prefixed_path, level=1)

        if self.storage.exists(prefixed_path):
            # noinspection PyBroadException
            try:
                # attempt the S3 hash first
                entry_path = os.path.join(self.storage.location, prefixed_path)
                if self.storage.entries.get(entry_path).e_tag == '"%s"' % hashlib.md5(
                    source_storage.open(path).read()
                ).hexdigest():
                    self.log(u"Skipping '%s' (not modified based on MD5 SUM)" % path, level=1)
                    return False
            except Exception as e:
                print(e)
                pass
            try:
                # When was the target file modified last time?
                target_last_modified = self.storage.modified_time(prefixed_path)
            except (OSError, NotImplementedError, AttributeError):
                # The storage doesn't support ``modified_time`` or failed
                pass
            else:
                try:
                    # When was the source file modified last time?
                    source_last_modified = source_storage.modified_time(path)
                except (OSError, NotImplementedError, AttributeError):
                    pass
                else:
                    # The full path of the target file
                    if self.local:
                        full_path = self.storage.path(prefixed_path)
                    else:
                        full_path = None
                    # Skip the file if the source file is younger
                    if target_last_modified >= source_last_modified:
                        if not ((self.symlink and full_path
                                 and not os.path.islink(full_path)) or
                                (not self.symlink and full_path
                                 and os.path.islink(full_path))):
                            if prefixed_path not in self.unmodified_files:
                                self.unmodified_files.append(prefixed_path)
                            self.log("Skipping '%s' (not modified)" % path, level=1)
                            return False
            # Then delete the existing file if really needed
            if self.dry_run:
                self.log("Pretending to delete '%s'" % path, level=1)
            else:
                self.log("Deleting '%s'" % path, level=1)
                self.storage.delete(prefixed_path)
        return True
