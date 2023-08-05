def QueryProfile(userId):
    return {'query': 'query{profiles(gcID: "' + str(userId) + '"){name, email, avatar, mobilePhone, officePhone,' +
                 'address{streetAddress,city, province, postalCode, country}}}'}

def QueryProfileByUserName(userName):
    return {'query': 'query{profiles(name: "' + str(userName) + '"){name, email, avatar, mobilePhone, officePhone,' +
                 'address{streetAddress,city, province, postalCode, country}}}'}

def QueryProfileByEmail(email):
    return {'query': 'query{profiles(email: "' + str(email) + '"){name, email, avatar, mobilePhone, officePhone,' +
                 'address{streetAddress,city, province, postalCode, country}}}'}