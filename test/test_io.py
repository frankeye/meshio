# -*- coding: utf-8 -*-
#
import meshio

import numpy
import os
import pytest

# In general:
# Use values with an infinite decimal representation to test precision.

tri_mesh = {
        'points': numpy.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0]
            ]) / 3.0,
        'cells': {
            'triangle': numpy.array([
                [0, 1, 2],
                [0, 2, 3]
                ])
            },
        }

quad_mesh = {
        'points': numpy.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [2.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0]
            ]) / 3.0,
        'cells': {
            'quad': numpy.array([
                [0, 1, 4, 5],
                [1, 2, 3, 4]
                ])
            },
        }

tri_quad_mesh = {
        'points': numpy.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [2.0, 0.0, 0.0],
            [2.0, 1.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0]
            ]) / 3.0,
        'cells':  {
            'triangle': numpy.array([
                [0, 1, 4],
                [0, 4, 5]
                ]),
            'quad': numpy.array([
                [1, 2, 3, 4]
                ])
            }
        }

tet_mesh = {
        'points': numpy.array([
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.5, 0.5, 0.5],
            ]) / 3.0,
        'cells': {
            'tetra': numpy.array([
                [0, 1, 2, 4],
                [0, 2, 3, 4]
                ])
            },
        }


def _clone(mesh):
    mesh2 = {
        'points': numpy.copy(mesh['points'])
        }
    mesh2['cells'] = {}
    for key, data in mesh['cells'].items():
        mesh2['cells'][key] = numpy.copy(data)
    return mesh2


def _add_point_data(mesh, dim):
    numpy.random.seed(0)
    mesh2 = _clone(mesh)

    if dim == 1:
        data = numpy.random.rand(len(mesh['points']))
    else:
        data = numpy.random.rand(len(mesh['points']), dim)

    mesh2['point_data'] = {'a': data}
    return mesh2


def _add_cell_data(mesh, dim):
    mesh2 = _clone(mesh)
    numpy.random.seed(0)
    cell_data = {}
    for cell_type in mesh['cells']:
        num_cells = len(mesh['cells'][cell_type])
        if dim == 1:
            cell_data[cell_type] = {
                'b': numpy.random.rand(num_cells)
                }
        else:
            cell_data[cell_type] = {
                'b': numpy.random.rand(num_cells, dim)
                }

    mesh2['cell_data'] = cell_data
    return mesh2


@pytest.mark.parametrize('extension, file_format, meshes, atol', [
    (
        'dato', 'permas',
        [tri_mesh, quad_mesh, tri_quad_mesh, tet_mesh], 1.0e-15
    ),
    (
        'e', 'exodus',
        [
            tri_mesh,
            _add_point_data(tri_mesh, 2),
            _add_point_data(tri_mesh, 3),
        ],
        # TODO report exodus precision failure
        1.0e-8
    ),
    ('h5m', 'moab', [tri_mesh, tet_mesh], 1.0e-15),
    ('msh', 'gmsh', [tri_mesh, quad_mesh, tri_quad_mesh, tet_mesh], 1.0e-15),
    (
        'msh', 'ansys',
        [
            tri_mesh,
            quad_mesh,
            tri_quad_mesh,
            tet_mesh,
        ],
        1.0e-15
    ),
    ('mesh', 'medit', [tri_mesh, quad_mesh, tri_quad_mesh, tet_mesh], 1.0e-15),
    ('off', 'off', [tri_mesh], 1.0e-15),
    (
        'vtk', 'vtk-ascii',
        [
            tri_mesh,
            quad_mesh,
            tri_quad_mesh,
            tet_mesh,
            _add_point_data(tri_mesh, 1),
            _add_point_data(tri_mesh, 2),
            _add_point_data(tri_mesh, 3),
            _add_cell_data(tri_mesh, 1),
            _add_cell_data(tri_mesh, 2),
            _add_cell_data(tri_mesh, 3),
        ],
        # ASCII files are only meant for debugging, VTK stores only 11 digits
        # <https://gitlab.kitware.com/vtk/vtk/issues/17038#note_264052>
        1.0e-11
    ),
    (
        'vtk', 'vtk-binary',
        [
            tri_mesh,
            quad_mesh,
            tri_quad_mesh,
            tet_mesh,
            _add_point_data(tri_mesh, 1),
            _add_point_data(tri_mesh, 2),
            _add_point_data(tri_mesh, 3),
            _add_cell_data(tri_mesh, 1),
            _add_cell_data(tri_mesh, 2),
            _add_cell_data(tri_mesh, 3),
        ],
        1.0e-15
    ),
    (
        'vtu', 'vtu-ascii',
        [
            tri_mesh,
            quad_mesh,
            tri_quad_mesh,
            tet_mesh,
            _add_point_data(tri_mesh, 1),
            _add_point_data(tri_mesh, 2),
            _add_point_data(tri_mesh, 3),
            _add_cell_data(tri_mesh, 1),
            _add_cell_data(tri_mesh, 2),
            _add_cell_data(tri_mesh, 3),
        ],
        # ASCII files are only meant for debugging, VTK stores only 11 digits.
        # <https://gitlab.kitware.com/vtk/vtk/issues/17038#note_264052>
        1.0e-11
    ),
    (
        'vtu', 'vtu-binary',
        [
            tri_mesh,
            quad_mesh,
            tri_quad_mesh,
            tet_mesh,
            _add_point_data(tri_mesh, 1),
            _add_point_data(tri_mesh, 2),
            _add_point_data(tri_mesh, 3),
            _add_cell_data(tri_mesh, 1),
            _add_cell_data(tri_mesh, 2),
            _add_cell_data(tri_mesh, 3),
        ],
        1.0e-15
    ),
    (
        'xdmf', 'xdmf2',
        [
            tri_mesh,
            quad_mesh,
            tet_mesh,
            _add_point_data(tri_mesh, 1),
            _add_cell_data(tri_mesh, 1)
        ],
        # FIXME data is only stored in single precision
        # <https://gitlab.kitware.com/vtk/vtk/issues/17037>
        1.0e-6
    ),
    (
        'xdmf', 'xdmf3',
        [
            tri_mesh,
            quad_mesh,
            tet_mesh,
            _add_point_data(tri_mesh, 1),
            _add_cell_data(tri_mesh, 1)
        ],
        1.0e-15
    ),
    (
        'xml', 'dolfin-xml', [
            tri_mesh,
            tet_mesh,
            _add_cell_data(tri_mesh, 1),
        ],
        1.0e-15
    ),
    ])
def test_io(extension, file_format, meshes, atol):
    filename = 'test.' + extension
    for mesh in meshes:
        _write_read(filename, file_format, mesh, atol)
    return


def _write_read(filename, file_format, mesh, atol):
    '''Write and read a file, and make sure the data is the same as before.
    '''
    try:
        input_point_data = mesh['point_data']
    except KeyError:
        input_point_data = {}

    try:
        input_cell_data = mesh['cell_data']
    except KeyError:
        input_cell_data = {}

    meshio.write(
        filename,
        mesh['points'], mesh['cells'],
        file_format=file_format,
        point_data=input_point_data,
        cell_data=input_cell_data
        )
    points, cells, point_data, cell_data, _ = \
        meshio.read(filename, file_format)

    # Numpy's array_equal is too strict here, cf.
    # <https://mail.scipy.org/pipermail/numpy-discussion/2015-December/074410.html>.
    # Use allclose.

    # We cannot compare the exact rows here since the order of the points might
    # have changes. Just compare the sums
    assert numpy.allclose(mesh['points'], points, atol=atol, rtol=0.0)

    for cell_type, data in mesh['cells'].items():
        assert numpy.allclose(data, cells[cell_type])
    for key in input_point_data.keys():
        assert numpy.allclose(
            input_point_data[key], point_data[key],
            atol=atol, rtol=0.0
            )
    for cell_type, cell_type_data in input_cell_data.items():
        for key, data in cell_type_data.items():
            assert numpy.allclose(
                    data, cell_data[cell_type][key],
                    atol=atol, rtol=0.0
                    )

    os.remove(filename)
    return