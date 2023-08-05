import coverage
import json
import ntpath
import os


class CoverageWrapper(object):
    """Base class for different plugin implementations."""
    read_option = "r"
    write_option = "w"

    def __init__(self, config, outdir, logger):
        self.logger = logger
        self.logger.info(
            "Initialize CovController. config:{}. outdir:{}.".format(
                config,
                outdir
            )
        )
        self.coverage = coverage.coverage(config_file=config)
        self.covered_data = None
        self.covered_files = None
        self.content = None
        self.outdir = outdir
        self._ensure_outdir_exist()

    def start(self, test_name):
        self.current_test = test_name
        self._remove_all_obsolete_coverage()
        self.coverage.erase()
        self.coverage.start()

    def finish(self):
        self.coverage.stop()
        self.coverage.save()
        self.covered_data = self.coverage.get_data()
        self.covered_files = self.covered_data.measured_files()
        self._write_output()

    def mark_test_result(self, result):
        self._write_test_data(result)

    def _ensure_outdir_exist(self):
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    def _remove_all_obsolete_coverage(self):
        test_data_file_path = self._get_test_data_file_path()
        default = {
            "covered_files": []
        }
        test_data = self._get_object_from_file(test_data_file_path, default)
        for covered_file in test_data["covered_files"]:
            self._remove_obsolete_coverage(covered_file)

    def _remove_obsolete_coverage(self, file_path):
        out_file_path = self._get_out_file_path(file_path)

        if not os.path.exists(out_file_path):
            return

        with open(out_file_path, self.read_option) as content_file:
            coverage_data = json.loads(content_file.read())
            new_coverage_data = {}
            for k, v in coverage_data.items():
                try:
                    v.remove(self.current_test)
                except ValueError:
                    pass  # test not cover this line
                if v:
                    new_coverage_data[k] = v

        file = open(out_file_path, self.write_option)
        file.write(json.dumps(new_coverage_data))

    def _write_output(self):
        for measured_file_path in self.covered_files:
            self._init_content(measured_file_path)
            self._update_content(measured_file_path)
            self._write_out_file(measured_file_path)

    def _write_test_data(self, result):
        test_data_file_path = self._get_test_data_file_path()
        with open(test_data_file_path, self.write_option) as content_file:
            test_info = {
                "test_result": result,
                "covered_files": self.covered_files
            }
            content_file.write(json.dumps(test_info))

    def _get_test_data_file_path(self):
        return self.outdir + "/" + self.current_test

    def _init_content(self, measured_file_path):
        out_file_path = self._get_out_file_path(measured_file_path)
        self.content = self._get_object_from_file(out_file_path, {})

    def _write_out_file(self, measured_file_path):
        out_file_path = self._get_out_file_path(measured_file_path)
        file = open(out_file_path, self.write_option)
        file.write(json.dumps(self.content))

    def _get_out_file_path(self, measured_file_path):
        measured_file_name = ntpath.basename(measured_file_path)
        return self.outdir + "/" + measured_file_name

    def _update_content(self, measured_file_path):
        covered_lines = self.covered_data.lines(measured_file_path)
        for covered_line in covered_lines:
            key = str(covered_line)
            self.content.setdefault(key, []).append(self.current_test)

    def _get_object_from_file(self, file_path, default):
        if not os.path.exists(file_path):
            return default

        with open(file_path, self.read_option) as content_file:
            return json.loads(content_file.read())
