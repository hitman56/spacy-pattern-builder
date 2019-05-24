"""
Tests for `spacy-pattern-builder` module.
"""
import pytest
import en_core_web_sm
from spacy_pattern_builder.spacy_pattern_builder import build_dependency_pattern
from spacy_pattern_builder.exceptions import TokensNotFullyConnectedError
import spacy_pattern_builder.util as util


class TestSpacyPatternBuilder(object):

    @classmethod
    def setup_class(self):
        text = 'We introduce efficient methods for fitting Boolean models to molecular data, successfully demonstrating their application to synthetic time courses generated by a number of established clock models, as well as experimental expression levels measured using luciferase imaging.'
        nlp = en_core_web_sm.load()
        self.doc = nlp(text)

    def test_build_pattern_and_find_matches(self):
        doc = self.doc
        match_examples = [
            util.idxs_to_tokens(doc, [0, 1, 3]),  # [We, introduce, methods]
            util.idxs_to_tokens(doc, [13, 15, 16, 19]),  # [demonstrating, application, to, courses]
        ]
        token_feature_dict = {'DEP': 'dep_', 'TAG': 'tag_'}
        for match_example in match_examples:
            pattern = build_dependency_pattern(
                doc,
                match_example,
                token_feature_dict,
            )
            matches = util.find_matches(doc, pattern)
            assert match_example in matches

    def test_build_pattern_fails(self):
        doc = self.doc
        match_examples = [
            util.idxs_to_tokens(doc, [19, 20, 21, 27]),  # [courses, generated, by, models]
        ]
        token_feature_dict = {'DEP': 'dep_', 'TAG': 'tag_'}
        for match_example in match_examples:
            with pytest.raises(TokensNotFullyConnectedError):
                build_dependency_pattern(
                    doc,
                    match_example,
                    token_feature_dict,
                )
