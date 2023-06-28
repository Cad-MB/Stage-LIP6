const jsonConverter = require('../grammars/json_schema/converter/converter')
const dslParser = require("../grammars/dsl/parser");
const dslConverter = require("../grammars/dsl/conversions");
const {notObject} = require("../grammars/json_schema/converter/schema_inverter");

// schema -> DSL
console.log("schema -> DSL")
const userSettings = {
    datagen_language: "pt"
};

const schema = {
    schema: {
        type: "string"
    }};
let convertedDSL = jsonConverter.parseStringType(schema, userSettings);
console.log(convertedDSL)

// // DSL -> instance
// console.log("\nDSL -> instance")
// const DSL = `<!LANGUAGE pt>
// {
//         v: ${convertedDSL}
// }`;
//
// let generatedData = dslParser.parse(DSL)
// generatedData = JSON.stringify(dslConverter.cleanJson(generatedData.dataModel.data), null, 2)
// console.log(generatedData)