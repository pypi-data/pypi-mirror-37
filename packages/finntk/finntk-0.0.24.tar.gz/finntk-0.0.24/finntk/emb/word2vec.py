import logging
from finntk.utils import ResourceMan, urlretrieve
from gensim.models import KeyedVectors
from shutil import copyfileobj
import os
import zipfile

logger = logging.getLogger(__name__)


class Word2VecWordVecs(ResourceMan):
    RESOURCE_NAME = "word2vec-fi"

    URL = "http://vectors.nlpl.eu/repository/11/42.zip"

    def __init__(self):
        super().__init__()
        self._resources["vec"] = "word2vec.binvec"

    def _bootstrap(self, res):
        from gensim.test.utils import get_tmpfile

        logger.info("Downloading Word2Vec word vectors")
        zipped_tmp_fn = urlretrieve(self.URL)
        try:
            tmp_zip = zipfile.ZipFile(zipped_tmp_fn)
            tmp_fn = get_tmpfile("word2vec-fi.txt")
            try:
                copyfileobj(tmp_zip.open("model.txt"), open(tmp_fn, "wb"))
                logger.info("Converting Word2Vec word vectors")
                fi = KeyedVectors.load_word2vec_format(tmp_fn)
                fi.save(self._get_res_path("vec"))
            finally:
                os.remove(tmp_fn)
            copyfileobj(
                tmp_zip.open("synsets.txt"), open(self._get_res_path("synsets"), "wb")
            )
        finally:
            os.remove(zipped_tmp_fn)
