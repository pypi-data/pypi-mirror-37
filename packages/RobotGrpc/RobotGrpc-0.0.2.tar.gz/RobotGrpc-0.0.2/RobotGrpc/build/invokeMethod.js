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
const base = require("./base");
const [host, gitUrl, branch, accessToken, methodName, requestStr,] = process.argv.slice(2);
const request = JSON.parse(requestStr);
function main() {
    return __awaiter(this, void 0, void 0, function* () {
        const grpcObject = yield base.init({ gitUrl, branch, accessToken });
        const response = yield base.invoke({ host, grpcObject, methodName, request });
        return { methodName, request, response };
    });
}
main()
    .then((res) => {
    console.log(res);
})
    .catch((err) => {
    console.log(err.message);
    process.exit(-1);
});
