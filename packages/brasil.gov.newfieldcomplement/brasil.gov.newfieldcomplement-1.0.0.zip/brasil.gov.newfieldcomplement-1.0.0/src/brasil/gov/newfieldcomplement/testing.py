# -*- coding: utf-8 -*-

from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import brasil.gov.newfieldcomplement
import transaction


MANAGER = 'adm'
ADM = 'siteadm'
EDITOR = 'editor'
PASS = 'secret'


class BrasilGovNewfieldcomplementLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(
            package=brasil.gov.newfieldcomplement,
            name='dependencies.zcml',
        )
        z2.installProduct(app, 'Products.DateRecurringIndex')
        self.loadZCML(package=brasil.gov.newfieldcomplement)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'brasil.gov.newfieldcomplement:default')
        applyProfile(portal, 'brasil.gov.newfieldcomplement:tests')
        # workflow
        portal.portal_workflow.setChainForPortalTypes(
            ('Folder', ),
            'simple_publication_workflow'
        )
        # users
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        acl_users = api.portal.get_tool('acl_users')
        acl_users.userFolderAddUser(
            MANAGER,
            PASS,
            roles=['Member'],
            domains=[],
            groups=['Administrators'],
        )
        acl_users.userFolderAddUser(
            ADM,
            PASS,
            roles=['Member'],
            domains=[],
            groups=['Site Administrators'],
        )
        acl_users.userFolderAddUser(
            EDITOR,
            PASS,
            roles=['Member', 'Contributor', 'Editor'],
            domains=[],
            groups=[],
        )
        # content
        api.content.create(
            container=portal,
            type='Folder',
            id='relatorios',
            title=u'Relatórios',
        )
        api.content.transition(
            obj=portal['relatorios'],
            transition='publish',
        )

        transaction.commit()
        logout()


BRASIL_GOV_NEWFIELDCOMPLEMENT_FIXTURE = BrasilGovNewfieldcomplementLayer()


BRASIL_GOV_NEWFIELDCOMPLEMENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BRASIL_GOV_NEWFIELDCOMPLEMENT_FIXTURE,),
    name='BrasilGovNewfieldcomplementLayer:IntegrationTesting'
)


BRASIL_GOV_NEWFIELDCOMPLEMENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BRASIL_GOV_NEWFIELDCOMPLEMENT_FIXTURE,),
    name='BrasilGovNewfieldcomplementLayer:FunctionalTesting'
)


BRASIL_GOV_NEWFIELDCOMPLEMENT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        BRASIL_GOV_NEWFIELDCOMPLEMENT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='BrasilGovNewfieldcomplementLayer:AcceptanceTesting'
)
