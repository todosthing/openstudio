# -*- coding: utf-8 -*-

from general_helpers import max_string_length
from general_helpers import get_ajax_loader

from openstudio import Invoice, WorkshopProduct

from os_upgrade import set_version


def to_login(var=None):
    redirect(URL('default', 'user', args=['login']))


def index():
    """
        This function executes commands needed for upgrades to new versions
    """
    # first check if a version is set
    if not db.sys_properties(Property='Version'):
        db.sys_properties.insert(Property='Version',
                                 PropertyValue=0)
        db.sys_properties.insert(Property='VersionRelease',
                                 PropertyValue=0)

    # check if a version is set and get it
    if db.sys_properties(Property='Version'):
        version = float(db.sys_properties(Property='Version').PropertyValue)

        if version < 2018.1:
            print version
            session.flash = T("Please upgrade to at least 2018.1 before running upgrade for any later versions")

        if version < 2018.2:
            print version
            upgrade_to_20182()
            session.flash = T("Upgraded db to 2018.2")
        else:
            session.flash = T('Already up to date')

        # always renew permissions for admin group after update
        set_permissions_for_admin_group()

    set_version()

    # Clear system properties cache
    cache_clear_sys_properties()

    # Clear menu cache
    cache_clear_menu_backend()

    # Back to square one
    to_login()


def upgrade_to_20181():
    """
        Upgrade operations to 2018.1
    """
    ##
    # clear cache
    ##
    cache.ram.clear(regex='.*')

    ##
    # Set sorting order for subscriptions
    ##
    query = (db.school_subscriptions.SortOrder == None)
    db(query).update(SortOrder = 0)

    ##
    # Create default subscription group, add all subscriptions to it and give the group full permissions for each class
    # to maintain similar behaviour compared to before the update
    ##

    # Subscriptions
    ssgID = db.school_subscriptions_groups.insert(
        Name = 'All subscriptions',
        Description = 'All subscriptions',
    )

    query = (db.school_subscriptions.Archived == False)
    rows = db(query).select(db.school_subscriptions.ALL)
    for row in rows:
        db.school_subscriptions_groups_subscriptions.insert(
            school_subscriptions_id = row.id,
            school_subscriptions_groups_id = ssgID
        )

    # Class cards
    scgID = db.school_classcards_groups.insert(
        Name = 'All class cards',
        Description = 'All class cards'
    )

    query = (db.school_classcards.Archived == False)
    rows = db(query).select(db.school_classcards.ALL)
    for row in rows:
        db.school_classcards_groups_classcards.insert(
            school_classcards_id = row.id,
            school_classcards_groups_id = scgID
        )

    # Link subscription & class card groups to classes and give permissions
    rows = db(db.classes).select(db.classes.ALL)
    for row in rows:
        db.classes_school_subscriptions_groups.insert(
            classes_id = row.id,
            school_subscriptions_groups_id = ssgID,
            Enroll = True,
            ShopBook = True,
            Attend = True
        )

        db.classes_school_classcards_groups.insert(
            classes_id = row.id,
            school_classcards_groups_id = scgID,
            Enroll = True,
            ShopBook = True,
            Attend = True
        )

    ##
    # set Booking status to attending for all historical data in classes_attendance
    ##
    query = (db.classes_attendance.BookingStatus == None)
    db(query).update(BookingStatus='attending')
    # TODO: repeat the 2 lines above for all coming upgrades


def upgrade_to_20182():
    """
        Upgrade operations to 2018.2
    """
    ##
    # Set archived customers to deleted
    ##
    query = (db.auth_user.archived == True)
    db(query).update(trashed = True)

    ##
    # Set archived for all users to False
    ##
    db(db.auth_user).update(archived = False)

    ##
    # Migrate links to invoices
    ##
    rows = db(db.invoices).select(db.invoices.ALL)
    for row in rows:
        iID = row.id
        db.invoices_customers.insert(
            invoices_id = iID,
            auth_customer_id = row.auth_customer_id
        )

        if row.customers_subscriptions_id:
            db.invoices_customers_subscriptions.insert(
                invoices_id = iID,
                customers_subscriptions_id = row.customers_subscriptions_id
            )


    db(query).update(auth_customer_id = None,
                     customers_subscriptions_id = None)


    ##
    # Clean up old tables
    ##
    tables = [
        'paymentsummary',
        'overduepayments',
        'customers_payments',
        'workshops_messages',
        'workshops_products_messages',
        'customers_subscriptions_exceeded'
    ]

    for table in tables:
        try:
            db.executesql('''DROP TABLE '{table'}'''.format(table=table))
        except:
            pass
