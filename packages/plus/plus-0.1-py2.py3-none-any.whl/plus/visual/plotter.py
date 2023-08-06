from .visual import create_viz
import collections
import numpy as np
TORCH_INSTALLED = True
try:
    import torch
except Exception:
    TORCH_INSTALLED = False


def _convert_data_to_nparray(X):
    if isinstance(X, torch.Tensor):
        X = X.detach().cpu().numpy()
    elif isinstance(X, list):
        X = np.array(X)
    return X


class Plotter(object):
    """
        The highest abstraction for plotter(visualization)

        0. Support different backends including visdom, tensorboard(not implemented)
        1. Plot the metrics such as train/val loss, accuracy, etc.
        2. support image, heatmap

        Usage:

    """
    ALLOWABLE_PLOT_TYPES = ['line', 'scatter']

    def __init__(self, name, env, server='localhost', port=8097, backend='visdom', save_env=True):
        super(Plotter, self).__init__()

        self.name = name
        self.backend = backend
        self.env = env
        self.server = server
        self.port = port
        self.save_env = save_env

        if backend == 'visdom' or backend == 'tensorboard':
            self._plotter = create_viz(name, env, port, server, backend, save_env)
        else:
            raise ValueError("viz type is wrong. Neither visdom nor tensorboard")

    def _legalize_data(self, X):
        """
        if X is a scaler, the output is a one-dim (np array|tensor)
        :param X:
        :return:
        """
        if isinstance(X, np.ndarray):
            if np.isscalar(X):
                X = X[np.newaxis]
        elif TORCH_INSTALLED and isinstance(X, torch.Tensor):
            if len(X.size())==0:
                X = X.unsqueeze(0)
        elif isinstance(X, int) or isinstance(X, float):
                X = np.array([X])
        return X

    def _legalize_opts(self, opts, plot_name):

        if not opts:
            opts={'title': plot_name}
        elif isinstance(opts, dict):
            if 'title' not in opts:
                opts.setdefault('title', plot_name)
        else:
            raise ValueError()
        return opts

    def register_plot_type(self, plot_name, plot_type, opts=None):
        assert plot_type in self.ALLOWABLE_PLOT_TYPES

        opts = self._legalize_opts(opts, plot_name)

        if self.backend == 'visdom':
            self._plotter.regis_visdom_logger(plot_name, plot_type, opts)
        else:
            raise NotImplementedError()

    def update_plot(self, plot_name, X, Y=None):
        """Update line/scatter plot

        Args:
            plot_name(str) : the plot name registered before.
            x(Tensor|np.ndarray|scalar): (N*K) OR (N,) \
            N is the number of points will be ploted in each plot. K is the number of plots
            y(Tensor|scalar|np.ndarray): Shape: (N*K) Or (N,)

        """
        X, Y = self._legalize_data(X), self._legalize_data(Y)
        self._plotter.update_plot(plot_name, X, Y)

    def image(self, *args, **kwargs):
        """This function draws an img. It takes as input an `CxHxW` or `HxW` tensor \
        `img` that contains the image. The array values can be float in [0,1] or \
        uint8 in [0, 255]

        Args:
            img(np.ndarray|Tensor) : the image to plot
            win(str): the window
                default: None
            env: the environment
                default: None
            opts: default: None the options

        """
        self._plotter.image(*args, **kwargs)

    def images(self, imgs, opts=None):
        """Given a 4D tensor of shape (B x C x H x W), \
        or a list of images all of the same size, makes a grid of images of size (B / nrow, nrow). \
        This is a modified from `make_grid()` https://github.com/pytorch/vision/blob/master/torchvision/utils.py

        Args:
            imgs(Tensor|np.ndarray): (B x C x H x W)
            opts(dict):
        """
        opts = self._legalize_opts(opts)
        self._plotter.images(imgs, opts)

    def heatmap(self, *args, **kwargs):
        self._plotter.heatmap(*args, **kwargs)

    

class PlotterManager(object):
    def __init__(self):
        self.plt_dict = {}

    def create_plotter(self, name, env, server, port, backend, save_env, plotter_cls=Plotter):
        plotter = plotter_cls(name, env, server, port, backend, save_env)
        assert name not in self.plt_dict, "Plotter Manager: the name in plt_dict already exist"
        self.plt_dict[name] = plotter
        return plotter


def get_plotter(name=None):
    name = name if name else 'root'
    return plt_manager.plt_dict.get(name, None)


def create_plotter(name, env, server='localhost', port=8097, backend='visdom', save_env=True, plotter_cls=Plotter):
    name = name if name else 'root'

    plotter = plt_manager.create_plotter(name, env, server, port, backend, save_env, plotter_cls)

    return plotter


plt_manager = PlotterManager()