import numpy as np


# a:activation
# b:bias
# w:weight
# z:a=g(z)
class NetWork:
    def __init__(self, learning_rate=0.5):
        np.random.seed(1)
        self.layers = []
        self.w_all = []
        self.b_all = []
        self.lr = learning_rate
        self.init_flag = False

    def check_init(self):
        assert self.init_flag is True, "神经网络未初始化"

    def train_check(self, x_batch, y_batch):
        assert x_batch is not None, "input为空"
        assert y_batch is not None, "label为空"
        assert len(self.layers) > 0, "未搭建神经网络"
        assert len(x_batch[0]) is self.layers[0].units, "输入参数形状与输入层不符"
        assert len(y_batch[0]) is self.layers[-1].units, "label形状与输出层不符"
        self.check_init()

    def predict_check(self, x_batch):
        assert x_batch is not None, "input为空"
        assert len(self.layers) > 0, "未搭建神经网络"
        assert len(x_batch[0]) is self.layers[0].units, "输入参数形状与输入层不符"
        self.check_init()

    def relu(self, x):
        pass

    def relu_gradient(self, z):
        pass

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_gradient(self, z):
        g = np.multiply(self.sigmoid(z), (1 - self.sigmoid(z)))
        return g

    def init_all_var(self):
        for i in range(len(self.layers)):
            layer = self.layers[i]
            if i is not 0:
                if isinstance(layer, Dense):
                    # 初始化权重为-1至1的随机数
                    w = np.random.rand(layer.units, self.layers[i - 1].units) * 2 - 1
                    b = np.random.rand(layer.units) * 2 - 1
                    self.w_all.append(w)
                    self.b_all.append(np.vstack(b))
        self.init_flag = True

    def add_layer(self, layer):
        self.layers.append(layer)

    def fit(self, x_batch, y_batch):
        self.train_check(x_batch, y_batch)
        x_batch = np.array(x_batch)
        y_batch = np.array(y_batch)
        h_total = np.zeros((x_batch.shape[0], self.layers[-1].units))
        # 所有参数的偏导数
        D_w = [np.zeros(self.w_all[i].shape) for i in range(len(self.w_all))]
        D_b = [np.zeros(self.b_all[i].shape) for i in range(len(self.b_all))]
        m, n = x_batch.shape
        for i in range(x_batch.shape[0]):
            a_all = []
            z_all = []
            x = np.vstack(x_batch[i].T)
            y = np.vstack(y_batch[i].T)
            # 前向传播
            for j in range(len(self.layers)):
                if j is 0:
                    a_all.append(x)
                    z_all.append(x)
                else:
                    w = self.w_all[j - 1]
                    b = self.b_all[j - 1]
                    a_before = a_all[j - 1]
                    z = np.matmul(w, a_before) + b
                    a = self.sigmoid(z)
                    z_all.append(z)
                    a_all.append(a)
            # 预测值为最后一个a
            h = a_all[-1]
            h_total[i] = h.T
            # 反向传播
            # 最后一层误差
            delta = h - y
            D_w[-1] += np.matmul(delta, a_all[-2].T)
            D_b[-1] += delta
            for j in reversed(range(0, len(self.w_all) - 1)):
                # 后一层的误差
                delta = np.multiply(np.matmul(self.w_all[j + 1].T, delta), self.sigmoid_gradient(z_all[j + 1]))
                D_w[j] += np.matmul(delta, a_all[j].T)
                D_b[j] += delta

        w_grad = [np.array(D_w[i]) / m for i in range(len(self.w_all))]
        b_grad = [np.array(D_b[i]) / m for i in range(len(self.b_all))]
        for i in range(len(self.w_all)):
            self.w_all[i] -= self.lr * w_grad[i]
            self.b_all[i] -= self.lr * b_grad[i]
        J = np.mean(-y_batch * np.log(h_total) - (np.array([[1]]) - y_batch) * np.log(1 - np.array(h_total)))
        return J, h_total

    def predict(self, x_batch):
        self.predict_check(x_batch)
        x_batch = np.array(x_batch)
        h_total = np.zeros((x_batch.shape[0], self.layers[-1].units))
        # 所有参数的偏导数
        D_w = [np.zeros(self.w_all[i].shape) for i in range(len(self.w_all))]
        D_b = [np.zeros(self.b_all[i].shape) for i in range(len(self.b_all))]
        m, n = x_batch.shape
        for i in range(x_batch.shape[0]):
            a_all = []
            z_all = []
            x = np.vstack(x_batch[i].T)
            # 前向传播
            for j in range(len(self.layers)):
                if j is 0:
                    a_all.append(x)
                    z_all.append(x)
                else:
                    w = self.w_all[j - 1]
                    b = self.b_all[j - 1]
                    a_before = a_all[j - 1]
                    z = np.matmul(w, a_before) + b
                    a = self.sigmoid(z)
                    z_all.append(z)
                    a_all.append(a)
            # 预测值为最后一个a
            h = a_all[-1]
            h_total[i] = h.T
        return h_total


class Layer:
    def __init__(self, units):
        self.units = units


class Dense(Layer):
    def __init__(self, units):
        super().__init__(units)
