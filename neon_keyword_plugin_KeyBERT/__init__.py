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

# # NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# # All trademark and other rights reserved by their respective owners
# # Copyright 2008-2021 Neongecko.com Inc.

from keybert import KeyBERT

from ovos_plugin_manager.keywords import KeywordExtractor


class KeyBERTExtractor(KeywordExtractor):

    def __init__(self, config=None):
        super(KeyBERTExtractor, self).__init__(config)
        # TODO read all from config
        model = "all-MiniLM-L6-v2"
        self.max_ngram_size = 3
        self.diversity = 0.7
        self.use_maxsum = True
        self.use_mmr = False
        self.kw_model = KeyBERT(model=model)
        self.thresh = self.config.get("thresh", 0.4)

    def extract(self, text, lang):
        if lang == "en":
            stopwords = "english"
        else:
            stopwords = []
        kws = []
        if self.use_maxsum:
            try:
                kws = self.kw_model.extract_keywords(text,
                                                     keyphrase_ngram_range=(1, self.max_ngram_size),
                                                     stop_words=stopwords,
                                                     use_maxsum=True, nr_candidates=20, top_n=5)
            except TypeError:
                # TypeError: 'NoneType' object is not iterable
                # with self.use_maxsum if candidates detection fails
                pass

        if not kws and self.use_mmr:
            kws = self.kw_model.extract_keywords(text,
                                                 keyphrase_ngram_range=(1, self.max_ngram_size),
                                                 stop_words=stopwords,
                                                 use_mmr=True, diversity=0.7)

        if not kws:
            kws = self.kw_model.extract_keywords(text, stop_words=stopwords,
                                                 keyphrase_ngram_range=(1, self.max_ngram_size))

        kws = sorted([k for k in kws if k[1] >= self.thresh],
                     key=lambda k: k[1], reverse=True)
        return kws

