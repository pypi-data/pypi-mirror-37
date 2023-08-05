import { GrpcObject } from "@grpc/grpc-js/build/src/make-client";
export declare function init(opt: {
    gitUrl: string;
    branch: string;
    accessToken: string;
}): Promise<GrpcObject>;
export declare function invoke(opt: {
    host: string;
    methodName: string;
    request: string;
    grpcObject: GrpcObject;
}): Promise<any>;
