"""
Test scraper logic.
"""
from __future__ import absolute_import

from tools.scrape import github


def test_vundle_plugin_regex():
    vimrc = """
    Bundle 'gmarik/vundle0'
    Bundle 'gmarik/vundle1'
    Bundle    'gmarik/vundle2'
            \tBundle   'gmarik/vundle3'
    Bundle 'gmarik/vundle4' " Comment: Merry Swiftmas!!!!
    Bundle "gmarik/vundle5"
    Bundle 'taglist'
    Bundle 'ervandew/supertab.git'
    Bundle 'git://github.com/scrooloose/nerdtree'
    Bundle 'git://github.com/kien/ctrlp.vim.git'
    Bundle 'calendar.vim--Matsumoto'
    Bundle 'git://git.wincent.com/command-t.git'
    Bundle 'git@github.com:Valloric/YouCompleteMe.git'
    Bundle 'rstacruz/sparkup', {'rtp': 'vim/'}
    Bundle 'https://github.com/Raimondi/delimitMate/'

    Bundle 'uh/oh
    "Bundle 'commented/out'
    """

    expected_matches = [
        'gmarik/vundle0',
        'gmarik/vundle1',
        'gmarik/vundle2',
        'gmarik/vundle3',
        'gmarik/vundle4',
        'gmarik/vundle5',
        'taglist',
        'ervandew/supertab.git',
        'git://github.com/scrooloose/nerdtree',
        'git://github.com/kien/ctrlp.vim.git',
        'calendar.vim--Matsumoto',
        'git://git.wincent.com/command-t.git',
        'git@github.com:Valloric/YouCompleteMe.git',
        'rstacruz/sparkup',
        'https://github.com/Raimondi/delimitMate/'
    ]

    assert github._VUNDLE_PLUGIN_REGEX.findall(vimrc) == expected_matches


def test_neobundle_plugin_regex():
    vimrc = """
    NeoBundle 'scrooloose/nerdtree'
    NeoBundleFetch 'Shougo/neobundle.vim'
    NeoBundleLazy 'Shougo/unite.vim'
    """

    expected_matches = [
        'scrooloose/nerdtree',
        'Shougo/neobundle.vim',
        'Shougo/unite.vim',
    ]

    assert github._NEOBUNDLE_PLUGIN_REGEX.findall(vimrc) == expected_matches


def test_bundle_owner_repo_regex():
    def test(bundle, expected):
        parse_bundle = github._BUNDLE_OWNER_REPO_REGEX
        assert parse_bundle.search(bundle).groups() == expected

    test('gmarik/vundle', ('gmarik', 'vundle'))
    test('gmarik/vundle/', ('gmarik', 'vundle'))
    test('taglist', (None, 'taglist'))
    test('ervandew/supertab.git', ('ervandew', 'supertab'))
    test('git://github.com/scrooloose/nerdtree',
         ('scrooloose', 'nerdtree'))
    test('git://github.com/kien/ctrlp.vim.git', ('kien', 'ctrlp.vim'))
    test('calendar.vim--Matsumoto', (None, 'calendar.vim--Matsumoto'))

    # Don't care about non-GitHub repos. They'll just 404 when we scrape.
    test('git://git.wincent.com/command-t.git',
         ('git.wincent.com', 'command-t'))

    test('git@github.com:Valloric/YouCompleteMe.git',
         ('Valloric', 'YouCompleteMe'))
    test('https://github.com/vim-scripts/The-NERD-tree.git',
         ('vim-scripts', 'The-NERD-tree'))
    test('https://github.com/Raimondi/delimitMate/',
         ('Raimondi', 'delimitMate'))


def test_submodule_is_bundle_regex():
    is_bundle = github._SUBMODULE_IS_BUNDLE_REGEX.search

    assert is_bundle('submodule "bundle/ropevim"')
    assert is_bundle('submodule "vim/bundle/handlebars"')
    assert is_bundle('submodule "available-bundles/unimpaired"')
    assert is_bundle('submodule "vim/vim.symlink/bundle/vim-pathogen"')

    assert not is_bundle('submodule ".emacs.d/packages/groovy"')
    assert not is_bundle('submodule "theme/sundown"')
    assert not is_bundle('submodule "jedi"')
