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
const lodash_1 = require("lodash");
const grpc = require("@grpc/grpc-js");
const load_proto_1 = require("@yunke/load-proto");
const Long = require("long");
const clientMap = {};
function init(opt) {
    return __awaiter(this, void 0, void 0, function* () {
        const { gitUrl, branch, accessToken } = opt;
        const root = yield load_proto_1.loadProto([gitUrl], branch, accessToken);
        root.resolveAll();
        const grpcObject = grpc.loadPackageDefinition(load_proto_1.createPackageDefinition(root));
        return grpcObject;
    });
}
exports.init = init;
function transform(res) {
    if (Array.isArray(res)) {
        return res.map(item => transform(item));
    }
    else if (res instanceof Long) {
        return res.toNumber();
    }
    else if (typeof res === 'object') {
        const clone = {};
        Object.keys(res).forEach((key) => {
            clone[key] = transform(res[key]);
        });
        return clone;
    }
    return res;
}
function invoke(opt) {
    return __awaiter(this, void 0, void 0, function* () {
        const { host, methodName, request, grpcObject } = opt;
        const split = methodName.split('.');
        const service = split.slice(0, split.length - 1).join('.');
        const method = split[split.length - 1];
        const Service = lodash_1.get(grpcObject, service);
        if (!Service) {
            throw new Error(`Service name: ${service} not exists!`);
        }
        let client = clientMap[`${host}-${service}`];
        if (!client) {
            client = new Service(host, grpc.credentials.createInsecure());
            clientMap[`${host}-${service}`] = client;
        }
        if (!client[method]) {
            throw new Error(`Method name: ${method} not exists!`);
        }
        return new Promise((resolve, reject) => {
            client[method](request, (err, response) => {
                if (err) {
                    reject(err);
                    return;
                }
                resolve(transform(response));
            });
        });
    });
}
exports.invoke = invoke;
