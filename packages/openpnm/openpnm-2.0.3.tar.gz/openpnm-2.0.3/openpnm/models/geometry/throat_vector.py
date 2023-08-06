r"""
===============================================================================
Submodule -- throat_vector
===============================================================================

"""
from transforms3d import _gohlketransforms as tr


def pore_to_pore(target):
    r"""
    Calculates throat vector as straight path between connected pores.

    Parameters
    ----------
    geometry : OpenPNM Geometry object
        The object containing the geometrical properties of the throats

    Notes
    -----
    There is an important impicit assumption here: the positive direction is
    taken as the direction from the pore with the lower index to the higher.
    This corresponds to the pores in the 1st and 2nd columns of the
    'throat.conns' array as stored on the etwork.
    """
    network = target.project.network
    throats = network.throats(target.name)
    conns = network['throat.conns']
    P1 = conns[:, 0]
    P2 = conns[:, 1]
    coords = network['pore.coords']
    vec = coords[P2] - coords[P1]
    unit_vec = tr.unit_vector(vec, axis=1)
    return unit_vec[throats]
