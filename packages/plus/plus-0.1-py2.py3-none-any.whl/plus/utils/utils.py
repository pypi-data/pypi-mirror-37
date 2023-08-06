# --------------------------------------------------------
# Spatial Task Attention Network
# Copyright (c) 2016 by Contributors
# Copyright (c) 2018 Venus Group, ShanghaiTech University
# Licensed under The Apache-2.0 License [see LICENSE for details]
# Written by Shipeng Yan, Songyang Zhang
# --------------------------------------------------------

import sys
sys.path.append("../")


def pack_msg_dict(kwargs, sep='\t'):
    """

    :param kwargs:
    :param sep: \t \n
    :return:
    """
    msg = ['{0}={1}'.format(k, v) for k, v in kwargs.items()]
    msg = sep + sep.join(msg)
    return msg


def get_output_dim(net_spec_file, net_spec_attr, input):
    """Get the output dim so you don't need to manually calculate
    the dimensions of network
    :param net_spec_file:
    :param input: The input should be a legal input of the net
    :return: A shape(tuple)
    """
    # TODO: Can't deal with all situations such as TCML
    from configs import utils, config_manager
    from torch.autograd import Variable
    input = Variable(input)
    net_spec_file = net_spec_file
    net_mgr = config_manager.NetConfig(net_spec_file)
    net = utils.build(net_mgr.cfg[net_spec_attr])
    output = net(input)
    return output.shape


def load_state_dict(model, pretrained_dict):
    model_dict = model.state_dict()
    # 1. filter out unnecessary keys
    # pretrained_dict = {k:v for k,v in pretrained_dict.items() if k in model_dict}
    tmp_dict = {}
    for k, v in pretrained_dict.items():
        if k in model_dict:
            tmp_dict[k] = v
        else:
            print("The para {} in ckpt is Ignored.".format(k))
    pretrained_dict = tmp_dict
    # 2. overwrite entries in the existing state dict
    model_dict.update(pretrained_dict)
    # 3. load the new state dict
    model.load_state_dict(model_dict)


def set_requires_grad_stat(module, requires_grad=False):
    for p in module.parameters():
        p.requires_grad = requires_grad


def random_init(seed=0):
    import torch
    import random
    import numpy as np
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)


def one_hot_encoding(y, n_class=5):
    """

    :param y: Only support B/ (B,T) Tensor
    :param n_class: the number of classes
    :return: y
    """
    import torch

    is_seq_input = len(y.size())==2
    if is_seq_input:
        B, T = y.size()
        y = y.view(-1)

    gpuid = torch.cuda.current_device()
    device = torch.device("cuda:{0}".format(gpuid))
    y_onehot = torch.FloatTensor(y.size(0),n_class).to(device)
    y_onehot.scatter_(1, y, 1)

    if is_seq_input:
        y_onehot = y_onehot.view(B, T)

    return y_onehot


def test_model_ckpts(model, dataloader, epoch_test, sample_n=100, epoch_n=2, seed=0, ckpts=None, test_model=True, \
                     logger=None):
    """
    :param model:
    :param dataloader:
    :param epoch_test:
        signature: epoch_test(model=, dataloader=) return accu,xxx the first returned value should be accu/the value
        Tip: You could use partial function make the signature satisfy the requirement

    :param ckpts:
    :param test_model: True->Test model, False->Test ckpts
    :return: centers, deviations
    """

    import torch
    import logging

    model.eval()
    set_requires_grad_stat(model)
    if not logger:
        logger = logging.getLogger()

    centers, deviations = [], []
    with torch.no_grad():
        if test_model:
            center, deviation = _test_model_ckpt(model, dataloader, epoch_test, sample_n, epoch_n, seed)
            centers.append(center)
            deviations.append(deviation)
            logger.info("{:.2f}%+-{:.2f}%".format(center, deviation))
        else:
            ori_model_state_dict = model.state_dict()
            for ckpt in ckpts:
                logger.info("Checkpoint:{}".format(ckpt))

                pretrained_state_dict = torch.load(ckpt)
                load_state_dict(model, pretrained_state_dict)
                center, deviation = _test_model_ckpt(model, dataloader, epoch_test, sample_n, epoch_n, seed)

                centers.append(center)
                deviations.append(deviation)

                logger.info("{:.2f}%+-{:.2f}%".format(center, deviation))

                # restore
                load_state_dict(model, ori_model_state_dict)

    return centers, deviations


def _test_model_ckpt(model, dataloader, epoch_test, sample_n, epoch_n, seed):
    """
    Don't directly call this function
    :param model:
    :param dataloader:
    :param epoch_test:
    :param sample_n:
    :param epoch_n:
    :param seed:
    :return:
    """
    # reset random seed for fix results
    import logging
    import numpy as np
    import torch
    import random
    from tqdm import tqdm

    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    random.seed(seed)
    np.random.seed(seed)

    samples = []

    for i in tqdm(range(sample_n)):
        # calc_accu_epochs
        accu_i = 0
        for e in range(epoch_n):
            cur_epoch_accu = epoch_test(model=model, dataloader=dataloader)[0]
            # import pdb;pdb.set_trace()
            accu_i += cur_epoch_accu / epoch_n
        samples.append(accu_i)
    samples = np.asarray(samples)
    center, deviation = calc_confidence_interval(samples)

    # Trick, Most time it is correct.
    if center<1:
        center, deviation = center*100, deviation*100

    return center, deviation


def calc_confidence_interval(samples, confidence_value=0.95):
    # samples should be a numpy array
    import numpy as np, scipy.stats as st
    if type(samples) is list:
        samples = np.asarray(samples)
    # print('Results List:', samples)
    stat_accu = st.t.interval(confidence_value, len(samples)-1, loc=np.mean(samples), scale=st.sem(samples))
    center = (stat_accu[0]+stat_accu[1])/2
    deviation = (stat_accu[1]-stat_accu[0])/2
    return center, deviation




if __name__ == '__main__':
    pass
