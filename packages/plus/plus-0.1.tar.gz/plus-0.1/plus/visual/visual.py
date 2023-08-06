"""Visual Utilities
Problems:
TODO:
Visual Design:
    Consider that people may want to customize their own plot, I recommend that create a plotter class that combines these plotter provided by the lib.

"""

import matplotlib
matplotlib.use('Agg')

from plus.utils import get_layer, get_para

import visdom

from tensorboardX import SummaryWriter
import torch

from plus.logger.visdomlogger import VisdomPlotLogger
# from torchnet.logger import VisdomPlotLogger
# Temporarily, don't consider multiple progress situation

# And in the current design, the Visual Class is designed for the oneshot situation

buffer = []


def hook_pre_forward(module, input):
    # only records input
    module.in_ = input


def hook_forward(module, input, output):
    # records input and output
    # if isinstance(module, nn.Linear):
    #     import pdb;pdb.set_trace()
    # if not hasattr(module, 'out_'):
    module.out_ = output.data
    # else:
    # module.out_ = torch.cat([module.out_, output.data])
    # module.in_ = input


######## Plotter ##########

# TODO: Do we need a plotter manager

class BasePlotter(object):
    #TODO: Visualize feature map

    def __init__(self):
        super(object, self).__init__()
        self.plotters = {}


class MatPlotter(object):
    def __init__(self):
        super(object, self).__init__()


class VisdomPlotter(object):

    def __init__(self, env, server='localhost', port=8097, save_env=True):
        super(VisdomPlotter, self).__init__()
        self.env = env
        self.port = port
        self.plotters = {}

        self.server = server
        self.save_env = save_env
        # assert 'http://' not in self.server
        self.viz = visdom.Visdom(env=env, port=port, server='http://'+server)

    def text(self, msg):
        self.viz.text(msg, self.env, opts={'title': 'Message'})

    def heatmap(self):
        raise NotImplementedError()

    def matplot(self, plot, opts):
        self.viz.matplot(plot, opts, self.env)

    def image(self, image, opts):
        if getattr(image, 'is_cuda') and image.is_cuda:
            image = image.cpu()
        # if the object is Variable, But I don't want to have dependency on the dl frame
        # Pytorch
        if 'data' in dir(image):
            image = image.data
        image = image.numpy()
        #dict(title=title, resizeable=True))
        self.viz.image(image, env=self.env, opts=opts)

    def images(self, imgs, title):
        if getattr(imgs, 'is_cuda') and imgs.is_cuda:
            imgs = imgs.cpu()
        if 'data' in dir(imgs):
            imgs = imgs.data
        imgs = imgs.numpy()
        self.viz.images(imgs, env=self.env, opts=dict(title=title))

    def update_plot(self, plt_name, X, Y=None):
        self.plotters[plt_name].log(X, Y)
        if self.save_env:
            self.viz.save([self.env])

    def regis_visdom_logger(self, plot_name, plot_type, opts):
        assert plot_name not in self.plotters, "the plot name already exists"
        plotter = VisdomPlotLogger(plot_type, port=self.port, env=self.env, server=self.server, opts=opts)
        self.plotters[plot_name] = plotter

    def regis_weight_ratio_plot(self, model, layer_index, para_name, logger_name='', caption=''):
        """
        :param layer_index:
        :param para_name:
        :param logger_name:
        :param caption:
        """
        para = get_para(model, layer_index, para_name)
        kwargs = {
            'para': para,
            'env': self.env,
            'logger_name': layer_index + '_' + para_name + '_weightratio' if logger_name == '' else logger_name,
            'server': self.server,
            'caption': caption,
        }
        plotter = WeightRatioVd(**kwargs)
        self.regis_plot(name=logger_name, plotter=plotter)

    def regis_norm_plot(self, model, layer_index, para_name, logger_name='', caption=''):
        """
        :param layer_index:
        :param para_name:
        :param env:
        :param logger_name:
        :param caption:
        """
        para = get_para(model, layer_index, para_name)
        kwargs = {
            'para': para,
            'env': self.env,
            'logger_name': layer_index + '_' + para_name + '_norm' if logger_name == '' else logger_name,
            'server': self.server,
            'caption': caption,
        }
        plotter = NormVd(**kwargs)
        self.regis_plot(name=logger_name, plotter=plotter)

    def regis_mean_std(self, model, layer_index, logger_name='', caption=''):
        layer = get_layer(model, layer_index)
        kwargs = {
            'layer': layer,
            'env': self.env,
            'logger_name': layer_index  + '_meanstd' if logger_name == '' else logger_name,
            'server': self.server,
            'caption': caption,
        }
        plotter = MeanStdVd(**kwargs)
        self.regis_plot(name=logger_name, plotter=plotter)


class TensorboardPlotter(BasePlotter):

    def __init__(self, env):
        """
        Tensorboad Backend Visual tool
        """
        super(TensorboardPlotter, self).__init__()
        self.comment = env  # writer summary name
        self.writer = SummaryWriter(comment=env)

        self.plots = []

    def regis_weight_ratio_plot(self, model, layer_index, para_name, logger_name=''):
        """
        :param layer_index:
        :param para_name:
        :param logger_name:
        :param caption:
        """
        para = get_para(model, layer_index, para_name)
        kwargs = {
            'para': para,
            'env': self.env,
            'logger_name': layer_index + '_' + para_name + '_weightratio' if logger_name == '' else logger_name,
        }
        plotter = WeightRatioTB(**kwargs)
        self.regis_plot(plotter=plotter)

    def regis_norm_plot(self, model, layer_index, para_name, logger_name=''):
        """
        :param layer_index:
        :param para_name:
        :param env:
        :param logger_name:
        :param caption:
        """
        para = get_para(model, layer_index, para_name)
        kwargs = {
            'para': para,
            'env': self.env,
            'logger_name': layer_index + '_' + para_name + '_norm' if logger_name == '' else logger_name,
        }
        plotter = NormTB(**kwargs)
        self.regis_plot(plotter=plotter)

    def regis_mean_std(self, model, layer_index, logger_name=''):
        layer = get_layer(model, layer_index)
        kwargs = {
            'layer': layer,
            'env': self.env,
            'logger_name': layer_index  + '_meanstd' if logger_name == '' else logger_name,
        }
        plotter = MeanStdTB(**kwargs)
        self.regis_plot(plotter=plotter)



####### Visdom ########
class WeightRatioVd(object):
    def __init__(self, para, env, logger_name, server, caption=''):
        self.para = para
        self.para.register_hook(lambda grad: grad)
        self.logger = VisdomPlotLogger('line', env=env, server=server,
                                       opts={'title': caption + '\n' + logger_name, 'caption': caption})
        self.iter_n = 0

    def plot(self):
        eps = 1e-6
        ratio = torch.norm(self.para.grad.data, 2) / torch.norm(self.para.data + eps, 2)
        self.logger.log(self.iter_n, ratio)
        self.iter_n += 1


class MeanStdVd(object):
    """ plot the mean and std of the layer output """

    def __init__(self, layer, env, logger_name, server, caption):
        self.layer = layer
        self.layer.register_forward_hook(hook_forward)
        self.mean_logger = VisdomPlotLogger('line', env=env, server=server,
                                            opts={'title': 'mean_' + caption + logger_name, 'caption': caption})
        self.std_logger = VisdomPlotLogger('line', env=env, server=server,
                                           opts={'title': 'std_' + caption + logger_name, 'caption': caption})
        self.iter_n = 0

    def plot(self):
        mean = torch.mean(self.layer.out_)
        std = torch.std(self.layer.out_)
        del self.layer.out_
        self.mean_logger.log(self.iter_n, mean)
        self.std_logger.log(self.iter_n, std)
        self.iter_n += 1


class NormVd(object):
    def __init__(self, para, env, logger_name, caption=''):
        self.para = para
        self.logger = VisdomPlotLogger('line', env=env,
                                       opts={'title': 'norm_' + caption + logger_name, 'caption': caption})
        self.iter_n = 0

    def plot(self):
        self.logger.log(self.iter_n, torch.mean(self.para.data ** 2))
        self.iter_n += 1


####### Tensorboard ########
class WeightRatioTB(object):
    def __init__(self, para, logger_tag):
        # import pdb;pdb.set_trace()
        self.para = para
        self.para.register_hook(lambda grad: grad)
        self.logger_tag = logger_tag
        self.iter_n = 0

    def plot(self, writer):
        eps = 1e-6

        ratio = torch.norm(self.para.grad.data, 2) / torch.norm(self.para.data + eps, 2)

        writer.add_scalar(self.logger_tag, ratio, self.iter_n)

        self.iter_n += 1


class MeanStdTB(object):
    """ plot the mean and std of the layer output """

    def __init__(self, layer, logger_tag):
        self.layer = layer
        self.layer.register_forward_hook(hook_forward)

        self.mean_logger_tag = 'mean_' + logger_tag
        self.std_logger_tag = 'std_' + logger_tag

        self.iter_n = 0

    def plot(self, writer):
        mean = torch.mean(self.layer.out_)
        std = torch.std(self.layer.out_)
        del self.layer.out_
        writer.add_scalar(self.mean_logger_tag, mean, self.iter_n)
        writer.add_scalar(self.std_logger_tag, std, self.iter_n)

        self.iter_n += 1


class NormTB(object):
    def __init__(self, para, logger_tag):
        self.para = para
        self.logger_tag = logger_tag
        # self.logger = VisdomPlotLogger('line', env=env, opts={'title': 'norm_' + caption + logger_name, 'caption': caption})
        self.iter_n = 0

    def plot(self, writer):
        writer.add_scalar(self.logger_tag, torch.mean(self.para.data ** 2), self.iter_n)

        self.iter_n += 1


# class TensorboardManager(object):
#     def __init__(self, model, comment):
#         self.model = model
#         self.comment = comment
#         self.comment_list = []
#
#         if comment in self.comment_list:
#             print("====================You have use this comment before==========================")
#         else:
#             self.comment_list.append(comment)

##### Manager #####


class VisualManager(object):
    def __init__(self):
        self.viz_dict = {}

    def create_tensorboard_viz(self, name, comment=''):
        viz = TensorboardPlotter(comment)
        assert name not in self.viz_dict, "Visual Manager: the name in viz_dict already exist"
        self.viz_dict[name] = viz

    def create_visdom_viz(self, name, env, port, server, save_env=True):
        viz = VisdomPlotter(env, server, port, save_env)
        assert name not in self.viz_dict, "Visual Manager: the name in viz_dict already exist"
        self.viz_dict[name] = viz


def get_viz(name=None):
    name = name if name else 'root'
    return viz_manager.viz_dict[name]


def create_viz(name, env='debug', port=8097, server='http://localhost', backend='visdom', save_env=True):
    name = name if name else 'root'
    if backend == 'visdom':
        viz_manager.create_visdom_viz(name, env, port, server, save_env)
    elif backend == 'tensorboard':
        # TODO: Add port para to make tensorboard support port configuration
        viz_manager.create_tensorboard_viz(name, env)
    else:
        raise ValueError("viz type is wrong. Neither visdom nor tensorboard")

    return get_viz(name)


viz_manager = VisualManager()