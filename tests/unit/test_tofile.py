#!/usr/bin/env python3
"""Test functions in tofile."""

import binascii
from os.path import abspath

from tolkein import tofile

VALUE = ['record1', 'record2', 'record3', 'record4', 'record5']
EXAMPLE_JSON = '[\n "record1",\n "record2",\n "record3",\n "record4",\n "record5"\n]'
EXAMPLE_YAML = '- record1\n- record2\n- record3\n- record4\n- record5\n'


def test_read_file_that_exists():
    """Test read_file with a valid files."""
    assert tofile.read_file('tests/files/infile') == 'testfile content\n'
    assert tofile.read_file('tests/files/infile.gz') == 'testfile content\n'


def test_read_file_that_does_not_exist():
    """Test read_file with non-existent files."""
    assert tofile.read_file('nofile') is None
    assert tofile.read_file('nofile.gz') is None
    assert tofile.read_file('tests/files/nofile') is None
    assert tofile.read_file('tests/files/nofile.gz') is None


def test_load_yaml(mocker):
    """Test YAML file loading."""
    mocked_read_file = mocker.patch.object(tofile, 'read_file')
    mocked_read_file.return_value = EXAMPLE_JSON
    tofile.load_yaml('identifiers.yaml')
    mocked_read_file.assert_called()
    mocked_read_file.assert_called_with('identifiers.yaml')


def test_write_file_json(tmpdir):
    """Test write_file JSON file output."""
    path = tmpdir.mkdir('sub').join('outfile.json')
    pathname = abspath(path)
    tofile.write_file(pathname, VALUE)
    assert len(tmpdir.listdir()) == 1
    assert path.read() == EXAMPLE_JSON
    tmpdir.remove()


def test_write_file_yaml(tmpdir):
    """Test write_file YAML file output."""
    path = tmpdir.mkdir('sub').join('outfile.yaml')
    pathname = abspath(path)
    tofile.write_file(pathname, VALUE)
    assert len(tmpdir.listdir()) == 1
    assert path.read() == EXAMPLE_YAML
    tmpdir.remove()


def test_write_file_plain(tmpdir):
    """Test write_file text file output."""
    path = tmpdir.mkdir('sub').join('outfile.txt')
    pathname = abspath(path)
    example_string = 'file content\n'
    tofile.write_file(pathname, example_string)
    assert len(tmpdir.listdir()) == 1
    assert path.read() == example_string
    tmpdir.remove()


def test_write_file_invalid_path():
    """Test write_file to bad path."""
    example_string = 'file content\n'
    assert tofile.write_file('path/does/not/exist', example_string) is False
    assert tofile.write_file('path/does/not/exist.gz', example_string) is False


def test_write_file_json_gz(tmpdir):
    """Test write_file gzipped JSON output."""
    path = tmpdir.mkdir('sub').join('outfile.json.gz')
    pathname = abspath(path)
    tofile.write_file(pathname, VALUE)
    assert len(tmpdir.listdir()) == 1
    with open(pathname, 'rb') as fh:
        assert binascii.hexlify(fh.read(2)) == b'1f8b'
    tmpdir.remove()


def test_write_file_yaml_gz(tmpdir):
    """Test write_file gzipped YAML output."""
    path = tmpdir.mkdir('sub').join('outfile.yaml.gz')
    pathname = abspath(path)
    tofile.write_file(pathname, VALUE)
    assert len(tmpdir.listdir()) == 1
    with open(pathname, 'rb') as fh:
        assert binascii.hexlify(fh.read(2)) == b'1f8b'
    tmpdir.remove()
