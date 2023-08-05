def createProfile(userId, name, email):
    return {'query': 'mutation{createProfile(gcId: "' + str(userId) + '", name: "' + name + '", email:"' +
                              email + '"){gcID, name, email}}'}

def disableProfile(userId):
    return {'query': 'mutation{ModifyProfile(gcId: "' + str(userId) +'"){gcID, name, email}}'}