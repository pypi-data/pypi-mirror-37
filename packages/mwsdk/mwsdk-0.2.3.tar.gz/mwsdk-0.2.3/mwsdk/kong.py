from mwutils.mw_consul import KongConf,KongAdminConf
import requests
class KongError(Exception):
    pass

get_host = lambda host: '{http}{host}'.format(http='http://' if not host.startswith('http://') else '',
                                              host=host)
replace = lambda service:service.replace('.','_').replace('/','_')
# 补充 /
get_backslash = lambda path:'{bs}{path}'.format(bs='/' if not path.startswith('/') else '',
                                                path=path)
class Kong():
    def _init_conf(self):
        self._kong = KongConf()
        self._kong_admin = KongAdminConf()

    def __init__(self):
        self._init_conf()

    @property
    def ip(self):
        return self._kong.ip

    @property
    def port(self):
        return self._kong.port

    @property
    def admin_port(self):
        return self._kong_admin.port

    @property
    def host(self):
        return self._kong.host_url()

    @property
    def admin_host(self):
        return self._kong_admin.host_url()

    def reload(self):
        # 重新導入kong的配置
        self._init_conf()

    def reg_service(self,service,service_host, auth='jwt', kong_uris=''):
        '''
        :param kong_admin: 用于注册服务
        :param service_host: 本地服务的host，用于设定upstream_url
        :param service: 服务api，如：rightmanage/v1.0
        :param kong_uris: 空的host uris，为空时值为service,如：rightmanage/v1.0
        :param auth: 认证类型，可为str或list，如：'jwt'，或：['jwt','key']
        :return:
        '''
        ''''
        # 注册 服务API
        resp = requests.post('http://{kong}/apis/'.format(kong=KONG),
                             json={'name': 'rightmanage_v1.0',
                                   'uris': '/rightmanage/v1.0',
                                   'upstream_url': 'http://{server}/rightmanage/v1.0'.format(server=SERVER)})
        print('注册 服务API', resp.text)

        resp = requests.post('http://{kong}/apis/rightmanage_v1.0/plugins'.format(kong=KONG),
                             json={"name": "jwt"})
        print('注册服务API JWT', resp.text)
        '''
        api_url = '{kong}/apis/'.format(kong=self.admin_host)
        # 如果kong_uris有值，则需要用它注册
        api_name = replace(get_backslash(service if not kong_uris else kong_uris)[1:])
        if kong_uris:
            uris = '{service}'.format(service=get_backslash(kong_uris))
        else:
            uris = '{service}'.format(service=get_backslash(service))
        print('uris',uris)
        upstream_url = '{service_host}{service}'.format(service_host=get_host(service_host),
                                                        service=get_backslash(service))
        try:
            # 删除旧的api
            requests.delete('{kong}/apis/{api_name}'.format(kong=self.admin_host,
                                                            api_name=api_name))
            resp = requests.post(api_url,
                                 json={'name': api_name,
                                       'uris': uris,
                                       'upstream_url': upstream_url,
                                       'preserve_host': True})
            print('注册%s服务 to kong 成功,'%service, resp.text)
        except Exception as e:
            print('注册 %s服务失败,error:%s' % (service, e))
            import sys
            sys.exit(-1)
        if auth:
            if isinstance(auth, str):
                auth, auth_str = [], auth
                auth.append(auth_str)
            if 'jwt' in auth:
                jwt_data =  {"name": "jwt",
                             "config.uri_param_names": "jwt",
                             "config.claims_to_verify": "exp",
                             "config.key_claim_name": "iss",
                             "config.secret_is_base64": "false",
                             "config.cookie_names": "sessionid"
                             }
                resp = requests.post('{kong}/apis/{api_name}/plugins'.format(kong=self.admin_host,
                                                                             api_name=api_name),
                                     json=jwt_data)
                if resp.status_code!=201:
                    # 在0.12.1之前的kong 不支持config.cookie_names
                    jwt_data.pop('config.cookie_names')
                    resp = requests.post('{kong}/apis/{api_name}/plugins'.format(kong=self.admin_host,
                                                                                 api_name=api_name),
                                         json=jwt_data)
                if resp.status_code==201:
                    print('注册%s服务API JWT 成功'%service, resp.text)
                else:
                    print('注册%s服务API JWT 失败' % service, resp.status_code,resp.text)
            else:
                raise Exception('不支持的auth(%s)' % auth)

    def add_upstream_target(self, upstream_name, service_host, weight):
        '''

        :return:
        '''
        ''''
        # create an upstream
        $ curl -X POST http://kong:8001/upstreams \
            --data "name=address.v1.service"

        # add two targets to the upstream
        $ curl -X POST http://kong:8001/upstreams/address.v1.service/targets \
            --data "target=192.168.101.75:80"
            --data "weight=100"
        $ curl -X POST http://kong:8001/upstreams/address.v1.service/targets \
            --data "target=192.168.100.76:80"
            --data "weight=50"

        # create a Service targeting the Blue upstream
        $ curl -X POST http://kong:8001/apis/ \
            --data "name=service-api" \
            --data "uris=/aa"
            --data "upstream_url=http://address.v1.service"
        '''
        upstream_api_url = '{kong}/upstreams/'.format(kong=self.admin_host)
        # add upstream
        try:
            resp = requests.post(upstream_api_url, json={'name':upstream_name})
            print('add %s upstream to kong 成功,' % upstream_name, resp.text)
        except Exception as e:
            print('add %s upstream失败,error:%s' % (upstream_name, e))
            import sys
            sys.exit(-1)
        targets_api_url = '{kong}/upstreams/{upstream_name}/targets'.format(kong=self.admin_host, upstream_name=upstream_name)
        try:
            resp = requests.post(targets_api_url,
                                 json={'target': service_host,'weight': weight})
            print('add target for %s to kong 成功,' % upstream_name, resp.text)
        except Exception as e:
            print('add target for %s失败,error:%s' % (upstream_name, e))
            import sys
            sys.exit(-1)



if __name__ == '__main__':
    '''
    curl -X Delete 'http://192.168.101.31:8001/apis/test_v1_0'
    curl -X Post 'http://192.168.101.31:8001/apis/' -d '{"upstream_url": "http://192.168.101.88:8001/test/v1.0", "preserve_host": true, "uris": "/test/v1.0", "name": "test_v1_0"}'
    curl -X Post 'http://192.168.101.31:8001/apis/test_v1_0/plugins' -d '{"name": "jwt"}'
    '''
    k = Kong()
    k.add_upstream_target('monitor-srv','192.168.101.88:8999',100)
    k.reg_service('monitor-srv/api/doc','monitor-srv',auth='',kong_uris='monitor-srv-test1')