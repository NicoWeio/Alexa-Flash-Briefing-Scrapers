const GOLEM = require('./golem');

exports.handler = async (event) => {
    const response = {
        statusCode: 200,
        body: JSON.stringify(await GOLEM()),
    };
    return response;
};
