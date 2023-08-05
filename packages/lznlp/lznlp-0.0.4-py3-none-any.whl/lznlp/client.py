# -*- coding: utf-8 -*-
import gzip
import logging
import json
from functools import partial
from io import BytesIO

import requests

from . import __VERSION__
from .exceptions import HTTPError, TaskNotFoundError, TaskError, TimeoutError

# DEFAULT_LZNLP_URL = 'http://127.0.0.1:8090'            # for localhost
DEFAULT_LZNLP_URL = 'http://192.168.3.222:8090'
DEFAULT_TIMEOUT = 30 * 60

text_type = str
string_types = (str,)

logger = logging.getLogger(__name__)


def _gzip_compress(buf):
    zbuf = BytesIO()
    with gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=9) as zfile:
        zfile.write(buf)
    return zbuf.getvalue()


_json_dumps = partial(json.dumps, ensure_ascii=False, sort_keys=True)


class LZNLP(object):
    """LiangZhiNLP HTTP API 访问的封装类

    :param string lznlp_url: LiangZhi HTTP API 的 URL，默认为 `http://127.0.0.1`。

    :param bool compress: 是否压缩大于 10K 的请求体，默认为 True。

    :param int timeout: HTTP 请求超时时间，默认为 60 秒。

    """

    def __init__(self, lznlp_url=DEFAULT_LZNLP_URL, compress=True, session=None, timeout=60):
        self.lznlp_url = lznlp_url.rstrip('/')
        self.compress = compress
        self.timeout = timeout

        # Enable keep-alive and connection-pooling.
        self.session = session or requests.session()
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['User-Agent'] = 'lznlp.sdk/{} {}'.format(
            __VERSION__, requests.utils.default_user_agent()
        )

    def _api_request(self, method, path, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        url = self.lznlp_url + path
        if method == 'POST':
            if 'data' in kwargs:
                headers = kwargs.get('headers', {})
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                data = _json_dumps(kwargs['data'])
                if isinstance(data, text_type):
                    data = data.encode('utf-8')
                if len(data) > 10 * 1024 and self.compress:  # 10K
                    headers['Content-Encoding'] = 'gzip'
                    data = _gzip_compress(data)
                kwargs['data'] = data
                kwargs['headers'] = headers

        r = self.session.request(method, url, **kwargs)

        http_error_msg = ''

        if 400 <= r.status_code < 600:
            reason = r.reason
            try:
                reason = r.json()['message']
            except:
                pass
            http_error_msg = 'HTTPError: %s %s' % (r.status_code, reason)

        if http_error_msg:
            raise HTTPError(http_error_msg, response=r)

        return r

    def get_naf(self):
        """ LiangZhiNLP NAF结构模板接口
        ：return： NAF结构模板

        调用示例：

        >>> import lznlp
        >>> nlp = lznlp.LZNLP()
        >>> nlp.get_naf()
        """
        api_endpoint = '/naf'
        r = self._api_request('GET', api_endpoint)
        return r.json()

    def seg(self, text, tool='jieba', userdict='null', mode='normal'):
        """LiangZhiNLP 分词接口封装

        :param text: 需要做分词的文本
        :type text: string

        :param tool: 使用不同的工具分词，默认使用 'jieba'
        :type tool: string

        :param userdict: 添加自定义词典的文件路径，默认不添加
        :type userdict: string

        :param mode: 不同的分词模式，默认使用 'normal'，可以选'pos'
        :type mode: string

        :returns: 接口返回的分词结果

        调用示例：

        >>> import lznlp
        >>> nlp = lznlp.LZNLP()
        >>> nlp.seg('我在人民广场吃炸鸡', 'jieba')
        ["我", "在", "人民广场", "吃", "炸鸡"]

        """
        params = {"text": text, "tool": tool, "userdict": userdict, "mode": mode}
        api_endpoint = '/segment'
        r = self._api_request('POST', api_endpoint, params=params)
        return r.json()

    def get_regex(self, url):
        """LiangZhiNLP 正则表达式访问接口

        :param url: 获取正则表达式的微服务地址
        :type url: string

        :returns: 包含正则表达式的JSON结构信息

        调用示例:

        >>> import lznlp
        >>> nlp = lznlp.LZNLP()
        >>> nlp.get_regex('/rule/regex/doc_test/entity1')
        {"body":{"update_time":"2018-09-26 13:33:50.0","create_time":"2018-09-26 13:33:00.0","regex_name":"digit","document":"doc_test","content":"^[0-9]*$","knowledge":"entity1"},"status":"ok"}

        """
        if 'regex' in url:
            r = self._api_request('GET', url)
            return r.json()
        else:
            return None

    def get_dict(self, url):
        """LiangZhiNLP 词典访问接口

        :param url: 获取词典的微服务地址
        :type url: string

        :returns: 包含词典的JSON结构信息

        调用示例:

        >>> import lznlp
        >>> nlp = lznlp.LZNLP()
        >>> nlp.get_dict('/rule/dict/doc_test/entity2')
        {"body":{"update_time":"2018-09-26 13:33:50.0","create_time":"2018-09-26 13:33:00.0","dict_name":"country","document":"doc_test","content":"中国|中华人民共和国,美国|美利坚合众国","knowledge":"entity1"},"status":"ok"}

        """
        if 'dict' in url:
            r = self._api_request('GET', url)
            return r.json()
        else:
            return None

    def get_labeled_corpus(self, task_id, limit=1, skip=0):
        """LiangZhiNLP 标注语料访问接口

        :param task_id: 语料的任务ID
        :type task_id: int

        :param limit: 限制返回结果数量
        :type limit: int

        :param skip: 跳过语料的数量
        :type skip: int

        :returns: 包含语料的JSON结构信息

        调用示例:

        >>> import lznlp
        >>> nlp = lznlp.LZNLP()
        >>> nlp.get_labeled_corpus(131, 1000, 100) # 从第100条取出1000条taskID为131的语料（limit=0为取全部，默认为1, skip默认为0）

        """
        url = '/corpus/labeled/' + str(task_id) + '/' + str(limit) + '/' + str(skip)
        r = self._api_request('GET', url)
        return r.json()


class TextClassifierV1(LZNLP):

    def __init__(self):
        super().__init__()

    def train_supervised(self,
                         name,
                         aim,
                         project_name,
                         author,
                         input_file,
                         output,
                         label_prefix="__label__",
                         lr=0.1,
                         lr_update_rate=100,
                         dim=100,
                         ws=5,
                         epoch=5,
                         min_count=1,
                         neg=5,
                         word_ngrams=1,
                         loss="softmax",
                         bucket=0,
                         minn=0,
                         maxn=0,
                         thread=12,
                         t=0.0001,
                         silent=1,
                         encoding="utf-8",
                         pretrained_vectors=""):
        """ LiangZhiNLP FastText 训练监督模型接口封装
        :param name: 模型名称
        :type name: string
        :param aim: 模型目标
        :type aim: string
        :param project_name: 适用项目名称
        :type project_name: string
        :param author: 作者
        :type author: string
        :param input_file: 训练样本集的路径
        :type input_file: string
        :param output: 模型保存路径
        :type output: string
        :param label_prefix: 样本标签前缀，默认 "__label__"
        :type label_prefix: string
        :param lr: 学习速率，默认 0.1
        :type lr: float
        :param lr_update_rate: 学习速率的更新速率，默认 100
        :type lr_update_rate: int
        :param dim: 词向量长度，默认 100
        :type dim: int
        :param ws: 上下文窗口大小，默认 5
        :type ws: int
        :param epoch: 训练批次数，默认 5
        :type epoch: int
        :param min_count: minimal number of word occurences，默认 1
        :type min_count: int
        :param neg: number of negatives sampled，默认 5
        :type neg: int
        :param word_ngrams: max length of word ngram，默认 1
        :type word_ngrams: int
        :param loss: 损失函数，包括 ns, hs, softmax，默认 "softmax"
        :type loss: string
        :param bucket: number of buckets，默认 0
        :type bucket: int
        :param minn: min length of char ngram，默认 0
        :type minn: int
        :param maxn: max length of char ngram，默认 0
        :type maxn: int
        :param thread: 线程数，默认 12
        :type thread: int
        :param t: 采样阈值，默认 0.0001
        :type t: float
        :param silent: 禁用 C++ 拓展的日志输出，默认开启 1
        :type silent: int
        :param encoding: 训练集的编码方式，默认 "utf-8"
        :type encoding: string
        :param pretrained_vectors: 预训练向量文件路径
        :type pretrained_vectors: string
        :return: 模型训练的状态
        调用示例
        >>> import lznlp
        >>> text_classifier = lznlp.TextClassifierV1()
        >>> text_classifier.train_supervised("classifier", "test", "hangzhouguojian", "tester",
                                 "scripts/tools/fasttext/resource/data/labeled_data.txt",
                                 "scripts/tools/fasttext/resource/models/test_model")["status]
         "ok"
        """
        params = {"name": name,
                  "aim": aim,
                  "projectName": project_name,
                  "author": author,
                  "inputFile": input_file,
                  "output": output,
                  "labelPrefix": label_prefix,
                  "lr": str(lr),
                  "lrUpdateRate": str(lr_update_rate),
                  "dim": str(dim),
                  "ws": str(ws),
                  "epoch": str(epoch),
                  "minCount": str(min_count),
                  "neg": str(neg),
                  "wordNgrams": str(word_ngrams),
                  "loss": loss,
                  "bucket": str(bucket),
                  "minx": str(minn),
                  "maxn": str(maxn),
                  "thread": str(thread),
                  "t": str(t),
                  "silent": str(silent),
                  "encoding": encoding,
                  "pretrainedVectors": pretrained_vectors}
        api_endpoint = '/fasttext/train/supervised'
        r = self._api_request('POST', api_endpoint, params=params)
        return r.json()

    def load_model(self, input_file, label_prefix='__label__'):
        """ LiangZhiNLP FastText 加载模型接口封装
        :param input_file: 需要加载的模型文件路径
        :type input_file: string
        :param label_prefix: 标签的前缀表示，默认是 "__label__"
        :type label_prefix: string
        :return: 返回模型加载与否的状态
        调用示例：
        >>> import lznlp
        >>> text_classifier = lznlp.TextClassifierV1()
        >>> text_classifier.load_model("scripts/tools/fasttext/resource/models/test_model.bin")['status']
        "ok"
        """
        params = {'inputFile': input_file, 'labelPrefix': label_prefix}
        api_endpoint = '/fasttext/loadModel'
        r = self._api_request('POST', api_endpoint, params=params)
        return r.json()

    def predict(self, text, k=1):
        """LiangZhiNLP FastText 分类预测接口封装
        :param text: 待预测的文本
        :type text: string
        :param k: 结果给出概率最大的 k 个标签，默认是1
        :type k: int
        :return: 返回预测的标签结果
        调用示例：
        >>> import lznlp
        >>> text_classifier = lznlp.TextClassifierV1()
        >>> text_classifier.predict('I like soccer!', 1)['result']
        [[1]]
        """
        params = {'text': text, 'k': str(k)}
        api_endpoint = '/fasttext/predict'
        r = self._api_request('POST', api_endpoint, params=params)
        return r.json()

class XGBoost(LZNLP):

    def __init__(self):
        super().__init__()

    def train(self,
              name,
              aim,
              project_name,
              author,
              data,
              output,
              num_round,
              test_data,
              save_model=1,
              booster="gbtree",
              silent=0,
              nthread=4,
              disable_default_eval_metric=0,
              eta=0.3,
              gamma=0,
              max_depth=6,
              min_child_weight=1,
              max_delta_step=0,
              subsample=1,
              colsample_bytree=1,
              colsample_bylevel=1,
              lambdax=1,
              alpha=0,
              tree_method="auto",
              objective="reg:linear",
              base_score=0.5):
        """ LiangZhiNLP XGBoost 训练监督模型接口封装
        :param name: 模型名称
        :type name: string
        :param aim: 模型目标
        :type aim: string
        :param project_name: 适用项目名称
        :type project_name: string
        :param author: 作者
        :type author: string
        :param data: 训练样本集的路径
        :type data: string
        :param output: 模型保存路径
        :type output: string
        :param num_round: boosting迭代次数
        :type num_round: string
        :param test_data: 测试样本数据，验证集
        :type test_data: string
        :param save_model: 是否要保存模型到文件，默认 1
        :type save_model: int
        :param booster: 使用哪个booster. 可以是gbtree, gblinear 或 dart，默认 "gbtree"
        :type booster: string
        :param silent: 是否打印运行日志，默认 0
        :type silent: int
        :param nthread: 运行的并行线程数量，默认 4
        :type nthread: int
        :param disable_default_eval_metric: 是否停用默认的评估方法，默认 0，大于0为停用
        :type disable_default_eval_metric: int
        :param eta: 更新的收敛步长，默认 0.3，取值0-1
        :type eta: float
        :param gamma: 进一步切分叶子节点的最小损失，默认 0，取值0-无穷
        :type gamma: int
        :param max_depth: 最大的树的深度，默认 6，取值0-无穷
        :type max_depth: int
        :param min_child_weight: minimum sum of instance weight needed in a child, range [0, infinite]，默认 1
        :type min_child_weight: int
        :param max_delta_step: "maximum delta step we allow each leaf output to be, range [0, infinite]，默认 0
        :type max_delta_step: int
        :param subsample: subsample ratio of the training instances, range (0, 1]，默认 1
        :type subsample: float
        :param colsample_bytree: subsample ratio of columns when constructing each tree, range (0, 1]，默认 1
        :type colsample_bytree: float
        :param colsample_bylevel: subsample ratio of columns for each split in each level, range (0, 1]，默认 1
        :type colsample_bylevel: float
        :param lambdax: L2 regularization term on weights，默认 1
        :type lambdax: int
        :param alpha: L1 regularization term on weights，默认 0
        :type alpha: int
        :param tree_method: the tree construction algorithm used in XGBoost. Can be auto, exact, approx, hist, gpu_exact, gpu_hist，默认 "auto"
        :type tree_method: string
        :param objective: learning objective, can be reg:linear, reg:logistic, binary:logistic, binary:logitraw, binary:hinge, count:poisson, survival:cox, multi:softmax, multi:softprob, rank:pairwise, rank:ndcg, rank:map, rank:gamma, reg:tweedie，默认 "reg:linear"
        :type objective: string
        :param base_score: the initial prediction score of all instances, global bias，默认 0.5
        :type base_score: float
        :return: 模型训练的状态
        调用示例
        >>> import lznlp
        >>> xgboost = lznlp.XGBoost()
        >>> xgboost.train("xxx classifier", "test", "hangzhouguojian", "tester",
                                 "scripts/tools/xgboost/resource/train.txt",
                                 "scripts/tools/xgboost/resource/models/test_model.model",
                                 "10", "scripts/tools/xgboost/resource/test.txt")
         "ok"
        """
        params = {"name": name,
                  "aim": aim,
                  "projectName": project_name,
                  "author": author,
                  "data": data,
                  "output": output,
                  "numRound": num_round,
                  "testData": test_data,
                  "saveModel": str(save_model),
                  "booster": booster,
                  "silent": str(silent),
                  "nthread": str(nthread),
                  "disableDefaultEvalMetric": str(disable_default_eval_metric),
                  "eta": str(eta),
                  "gamma": str(gamma),
                  "maxDepth": str(max_depth),
                  "minChildWeight": str(min_child_weight),
                  "maxDeltaStep": str(max_delta_step),
                  "subsample": str(subsample),
                  "colsampleBytree": str(colsample_bytree),
                  "colsampleBylevel": str(colsample_bylevel),
                  "lambda": str(lambdax),
                  "alpha": str(alpha),
                  "treeMethod": tree_method,
                  "objective": objective,
                  "baseScore": str(base_score)}
        api_endpoint = '/xgboost/train'
        r = self._api_request('POST', api_endpoint, params=params)
        return r.json()

    def predict(self, model_file, test_data, nthread=4):
        """LiangZhiNLP XGBoost 分类预测接口封装
        :param model_file: 训练好的模型文件
        :type model_file: string
        :param test_data: 待预测的数据文件
        :type test_data: string
        :param nthread: 运行的并行线程数量，默认 4
        :type nthread: int
        :return: 返回预测的标签概率结果
        调用示例：
        >>> import lznlp
        >>> xgboost = lznlp.XGBoost()
        >>> xgboost.predict('scripts/tools/xgboost/resource/models/test_model.model', 'scripts/tools/xgboost/resource/test_no_label.txt')
        """
        params = {'modelFile': model_file, 'testData': test_data, 'nthread': str(nthread)}
        api_endpoint = '/xgboost/predict'
        r = self._api_request('POST', api_endpoint, params=params)
        return r.json()