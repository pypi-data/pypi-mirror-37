# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE
#
# Copyright 2018 by it's authors.
# Some rights reserved. See LICENSE.rst, CONTRIBUTORS.rst.

from bika.lims import logger, api
from bika.lims.config import PROJECTNAME as product
from bika.lims.upgrade import upgradestep
from bika.lims.upgrade.utils import UpgradeUtils

version = '1.2.6'  # Remember version number in metadata.xml and setup.py
profile = 'profile-{0}:default'.format(product)


@upgradestep(product, version)
def upgrade(tool):
    portal = tool.aq_inner.aq_parent
    ut = UpgradeUtils(portal)
    ver_from = ut.getInstalledVersion(product)

    if ut.isOlderVersion(product, version):
        logger.info("Skipping upgrade of {0}: {1} > {2}".format(
            product, ver_from, version))
        return True

    logger.info("Upgrading {0}: {1} -> {2}".format(product, ver_from, version))

    # -------- ADD YOUR STUFF HERE --------
    rename_bika_setup()

    logger.info("{0} upgraded to version {1}".format(product, version))
    return True


def rename_bika_setup():
    """
    Rename Bika Setup to just Setup to avoid naming confusions for new users
    """
    logger.info("Renaming Bika Setup...")
    bika_setup = api.get_bika_setup()
    bika_setup.setTitle("Setup")
    bika_setup.reindexObject()
    setup = api.get_portal().portal_setup
    setup.runImportStepFromProfile('profile-bika.lims:default', 'controlpanel')

