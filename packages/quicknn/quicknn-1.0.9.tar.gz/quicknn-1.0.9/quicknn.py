import tensorflow as tf
import numpy as np
import pandas as pd
from functools import partial
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from qnn_config import TF_SAVER, logdir


class QuickNN:
    """
An implementation of Feedforward Neural Networks for quick applications.

    model_name : string, optional (default='nn')
        This string will be the name of the folder in which the model will be saved. The default is 'qnn'.

    list_neurons : list of integers
        List in which each integer except for the last, represent the dimension of a hidden layer.
        The last represents the dimension of the output layer.

    save_dir : string, optional (default='default')
        Path to the save directory, in which checkpoints of the model will be save.
        The default is Path(os.getenv("HOME")) / '.local' / 'share' / 'quicknn'

    activation : function, optional (default=tf.nn.relu)
        The activation function for each hidden layer.

    initializer : function, optional (default=tf.truncated_normal_initializer)
        The function that indicates the way in which each weight of the network will be initialized.

    training_func : function, optional (default=tf.train.GradientDescentOptimizer)
        The optimization algorithm gradient based, to minimize the cost function.

    problem : str, optional (default='regression')
        The type of the problem: whether of regression or classification.
    """
    def __init__(self, model_name='qnn', list_neurons=None, save_dir='default',
                 activation=tf.nn.relu, initializer=tf.truncated_normal_initializer,
                 training_func=tf.train.GradientDescentOptimizer, problem='regression'):

        self.model_name = model_name
        self.list_neurons = list_neurons
        self.activation = activation
        self.initializer = initializer
        self.training_func = training_func
        self.problem = problem

        if save_dir != 'default':
            self.save_path = save_dir / '{0}'.format(self.model_name)
        else:
            save_dir_temp = (TF_SAVER / '{0}'.format(self.model_name))
            save_dir_temp.mkdir_p()
            self.save_path = TF_SAVER / '{0}'.format(self.model_name) / '{0}'.format(self.model_name)

        if self.problem == 'classification':
            self._training_name = 'train_accuracy'
            self._validation_name = 'val_accuracy'
            self._loss_name = 'accuracy'
        else:
            assert self.problem == 'regression'
            self._training_name = 'training_loss'
            self._validation_name = 'validation_loss'
            self._loss_name = 'loss'

        self.training = True
        self._flag_first_run = True
        self._step = 0
        self._epoch = 1
        self.learning_rate = None
        self._X = None
        self._y = None
        self.X = None
        self.y = None
        self.X_val = None
        self.X_val = None
        self._training_op = None
        self._loss = None
        self._sess = None
        self._init_op = None
        self._saver = None
        self._writer = None
        self._loss_summary = None
        self._loss_summary_train = None
        self._loss_summary_val = None
        self._flag_categories = None
        self._training = None
        self._metric = None
        self.outputs = None
        self.validation = None
        self.features = None
        self.n_features = None
        self.n_examples = None
        self.cat_cols = None
        self.ohe = None
        self.func_y = None
        self.inv_func_y = None
        self.restore_prev = None
        self.list_dropout_rate = None
        self.batch_size = None
        self.n_epochs = None
        self.loss_func = None
        self.metric_func = None

    def fit(self, X, y, batch_size=16, n_epochs=5, learning_rate=0.001, list_dropout_rate=None,
            validation=None, test_size=0.15, func_y=None, inv_func_y=None, restore_prev=None, metric=None):
        """
Trains the model.

        To handling categorical variables, is required to feed X parameter with a pandas.DataFrame object,
        in which dtypes of categorical columns are all 'object'. The method fit will recognize it and than
        transform it with numerical encode. The model will feed with one-hot-encode transformation in batches
        of the training set provided.

        Parameters
        ----------
        X : array-like, shape=(n_examples, n_features)

        y : array-like, shape=(n_examples, [1]), the second dimension is optional.

        batch_size : integer, optional (default=32)
            The number of examples per iteration that will feed the neural network.

        n_epochs : integer, optional (default=100)
            The number of epochs, or how many times the model will see the whole training set in average.

        learning_rate : float between 0 and 1, optional (default=0.001)
            Learning rate of the optimizer operation.

        list_dropout_rate: list of float between 0 and 1, optional (default=None)
            List in which each number indicates the dropout rate of each layer from the input to the last hidden layer.
            It must have the same length of list_neurons.

        validation : bool, optional (default=None)
           Flag option for validation that if set to True the model training is done only on a part of the data.
           The default value is set to False.

        test_size : float between 0 and 1, optional (default=0.15)
           Test size ratio of the whole training set feed to X parameter to validate the model if validation param is
           set to True.

        func_y : function, optional (default=None)
           A function to map y. If set, it requires the inverse function to validate the results.

        inv_func_y : function, optional (default=None)
           The inverse function of the function feed to func_y parameter.

        restore_prev : bool, optional (default=None)
           Restore the model of the previous checkpoint.

        metric : function, optional (default=None)
           The function to evaluate the model and compare with others.
        """

        self.batch_size = batch_size
        self.n_epochs = n_epochs
        self.learning_rate = learning_rate
        self.validation = validation
        self.func_y = func_y
        self.inv_func_y = inv_func_y
        self.restore_prev = restore_prev
        self.list_dropout_rate = list_dropout_rate
        self.metric_func = metric

        if self._flag_first_run:
            self.X = X
            self.y = y
            self._check_pandas()
            self._check_validation(test_size)
            self._flag_first_run = None
        else:
            if not self.validation:
                self.X = X
                self.y = y
            self._check_pandas_not_first_run()

        self._check_func_y()
        self._make_graph()

        with tf.Session() as self._sess:
            self._global_initializer()
            self._train()
            self._saver.save(self._sess, self.save_path, global_step=self._step)

    def _check_pandas(self):

        if isinstance(self.X, pd.DataFrame):
            self.features = self.X.columns.tolist()
            self._check_categories()
            self.X = self.X.values
        else:
            self.n_features = self.X.shape[1]

        if isinstance(self.y, pd.DataFrame):
            self.y = self.y.values
        elif isinstance(self.y, pd.Series):
            self.y = self.y.values

        self.y = np.expand_dims(self.y, axis=1) if len(self.y.shape) == 1 else self.y

    def _check_categories(self):

            if not self._flag_categories:
                self.cat_cols = self.X.select_dtypes(include='O').columns.tolist()
                if self.cat_cols:
                    self._fit_ohe()
                else:
                    self.n_features = self.X.shape[1]

            if self.cat_cols:
                self._flag_categories = True
            else:
                self.n_features = self.X.shape[1]

    def _fit_ohe(self):

        self.X[self.cat_cols] = self.X.select_dtypes('O').apply(lambda col: col.astype('category').cat.codes)
        self.n_features = self.X[self.cat_cols].nunique().sum() + self.X.shape[1] - len(self.cat_cols)
        cat_cols_crit = self._make_cat_cols_crit()
        self.ohe = OneHotEncoder(categorical_features=cat_cols_crit, sparse=False)
        self.ohe.fit(self.X)

    def _make_cat_cols_crit(self):
        cat_cols_crit = []
        for col in self.features:
            if col in self.cat_cols:
                cat_cols_crit.append(True)
            else:
                cat_cols_crit.append(False)
        return cat_cols_crit

    def _check_func_y(self):

        if self.func_y is not None:
            self.y = self.func_y(self.y)

    def _check_validation(self, test_size):

        if self.validation:
            self.X, self.X_val, self.y, self.y_val = train_test_split(self.X, self.y, test_size=test_size)

            if self.cat_cols:
                self.X_val = self.ohe.transform(self.X_val)

    def _check_pandas_not_first_run(self):
        if isinstance(self.X, pd.DataFrame):
            self.X = self.X.values

        if isinstance(self.y, pd.DataFrame):
            self.y = self.y.values
        elif isinstance(self.y, pd.Series):
            self.y = self.y.values

        self.y = np.expand_dims(self.y, axis=1) if len(self.y.shape) == 1 else self.y

    def _make_graph(self):

        tf.reset_default_graph()

        self._make_placeholder()
        self._make_layers()
        self._make_loss()
        self._make_training_op()
        self._make_init_op()

    def _make_placeholder(self):

        self._X = tf.placeholder('float', (None, self.n_features), name="X")

        if self.problem == 'regression':
            self._y = tf.placeholder(tf.float32, None, name="y")
        else:
            assert self.problem == 'classification'
            self._y = tf.placeholder(tf.int32, None, name="y")

        self._training = tf.placeholder_with_default(input=False, shape=(), name="training_flag")

    def _make_layers(self):

        make_layer = partial(tf.layers.dense,
                             kernel_initializer=self.initializer,
                             activation=self.activation)

        self._check_dropout()
        drop_op = tf.layers.dropout(self._X, rate=self.list_dropout_rate[0], training=self._training)

        for num, (neurons, drop_rate) in enumerate(zip(self.list_neurons[:-1], self.list_dropout_rate[1:])):
            layer_temp = make_layer(inputs=drop_op, units=neurons,
                                    name="hidden_{0}".format(num))
            drop_op = tf.layers.dropout(layer_temp, rate=drop_rate, training=self._training)

        self.outputs = make_layer(inputs=drop_op, units=self.list_neurons[-1], name="outputs", activation=None)

    def _check_dropout(self):

        if self.list_dropout_rate is not None:
            assert len(self.list_neurons) == len(self.list_dropout_rate)
            assert 1 not in self.list_dropout_rate

            for i in range(len(self.list_dropout_rate)):
                if self.list_dropout_rate[i] == 0:
                    self.list_dropout_rate[i] = 1e-7

        else:
            self.list_dropout_rate = [1e-7] * len(self.list_neurons)

    def _make_loss(self):

        self._check_loss_func()
        self._loss = self.loss_func(self._y, self.outputs)
        self._check_metric_func()
        self._check_loss_options()

    def _check_loss_func(self):
        if self.problem == 'regression':
            self.loss_func = partial(tf.losses.mean_squared_error,
                                     reduction=tf.losses.Reduction.MEAN)
        else:
            assert self.problem == 'classification'
            self.loss_func = self._clf_loss

    @staticmethod
    def _clf_loss(y_true, y_pred):
        xentropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=tf.squeeze(y_true), logits=y_pred)
        clf_loss = tf.reduce_mean(xentropy)
        return clf_loss

    def _check_metric_func(self):

        if self.problem == 'regression':
            if self.metric_func == 'mse':
                self.metric_func = partial(tf.losses.mean_squared_error, reduction=tf.losses.Reduction.MEAN)
            elif self.metric_func == 'rmse':
                self.metric_func = self._root_mean_squared_error
            else:
                self.metric_func = self.loss_func
        else:
            assert self.problem == 'classification'
            self.metric_func = self._accuracy

        self._metric = self.metric_func(self._y, self.outputs)

    @staticmethod
    def _root_mean_squared_error(y_true, y_pred):
        return tf.sqrt(tf.reduce_mean(tf.square(y_true - y_pred)))

    @staticmethod
    def _accuracy(y_true, y_pred):
        correct = tf.nn.in_top_k(predictions=y_pred, targets=tf.squeeze(y_true), k=1)
        return tf.reduce_mean(tf.cast(correct, tf.float32))

    def _check_loss_options(self):

        if self.validation:
            if self.inv_func_y is not None:

                self._loss_train_exp = self.metric_func(self.inv_func_y(self._y), self.inv_func_y(self.outputs))

                self._loss_val_exp = self.metric_func(self._y, self.inv_func_y(self.outputs))

                self._loss_summary_train = tf.summary.scalar(f"{self._training_name}", self._loss_train_exp)
                self._loss_summary_val = tf.summary.scalar(f"{self._validation_name}", self._loss_val_exp)
            else:
                self._loss_summary_train = tf.summary.scalar(f"{self._training_name}", self._metric)
                self._loss_summary_val = tf.summary.scalar(f"{self._validation_name}", self._metric)
        else:
            if self.inv_func_y is not None:
                self._loss_exp = self.metric_func(self.inv_func_y(self._y), self.inv_func_y(self.outputs))

            else:
                self._loss_summary = tf.summary.scalar("loss", self._metric)

    def _make_training_op(self):

        with tf.name_scope("training_operation"):
            self._training_op = self.training_func(learning_rate=self.learning_rate).minimize(self._loss)

    def _make_init_op(self):

        self._init_op = tf.global_variables_initializer()
        self._writer = tf.summary.FileWriter(logdir, tf.get_default_graph())
        self._saver = tf.train.Saver(max_to_keep=2)

    def _global_initializer(self):

        self._sess.run(self._init_op)

        if self.restore_prev:
            self._saver.restore(self._sess, tf.train.latest_checkpoint(self.save_path.parent))

    def _train(self):

        starting_epoch = self._epoch

        for epoch in range(starting_epoch, self.n_epochs + 1):

            self._iteration(epoch)

            self._saver.save(self._sess, self.save_path, global_step=self._epoch)
            self._epoch += 1

    def _iteration(self, epoch):

        self._data_shuffler()

        generator = (_ for _ in self._gen_batches())

        loss_temp, loss_temp_train, loss_temp_val = [], [], []

        for batch in generator:
            self._step += 1

            X_batch, y_batch = batch

            if self._flag_categories:
                X_batch = self.ohe.transform(X_batch)

            self._summary_evaluation(X_batch, y_batch)

            self._sess.run(self._training_op, feed_dict={self._X: X_batch, self._y: y_batch,
                                                         self._training: self.training})

            if self.validation:
                if self.inv_func_y is not None:
                    loss_temp_train.append(self._loss_train_exp.eval(feed_dict={self._X: X_batch, self._y: y_batch,
                                                                                self._training: self.training}))
                    loss_temp_val.append(self._loss_val_exp.eval(feed_dict={self._X: self.X_val, self._y: self.y_val}))
                else:
                    loss_temp_train.append(self._metric.eval(feed_dict={self._X: X_batch, self._y: y_batch,
                                                                        self._training: self.training}))
                    loss_temp_val.append(self._metric.eval(feed_dict={self._X: self.X_val, self._y: self.y_val}))

            else:
                if self.inv_func_y is not None:
                    loss_temp.append(self._loss_train_exp.eval(feed_dict={self._X: X_batch, self._y: y_batch,
                                                                          self._training: self.training}))
                else:
                    loss_temp.append(self._metric.eval(feed_dict={self._X: X_batch, self._y: y_batch,
                                                                  self._training: self.training}))

        if self.validation:
            print("Epoch:", epoch, "|",
                  f"{self._training_name}:", np.mean(loss_temp_train), "|",
                  f"{self._validation_name}:", np.mean(loss_temp_val))
        else:
            print("Epoch:", epoch, "|", f"{self._loss_name}:", np.mean(loss_temp))

    def _data_shuffler(self):

        self.n_examples = self.y.shape[0]

        p = np.random.permutation(self.n_examples)

        self.X, self.y = self.X[p], self.y[p]

    def _gen_batches(self):

        assert self.n_examples >= self.batch_size, "batch size must be equal or lower than number of observations"

        for i in range(0, self.n_examples - self.n_examples % self.batch_size, self.batch_size):
            yield self.X[i:i + self.batch_size], self.y[i:i + self.batch_size]

    def _summary_evaluation(self, X_batch, y_batch):

        if self.validation:
            loss_summary_train_eval = self._loss_summary_train.eval(feed_dict={self._X: X_batch, self._y: y_batch,
                                                                               self._training: self.training})
            loss_summary_val_eval = self._loss_summary_val.eval(feed_dict={self._X: self.X_val, self._y: self.y_val})
            self._writer.add_summary(loss_summary_train_eval, self._step)
            self._writer.add_summary(loss_summary_val_eval, self._step)

        else:
            loss_summary_eval = self._loss_summary.eval(feed_dict={self._X: X_batch, self._y: y_batch,
                                                                   self._training: self.training})
            self._writer.add_summary(loss_summary_eval, self._step)

    def predict(self, X):
        """
Return the predicted values for each example provide.

        X : array-like, shape=(n_examples, n_features)

        return : one dimensional array with shape=(n_examples, [1])
        """
        if self._flag_categories:
            X = self.ohe.transform(X)

        with tf.Session() as self._sess:
            self._saver.restore(self._sess, tf.train.latest_checkpoint(self.save_path.parent))
            outputs = self.outputs.eval(feed_dict={self._X: X})

        if self.problem == 'classification':
            return outputs
        else:
            assert self.problem == 'regression'
            return np.ravel(outputs)
