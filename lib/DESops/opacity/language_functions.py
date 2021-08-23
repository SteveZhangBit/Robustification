"""
Functions related to automaton languages
"""
import warnings

from DESops.automata.event import Event
from DESops.automata.NFA import NFA
from DESops.basic_operations import composition
from DESops.basic_operations.construct_complement import complement
from DESops.basic_operations.product_NFA import product_NFA


def language_inclusion(g, h, Eo, return_num_states=False, return_unincluded_path=False):
    """
    Returns whether the language marked by g is a subset of the language marked by h

    Returns: opaque(, num_states)(, unincluded_path)

    Note: Only use this if the event sets are the same for both automata

    g, h: the two automata
    Eo: the set of observable events
    return_num_states: if True, the number of states in the product g x det(h)^c is returned as an additional value
    return_unincluded_path: if True, a list of observable events representing a path marked in g but not h is returned as an additional value
    """
    h_det = composition.observer(h)
    complement(h_det, inplace=True, events=Eo)

    prod = product_NFA([g, h_det], save_marked_states=True)

    opaque = True
    for v in prod.vs:
        if v["marked"]:
            opaque = False
            violating_id = v.index
            break

    return_list = [opaque]

    if return_num_states:
        return_list.append(prod.vcount())

    if return_unincluded_path:
        if opaque:
            return_list.append(None)
        else:
            inits = [v.index for v in prod.vs if v["init"]]
            return_list.append(find_path_between(prod, inits, violating_id))

    if len(return_list) == 1:
        return return_list[0]
    else:
        return tuple(return_list)


def moore_to_standard(g):
    """
    Returns an automaton that augments every event in g with whether the target vertex is secret
    A new initial vertex is added that reaches each old initial vertex via an e_init event
    The new automaton marks every string that begins with e_init and is followed by a string generated by g
    """
    h = NFA()
    h.add_vertices(g.vcount() + 1)

    # create new initial state that leads to old initial states via e_init
    # this means that vertex i in g is vertex i+1 in h
    for v in g.vs:
        if v["init"]:
            label = (Event("e_init"), v["secret"])
            h.add_edge(0, v.index + 1, label)
    h.vs["init"] = False
    h.vs[0]["init"] = True

    # all vertices except the initial one should be marked, because we should always have an e_init event
    h.vs["marked"] = True
    h.vs[0]["marked"] = False

    h.Euo = set()
    for t in g.es:
        label = (t["label"], t.target_vertex["secret"])
        h.add_edge(t.source + 1, t.target + 1, label)
        if t["label"] in g.Euo:
            h.Euo.add(label)

    h.generate_out()
    return h


def concatenate_union(g, h):
    """
    Constructs an automaton that marks any string in either in h, or in the concatenation of g and h

    The resulting automaton overwrites the original g
    """
    offset = g.vcount() - 1
    g.add_vertices(h.vcount() - 1)

    for t in h.es:
        if t.source == 0:
            # transitions from the initial state of h use marked states of g as their source
            for v in g.vs:
                if v["marked"]:
                    g.add_edge(v.index, t.target + offset, t["label"], fill_out=True)
        else:
            g.add_edge(t.source + offset, t.target + offset, t["label"], fill_out=True)

    # marked states correpsond to initial states in h
    for v in g.vs:
        if v["marked"]:
            v["init"] = True
        # fix vertices that didn't get marked as initial or non-initial
        if v["init"] is None:
            v["init"] = False

    # new marked states are those that are marked in h
    g.vs["marked"] = False
    for v in h.vs:
        if v["marked"]:
            g.vs[v.index + offset]["marked"] = True


def construct_H_NS(k, joint, secret_type, events, Euo):
    if k == "infinite":
        if not joint:
            raise ValueError("Separate infinite-step opacity is not implemented")
        h = H_infinite_NS(secret_type, events, Euo)

    else:
        h = H_star(events)

        if joint:
            # no secret behavior is allowed in final K+1 steps
            for _ in range(0, k + 1):
                concatenate_union(h, H_epoch_NS(secret_type, events, Euo))

        else:
            # nonsecret bahvaior must occur K epochs ago
            concatenate_union(h, H_epoch_NS(secret_type, events, Euo))
            # epochs 0 to K-1 steps ago don't matter
            for _ in range(0, k):
                concatenate_union(h, H_epoch_all(events, Euo))

    h.Euo = Euo
    return h


def H_star(events):
    """
    Returns an automaton that marks all strings

    events: set of (e, S/NS) pairs
    """
    h = NFA()
    h.add_vertex()
    h.vs["init"] = [True]
    h.vs["marked"] = [True]

    for e in events:
        h.add_edge(0, 0, e)

    h.generate_out()
    return h


def H_epoch_all(events, Euo):
    """
    Returns an automaton that marks any single epoch

    events: set of (e, S/NS) pairs
    Euo: set of (e, S/NS) pairs that are unobservable
    """
    h = NFA()
    h.add_vertices(2)
    h.vs["init"] = [True, False]
    h.vs["marked"] = [False, True]

    for e in events:
        if e in Euo:
            h.add_edge(1, 1, e)
        else:
            h.add_edge(0, 1, e)

    h.generate_out()
    return h


def H_epoch_NS(secret_type, events, Euo):
    """
    Returns an automaton that marks any single epoch in which nonsecret behavior occurs

    events: set of (e, S/NS) pairs
    Euo: set of (e, S/NS) pairs that are unobservable
    """
    h = NFA()

    if secret_type == 1:
        h.add_vertices(2)
        h.vs["init"] = [True, False]
        h.vs["marked"] = [False, True]
        for e in events:
            secret = e[1]
            if not secret:
                if e in Euo:
                    h.add_edge(1, 1, e)
                else:
                    h.add_edge(0, 1, e)

    else:
        h.add_vertices(3)
        h.vs["init"] = [True, False, False]
        h.vs["marked"] = [False, False, True]
        for e in events:
            secret = e[1]
            if e in Euo:
                h.add_edge(2, 2, e)
                h.add_edge(1, 1, e)
                if not secret:
                    h.add_edge(1, 2, e)

            else:
                h.add_edge(0, 1, e)
                if not secret:
                    h.add_edge(0, 2, e)

    h.generate_out()
    return h


def H_infinite_NS(secret_type, events, Euo):
    """
    Returns an automaton that marks strings that exhibit no secret behavior at any point

    events: set of (e, S/NS) pairs
    Euo: set of (e, S/NS) pairs that are unobservable
    """
    h = NFA()

    if secret_type == 1:
        h.add_vertices(3)
        h.vs["init"] = [True, False, False]
        h.vs["marked"] = [False, False, True]
        for e in events:
            secret = e[1]
            h.add_edge(1, 1, e)
            h.add_edge(2, 1, e)

            if not secret:
                h.add_edge(2, 2, e)
                if e not in Euo:
                    h.add_edge(0, 2, e)

            if e not in Euo:
                h.add_edge(0, 1, e)

    else:
        h.add_vertices(4)
        h.vs["init"] = [True, False, False, False]
        h.vs["marked"] = [False, False, False, True]
        for e in events:
            secret = e[1]
            h.add_edge(1, 2, e)
            h.add_edge(2, 2, e)

            if e in Euo:
                h.add_edge(1, 1, e)
                h.add_edge(3, 3, e)
                if not secret:
                    h.add_edge(1, 3, e)

            else:
                h.add_edge(0, 1, e)
                h.add_edge(3, 1, e)
                if not secret:
                    h.add_edge(0, 3, e)
                    h.add_edge(3, 3, e)

    h.generate_out()
    return h


def find_path_between(g, source, target):
    """
    Finds a shortest path from a source vertex to a target vertex
    Returns the list of event labels associated with the path
    If any vertex is in both a source and a target, returns an empty list
    If no target vertex can be reached from any source vertex, returns None

    g: the automaton
    source: a vertex ID or a list of vertex IDs
    target: a vertex ID or a list of vertex IDs

    Only one of source and target can be a list
    """
    with warnings.catch_warnings():
        # suppress warning when not every target is reachable from every source
        warnings.simplefilter("ignore")

        if isinstance(source, list):
            if isinstance(target, list):
                raise ValueError("Only one of source and target can be a list")

            # return empty list if source and target intersect
            if target in source:
                return []

            paths = g._graph.get_shortest_paths(
                target, source, mode="IN", output="epath"
            )

        else:
            # return empty list if source and target intersect
            if isinstance(target, list) and source in target:
                return []
            if source == target:
                return []

            paths = g._graph.get_shortest_paths(source, target, output="epath")

        # if all paths were empty, then target can't be reached from source
        if all([(path == []) for path in paths]):
            return None

        # get shortest non-empty path
        while [] in paths:
            paths.remove([])
        path = min(paths)

        path_labels = list()
        for i in path:
            t = g.es[i]["label"]
            if isinstance(t, Event):
                path_labels.append(t.label)
            else:
                path_labels.append(t)

        return path_labels
