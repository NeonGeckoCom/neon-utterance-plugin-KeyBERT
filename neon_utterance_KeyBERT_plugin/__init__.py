# # NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# # All trademark and other rights reserved by their respective owners
# # Copyright 2008-2021 Neongecko.com Inc.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from keybert import KeyBERT

from neon_transformers import UtteranceTransformer
from neon_transformers.tasks import UtteranceTask


class KeyBERTExtractor(UtteranceTransformer):
    task = UtteranceTask.KEYWORD_EXTRACTION

    def __init__(self, name="KeyBERT", priority=60):
        super().__init__(name, priority)
        # TODO read all from config
        model = "all-MiniLM-L6-v2"
        self.max_ngram_size = 3
        self.diversity = 0.7
        self.use_maxsum = True
        self.use_mmr = False
        self.kw_model = KeyBERT(model=model)
        self.thresh = self.config.get("thresh", 0.4)

    def extract(self, doc, lang="en"):
        if lang == "en":
            stopwords = "english"
        else:
            stopwords = []
        if self.use_maxsum:
            return self.kw_model.extract_keywords(doc,
                                                  keyphrase_ngram_range=(1, self.max_ngram_size),
                                                  stop_words=stopwords,
                                                  use_maxsum=True, nr_candidates=20, top_n=5)
        if self.use_mmr:
            return self.kw_model.extract_keywords(doc,
                                                  keyphrase_ngram_range=(1, self.max_ngram_size),
                                                  stop_words=stopwords,
                                                  use_mmr=True, diversity=0.7)
        return self.kw_model.extract_keywords(doc, stop_words=stopwords,
                                              keyphrase_ngram_range=(1, self.max_ngram_size))

    def transform(self, utterances, context=None):
        keywords = []
        context = context or {}
        lang = context.get("lang", "en").split("-")[0]
        for utt in utterances:
            try:
                keywords += [k for k in self.extract(utt, lang=lang)
                             if k[1] >= self.thresh]
            except TypeError:
                # TypeError: 'NoneType' object is not iterable
                # with self.use_maxsum if candidates detection fails
                pass

        keywords = sorted(keywords, key=lambda k: k[1], reverse=True)
        # return unchanged utterances + data
        return utterances, {"keybert_keywords": keywords}
