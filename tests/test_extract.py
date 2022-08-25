# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
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
import json
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from neon_utterance_KeyBERT_plugin import *


class KeyBertExtractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extractor = KeyBERTExtractor()

    def test_transform(self):
            text = [
                "Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning " \
                "competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud " \
                "Next conference in San Francisco this week, the official announcement could come as early as tomorrow. " \
                "Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. "]

            lang = self.extractor.transform(text)
            self.assertEqual(lang, ([
                                        'Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning competitions. '
                                        'Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud Next conference in San Francisco this week,'
                                        ' the official announcement could come as early as tomorrow. Reached by phone, Kaggle co-founder'
                                        ' CEO Anthony Goldbloom declined to deny that the acquisition is happening. '],
                                    {'keybert_keywords': [('kaggle founder ceo', 0.6321),
                                                          ('reached phone kaggle', 0.5141),
                                                          ('google hosting', 0.4067)]})
                             )
    def test_extract(self):
            text = ["Sources tell us that Google is acquiring Kaggle, a platform that hosts data science and machine learning "\
                "competitions. Details about the transaction remain somewhat vague, but given that Google is hosting its Cloud "\
                "Next conference in San Francisco this week, the official announcement could come as early as tomorrow. "\
                "Reached by phone, Kaggle co-founder CEO Anthony Goldbloom declined to deny that the acquisition is happening. "]

            lang = self.extractor.extract(text)
            self.assertEqual(lang,[('cloud conference', 0.3648), ('sources tell google', 0.3802),
                                   ('google hosting', 0.4067), ('reached phone kaggle', 0.5141),
                                   ('kaggle founder ceo', 0.6321)])


