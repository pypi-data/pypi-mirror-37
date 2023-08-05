import semver

class semver_max(object):
    def __init__(self):
        pass

    def _max_ver(self, v1, v2):

        cmp_res = semver.compare(v1, v2)

        if cmp_res == 0 or cmp_res == 1:
            b1, b2 = semver.parse(v1).get('build'), semver.parse(v2).get('build')
            b1, b2 = b1 or '.0', b2 or '.0'

            res = semver.cmp(int(b1.split('.')[1]), int(b2.split('.')[1]))
            if res == 0 or res == 1:
                return v1

        return v2

    def find_version(self, version, version_dirs):

        ret_version = version
        if version is None:
            for version_dir in version_dirs:
                if ret_version is None:
                    ret_version = version_dir
                else:
                    ret_version = self._max_ver(version_dir, ret_version)
        else:
            if version not in version_dirs:
                raise RunnerRuntimeError("version is not exits.")

        return ret_version
