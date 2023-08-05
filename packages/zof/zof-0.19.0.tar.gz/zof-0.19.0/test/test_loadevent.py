import unittest
from zof.event import load_event
from zof.objectview import to_json


class LoadEventTestCase(unittest.TestCase):
    def test_empty(self):
        # Loading empty bytes is an error.
        event = load_event(b'')
        self.assertEqual('EXCEPTION', event['event'])
        self.assertEqual('EOF', event['reason'])

        # Loading only white space is an error.
        event = load_event(b'  ')
        self.assertEqual('EXCEPTION', event['event'])
        self.assertEqual('Expecting value: line 1 column 3 (char 2)',
                         event['reason'])

    def test_empty_dict(self):
        # Test empty event as bytes.
        event = load_event(b'{}')
        self.assertIsInstance(event, dict)
        self.assertEqual(event, {})

    def test_empty_dict2(self):
        # Test empty event as unicode str.
        event = load_event('{}')
        self.assertIsInstance(event, dict)
        self.assertEqual(event, {})

    def test_empty_dict3(self):
        # Test empty event with extra whitespace.
        event = load_event(b' {} \n')
        self.assertIsInstance(event, dict)
        self.assertEqual(event, {})

    def test_empty_dict_multiple(self):
        # Test that multiple empty events fail.
        event = load_event(b'{}{}')
        self.assertEqual('EXCEPTION', event['event'])
        self.assertEqual('Extra data: line 1 column 3 (char 2)',
                         event['reason'])

    def test_truncated_input(self):
        # Test that truncated input is detected.
        event = load_event(b'{ ')
        self.assertEqual('EXCEPTION', event['event'])
        self.assertEqual(
            'Expecting property name enclosed in double quotes: line 1 column 3 (char 2)',
            event['reason'])

    def test_other_value(self):
        # Test that non-mapping objects still work.
        event = load_event(b'[1, 2, 3]')
        self.assertIsInstance(event, list)
        self.assertEqual(event, [1, 2, 3])

    def test_utf8(self):
        # Test that Unicode/UTF-8 works.
        data = load_event(
            b'{"x":"\xe2\x82\xac\xf0\x90\x8c\x82\xf4\x8f\xbf\xbd"}')
        self.assertIsInstance(data, dict)
        self.assertEqual(data, {'x': '\u20AC\U00010302\U0010fffd'})

    def test_event_data(self):
        # Test that `data` is NOT converted from hexadecimal to binary.
        event = load_event(b'{"data":"deadbeef"}')
        self.assertEqual(event, {'data': 'deadbeef'})
        # Non-hex data should raise an exception. (FIXME- old)
        #event = load_event(b'{"data":"nonhex"}')
        #self.assertEqual('EXCEPTION', event['event'])
        #self.assertTrue(
        #    event['reason'].startswith('non-hexadecimal number found'))

    def test_event_pkt(self):
        # Test that `_pkt` lists are converted to dictionaries.
        #event = load_event(
        #    b'{"data": "ff", "_pkt": [{"field":"a", "value":1}]}')
        #self.assertEqual(event['pkt'], {'a': 1})
        #self.assertFalse("_pkt" in event)
        # _pkt requires the `data` value, otherwise it's not translated
        event = load_event(b'{"_pkt": [{"field":"a", "value":1}]}')
        self.assertFalse("pkt" in event)
        self.assertTrue("_pkt" in event)

    def test_event_payload(self):
        event = load_event(
            b'{"foo": 27, "data": "ff07", "_pkt": [{"field":"a", "value":9}, {"field": "X_PKT_POS", "value":1}]}'
        )
        self.assertEqual(event['foo'], 27)
        self.assertEqual(event['data'], 'ff07')
        #self.assertEqual(event['pkt'], {'a':9, 'x_pkt_pos': 1, 'payload': b'\x07'})
        #self.assertEqual(event['pkt']['payload'], b'\x07')

    def test_to_json(self):
        # Test that to_json also works.
        event = load_event(b'{"foo":"bar"}')
        s = to_json(event)
        self.assertEqual(s, '{"foo":"bar"}')

    def test_load_event_time(self):
        import timeit
        result = timeit.timeit(
            """load_event(b'{"foo": 27, "data": "ff07", "_pkt": [{"field":"a", "value":9}, {"field": "X_PKT_POS", "value":1}]}')""",
            setup='from zof.event import load_event',
            number=10000)
        print('[test_load_event_time=%r]' % result)
