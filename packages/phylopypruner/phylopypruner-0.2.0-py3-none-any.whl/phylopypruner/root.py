"This module contains methods for rooting TreeNode objects."

def outgroup(tree, outgroups):
    """Root the provided tree by the provided outgroups, given that at least
    one of the outgroups are present within the tree and that the OTUs that are
    present are non-repetetive and form a monophyletic group. Returns the
    rooted tree and True if the conditions are met or the input tree and False
    if the conditions were not met.

    Parameters
    ----------
    tree : TreeNode object
        The node you wish to root.
    outgroups : list of strings
        Root the provided TreeNode object using the OTUs within this list.

    Returns
    -------
    tree : TreeNode object
        Tree rerooted at outgroups if conditions are met, input tree if not.
    rooted : bool
        True if conditions are met, False if not.
    """
    rooted = False
    if not tree.outgroups_present(outgroups):
        return tree, rooted

    if tree.repetetive_outgroups(outgroups):
        return tree, rooted

    if len(outgroups) == 1:
        outgroup_otu = outgroups[0]
        for leaf in tree.iter_leaves():
            otu = leaf.otu()
            if otu == outgroup_otu:
                rooted = True
                return tree.reroot(leaf), rooted

    for branch in tree.iter_branches():
        if branch.is_monophyletic_outgroup(outgroups):
            rooted = True
            return tree.reroot(branch), rooted
    return tree, rooted

def midpoint(tree):
    """Calculate the tip to tip distances of the provided tree root the tree
    halfway between the two longest tips.

    Parameters
    ----------
    tree : TreeNode object
        The tree to be rooted.

    Returns
    -------
    tree_rooted : TreeNode object
        Midpoint rooted input tree.
    """
    longest_dist = None
    dists = tree.distances()
    for pair in dists:
        if not longest_dist or longest_dist < dists[pair]:
            longest_dist = dists[pair]
            node_a, node_b = pair

    if not longest_dist or not node_a or not node_b:
        return tree

    mid = longest_dist / 2.0
    parent = node_a.parent
    while parent:
        if node_a and node_b in parent.traverse_preorder():
            # smallest node that includes both nodes under comparision
            smallest_subtree = parent
        parent = parent.parent

    closest_diff = None
    closest_node = None
    for node_c in smallest_subtree.traverse_preorder():
        print(node_a.view())
        print(node_b.view())
        print(node_c.view())
        print(smallest_subtree.view())
        diff_a = abs(mid - node_a.distance_to(node_c))
        diff_b = abs(mid - node_b.distance_to(node_c))
        if not closest_diff or diff_a < closest_diff or diff_b < closest_diff:
            if diff_a < diff_b:
                closest_diff = diff_a
            else:
                closest_diff = diff_b
            closest_node = node_c

    if closest_node:
        print(closest_node.view())

    return tree
