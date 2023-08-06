from unittest import TestCase
from unittest.mock import patch, Mock, call

from ..expand_by_entities import (
    expand_by_entities,
    partition_by_entities,
    _aggregate_entities,
)
from ..elements import (
    Datum,
    Entity,
    Intent,
)


class ExpandByEntitiesTestCase(TestCase):

    def setUp(self):
        self.utterance = '我想訂明天從紐約飛到新加坡的機票'
        self.entities = [
            Entity(name='日期', value='明天', start=3, end=5, replacements=['下禮拜二']),
            Entity(name='出發地', value='紐約', start=6, end=8),
            Entity(name='目的地', value='新加坡', start=10, end=13, replacements=['斯堪地那維亞', 'KIX']),
        ]
        self.intents = [
            Intent(name='訂機票'),
        ]
        self.datum = Datum(
            utterance=self.utterance,
            intents=self.intents,
            entities=self.entities,
        )

        self.expected_utterances = [
            '我想訂明天從紐約飛到新加坡的機票',
            '我想訂下禮拜二從紐約飛到新加坡的機票',
            '我想訂明天從紐約飛到斯堪地那維亞的機票',
            '我想訂下禮拜二從紐約飛到斯堪地那維亞的機票',
            '我想訂明天從紐約飛到KIX的機票',
            '我想訂下禮拜二從紐約飛到KIX的機票',
        ]
        self.expected_entity_lists = [
            [
                Entity(name='日期', value='明天', start=3, end=5),
                Entity(name='出發地', value='紐約', start=6, end=8),
                Entity(name='目的地', value='新加坡', start=10, end=13),
            ],
            [
                Entity(name='日期', value='下禮拜二', start=3, end=7),
                Entity(name='出發地', value='紐約', start=8, end=10),
                Entity(name='目的地', value='新加坡', start=12, end=15),
            ],
            [
                Entity(name='日期', value='明天', start=3, end=5),
                Entity(name='出發地', value='紐約', start=6, end=8),
                Entity(name='目的地', value='斯堪地那維亞', start=10, end=16),
            ],
            [
                Entity(name='日期', value='下禮拜二', start=3, end=7),
                Entity(name='出發地', value='紐約', start=8, end=10),
                Entity(name='目的地', value='斯堪地那維亞', start=12, end=18),
            ],
            [
                Entity(name='日期', value='明天', start=3, end=5),
                Entity(name='出發地', value='紐約', start=6, end=8),
                Entity(name='目的地', value='KIX', start=10, end=13),
            ],
            [
                Entity(name='日期', value='下禮拜二', start=3, end=7),
                Entity(name='出發地', value='紐約', start=8, end=10),
                Entity(name='目的地', value='KIX', start=12, end=15),
            ],
        ]
        self.expected_intents = [
            [Intent(name='訂機票')],
            [Intent(name='訂機票')],
            [Intent(name='訂機票')],
            [Intent(name='訂機票')],
            [Intent(name='訂機票')],
            [Intent(name='訂機票')],
        ]
        self.expected_data = []
        self.expected_data_without_replacement = []
        for utt, ents, ints in zip(
                self.expected_utterances,
                self.expected_entity_lists,
                self.expected_intents,
            ):
            self.expected_data.append(Datum(
                utterance=utt,
                entities=ents,
                intents=ints,
            ))

    def test_expand_by_entiies(self):
        result = expand_by_entities(
            self.datum,
            include_orig=True,
        )

        # correct expand numbers
        self.assertEqual(6, len(result))
        for idx, datum in enumerate(result):
            with self.subTest(datum_idx=idx):
                self.assertIn(datum, self.expected_data)

    @patch('uttut.expand_by_entities.partition_by_entities', return_value=([[]], []))
    def test_expand_by_entities_call_partition_correctly(self, patch_partition):
        expand_by_entities(
            self.datum,
            include_orig=True,
        )
        patch_partition.assert_called_once_with(self.datum, True)

    @patch('uttut.expand_by_entities.partition_by_entities', return_value=([[]], []))
    def test_expand_by_entities_call_partition_correctly_false(self, patch_partition):
        expand_by_entities(
            self.datum,
            include_orig=False,
        )
        patch_partition.assert_called_once_with(self.datum, False)

    fake_parts = [['a', 'b'], ['c']]
    fake_entity_names = ['Z', None]

    @patch(
        'uttut.expand_by_entities.partition_by_entities',
        return_value=(fake_parts, fake_entity_names),
    )
    @patch('uttut.expand_by_entities.get_kth_combination', return_value=['a', 'c'])
    def test_expand_by_entities_correctly_use_sampling_method(self, patch_get_k, _):
        mock_sampling_method = Mock(return_value=[0, 1])

        expand_by_entities(
            self.datum,
            sampling_method=mock_sampling_method,
            include_orig=True,
        )

        mock_sampling_method.assert_called_once_with(2)
        patch_get_k.assert_has_calls([
            call(self.fake_parts, 0),
            call(self.fake_parts, 1),
        ])

    def test_partition_by_entities(self):
        actual_parts, entity_names = partition_by_entities(self.datum, False)
        expected_parts = [
            ['我想訂'],
            ['下禮拜二'],
            ['從'],
            ['紐約'],
            ['飛到'],
            ['斯堪地那維亞', 'KIX'],
            ['的機票'],
        ]
        for exp_part, act_part in zip(expected_parts, actual_parts):
            self.assertEqual(set(exp_part), set(act_part))
        self.assertEqual(
            entity_names,
            [None, '日期', None, '出發地', None, '目的地', None],
        )

    def test_partition_by_entities_include_orig(self):
        actual_parts, entity_names = partition_by_entities(self.datum, True)
        expected_parts = [
            ['我想訂'],
            ['明天', '下禮拜二'],
            ['從'],
            ['紐約'],
            ['飛到'],
            ['新加坡', '斯堪地那維亞', 'KIX'],
            ['的機票'],
        ]
        for exp_part, act_part in zip(expected_parts, actual_parts):
            self.assertEqual(set(exp_part), set(act_part))
        self.assertEqual(
            entity_names,
            [None, '日期', None, '出發地', None, '目的地', None],
        )

    def test__aggregate_entities(self):
        segments = ['我想喝', '珍奶', '半糖']
        entity_names = [None, 'DRINK', 'SUGAR']

        expected_entities = [
            Entity(name='DRINK', value='珍奶', start=3, end=5),
            Entity(name='SUGAR', value='半糖', start=5, end=7),
        ]

        actual_entities = _aggregate_entities(segments, entity_names)
        self.assertEqual(expected_entities, actual_entities)
