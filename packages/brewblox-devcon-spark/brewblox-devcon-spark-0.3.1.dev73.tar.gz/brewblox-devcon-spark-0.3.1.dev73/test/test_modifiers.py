"""
Tests brewblox_devcon_spark.codec.modifiers
"""

from brewblox_devcon_spark.codec import _path_extension  # isort:skip

import pytest

import TempSensorOneWire_pb2
from brewblox_devcon_spark.codec import modifiers

_path_extension.avoid_lint_errors()


@pytest.fixture(scope='module')
def mod():
    return modifiers.Modifier('config/fahrenheit_system.txt', strip_readonly=False)


@pytest.fixture(scope='module')
def k_mod():
    return modifiers.Modifier(None)


def generate_encoding_data():
    return {
        'value[degF]': 10,
        'valid': True,
        'offset[delta_degF]': 20,
        'address': 'aabbccdd',
    }


def generate_decoding_data():
    return {
        'value': -50062,
        'valid': True,
        'offset': 45511,
        'address': 3721182122,
    }


def test_encode_options(mod):
    vals = generate_encoding_data()
    mod.encode_options(TempSensorOneWire_pb2.TempSensorOneWire(), vals)

    # converted to delta_degC
    # scaled * 256
    # rounded to int
    assert vals == generate_decoding_data()


def test_decode_options(mod):
    vals = generate_decoding_data()
    mod.decode_options(TempSensorOneWire_pb2.TempSensorOneWire(), vals)
    print(vals)
    assert vals['offset[delta_degF]'] == pytest.approx(20, 0.1)
    assert vals['value[degF]'] == pytest.approx(10, 0.1)


def test_decode_no_system(k_mod):
    vals = generate_decoding_data()
    k_mod.decode_options(TempSensorOneWire_pb2.TempSensorOneWire(), vals)
    print(vals)
    assert vals['offset[kelvin]'] > 0
    assert vals['value[kelvin]'] > 0


def test_pack_bit_flags(mod):
    assert mod.pack_bit_flags([0, 2, 1]) == 7

    with pytest.raises(ValueError):
        mod.pack_bit_flags([8])


def test_unpack_bit_flags(mod):
    assert mod.unpack_bit_flags(7) == [0, 1, 2]
    assert mod.unpack_bit_flags(255) == [i for i in range(8)]
