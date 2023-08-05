import requests
from oidc_provider.lib.claims import ScopeClaims
from .helper import graphql_query, graphql_mutation, graphql_post, model_configuration
from django.utils.translation import gettext as _
from django.db.models.signals import post_save

def create_profile(id, name, email):
    configuration = model_configuration.getdefault()

    # ToDo replace this with messages over Kafka system for notification
    if configuration.trigger is True:
        attempt = 0
        retrys = 3
        success = False

        if(name in queryProfileByName(name)):
            return None

        if(email in queryProfileByEmail(email)):
            return None

        query = graphql_mutation.createProfile(id, name, email)

        while not success and attempt < retrys:
            response = requests.post(configuration.end_point, headers={'Authorization': 'Token ' + configuration.token},
                                    data=query)
            if not response.status_code == requests.codes.ok:
                attempt = attempt + 1
            else:
                success = True
        if not success:
            # Write this to log eventually
            raise Exception('Error setting user data / Server Response ' + str(response.status_code))

post_save.connect(create_profile, sender=User)

def queryprofile(userId):
    # Get rest of information from Profile as a Service
    query = graphql_query.QueryProfile(userId)
    return graphql_post.executeQuery(query)

def queryProfileByName(userName):
    query = graphql_query.QueryProfileByUserName(userName)
    return graphql_post.executeQuery(query)

def queryProfileByEmail(email):
    query = graphql_query.QueryProfileByEmail(email)
    return graphql_post.executeQuery(query)

def disableProfile(userId):
    query = graphql_mutation.disableProfile(userId)
    return graphql_post.executeQuery(query)

def userinfo(claims, user):
    """
    Populate claims dict.
    """
    retrys = 3

    claims['name'] = user.name
    claims['email'] = user.email

    if model_configuration.getdefault().trigger:
        return claimsfromprofiles(retrys, claims)
    else:
        return claims

def claimsfromprofiles(retry, claims):
    response = queryprofile(retry)

    if response is None:
        return claims

    try:
        profileclaims = claims
        response_address = response['data']['profiles'][0].get('address')

        profileclaims['picture'] = checkvalue(response['data']['profiles'][0].get('avatar'))
        if response['data']['profiles'][0].get('mobilePhone') is not None:
            profileclaims['phone_number'] = checkvalue(response['data']['profiles'][0].get('mobilePhone'))
        else:
            profileclaims['phone_number'] = checkvalue(response['data']['profiles'][0].get('officePhone'))

        if response_address is not None:

            if 'streetAddress' in response_address:
                profileclaims['address']['street_address'] = checkvalue(response_address.get('streetAddress'))
            if 'city' in response_address:
                profileclaims['address']['locality'] = checkvalue(response_address.get('city'))
            if 'province' in response_address:
                profileclaims['address']['region'] = checkvalue(response_address.get('province'))
            if 'postalCode' in response_address:
                profileclaims['address']['postal_code'] = checkvalue(response_address.get('postalCode'))
            if 'country' in response_address:
                profileclaims['address']['country'] = checkvalue(response_address.get('country'))
    except Exception:
        return claims

    return profileclaims


def checkvalue(stringvalue):
    if stringvalue is not None:
        return stringvalue
    else:
        return ''


class CustomScopeClaims(ScopeClaims):
    info_modify_profile = (
        _('Profile Modification'),
        _('Ability to view and modify your profile information'),
    )

    def scope_modify_profile(self):
        # self.user - Django user instance.
        # self.userinfo - Dict returned by OIDC_USERINFO function.
        # self.scopes - List of scopes requested.
        # self.client - Client requesting this claims.
        dic = {
            'modify_profile': 'True',
            'detailed_profile': 'True'
        }

        return dic

    info_profile = (
        _('Basic profile'),
        _('Access to your name, email, avatar, and address'),
    )

    info_detailed_profile = (
        _('Detailed User profile'),
        _('Access to your name, email, avatar, address, and organization information'),
    )

    def scope_detailed_profile(self):
        dic = {
            'detailed_profile': 'True',
        }

        return dic