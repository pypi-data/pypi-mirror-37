import sys
sys.path.insert(0, '../../')
sys.path.insert(0, '../')
sys.path.insert(0, './')

print(sys.path)

from plus.visual import Plotter


class TestVisdom(object):
    """
    How to run this program:
     python -m Venus.test.test_visual
    """
    def __init__(self):
        self.plotter = Plotter(env='test', server='localhost', port=8888, type='visdom')

    def test_double_plot(self):
        for i in range(20):
            self.plotter.plot_train_test_loss([i,i], [i-2,i+2])

    def test(self):
        self.test_double_plot()


if __name__ == '__main__':

    visdom = TestVisdom()
    visdom.test_double_plot()
