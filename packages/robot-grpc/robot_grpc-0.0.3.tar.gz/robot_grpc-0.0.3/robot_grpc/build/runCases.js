"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const base = require("./base");
const jsondiffpatch_1 = require("jsondiffpatch");
const [host, gitUrl, branch, accessToken, caseFilePath, caseName,] = process.argv.slice(2);
const cssText = fs.readFileSync(require.resolve('jsondiffpatch/dist/formatters-styles/html.css'));
function main() {
    return __awaiter(this, void 0, void 0, function* () {
        if (!fs.existsSync(caseFilePath)) {
            throw new Error(`Cases file not exists: ${caseFilePath}`);
        }
        const cases = require(caseFilePath);
        const grpcObject = yield base.init({ gitUrl, branch, accessToken });
        let casesArr = [];
        if (Array.isArray(cases.cases)) {
            casesArr = cases.cases;
        }
        else {
            Object.keys(cases.cases).forEach((key) => {
                casesArr.push(Object.assign({}, (cases.cases[key]), { name: key }));
            });
        }
        if (caseName) {
            casesArr = casesArr.filter(item => item.name === caseName);
        }
        return yield Promise.all(casesArr.map((item) => __awaiter(this, void 0, void 0, function* () {
            const responseRes = yield base.invoke({
                host,
                grpcObject,
                methodName: item.id,
                request: item.request,
            });
            const diffPatcher = new jsondiffpatch_1.DiffPatcher();
            const delta = diffPatcher.diff(responseRes, item.response);
            if (delta) {
                return {
                    methodName: item.id,
                    caseName: item.name,
                    delta,
                    html: jsondiffpatch_1.formatters.html.format(delta, responseRes)
                };
            }
            return {
                methodName: item.id,
                delta,
                caseName: item.name,
                html: '',
            };
        })));
    });
}
main()
    .then((res) => {
    const hasDiff = res
        .filter(item => !!item.delta);
    const html = `<h2>Success/Total: ${res.length - hasDiff.length}/${res.length}</h2>` + res
        .map((item) => {
        return `<h3>${item.methodName}   ${item.caseName}</h3>` +
            `<p>${item.delta ? `<span class="label fail">FAIL</span> 详情: ` : `<span class="label pass">PASS</span>`}</p>` +
            `${item.html}`;
    })
        .join('');
    console.log(`<style>${cssText}</style>${html}`);
    if (hasDiff.length > 0) {
        process.exit(2);
    }
})
    .catch((err) => {
    console.log(err.message);
    process.exit(1);
});
