const EXCLUDED_OPERATION_NAMES = ['getHealthStatus'];

module.exports = {
    schemaFile: 'https://lovolab.ru/api/openapi.json',
    apiFile: './src/redux/service.ts',
    apiImport: 'api',
    outputFile: './src/redux/autogen.ts',
    exportName: 'cheerApi',
    hooks: {
        queries: true,
        lazyQueries: true,
        mutations: true,
    },
    filterEndpoints: (operationName) => !EXCLUDED_OPERATION_NAMES.includes(operationName),
};
