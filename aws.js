const GOLEM = require('./golem');

exports.handler = async (event) => {
    const response = {
        statusCode: 200,
        body: await GOLEM(),
    };
    return response;
};
