def insert_pdb_layer(obj, layer_index, debugger_type='pdb', where='pre_forward'):
    """Insert (i)pdb into some layer (in/out)
    :param layer_index:
    :param debugger: ['pdb', 'ipdb']
    :param where: ['pre_forward', 'forward']
    :return:
    """
    try:
        layer = get_layer(obj, layer_index)
        regis_hook[where](layer, debugger(debugger_type))
    except ValueError:
        raise ValueError("where arg in pdb_layer method should be pre or after.")


def get_layer(model, layer_index):

    # TODO: ADD other frames' support such as MXNET, Tensorflow, etc.
    from torch import nn
    assert isinstance(model, nn.Module), "Model should be a subclass of nn.Module."

    layers_index = layer_index.split('.')
    ind_path = ''
    for ind in layers_index:
        # if ind.isdigit():
        #     ind = int(ind)
        try:
            # Caution: Depends on pytorch (_modules)
            model = model._modules[ind]
        except KeyError as e:
            print('\n', repr(e), 'Current model is {},index should be in :'.format(ind_path))
            print('\t\n'.join(model.state_dict().keys()))
            import pdb
            pdb.set_trace()
        finally:
            ind_path = ind_path + '.' + ind
    layer = model
    return layer


def get_para(model, layer_index, para_name):
    # TODO: ADD other frames' support such as MXNET, Tensorflow, etc.
    from torch import nn
    assert isinstance(model, nn.Module), "Model should be a subclass of nn.Module."

    layer = get_layer(model, layer_index)
    try:
        # TODO: ADD other frames' support such as MXNET, Tensorflow, etc.
        # Caution: _parameters depends on pytorch
        para = layer._parameters[para_name]

    except KeyError as e:
        print(repr(e))
        print('Hint:')
        print("\t layer: ")
        print("\t\tClass Info: ", layer.__class__)
        print("\t\tLayer Index: ", layer_index)
        print("\t para: ", list(layer._parameters.keys()))
        import pdb;
        pdb.set_trace()

    return para


def register_para_gradient_hook(model, layer_index, para_name):
    para = get_layer(model, layer_index, para_name)
    para.register_hook(lambda grad: grad)


def register_var_gradient_hook(var):
    #TODO: NotImplemented
    raise NotImplementedError()


def register_pre_forward_hook(module, hook):
    from torch import nn
    # TODO: ADD other frames' support such as MXNET, Tensorflow, etc.
    assert isinstance(module, nn.Module)
    module.register_forward_pre_hook(hook)


def register_forward_hook(module, hook):
    from torch import nn
    # TODO: ADD other frames' support such as MXNET, Tensorflow, etc.
    assert isinstance(module, nn.Module)
    module.register_forward_hook(hook)


def register_backward_hook(module, hook):
    from torch import nn
    # TODO: ADD other frames' support such as MXNET, Tensorflow, etc.
    assert isinstance(module, nn.Module)
    module.register_backward_hook(hook)


def debugger(debugger_type):
    def debug(*args):
        if debugger_type == 'pdb':
            import pdb
            pdb.set_trace()
        elif debugger_type == 'ipdb':
            import ipdb
            ipdb.set_trace()
    return debug


def list_sub_paras(layer):
    # TODO: ADD other frames' support such as MXNET, Tensorflow, etc.
    print("\n".join(layer.state_dict().keys()))


def list_sub_modules(layer):
    # TODO: ADD other frames' support such as MXNET, Tensorflow, etc.
    for l in layer.named_modules():
        print(l)


regis_hook = {
    'pre_forward': register_pre_forward_hook,
    'forward': register_forward_hook,
    'backward': register_backward_hook,
}
