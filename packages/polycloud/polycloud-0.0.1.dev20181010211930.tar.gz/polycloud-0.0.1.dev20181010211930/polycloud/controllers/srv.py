from cement import Controller, ex


class Services(Controller):
    class Meta:
        label = 'srv'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(help='create services',
        arguments=[(
            ['service_name'],
            {'help': 'poly srv create srv_text'},
        )]
        )
    def create(self):
        service_name = self.app.pargs.service_name
        self.app.log.info('creating service : %s' % service_name)
