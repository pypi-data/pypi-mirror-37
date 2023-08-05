import { GrpcObject, ServiceClient, ServiceClientConstructor } from "@grpc/grpc-js/build/src/make-client";
import { get } from 'lodash';
import * as grpc from '@grpc/grpc-js'
import { createPackageDefinition, loadProto } from '@yunke/load-proto';
import * as Long from "long";

const clientMap: { [key: string]: ServiceClient } = {};

export async function init(opt: { gitUrl: string, branch: string, accessToken: string }): Promise<GrpcObject> {
  const { gitUrl, branch, accessToken } = opt;
  const root = await loadProto([gitUrl], branch, accessToken);
  root.resolveAll();
  const grpcObject = grpc.loadPackageDefinition(createPackageDefinition(root));
  return grpcObject;
}

function transform(res: any): any {
  if (Array.isArray(res)) {
    return res.map(item => transform(item));
  } else if (res instanceof Long) {
    return res.toNumber();
  } else if (typeof res === 'object') {
    const clone: any = {};
    Object.keys(res).forEach((key) => {
      clone[key] = transform(res[key]);
    });
    return clone;
  }
  return res;
}

export async function invoke(opt: {
  host: string,
  methodName: string,
  request: string,
  grpcObject: GrpcObject
}): Promise<any> {
  const { host, methodName, request, grpcObject } = opt;

  const split = methodName.split('.');
  const service = split.slice(0, split.length - 1).join('.');
  const method = split[split.length - 1];

  const Service: ServiceClientConstructor = get(grpcObject, service) as ServiceClientConstructor;

  if (!Service) {
    throw new Error(`Service name: ${service} not exists!`);
  }

  let client = clientMap[`${host}-${service}`];
  if (!client) {
    client = new Service(
        host,
        grpc.credentials.createInsecure(),
    );
    clientMap[`${host}-${service}`] = client;
  }

  if (!client[method]) {
    throw new Error(`Method name: ${method} not exists!`);
  }

  return new Promise((resolve, reject) => {
    client[method](request, (err: any, response: any) => {
      if (err) {
        reject(err);
        return;
      }

      resolve(transform(response));
    })
  })
}
