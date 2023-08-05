from __future__ import absolute_import
import wrapt


# pip master has most commands moved into _internal folder
@wrapt.when_imported('requests.sessions')
def apply_patches(sessions):
    override_ssl_handler(sessions)


def override_ssl_handler(sessions):
    class SslContextHttpAdapter(sessions.HTTPAdapter):
        """Transport adapter that allows us to use system-provided SSL
        certificates."""

        def init_poolmanager(self, *args, **kwargs):
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.load_default_certs()
            kwargs['ssl_context'] = ssl_context
            return super(SslContextHttpAdapter, self).init_poolmanager(*args, **kwargs)

    def wrapper(wrapped, instance, args, kwargs):
        retries = kwargs.get("retries", 0)
        wrapped(*args, **kwargs)
        secure_adapter = SslContextHttpAdapter(max_retries=retries)
        instance.mount("https://", secure_adapter)

    wrapt.wrap_function_wrapper(sessions.Session, '__init__', wrapper)
