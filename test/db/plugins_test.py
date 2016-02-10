"""
Test plugin merge and matching.
"""
from __future__ import absolute_import

import db.plugins


def test_update_plugin():
    def assert_update(old, new, expected):
        updated = db.plugins.update_plugin(old, new)
        assert updated == expected

    # Ensure we get basic dict.update behavior.
    assert_update({'a': 1, 'b': 1}, {'a': 2, 'c': 1},
                  {'a': 2, 'b': 1, 'c': 1})

    # Should keep latest updated date.
    assert_update({'updated_at': 1}, {}, {'updated_at': 1})
    assert_update({}, {'updated_at': 5}, {'updated_at': 5})
    assert_update({'updated_at': 1}, {'updated_at': 5}, {'updated_at': 5})

    # Should keep earliest created date.
    assert_update({'created_at': 1}, {}, {'created_at': 1})
    assert_update({}, {'created_at': 5}, {'created_at': 5})
    assert_update({'created_at': 1}, {'created_at': 5}, {'created_at': 1})


def test_merge_dict_except_none():
    merge = db.plugins._merge_dict_except_none

    # Basic merge works
    assert merge({'a': 1}, {}) == {'a': 1}
    assert merge({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}
    assert merge({'a': 1}, {'a': 2}) == {'a': 2}
    assert merge({'a': 1, 'b': 2}, {'a': 3}) == {'a': 3, 'b': 2}

    # Does not merge in any None values
    assert merge({'a': 1}, {'a': None}) == {'a': 1}
    assert merge({'a': 1}, {'b': None}) == {'a': 1}
    assert merge({'a': 1}, {'a': None, 'b': 2}) == {'a': 1, 'b': 2}

    # Make sure we don't mutate arguments
    dict_a = {'a': 1, 'b': 2}
    dict_b = {'a': 3, 'c': 4}
    assert merge(dict_a, dict_b) == {'a': 3, 'b': 2, 'c': 4}
    assert dict_a == {'a': 1, 'b': 2}
    assert dict_b == {'a': 3, 'c': 4}


def test_generate_normalized_name():
    def test(name, expected):
        gen = db.plugins._normalize_name
        assert gen({'vimorg_name': name}) == expected

    test('nerdcommenter', 'nerdcommenter')
    test('The NERD Commenter', 'nerdcommenter')
    test('The-NERD-Commenter', 'nerdcommenter')
    test('The-vim-NERD-Commenter.vim', 'nerdcommenter')  # This I made up
    test('NERD_tree', 'nerdtree')
    test(u'oh-l\xe0-l\xe0', 'ohlala')
    test(u'\u2605darkZ\u2605', 'darkz')
    test('abc-vim', 'abc')
    test('cscope.vim', 'cscope')
    test('vim-powerline', 'powerline')
    test('systemverilog.vim--Kanovsky', 'systemverilog')
    test('Ruby/Sinatra', 'rubysinatra')
    test('bufexplorer.zip', 'bufexplorer')
    test('runzip', 'runzip')


def test_is_similar_author_name():
    similar = db.plugins._is_similar_author_name

    assert similar('Tim Pope', 'Tim Pope')
    assert similar(u'Kim Silkeb\xe6kken', u'Kim Silkeb\xe6kken')
    assert similar('nanotech', 'NanoTech')
    assert similar('Marty Grenfell', 'Martin Grenfell')
    assert similar('gmarik', 'gmarik gmarik')
    assert similar('Miles Sterrett', 'Miles Z. Sterrett')
    assert similar('Suan', 'Suan Yeo')
    assert similar('jlanzarotta', 'jeff lanzarotta')

    # Unfortunately, the following will cause some assertions below to fail
    #self.assertTrue(similar('Shougo', 'Shougo Matsushita'))

    assert not similar('Bob', 'Joe')
    assert not similar('Paul Graham', 'Paul Bucheit')
    assert not similar('Taylor Swift', 'Barack Obama')


def test_are_plugins_different():
    diff = db.plugins._are_plugins_different

    assert diff({'vimorg_id': 1}, {'vimorg_id': 2})
    assert diff({'github_owner': 'tpope', 'github_repo_name': 'Red'},
                {'github_owner': 'tpope', 'github_repo_name': 'Long Live'})
    assert diff({'github_owner': 'tpope', 'github_repo_name': 'bbq'},
                {'github_owner': 'sjl', 'github_repo_name': 'bbq'})
    assert diff({'vimorg_id': 1, 'github_owner': 2, 'github_repo_name': 2},
                {'vimorg_id': 1, 'github_owner': 3, 'github_repo_name': 3})
    assert diff({'vimorg_id': 2, 'github_owner': 1, 'github_repo_name': 1},
                {'vimorg_id': 3, 'github_owner': 1, 'github_repo_name': 1})

    assert not diff({}, {})
    assert not diff({'vimorg_id': 1}, {})
    assert not diff({}, {'vimorg_id': 1})
    assert not diff({'vimorg_id': 1}, {'vimorg_id': 1})
    assert not diff({}, {'github_owner': 'sjl', 'github_repo_name': 'Gundo'})
    assert not diff({'github_owner': 'sjl', 'github_repo_name': 'Gundo'}, {})
    assert not diff({'github_owner': 'sjl', 'github_repo_name': 'Gundo'},
                    {'github_owner': 'sjl', 'github_repo_name': 'Gundo'})
    assert not diff({'vimorg_id': 1},
                    {'github_owner': 'sjl', 'github_repo_name': 'Gundo'})
