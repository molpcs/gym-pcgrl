import tensorflow as tf
from tensorflow.keras import layers
from gym import spaces
import numpy as np

from stable_baselines.common.policies import ActorCriticPolicy, FeedForwardPolicy
from stable_baselines.common.distributions import CategoricalProbabilityDistributionType, ProbabilityDistributionType, CategoricalProbabilityDistribution, ProbabilityDistribution
from stable_baselines.a2c.utils import conv, linear, conv_to_fc



def Cnn(image, **kwargs):
    activ = tf.nn.relu
    layer_1 = activ(conv(image, 'c1', n_filters=32, filter_size=3, stride=2, init_scale=np.sqrt(2), **kwargs)) # filter_size=3
    layer_2 = activ(conv(layer_1, 'c2', n_filters=64, filter_size=3, stride=2, init_scale=np.sqrt(2), **kwargs)) #filter_size = 3
    layer_3 = activ(conv(layer_2, 'c3', n_filters=64, filter_size=3, stride=1, init_scale=np.sqrt(2), **kwargs))
    layer_3 = conv_to_fc(layer_3)
    return activ(linear(layer_3, 'fc1', n_hidden=512, init_scale=np.sqrt(2)))


def FullyConv(image, n_tools, **kwargs):
    # legacy accident, ran with regular Categorical dist.
    activ = tf.nn.relu
    x = activ(conv(image, 'c1', n_filters=32, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c2', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c3', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
   #return x # if we're using stable_baselines' FeedForwardPolicy, for example
    act = conv_to_fc(x)
  # val = activ(conv(x, 'v1', n_filters=64, filter_size=3, stride=2,
  #     init_scale=np.sqrt(2)))
  # val = activ(conv(val, 'v2', n_filters=64, filter_size=3, stride=2,
  #     init_scale=np.sqrt(3)))
  ##val = activ(conv(val, 'v3', n_filters=64, filter_size=3, stride=2,
  ##    init_scale=np.sqrt(2)))
  # val = activ(conv(val, 'v4', n_filters=1, filter_size=1, stride=1,
  #     init_scale=np.sqrt(2)))
    val = conv_to_fc(x)
    return act, val


def FullyConv2(image, n_tools, **kwargs):
    activ = tf.nn.relu
    x = activ(conv(image, 'c1', n_filters=32, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c2', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c3', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c4', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c5', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c6', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c7', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c8', n_filters=n_tools, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
   #return x
    act = conv_to_fc(x)
    val = activ(conv(x, 'v1', n_filters=64, filter_size=3, stride=2,
        init_scale=np.sqrt(2)))
    val = activ(conv(val, 'v2', n_filters=64, filter_size=3, stride=2,
        init_scale=np.sqrt(3)))
   #val = activ(conv(val, 'v3', n_filters=64, filter_size=3, stride=2,
   #    init_scale=np.sqrt(2)))
    val = activ(conv(val, 'v4', n_filters=64, filter_size=1, stride=1,
        init_scale=np.sqrt(2)))
    val = conv_to_fc(val)
    return act, val


def FullyConvFix(image, **kwargs):
    activ = tf.nn.relu
    x = activ(conv(image, 'c1', n_filters=32, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c2', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c3', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c4', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
    x = activ(conv(x, 'c5', n_filters=64, filter_size=3, stride=1,
        pad='SAME', init_scale=np.sqrt(2)))
   #return x
    act = conv_to_fc(x)
    return act, val


def ValShrink(val, **kwargs):
    val = activ(conv(x, 'v1', n_filters=64, filter_size=3, stride=2,
        init_scale=np.sqrt(2)))
    val = activ(conv(val, 'v2', n_filters=64, filter_size=3, stride=2,
        init_scale=np.sqrt(3)))
    val = activ(conv(val, 'v3', n_filters=64, filter_size=3, stride=2,
        init_scale=np.sqrt(2)))
    val = activ(conv(val, 'v4', n_filters=64, filter_size=1, stride=1,
        init_scale=np.sqrt(2)))
    val = conv_to_fc(val)
    return val


def FractalNet(image, n_tools, n_recs, blocks=[64], **kwargs):
    '''
     - blocks: a list, ordered from network in to out, of each block's n_chan
    '''
    x = layers.Conv2D(blocks[0], 1, 1, activation='relu')(image) # embedding
    for n_chan in blocks:
        x = FractalBlock(x, n_chan)
    act = layers.Conv2D(n_tools, 1, 1, activation='relu')(x)
    act = conv_to_fc(act)
    val = ValShrink(x)
    return act, val


def FractalBlock(image, n_recs, n_chan, **kwargs):
    x = layers.Conv2D(n_chan, 1, 1, activation='relu')(image) # embed
    child = None
    for i in ranve(n_recs):
        child = SubFractal(child, n_chan, **kwargs)
    x = child(x)
    return x


class SubFractal(tf.Module):
    def __init__(self, child, n_chan, **kwargs):
        '''
            -child: a SubFractal
        '''
        self.child = child
        self.skip = layers.Conv2D(n_chan, 3, 1, padding='same', activation='relu')


    def __call__(self, x):
        x = self.skip(x)
        if self.child:
            x_body = self.child(self.child(x))
            x = x + x_body
        return x


class NoDenseCategoricalProbabilityDistributionType(ProbabilityDistributionType):
    def __init__(self, n_cat):
        """
        The probability distribution type for categorical input

        :param n_cat: (int) the number of categories
        """
        self.n_cat = n_cat

    def probability_distribution_class(self):
        return CategoricalProbabilityDistribution

    def proba_distribution_from_latent(self, pi_latent_vector, vf_latent_vector, init_scale=1.0, init_bias=0.0):
        pdparam = pi_latent_vector
        q_values = vf_latent_vector
        return self.proba_distribution_from_flat(pdparam), pdparam, q_values

    def param_shape(self):
        return [self.n_cat]

    def sample_shape(self):
        return []

    def sample_dtype(self):
        return tf.int64


class FullyConvPolicy(ActorCriticPolicy):
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, **kwargs):
        super(FullyConvPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, **kwargs)
        n_tools = int(ac_space.n / (ob_space.shape[0] * ob_space.shape[1]))
        self._pdtype = NoDenseCategoricalProbabilityDistributionType(ac_space.n)
        with tf.variable_scope("model", reuse=kwargs['reuse']):
            pi_latent, vf_latent = FullyConv2(self.processed_obs, n_tools, **kwargs)
            self._value_fn = linear(vf_latent, 'vf', 1)
            self._proba_distribution, self._policy, self.q_value = \
                self.pdtype.proba_distribution_from_latent(pi_latent, vf_latent, init_scale=0.01)
        self._setup_init()

    def step(self, obs, state=None, mask=None, deterministic=False):
        if deterministic:
            action, value, neglogp = self.sess.run([self.deterministic_action, self.value_flat, self.neglogp],
                                                   {self.obs_ph: obs})
        else:
            action, value, neglogp = self.sess.run([self.action, self.value_flat, self.neglogp],
                                                   {self.obs_ph: obs})
        return action, value, self.initial_state, neglogp

    def proba_step(self, obs, state=None, mask=None):
        return self.sess.run(self.policy_proba, {self.obs_ph: obs})

    def value(self, obs, state=None, mask=None):
        return self.sess.run(self.value_flat, {self.obs_ph: obs})


class CustomPolicy(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomPolicy, self).__init__(*args, **kwargs, cnn_extractor=Cnn, feature_extraction="cnn")

