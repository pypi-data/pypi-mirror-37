"""\
visaplan.plone.interfaces: schemas for Dexterity-based content types

The schemas reflect fields which are currently implemented one-by-one
for the Archetypes-based content types of the UNITRACC family of Plone sites.
"""

# MessageFactory moved to factories module
from .behaviors import (
    IHeightAndWidth,
    ICaptionAndLegend,
    IExcludeFromSearch,
    IHierarchicalBuzzword,
    )
