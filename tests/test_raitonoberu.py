"""test module."""
import os
import yaml
from unittest import mock
from itertools import product

import pytest


@pytest.mark.parametrize(
    'user_agent, session',
    product(
        [None, mock.Mock()],
        [None, mock.Mock()]
    )
)


def test_init(user_agent, session):
    with mock.patch('Raitonoberu.raitonoberu.aiohttp') as m_aio:
        from Raitonoberu.raitonoberu import Raitonoberu
        # run
        obj = Raitonoberu(user_agent, session)
        # test
        if user_agent is None:
            obj.headers == {"User-Agent": "Raitonoberu"}
        else:
            obj.headers == user_agent
        if session is None:
            obj.session == m_aio.ClientSession.return_value
            m_aio.ClientSession.assert_called_once_with(headers=obj.headers)
        else:
            obj.session == session


def test_del():
    session = mock.Mock()
    with mock.patch('Raitonoberu.raitonoberu.Raitonoberu.__init__', return_value=None):
        from Raitonoberu.raitonoberu import Raitonoberu
        obj = Raitonoberu()
        obj.session = session
        # run
        del obj
        # test
        session.close.assert_called_once_with()


@pytest.mark.asyncio
@pytest.mark.parametrize('term', ['term'])
async def test_get_search_page(term):
    from Raitonoberu.raitonoberu import Raitonoberu
    obj = Raitonoberu()
    # run
    res = await obj.get_search_page(term=term)
    # test
    # the actual result with 'term' as input is
    # 'http://www.novelupdates.com/series/the-last-apostle/'
    assert res.startswith('http://www.novelupdates.com/series/')


def get_search_page_method_paramaters():
    """get data paramater for search page method."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data_file = os.path.join(dir_path, 'test_data.yaml')
    with open(data_file) as f:
        parameter = yaml.load(f)
    return parameter

@pytest.mark.asyncio
@pytest.mark.parametrize(
    'term, exp_res',
    get_search_page_method_paramaters()
)
async def test_get_first_search_result(term, exp_res):
    from Raitonoberu.raitonoberu import Raitonoberu
    obj = Raitonoberu()
    # run
    res = await obj.get_first_search_result(term=term)
    # test
    assert res == exp_res


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'term, exp_res',
    [
        (
            'I shall seal the heavens',
            [
                'Xian Ni (Shared Universe)',
                'Beseech The Devil (Shared Universe)',
                'Against Heaven (Shared Universe)',
                'A Will Eternal (Shared Universe)'
            ]
        ),
        ('Curing incurable diseases with semen', None),
        (
            'S.A.O.',
            [
                'Sword Art Online Alternative – Gun Gale Online (Spin-Off)',
                'Sword Art Online – Progressive (Spin-Off)',
                'Mahouka Koukou no Rettousei x Sword Art Online (Spin-Off)',
                'Sword Art Online Alternative – Clover’s Regret (Spin-Off)',
            ]
        ),
    ]
)
async def test_related_series(term, exp_res):
    """test related series category."""
    from Raitonoberu.raitonoberu import Raitonoberu
    obj = Raitonoberu()
    # run
    res = await obj.get_first_search_result(term=term)
    # test
    res['related_series'] == exp_res


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'term, exp_res',
    [
        ['Curing incurable diseases with semen', None],
        ['S.A.O.', 'Yen Press'],
        ['I shall seal the heavens', None],
    ]
)
async def test_english_publisher(term, exp_res):
    """test related series category."""
    from Raitonoberu.raitonoberu import Raitonoberu
    obj = Raitonoberu()
    # run
    res = await obj.get_first_search_result(term=term)
    # test
    res['english_publisher'] == exp_res
