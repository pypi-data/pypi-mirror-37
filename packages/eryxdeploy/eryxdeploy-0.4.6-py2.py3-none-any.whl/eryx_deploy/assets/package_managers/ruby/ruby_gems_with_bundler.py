from eryx_deploy.assets.package_managers.abs_package_manager import PackageManager


class RubyGemsWithBundler(PackageManager):
    def __init__(self, ruby_environment, package_group=None):
        self._ruby_environment = ruby_environment
        self._package_group = package_group

    def first_time_setup(self):
        self._ruby_environment.run("gem install bundler")
        self._do_not_generate_docs_for_gems()

    def update_dependencies(self):
        command = "bundle install"

        if self._package_group is not None:
            package_group_param = "--with {}".format(self._package_group)
            command = "{} {}".format(command, package_group_param)

        self._ruby_environment.run(command)

    def _do_not_generate_docs_for_gems(self):
        self._ruby_environment.run('echo "gem: --no-document" > ~/.gemrc')
