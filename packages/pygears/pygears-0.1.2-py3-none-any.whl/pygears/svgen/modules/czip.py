from pygears.svgen.svmod import SVModuleGen
from pygears.typing.queue import Queue
from pygears.svgen.inst import SVGenInstPlugin
from pygears.common.czip import zip_sync, zip_cat
from .syncguard import SVGenSyncGuard
from .cat_util import din_data_cat


class SVGenCZipBase(SVModuleGen):
    @property
    def is_generated(self):
        return True

    def get_sv_port_config(self, modport, type_, name):
        cfg = super().get_sv_port_config(modport, type_, name)

        if issubclass(type_, Queue):
            cfg['lvl'] = type_.lvl
        else:
            cfg['lvl'] = 0

        return cfg


class SVGenZipCat(SVGenCZipBase):
    def get_module(self, template_env):
        intfs = list(self.sv_port_configs())
        queue_intfs = [
            i for i in intfs if i['lvl'] > 0 and i['modport'] == 'consumer'
        ]

        context = {
            'queue_intfs': queue_intfs,
            'module_name': self.sv_module_name,
            'intfs': list(self.sv_port_configs()),
            'din_data_cat': din_data_cat
        }

        return template_env.render_local(__file__, "zip_cat.j2", context)


class SVGenZipSyncBase(SVGenCZipBase):
    def __init__(self, node):
        super().__init__(node)

        if 'outsync' not in self.node.params:
            self.node.params['outsync'] = True

        if self.node.params['outsync']:
            self.syncguard = SVGenSyncGuard(f'{self.sv_module_name}_syncguard',
                                            len(self.node.in_ports))
        else:
            self.syncguard = None

    @property
    def sv_file_name(self):
        if self.syncguard is None:
            return super().sv_file_name
        else:
            return super().sv_file_name, self.syncguard.sv_file_name

    def get_module(self, template_env, template_fn):

        context = {
            'outsync': self.node.params['outsync'],
            'module_name': self.sv_module_name,
            'intfs': list(self.sv_port_configs())
        }
        contents = template_env.render_local(__file__, template_fn, context)

        if self.syncguard is None:
            return contents
        else:
            return contents, self.syncguard.get_module(template_env)


class SVGenZipSync(SVGenZipSyncBase):
    def get_module(self, template_env):
        if all(map(lambda i: i['lvl'] > 0, self.sv_port_configs())):
            return super().get_module(template_env, 'zip_sync.j2')
        else:
            return super().get_module(template_env, 'zip_sync_simple.j2')


class SVGenCZipPlugin(SVGenInstPlugin):
    @classmethod
    def bind(cls):
        cls.registry['svgen']['module_namespace'][zip_sync] = SVGenZipSync
        cls.registry['svgen']['module_namespace'][zip_cat] = SVGenZipCat
